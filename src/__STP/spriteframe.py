import pygame as pg
import sys,math,random
from threading import Timer,Thread

class Sprite(pg.sprite.Sprite): #角色框架
    def __init__(self, image_file:tuple[str], initxy:tuple[float,float], direction:int):
        super().__init__()
        self.image:pg.Surface
        self.images={}
        for i in image_file:
            self.images[i]=pg.image.load(i)
        self.rect = self.image.get_rect() if self.image else pg.Rect(0,0,0,0)
        self.direction=direction
        self.rect.x=initxy[0],self.rect.y=initxy[1]

    def motion_gotoxy(self,dx:float,dy:float):
        self.rect.move_ip(dx,dy)
    def motion_glidesecstoxy(self,dx:float,dy:float,duration:int|float):
        distance=duration * 10
        if dx != self.rect.x:
            dx=distance*math.cos(math.radians(self.direction))
        if dy != self.rect.y:
            dy=distance*math.sin(math.radians(self.direction))

    def motion_turnright(self, degrees):
        self.image = pg.transform.rotate(self.image, degrees)
    def control_wait(self,s:float):
        Timer(s,lambda:0).start()

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