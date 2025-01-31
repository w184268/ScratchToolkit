from .config import Tuple,Union

class NestParser:
    def __init__(self,blocks:dict):
        """
        解析嵌套型积木块，生成python代码。
        """
        self.blocks=blocks
    
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
        type={'%s':'int|float|str','%b':'bool'}
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
        判断字符串是否为合法的标识符。
        """
        r=True
        for i in '!@#$%^&*()_+-=[]{}|;:,.<>?':
            if i in s:
                r=False
                break
        return r
    
    def create(self,funccode:dict):
        self.funccode=funccode
        if self.funcname not in self.funccode: #创建函数
            self.funccode[self.funcname]=[{},{}]
        for argname,argdefault,argtype in zip(eval(self.funcmuta['argumentnames']),eval(self.funcmuta['argumentdefaults']),self.argtypes):
            self.funccode[self.funcname][0][argname.replace(' ','_')]=[argdefault,type.get(argtype,'Any')] #type: ignore 
    
    def addcode(self,free=False,args:Union[str,Tuple[str,...]]="",opcode:str="",depth:int=0):
        if not free:
            self.funccode[self.funcname][1]['self.'+opcode+'('+', '.join(args)+')']=depth
        else:
            self.funccode[self.funcname][1][args]=depth
        
    def update(self):
        return self.funccode