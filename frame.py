#  ____                          _            _               _____                   ____                                             
# / ___|    ___   _ __    __ _  | |_    ___  | |__           |_   _|   ___           |  _ \   _   _    __ _    __ _   _ __ ___     ___ 
# \___ \   / __| | '__|  / _` | | __|  / __| | '_ \   _____    | |    / _ \   _____  | |_) | | | | |  / _` |  / _` | | '_ ` _ \   / _ \\
#  ___) | | (__  | |    | (_| | | |_  | (__  | | | | |_____|   | |   | (_) | |_____| |  __/  | |_| | | (_| | | (_| | | | | | | | |  __/
# |____/   \___| |_|     \__,_|  \__|  \___| |_| |_|           |_|    \___/          |_|      \__, |  \__, |  \__,_| |_| |_| |_|  \___|
#                                                                                             |___/   |___/                            
# Scratch-To-Pygame(Beta v0.0.1)
# Made by EricDing618.
                  
import pygame as pg
import sys
class Character(pg.sprite.Sprite): #角色框架
    def __init__(self, image_file, location):
        super().__init__()
        self.image = pg.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def turn_right(self, degrees):
        self.image = pg.transform.rotate(self.image, degrees)
class Background(pg.sprite.Sprite): #背景类
    def __init__(self, image_file, location):
        super().__init__()
        self.image = pg.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

class Game:
    def __init__(self):
        pg.init() #初始化
        screen = pg.display.set_mode(800,600) #舞台大小为800,600