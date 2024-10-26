import zipfile
import os,sys

try:
    import pygame as pg
    import loguru as log
    import cairosvg as csvg
except ImportError:
    print("You didn't install pygame,loguru or cairosvg!")
    os.system('pip install pygame loguru cairosvg')
except Exception:
    print("Please install gtk3 in ./bin!")

class Config:
    # Key maps to convert the key option in blocks to pygame constants
    KEY_MAPPING = {
        "up arrow": pg.K_UP,
        "down arrow": pg.K_DOWN,
        "left arrow": pg.K_LEFT,
        "right arrow": pg.K_RIGHT,
        "space": pg.K_SPACE,
        "a": pg.K_a,
        "b": pg.K_b,
        "c": pg.K_c,
        "d": pg.K_d,
        "e": pg.K_e,
        "f": pg.K_f,
        "g": pg.K_g,
        "h": pg.K_h,
        "i": pg.K_i,
        "j": pg.K_j,
        "k": pg.K_k,
        "l": pg.K_l,
        "m": pg.K_m,
        "n": pg.K_n,
        "o": pg.K_o,
        "p": pg.K_p,
        "q": pg.K_q,
        "r": pg.K_r,
        "s": pg.K_s,
        "t": pg.K_t,
        "u": pg.K_u,
        "v": pg.K_v,
        "w": pg.K_w,
        "x": pg.K_x,
        "y": pg.K_y,
        "z": pg.K_z,
        "0": pg.K_0,
        "1": pg.K_1,
        "2": pg.K_2,
        "3": pg.K_3,
        "4": pg.K_4,
        "5": pg.K_5,
        "6": pg.K_6,
        "7": pg.K_7,
        "8": pg.K_8,
        "9": pg.K_9,

        # Scratch supports these keys internally
        "enter": pg.K_RETURN,
        "<": pg.K_LESS,
        ">": pg.K_GREATER,
        "+": pg.K_PLUS,
        "-": pg.K_MINUS,
        "=": pg.K_EQUALS,
        ".": pg.K_PERIOD,
        ",": pg.K_COMMA,
        "%": pg.K_PERCENT,
        "$": pg.K_DOLLAR,
        "#": pg.K_HASH,
        "@": pg.K_AT,
        "!": pg.K_EXCLAIM,
        "^": pg.K_CARET,
        "&": pg.K_AMPERSAND,
        "*": pg.K_ASTERISK,
        "(": pg.K_LEFTPAREN,
        ")": pg.K_RIGHTPAREN,
        "[": pg.K_LEFTBRACKET,
        "]": pg.K_RIGHTBRACKET,
        "?": pg.K_QUESTION,
        "\\": pg.K_BACKSLASH,
        "/": pg.K_SLASH,
        "'": pg.K_QUOTE,
        "\"": pg.K_QUOTEDBL,
        "`": pg.K_BACKQUOTE,

        "backspace": pg.K_BACKSPACE,
        "escape": pg.K_ESCAPE,
        "f1": pg.K_F1,
        "f2": pg.K_F2,
        "f3": pg.K_F3,
        "f4": pg.K_F4,
        "f5": pg.K_F5,
        "f6": pg.K_F6,
        "f7": pg.K_F7,
        "f8": pg.K_F8,
        "f9": pg.K_F9,
        "f10": pg.K_F10,
        "f11": pg.K_F11,
        "f12": pg.K_F12,
    }
    def get_mapping(self,key):
        return self.KEY_MAPPING.get(key,None)
    
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
                self.cdir=self.p.join((self.p.DIR,self.p.NAME))
            else: #如果是一段文件名
                self.p=PathTool(fp,mode='n')
                self.cdir=self.p.join((THISPATH,self.p.NAME))
            self.outdir=self.p.join((self.cdir,'output'))
            f.extractall(self.cdir)
            os.makedirs(self.outdir,exist_ok=True)
            for fn in os.listdir(self.cdir): #批量转换
                p=PathTool(fn,'n')
                if p.SUFFIX=='.svg':
                    csvg.svg2png(url=p.join((self.cdir,p.FILE)),
                                 write_to=p.join((self.cdir,p.NAME+".png")))

    def getdir(self):
        return self.cdir,self.outdir
    
class CodeMaker: #转换核心，生成python代码
    def __init__(self):
        self.modules:list[str]=[] #根据情况导入所需要的库


def main(fp:str='./tests/work1.sb3',path=True):
    UnPackingScratch3File(fp,path)

if __name__=='__main__':
    match len(sys.argv):
        case 1:
            main()
        case 2:
            main(sys.argv[1])
        case 3:
            main(sys.argv[1],bool(int(sys.argv[2])))
        