import zipfile,json
import os,sys

try:
    import config
    import loguru as log
    import cairosvg as csvg
except ImportError:
    print("You didn't install pygame,loguru or cairosvg!")
    os.system('pip install pygame loguru cairosvg')
except Exception:
    print("Please install gtk3 in ./bin!") 

THISPATH=os.getcwd()
class PathTool:
    def __init__(self,fp:str|tuple[str],mode='p'):
        '''when mode is p,that means fp is a path; 
           when mode is n,that means fp is a file name.'''
        if isinstance(fp,str): fp=os.path.normpath(fp)

        match mode:
            case 'p':
                self.DIR=os.path.dirname(fp)
                self.FILE=os.path.basename(fp)
                self.NAME,self.SUFFIX=os.path.splitext(self.FILE)
            case 'n':
                self.FILE=fp
                self.NAME,self.SUFFIX=os.path.splitext(fp)
            case 'j':
                self.j=os.path.join(*(os.path.normpath(p) for p in fp))

    def join(self,args:tuple[str]=()):
        if hasattr(PathTool,'j'):
            return self.j
        elif len(args)!=0:
            return os.path.join(*args)
        
class UnPackingScratch3File:
    def __init__(self,fp:str,ispath=True):
        with zipfile.ZipFile(fp,'r') as self.f: #解压.sb3文件
            if ispath: #如果是一段路径
                self.p=PathTool(fp)
                self.cdir=self.p.join((self.p.DIR,self.p.NAME))
            else: #如果是一段文件名
                self.p=PathTool(fp,mode='n')
                self.cdir=self.p.join((THISPATH,self.p.NAME))

    def convert(self):
        self.outdir=self.p.join((self.cdir,'output'))
        self.f.extractall(self.cdir)
        os.makedirs(self.outdir,exist_ok=True)
        for fn in os.listdir(self.cdir): #批量转换
            p=PathTool(fn,'n')
            if p.SUFFIX=='.svg':
                csvg.svg2png(url=p.join((self.cdir,p.FILE)),
                                write_to=p.join((self.cdir,p.NAME+".png")))
                os.remove(p.join((self.cdir,p.FILE)))
    
class CodeParser: #解析project.json
    def __init__(self,last:UnPackingScratch3File):
        self.mod:list[str]=[] #根据情况导入所需要的库
        self.var=dict() #存储变量
        self.array=dict() #存储列表
        self.cdir,self.outdir=last.cdir,last.outdir
        self.t=PathTool(self.cdir)
        with open(self.t.join((self.cdir,"project.json")),'r',encoding='utf-8') as f: #导入project.json
            self.pj=json.load(f)
        self.make=CodeMaker(self.pj)


class CodeMaker: #转换核心，生成python代码
    def __init__(self,pj):
        self.tab=0 #Python代码的缩进
        self.name=[] #角色名
        self.code=[] #存储每行代码
        self.targets=pj["targets"] #所有角色信息
        self.code.extend(["import pygame as pg",
                          "import sys",
                          "",
                          "class Game:",
                          "    def __init__(self):"
                          "        pg.init() #初始化"])
        for t in self.targets:
            self.give(t)

    def give(self,args): #给予信息,args为每一个角色的字典信息
        if 'stp_'+args["name"] not in self.name:
            self.name.append('stp_'+args["name"])
        if args["isStage"]: #如果是舞台
            info=args["costumes"][0]
            self.code.extend([f"        screen = pg.display.setmode(({info["rotationCenterX"]},{info["rotationCenterY"]}))"])
        else:
            self.code.append(f"class {args["name"]}:")

    def return_result(self):
        return '\n'.join(self.code)
    
def main(fp:str='./tests/work1.sb3',path=True):
    info=UnPackingScratch3File(fp,path)
    info.convert()
    CodeParser(info)

if __name__=='__main__':
    match len(sys.argv):
        case 1:
            main()
        case 2:
            main(sys.argv[1])
        case 3:
            main(sys.argv[1],bool(int(sys.argv[2])))
        