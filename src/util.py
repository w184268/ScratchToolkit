from js2py import eval_js

OperatorSymbols=("+","-","*","/","%","==","!=","<",">","<=",">=")

def installed(name:str):
    try:
        if name=="pygame-ce":
            __import__("pygame")
        else:
            __import__(name)
    except ImportError:
        return False
    else:
        return True
class Data:
    def __init__(self):
        self.pj:dict
        self.baseinfo={
            "semver":self.pj['meta']['semver'],
            "vm":self.pj['meta']['vm'],
            "agent":self.pj['meta']['agent'],
            "platform_name":self.pj['meta']['platform']['name'],
            "platform_url":self.pj['meta']['platform']['url']
            }
        self.mod={ #根据情况导入所需要的库
            "internal":{
                "typing":["",["Any"]],
                "math":["",[]],
                "random":["",[]],
                "sys":["",[]],
                "threading":["",["Thread","Timer"]]
                },
            "third-party":{
                "pygame->pygame-ce":["pg",[]],
                "js2py":["",["eval_js"]]
                }
            }
        self.var={ #存储变量
            "public":{},
            "private":{}
            }
        self.array={ #存储列表
            "public":{},
            "private":{}
            }

class BlockID:
    def __init__(self,id:str,blocks:dict):
        self.id=id
        self.blocks=blocks

class SVariable:
    def __init__(self,name:str,value:str):
        self.name='self.var_'+name
        self.value=value

class SArray:
    def __init__(self,name:str,value:list):
        self.name='self.arr_'+name
        self.value=value

class ReduceJSCode:
    def __init__(self,code:list):
        self.code=code
        self.result=[]
        for i,j in enumerate(self.code):
            next_=self.code[i+1]
            if j in OperatorSymbols and isinstance(next_,str):
                self.result.append(j+next_)
            elif isinstance(next_,(SArray,SVariable)):
                self.result.append(j+next_.name)
    def reduce(self):
        return self.result