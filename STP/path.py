from config import *

import zipfile
import xml.etree.ElementTree as ET

from cairosvg import svg2png
from PIL import Image

class PathTool:
    def __init__(self,fp:str|tuple[str]=None,mode='p'):
        '''mode = 'p': fp是一个文件路径;    
           mode = 'n': fp是一个文件名;  
           mode = 'j': 只合并路径，fp的类型为tuple[str]。'''
        if fp:
            if isinstance(fp,str): fp=os.path.normpath(fp)
            #log.debug("Using the PathTool...")
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
    def __init__(self,fp:str):
        """
        解包.sb3文件。
        
        :param fp: .sb3文件位置
        """
        log.debug(f"Unpacking {fp}...")
        with zipfile.ZipFile(fp,'r') as self.f: #解压.sb3文件
            if os.path.basename(fp)!=fp: #如果是一段路径
                self.p=PathTool(fp)
                self.cdir=self.p.join((self.p.DIR,self.p.NAME))
            else: #如果是一段文件名
                self.p=PathTool(fp,mode='n')
                self.cdir=self.p.join((THISPATH,self.p.NAME))
            self.f.extractall(self.cdir)

            #格式化.json文档
            self.prj_path=self.p.join((self.cdir,'project.json'))
            with open(self.prj_path,'r',encoding='utf-8') as f:
               c=json.load(f)
            with open(self.prj_path,'w',encoding='utf-8') as f:
                json.dump(c,f,ensure_ascii=False,indent=4)
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

class PackingScratch3File:
    def __init__(self,dp:str):
        """
        打包.sb3文件。
        
        :param dp: .sb3文件解包后文件夹位置
        """
        if self.is_sb3_dir(dp):
            log.debug(f"Packing from {dp}...")
        else:
            log.error(f"{dp} is not a dir unpacked from a .sb3 file!")
            exit(1)
    def is_sb3_dir(self,dp:str):
        result=True
        if os.path.isdir(dp) and 'project.json' in os.listdir(dp):
            t=PathTool((dp,'project.json'),'j')
            with open(t.join(dp),'r',encoding='utf-8') as f:
                f:dict=json.load(f)
            for i in ('targets','monitors','extensions','meta'):
                if not f.get(i,[]):
                    result=False
                    break
                elif result != False:
                    result=True
        else:
            result=False
        return result