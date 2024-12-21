#  ____                          _            _               _____                   ____                                             
# / ___|    ___   _ __    __ _  | |_    ___  | |__           |_   _|   ___           |  _ \   _   _    __ _    __ _   _ __ ___     ___ 
# \___ \   / __| | '__|  / _` | | __|  / __| | '_ \   _____    | |    / _ \   _____  | |_) | | | | |  / _` |  / _` | | '_ ` _ \   / _ \\
#  ___) | | (__  | |    | (_| | | |_  | (__  | | | | |_____|   | |   | (_) | |_____| |  __/  | |_| | | (_| | | (_| | | | | | | | |  __/
# |____/   \___| |_|     \__,_|  \__|  \___| |_| |_|           |_|    \___/          |_|      \__, |  \__, |  \__,_| |_| |_| |_|  \___|
#                                                                                             |___/   |___/                            
# Scratch-To-Pygame(Beta v0.0.1)
# Made by EricDing618.
                  
import pygame as pg
import sys,math,random
class Sprite(pg.sprite.Sprite): #角色框架
    def __init__(self, image_file:tuple[str], initxy:tuple[float,float], direction:int):
        super().__init__()
        self.images={}
        for i in image_file:
            self.images[i]=pg.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.x=initxy[0],self.rect.y=initxy[1]

    def move(self,dx:float,dy:float):
        self.rect.move_ip(dx,dy)
    def move(self,dx:float,dy:float,duration:int|float):
        distance=duration * 10
        if dx != self.rect.x:
            dx=distance*pg.math.cos(pg.math.radians(self.direction))
        if dy != self.rect.y:
            dy=distance*pg.math.sin(pg.math.radians(self.direction))

    def turn_right(self, degrees):
        self.image = pg.transform.rotate(self.image, degrees)
