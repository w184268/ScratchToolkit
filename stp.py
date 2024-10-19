import zipfile
import os,sys

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
        with zipfile.ZipFile(fp,'r') as f: #解压.sb3文件
            if ispath: #如果是一段路径
                self.p=PathTool(fp)
                f.extractall(self.p.join((self.p.DIR,self.p.NAME)))
            else: #如果是一段文件名
                self.p=PathTool(fp,mode='n')
                f.extractall(self.p.join((THISPATH,self.p.NAME)))
def main(fp:str='./tests/work1.sb3',path=True):
    a=UnPackingScratch3File(fp,path)
if __name__=='__main__':
    match len(sys.argv):
        case 1:
            main()
        case 2:
            main(sys.argv[1])
        case 3:
            main(sys.argv[1],bool(int(sys.argv[2])))
        