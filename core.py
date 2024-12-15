import config

import json
import os,sys

from loguru import logger as log

log.remove()
log.add(sys.stdout,colorize=True,format="<level>[{time:YYYY-MM-DD HH:mm:ss}] [{level}]: {message}</level>")
THISPATH=os.getcwd()
with open("./spriteframe.py","r",encoding="utf-8") as f:
    SPRITE_INIT_CODE=f.read()
with open("./gameframe.py","r",encoding="utf-8") as f:
    GAME_INIT_CODE=''.join(i for i in f.readlines() if 'import' not in i)
with open("./settings.json",'r',encoding='utf-8') as f:
    USERSET:dict=json.load(f)

class CodeMaker: #转换核心，生成python代码
    def __init__(self,pj):
        self.code=[] #存储代码
        self.targets=pj["targets"] #所有角色信息
        self.code.append(SPRITE_INIT_CODE+'\n'+GAME_INIT_CODE)
        for t in self.targets:
            self.give(t)
        self.code.extend(["",
            "if __name__=='__main__':",
            "   rungame=Game()"
        ])

    def give(self,tgs:dict): #给予信息,tgs为targets下每个信息
        #为方便后面操作
        self.isStage:bool=tgs['isStage'] #是否为舞台
        self.name:str=tgs['name'] #角色名
        self.vars:dict=tgs['variables'] #变量
        self.lists:dict=tgs['lists'] #列表
        self.broadcasts:dict=tgs['broadcasts'] #广播
        self.blocks:dict=tgs["blocks"] #积木块
        self.sounds:list=tgs["sounds"] #音频
        self.volume:int=tgs['volume'] #音量
        self.layerOrder:int=tgs["layerOrder"] #角色的图层顺序，值越大，角色越靠前
        
        if self.isStage: #舞台，有些全局设置
            self.tempo:int=tgs['tempo'] #正常速度为60
            self.comments:dict=tgs['comments'] #键是注释的ID，值是注释的内容
            self.currentCostume:int=tgs['currentCostume'] #角色的当前服装索引
            self.costumes:list[dict]=tgs['costumes'] #角色的服装
            self.videoTransparency:int=tgs['videoTransparency'] #角色的视频透明度，范围是0到100，0表示完全透明，100表示完全不透明
            self.videoState:str=tgs['videoState'] #角色的视频状态，可以是on（开启视频）或off（关闭视频）。
            self.textToSpeechLanguage:str=tgs['textToSpeechLanguage'] #角色的文本到语音语言
            self.classname='stage_'+self.name
        else:
            self.visible:bool=tgs.get("visible",True) #角色是否可见
            self.x:float=tgs['x'] #x坐标
            self.y:float=['y'] #y坐标
            self.size:int=tgs['size'] #放大与缩小，100是原始尺寸
            self.direction:int=tgs['direction'] #朝向，0度表示朝右，90度表示朝上，180度表示朝左，270度表示朝下
            self.draggable:bool=tgs['draggable'] #角色的可拖动性
            self.rotation:str=tgs['rotationStyle'] #角色的旋转样式，可以是all around（围绕中心点旋转）、left-right（左右旋转）或don't rotate（不旋转）
            self.classname='spr_'+self.name
        for block in self.blocks.items():
            id,idinfo=block[0],block[1]
            self.add(id,idinfo)
    def add(self,id:str,kw): #积木管理
        type_=f"{self.classname} -> {id}"
        try:
            depth=self.get_nested_depth(kw)
        except Exception as e:
            log.warning(e)
            depth=self.get_nested_depth2(kw)
        opcode=kw["opcode"]
        log.debug(f'Converting {type_}(name="{opcode}" ,depth={depth})...')
        def restr(mode=0,string="",args=()):
            '''
            mode=0: 调用积木方法，string为方法名，args为传参
            mode=1: 创建一个类方法，string为方法名，args为参数名
            mode=2: 创建一个角色，string不填，args为角色信息，按照实际操作
            mode=3: 灵活性的，args不填，string可以是其他代码（如判断、循环等）
            '''
            match mode:
                case 0:
                    self.code.append('    '*(depth+2)+self.classname+'.'+string+'('+', '.join(args)+')')
                case 1:
                    self.code.append('    '*(depth+1)+"def "+string+'('+', '.join(args)+'):')
                case 2:
                    self.code.append('    '*(depth+2)+self.classname+'=Sprite('+','.join(args)+')')
                case 3:
                    self.code.append('    '*(depth+2)+string)
                
        if self.isStage:
            self.restr(2,"")
        match opcode: #匹配相应的积木名
            case "motion_movesteps":
                restr("")
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
        #print(block,type(block))
        parentdict=self.blocks.get(block['parent'],{})
        #print(parentdict)
        if block is not None and parentdict:
            inputs=parentdict.get('inputs',{})
            substack=inputs.get("SUBSTACK",[])
            #print(inputs,substack)
            if parentdict['opcode'] not in USERSET["blocks"]['ignore']:
                if 'topLevel' in block and block['topLevel']:
                    return depth
                if 'parent' in block:
                    if substack:
                        return self.get_nested_depth(parentdict, depth+1)
                    elif not block["shadow"]:
                        return self.get_nested_depth(parentdict, depth)
                    else:
                        return self.get_nested_depth(parentdict, depth + 1)

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
            parentdict=self.blocks.get(current_block['parent'],{})
            inputs=parentdict.get('inputs',{})
            substack=inputs.get("SUBSTACK",[])
            print(type(current_block))
            if current_block is not None and parentdict:
                if parentdict['opcode'] != "event_whenflagclicked":
                    if 'topLevel' in current_block and current_block['topLevel']:
                        continue
                    if 'parent' in current_block:
                        if substack:
                            stack.append(parentdict)
                            depth += 1
                        elif not current_block["shadow"]:
                            continue
                        else:
                            stack.append(parentdict)
                            depth += 1
        return depth