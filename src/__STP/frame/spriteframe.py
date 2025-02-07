import pygame as pg
import sys,math,random
from threading import Timer,Thread

class JSObject:
    def __init__(self,obj):
        self.obj=obj
    def __eq__(self,other):
        return str(self.obj)==str(other.obj)
    def __ne__(self,other):
        return str(self.obj)!=str(other.obj)
    def __str__(self):
        return str(self.obj)
    def __repr__(self):
        return str(self.obj)
class Sprite(pg.sprite.Sprite,Thread): #角色框架
    def __init__(self, image_file:tuple[str], initxy:tuple[int,int], direction:int):
        super().__init__()
        self.image:pg.Surface
        self.images={}
        for i in image_file:
            self.images[i]=pg.image.load(i)
        self.rect = self.image.get_rect() if self.image else pg.Rect(0,0,0,0)
        self.direction=direction
        self.rect.x,self.rect.y=initxy
        self.start()
        


    def motion_gotoxy(self,dx:float,dy:float):
        self.rect.move_ip(dx,dy)
    def motion_glidesecstoxy(self,dx:float,dy:float,duration:int|float):
        distance=duration * 10
        if self.rect:
            if dx != self.rect.x:
                dx=distance*math.cos(math.radians(self.direction))
            if dy != self.rect.y:
                dy=distance*math.sin(math.radians(self.direction))

    def motion_turnright(self, degrees):
        self.image = pg.transform.rotate(self.image, degrees)
    def control_wait(self,s:float):
        Timer(s,lambda:0).start()

