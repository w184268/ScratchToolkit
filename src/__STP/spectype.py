from .config import Tuple,Union,init_path,safe_eval
init_path()
from src.util import is_spcial

class ID:
    def __init__(self,id:str,blocks:dict):
        self.id=id
        self.blocks=blocks

class BlockBuffer:
    def __init__(self):
        self.buffer={}
    def add(self,id:str,value:tuple):
        self.buffer[id]=value
    def get(self,id:str,default=[]):
        return ''.join(self.buffer.get(id,default))
    def update(self):
        b1=self.buffer.copy()
        for id,values in b1.items():
            self.bigupdate(id,values)
        b2=self.buffer.copy()
        for id,values in b2.items():
            self.a=[]
            print(id,values)
            self.tidy(values)
            self.buffer[id]=self.a
        
    def tidy(self,v):
        if isinstance(v,list):
            for j in v:
                self.tidy(j)
        else:
            self.a.append(v)

    def bigupdate(self,_id="",values=(),recursive=False):
        a=[]
        for i in range(len(values)):
            value=values[i]
            if isinstance(value,(int,float,list)):
                a.append(value)
            elif isinstance(value,str):
                a.append("'"+value+"'")
            elif isinstance(value,ID):
                print(value.id)
                a.append(self.bigupdate(_id,('(',*self.buffer.get(value.id,()),')'),True))
            else:
                raise TypeError(f"Unsupported type {type(value)} in BlockBuffer.update()")
        self.buffer[_id]=a
        print(self.buffer)
        if recursive:
            return a

class InputParser:
    def __init__(self,blocks:dict,buffer:BlockBuffer):
        """
        解析含参型积木块，生成python代码。
        """
        self.blocks=blocks
        self.buffer=buffer
        self.code=[]
    
class VarListParser:
    def __init__(self,blocks:dict):
        """
        解析变量及列表型积木块，生成python代码。
        """
        self.blocks=blocks

class FuncParser:
    def __init__(self,blocks:dict,baseblock:dict):
        """
        解析函数型积木块，生成python代码。
        """
        self.blocks=blocks
        self.base=baseblock
        self.funcmuta=self.blocks[self.base['inputs']['custom_block'][1]]['mutation']
        self.type={'%s':'int|float|str','%b':'bool'}
        self.name=[]
        self.argtypes=[]
        c=self.funcmuta['proccode'].split(' ')
        for i in range(len(c)):
            if self.isidentifier(c[i]):
                if i==0 or not self.isidentifier(c[i-1]):
                    self.name.append(c[i])
                else:
                    self.name[-1]+=c[i]
            else:
                self.argtypes.append(c[i])
        self.funcname='_'+'_'.join(self.name)
    def isidentifier(self,s:str):
        """
        判断参数字符串是否为合法的标识符。
        """
        r=True
        for i in '!@#$%^&*()/\\+-=[]{}|;:,.<>?':
            if i in s:
                r=False
                break
        return r
    
    def create(self,funccode:dict):
        self.funccode=funccode
        if self.funcname not in self.funccode: #创建函数
            self.funccode[self.funcname]=[{},{}]
        for argname,argdefault,argtype in zip(safe_eval(self.funcmuta['argumentnames']),safe_eval(self.funcmuta['argumentdefaults']),self.argtypes):
            self.funccode[self.funcname][0][argname.replace(' ','_')]=[argdefault,self.type.get(argtype,'Any')] #type: ignore 
    
    def addcode(self,free=False,args:Union[str,Tuple[str,...]]="",opcode:str="",depth:int=0):
        if not free:
            self.funccode[self.funcname][1]['self.'+opcode+'('+', '.join(args)+')']=depth
        else:
            self.funccode[self.funcname][1][args]=depth
        
    def update(self):
        return self.funccode