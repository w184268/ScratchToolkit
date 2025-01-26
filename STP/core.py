from path import *

log.remove()
log.add(sys.stdout,colorize=True,format="<level>[{time:YYYY-MM-DD HH:mm:ss}] [{level}]: {message}</level>")

class CodeParser: #解析project.json
    def __init__(self,last:UnPackingScratch3File):
        """
        转换核心，生成python代码。
        
        :param pj: project.json解析后的dict类型
        """
        self.t=PathTool(self.cdir)
        with open(self.t.join((self.cdir,"project.json")),'r',encoding='utf-8') as f: #导入project.json
            self.pj=json.load(f)
        self.last=last
        self.mod:list[str]=[] #根据情况导入所需要的库
        self.var=dict() #存储变量
        self.array=dict() #存储列表
        self.cdir,self.outdir=last.cdir,last.outdir
        
        self.depth=0 #默认深度
        self.code=[] #存储代码（总）
        self.sprcode:dict[str,dict]={} #代码（每个角色）
        self.targets=self.pj["targets"] #所有角色信息
        self.code.append(SPRITE_INIT_CODE)
        self.fstr(f"pg.display.set_caption('{last.p.NAME}')",3)
        for t in self.targets:
            self.give(t)
            self.code.extend(self.sprcode)
            self.sprcode={} #恢复默认
        self.code.extend([
            GAME_INIT_CODE,
            "",
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
        self.fstr(mode=2,args=())
        self.funccode={"__init__":[[],[]]} #代码（角色下函数）
        for block in self.blocks.items():
            id,idinfo=block
            #print(block)
            if isinstance(idinfo,dict): #一般积木块
                self.add(id,idinfo)
                self.depth=0 #恢复默认
            else: #变量、常量、列表类型
                self.var_and_list(id,idinfo)
    def var_and_list(self,id:str,kw): #变量、常量、列表管理
        ...
    def add(self,id:str,kw): #积木管理
        type_=f"{self.classname} -> {id}"
        try:
            self.depth,self.base=self.get_nested_depth2(kw)
            #print(self.get_nested_depth(kw))
        except Exception as e:
            log.warning(e)
            self.depth,self.base=self.get_nested_depth(kw)
        self.opcode=kw["opcode"]
        log.debug(f'Converting {type_} (name="{self.opcode}" ,depth={self.depth})...')

        match self.opcode: #匹配相应的积木名
            case "control_wait":
                self.fstr("")
            case "control_forever":
                self.fstr("while True:",3)
            case "procedures_call":
                self.fstr(kw["mutation"]["proccode"],1,args=())
            case _:
                if self.opcode not in USERSET["blocks"]['ignore']:
                    log.warning(f'Unknown id "{self.opcode}"!')

    def write_result(self):
        self.outpyfile=self.t.join((self.outdir,self.last.p.NAME+".py"))
        with open(self.outpyfile,'w',encoding='utf-8') as f:
            f.write('\n'.join(self.code))
    def fstr(self,string="",mode=0,args=()):
        '''
        mode=0: 调用积木方法，string不填，args为传参  
        mode=1: 创建一个函数，string为方法名，args为参数名  
        mode=2: 创建一个角色，string不填，args为角色信息，按照实际操作  
        mode=3: 灵活性的，args不填，string是代码（如判断、循环等）
        '''
        args=(str(i) for i in args)
        match mode:
            case 0:
                #self.sprcode.append('    '*(self.depth+2)+self.classname+'.'+self.opcode+'('+', '.join(args)+')')
                if self.base.get('opcode','').startswith('procedures_'):
                    ...
            case 1:
                #self.funccode.append('    '*(self.depth+1)+"def "+string+'(self,'+', '.join(args)+'):')
                ...
            case 2:
                #self.code.append('    '*(self.depth+2)+self.classname+'=Sprite('+','.join(args)+')')
                self.code.extend([
                    'class '+self.classname+'(Sprite):',
                    '    def __init__(self,'+','.join(args)+'):',
                    '        super().__init__()'
                    ])
            case 3:
                self.code.append('    '*(self.depth+2)+string)

    def get_nested_depth(self,block:dict,depth=0):
        """
        递归函数，用于计算积木块的嵌套深度。
        
        :param block: 当前积木块
        :param depth: 当前深度
        :return: 积木块的嵌套深度
        """
        print(block,type(block))
        parentdict=self.blocks.get(block.get('parent',''),{})
        #print(parentdict)
        if block is not None and parentdict:
            inputs=parentdict.get('inputs',{})
            substack=inputs.get("SUBSTACK",[])
            #print(inputs,substack)
            if parentdict['opcode'] not in USERSET["blocks"]['ignore']:
                if block.get('topLevel',False):
                    return depth,block
                if 'parent' in block:
                    if substack: #嵌套类型
                        return self.get_nested_depth(parentdict, depth+1)
                    elif not block["shadow"]: #不隐藏的纯积木
                        return self.get_nested_depth(parentdict, depth)
                    else:
                        #return self.get_nested_depth(parentdict, depth + 1)
                        return self.get_nested_depth({}, depth+1)
            else:
                block={}

        return depth,block
    def get_nested_depth2(self,block,depth=0): #备用方法
        """
        使用迭代方法计算积木块的嵌套深度。
        
        :param block: 当前积木块
        :return: 积木块的嵌套深度
        """
        stack:list[dict] = [block] 
        while stack:
            current_block = stack.pop()
            parentdict=self.blocks.get(current_block.get('parent',''),{})
            inputs:dict=parentdict.get('inputs',{})
            substack=inputs.get("SUBSTACK",[])
            substackN=inputs.get("")
            #print(type(current_block))
            if current_block is not None and parentdict:
                if parentdict['opcode'] not in USERSET["blocks"]['ignore']:
                    if current_block.get('topLevel',False):
                        continue
                    if 'parent' in current_block:
                        if self.opcode in substack:
                            stack.append(parentdict)
                            depth += 1
                        elif not current_block["shadow"]:
                            continue
                        else:
                            print(current_block,parentdict)
                            #stack.append(parentdict)
                            stack.append({})
                            #depth += 1
                else:
                    current_block={}
        return depth,current_block