import zipfile,json
import os,sys
import xml.etree.ElementTree as ET
from datetime import datetime

try:
    import config
    from loguru import logger as log
    from cairosvg import svg2png
    from PIL import Image
    log.remove()
    log.add(sys.stdout,colorize=True,format="<level>[{time:YYYY-MM-DD HH:mm:ss}] [{level}]: {message}</level>")
except ImportError:
    print("You didn't install pygame,loguru,pillow or cairosvg!")
    os.system('pip install -r requirements.txt')
except Exception as e:
    print("Please install gtk3 in ./bin!")

THISPATH=os.getcwd()
INIT_CODE='''
import pygame as pg
import sys

class Background(pygame.sprite.Sprite): #背景类
    def __init__(self, image_file, location):
        super().__init__()
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
class Game:
    def __init__(self):
        pg.init() #初始化
        screen = pg.display.set_mode(800,600) #舞台大小为800,600
'''
class PathTool:
    def __init__(self,fp:str|tuple[str],mode='p'):
        '''when mode is p,that means fp is a path; 
           when mode is n,that means fp is a file name.'''
        if isinstance(fp,str): fp=os.path.normpath(fp)
        log.debug("Using the PathTool...")
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
        log.debug(f"Unpacking {fp}...")
        with zipfile.ZipFile(fp,'r') as self.f: #解压.sb3文件
            if ispath: #如果是一段路径
                self.p=PathTool(fp)
                self.cdir=self.p.join((self.p.DIR,self.p.NAME))
            else: #如果是一段文件名
                self.p=PathTool(fp,mode='n')
                self.cdir=self.p.join((THISPATH,self.p.NAME))
            self.f.extractall(self.cdir)
        log.success(f"Completed unpacking {fp} to {self.cdir}.")

    def convert(self):
        self.outdir=self.p.join((self.cdir,'output'))
        os.makedirs(self.outdir,exist_ok=True)
        for fn in os.listdir(self.cdir): #批量转换
            p=PathTool(fn,'n')
            if p.SUFFIX=='.svg':
                #with open(p.join((self.cdir,p.FILE)), 'r',encoding='utf-8') as f:
                #    svg_size = surface.SVGSurface(f.read(),).width, surface.SVGSurface(p.join((self.cdir,p.FILE))).height
                tree = ET.parse(p.join((self.cdir,p.FILE)))
                root = tree.getroot()
                svg_size = float(root.attrib['width']), float(root.attrib['height'])
                if svg_size != (0,0):
                    log.debug(f"The size of {fn} is {svg_size}.")
                    svg2png(url=p.join((self.cdir,p.FILE)),
                                    write_to=p.join((self.cdir,p.NAME+".png")),
                                    unsafe=True,
                                    parent_width=svg_size[0],
                                    parent_height=svg_size[1])
                else:
                    log.warning(f"{fn} has no size!")
                    image = Image.new("RGB",(1, 1),(0,0,0))
                    image.save(p.join((self.cdir,p.NAME+".png")))
                os.remove(p.join((self.cdir,p.FILE)))
                log.success(f"Removed {p.join((self.cdir,p.FILE))}.")
    
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
        self.outpyfile=self.t.join((self.outdir,last.p.NAME+".py"))
        with open(self.outpyfile,'w',encoding='utf-8') as f:
            f.write(self.make.return_result())

class CodeMaker: #转换核心，生成python代码
    def __init__(self,pj):
        #self.tab=2 #Python代码的缩进
        self.name=[] #角色名
        self.code=[] #存储每行代码
        self.targets=pj["targets"] #所有角色信息
        self.code.append(INIT_CODE)
        for t in self.targets:
            self.give(**t)

    def give(self,**tgs): #给予信息,tgs为targets下每个信息
        classname='char_'+tgs["name"]
        if classname not in self.name: #若角色名称未被记录
            self.name.append(classname)
        if tgs["isStage"]: #如果是舞台
            costumes=tgs["costumes"][0]
            for costume in costumes:
                self.code.append("")
        else:
            self.code.append(f"class {classname}(pg.sprite.Sprite):")
        for block in tgs["blocks"].items():
            id,idinfo=block[0],block[1]
            try:
                depth=self.get_nested_depth(idinfo)
            except Exception as e:
                log.warning(e)
                depth=self.get_nested_depth2(idinfo)
            self.add(id,f"{classname} -> {id}",depth,**idinfo)
    def add(self,id:str,type_:str,tab:int,**kw): #积木管理
        opcode=kw["opcode"]
        log.debug(f'Converting {type_}(name="{opcode}" ,depth={tab})...')
        def restr(string:str,func=False):
            if func:
                self.code.append('    '*(tab+1)+string)
            else:
                self.code.append('    '*(tab+2)+string)

        match opcode: #匹配相应的积木名
            case "motion_movesteps":
                pass
            case _:
                log.error(f'Unknown id "{opcode}"!')

    def return_result(self):
        return '\n'.join(self.code)
    
    def get_nested_depth(self,block,depth=0):
        """
        递归函数，用于计算积木块的嵌套深度。
        
        :param block: 当前积木块
        :param depth: 当前深度
        :return: 积木块的嵌套深度
        """
        if 'topLevel' in block and block['topLevel']:
            return depth
        if 'parent' in block and block["opcode"].endswith("_menu"):
            return self.get_nested_depth(block['parent'], depth)
        if 'parent' in block:
            return self.get_nested_depth(block['parent'], depth + 1)
        return depth
    def get_nested_depth2(self,block,depth=0): #备用方法
        """
        使用迭代方法计算积木块的嵌套深度。
        
        :param block: 当前积木块
        :return: 积木块的嵌套深度
        """
        stack = [block]   
        while stack:
            current_block = stack.pop()
            print(type(current_block))
            if 'topLevel' in current_block and current_block['topLevel']:
                continue
            if 'parent' in current_block and current_block.get("opcode","").endswith("_menu"):
                continue
            if 'parent' in current_block:
                stack.append(current_block['parent'])
                depth += 1
        return depth
    
def main(fp:str='./tests/work1.sb3',path=True):
    log.debug("stp.py is running!")
    info=UnPackingScratch3File(fp,path)
    info.convert()
    parser=CodeParser(info)
    log.success(f"Converted successfully(at {parser.outpyfile}).")

if __name__=='__main__':
    try:
        match len(sys.argv):
            case 1:
                main()
            case 2:
                main(sys.argv[1])
            case 3:
                main(sys.argv[1],bool(int(sys.argv[2])))
    except BaseException as e:
        log.error(e)
        exit(1)