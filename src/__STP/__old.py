'''
class Function():
    def __init__(self):
        self.func:dict[Sprite,dict[str,]]={}
        self.args:dict[Sprite,dict[str,tuple]]={}
    def add(self,sp:Sprite,func:str,exec,args=()):
        if self.func.get(sp,{}).get(func):
            self.func[sp][func]+=exec
            self.args[sp][func]+=args
        else:
            self.func[sp]={func:exec}
            self.args[sp]={func:args}
    def run(self,sp:Sprite,func:str):
        exec=self.func[sp][func]
        args=self.args[sp][func]
        for e,a in zip(exec,args):
            e(*a)
'''