'''
Created on May 31, 2014

@author: PC
'''

import pygame
from pygame.locals import *
import sys,os
import spritesheet

workspace = "C:/Users/PC/Google Drive/Game Project/Workspace"

x_bounds = [0,1000]
y_bounds = [0,600]

player1_rects = [(26,0,85,128),(154,0,85,128),(282,0,85,128),(410,0,85,128),(538,0,85,128),(666,0,85,128),(794,0,85,128),(922,0,85,128),
            (26,128,85,128),(154,128,85,128),(282,128,85,128),(410,128,85,128),(538,128,85,128),(666,128,85,128),(794,128,85,128),(922,128,85,128),
            (26,256,85,128),(154,256,85,128),(282,256,85,128),(410,256,85,128),(538,256,85,128),(666,256,85,128),(794,256,85,128),(922,256,85,128),
            (26,384,85,128),(154,384,85,128),(282,384,85,128),(410,384,85,128),(538,384,85,128),(666,384,85,128),(794,384,85,128),(922,384,85,128),
            (26,512,85,128),(154,512,85,128),(282,512,85,128),(410,512,85,128),(538,512,85,128)]

boss_rects_idle = [(0,8,45,49),(47,8,45,49),(90,8,44,49),(144,8,45,49),(188,8,45,49),(232,8,45,49)]
boss_rects_eat = [(0,190,44,49),(54,190,54,49),(108,190,54,49),(162,190,54,49),(216,190,54,49)]

irene_rects_stop = [(24,72,121,202),(24+121,72,121,202),(24+121*2,72,121,202),(24+121*3,72,121,202),(24+121*4,72,121,202),(24+121*5,72,121,202)]
irene_rects_start = [(24+121*5,72,121,202),(24+121*6,72,121,202),(24+121*7,72,121,202),(24+121*8,72,121,202),(24+121*9,72,121,202),(24+121*10,72,121,202)]
irene_rects_walk = [(24,324,121,202),(24+121,324,121,202),(24+121*2,324,121,202),(24+121*3,324,121,202),(24+121*4,324,121,202),(24+121*5,324,121,202),(24+121*6,324,121,202),(24+121*7,324,121,202),(24+121*8,324,121,202)]
irene_rects_idle = [(24+121*5,72,121,202)]
temp = []
for i in irene_rects_stop: # Hack
    temp.extend([i]) # Hack
irene_rects_stop = temp
temp = []
for i in irene_rects_start: # Hack
    temp.extend([i]) # Hack
irene_rects_start = temp
temp = []
for i in irene_rects_walk: # Hack
    temp.extend([i,i,i]) # Hack
irene_rects_walk = temp
temp = []
for i in irene_rects_idle: # Hack
    temp.extend([i]) # Hack
irene_rects_idle = temp

class Irene:
    def __init__(self,workspace,infile,rects,width,colorkey,scale,height):
        spritesheeter = spritesheet.spritesheet(workspace+infile)
        self.sprite_lib = {}
        newsprites = []
        for rect in rects:
            sprite = spritesheeter.image_at(rect,colorkey)
            if scale is not None:
                sprite = pygame.transform.scale(sprite,scale)
            newsprites.append(sprite)
        self.sprite_lib["idle"] = newsprites
        self.sprites = self.sprite_lib["idle"]
        self.width = width
        self.coord = [0,height]
        self.frame = 0
        self.position = self.sprites[self.frame].get_rect().move(self.coord[0],self.coord[1])
        self.orientation = "right"
        self.state = "idle"
        self.status = True
    def add_animation(self,workspace,infile,rects,colorkey,scale,name):
        spritesheeter = spritesheet.spritesheet(workspace+infile)
        newsprites = []
        for rect in rects:
            sprite = spritesheeter.image_at(rect,colorkey)
            if scale is not None:
                sprite = pygame.transform.scale(sprite,scale)
            newsprites.append(sprite)
        self.sprite_lib[name] = newsprites
    def stop(self):
        if self.state == "walk":
            self.frame = 0
            self.state = "idle"
            self.sprites = self.sprite_lib["idle"]
            self.orientation = "right"
    def walk_right(self,edge):
#         if self.sprites == self.sprite_lib["idle"]:
#             self.frame = -1
#             self.sprites = self.sprite_lib["start"]
#         if self.sprites == self.sprite_lib["start"]:
#             if self.frame < len(self.sprite_lib["start"])-1:
#                 self.frame+=1
#                 self.coord[0] = self.coord[0]+1
#                 self.position = self.sprites[self.frame].get_rect().move(self.coord[0],self.coord[1])
#             else:
#                 self.sprites = self.sprite_lib["walk"]
#                 self.frame = -1
#         elif self.sprites == self.sprite_lib["walk"]:
        if self.coord[0]+self.width <= edge:
            if self.state == "idle":
                self.sprites = self.sprite_lib["walk"]
                self.state = "walk"
            if self.orientation != "right":
                self.orientation = "right"
                newsprites = []
                for sprite in self.sprites:
                    newsprites.append(pygame.transform.flip(sprite,True,False))
                    self.sprites = newsprites
            self.frame += 1-len(self.sprites)*(self.frame==(len(self.sprites)-1))
            self.coord[0] = self.coord[0]+6
            self.position = self.sprites[self.frame].get_rect().move(self.coord[0],self.coord[1])
    def walk_left(self,edge):
#         if self.sprites == self.sprite_lib["idle"]:
#             self.frame = -1
#             self.sprites = self.sprite_lib["start"]
#         if self.sprites == self.sprite_lib["start"]:
#             if self.frame < len(self.sprite_lib["start"])-1:
#                 self.frame+=1
#                 self.coord[0] = self.coord[0]-1
#                 self.position = self.sprites[self.frame].get_rect().move(self.coord[0],self.coord[1])
#             else:
#                 self.sprites = self.sprite_lib["walk"]
#                 self.frame = -1
#         elif self.sprites == self.sprite_lib["walk"]:
        if self.coord[0] >= edge:
            if self.state == "idle":
                self.sprites = self.sprite_lib["walk"]
                self.state = "walk"
            if self.orientation != "left":
                self.orientation = "left"
                newsprites = []
                for sprite in self.sprites:
                    newsprites.append(pygame.transform.flip(sprite,True,False))
                    self.sprites = newsprites
            self.frame += 1-len(self.sprites)*(self.frame==(len(self.sprites)-1))
            self.coord[0] = self.coord[0]-6
            self.position = self.sprites[self.frame].get_rect().move(self.coord[0],self.coord[1])


class player:
    def __init__(self,workspace,infile,rects,width,colorkey,scale,height):
        spritesheeter = spritesheet.spritesheet(workspace+infile)
        self.sprite_lib = {}
        sprites_walk = []
        for rect in rects:
            sprite = spritesheeter.image_at(rect,colorkey)
            if scale is not None:
                sprite = pygame.transform.scale(sprite,scale)
            sprites_walk.append(sprite)
        self.sprite_lib["walk"] = sprites_walk
        self.sprites = self.sprite_lib["walk"]
        self.frame = 0
        self.width = width
        self.coord = [0,height]
        self.position = self.sprites[self.frame].get_rect().move(self.coord[0],self.coord[1])
        self.orientation = "right"
        self.status = True
    def walk_right(self,edge):
        if self.coord[0]+self.width <= edge:
            if self.orientation is not "right":
                self.orientation = "right"
                newsprites = []
                for sprite in self.sprites:
                    newsprites.append(pygame.transform.flip(sprite,True,False))
                    self.sprites = newsprites
            self.frame += 1-len(self.sprites)*(self.frame==(len(self.sprites)-1))
            self.coord[0] = self.coord[0]+3
            self.position = self.sprites[self.frame].get_rect().move(self.coord[0],self.coord[1])
    def walk_left(self,edge):
        if self.coord[0] >= edge:
            if self.orientation is not "left":
                self.orientation = "left"
                newsprites = []
                for sprite in self.sprites:
                    newsprites.append(pygame.transform.flip(sprite,True,False))
                    self.sprites = newsprites
            self.frame += 1-len(self.sprites)*(self.frame==(len(self.sprites)-1))
            self.coord[0] = self.coord[0]-3
            self.position = self.sprites[self.frame].get_rect().move(self.coord[0],self.coord[1])

class npc:
    def __init__(self,workspace,infile,rects_idle,rects_eat,width,colorkey,scale,height):
        spritesheeter = spritesheet.spritesheet(workspace+infile)
        self.sprite_lib = {}
        
        sprites_idle = []
        sprites_eat = []
        
        temp = []
        for i in rects_idle: # Hack
            temp.extend([i, i, i, i]) # Hack
        rects_idle = temp
        
        temp = []
        for i in rects_eat: # Hack
            temp.extend([i, i, i, i, i, i, i]) # Hack
        rects_eat = temp
        
        for rect in rects_idle:
            sprite = spritesheeter.image_at(rect,colorkey)
            if scale is not None:
                sprite = pygame.transform.scale(sprite,scale)
            sprites_idle.append(sprite)
        for rect in rects_eat:
            sprite = spritesheeter.image_at(rect,colorkey)
            if scale is not None:
                sprite = pygame.transform.scale(sprite,scale)
            sprites_eat.append(sprite)
        self.sprite_lib["idle"] = sprites_idle
        self.sprite_lib["eat"] = sprites_eat
        
        self.sprites = self.sprite_lib["idle"]
        self.frame_idle = 0
        self.frame_eat = 0
        self.width = width
        self.coord = [700,height]
        self.position = self.sprites[self.frame_idle].get_rect().move(self.coord[0],self.coord[1])
        self.orientation = "right"
        self.full = False
    def idle (self):
        self.sprites = self.sprite_lib["idle"]
        self.frame_idle += 1-len(self.sprites)*(self.frame_idle==(len(self.sprites)-1))
    def eat (self,player,gulp_sound):
        self.sprites = self.sprite_lib["eat"]
        self.frame_eat += 1
        if self.frame_eat > 5 and player.status:
            player.status = False
            gulp_sound.play()
        if self.frame_eat >= len(self.sprites)-1:
            self.full = True
 
def main():
    pygame.init()

    screen = pygame.display.set_mode((x_bounds[1], y_bounds[1]))
    pygame.display.set_caption('Irene Walk Test')
    background = pygame.image.load(workspace+'/1397522201169.gif').convert()
    background = pygame.transform.scale(background,(1000,600))
    screen.blit(background,(0,0))
    
    clock = pygame.time.Clock()
    
    player1 = player(workspace,"/Anime-Girl-Side_green.png",player1_rects,85,(0,255,0),None,400)
    boss = npc(workspace,"/warty_test.png",boss_rects_idle,boss_rects_eat,44,(0,0,0),(264,294),300)
    irene = Irene(workspace,"/Irene_W_Sprite_edited.png",irene_rects_idle,85,(255,255,255),None,400)
    irene.add_animation(workspace,"/Irene_W_Sprite_edited.png",irene_rects_stop,(255,255,255),None,"stop")
    irene.add_animation(workspace,"/Irene_W_Sprite_edited.png",irene_rects_start,(255,255,255),None,"start")
    irene.add_animation(workspace,"/Irene_W_Sprite_edited.png",irene_rects_walk,(255,255,255),None,"walk")
    
    gulp_sound = pygame.mixer.Sound(workspace+'/397119_SOUNDDOGS__hu.wav')
    gulp_sound_played = False
    
    while 1:
        clock.tick(30)
        screen.blit(background,(0,0))
    #Handle Input Events
        key = pygame.key.get_pressed()
        if  abs(irene.coord[0] - boss.coord[0]) < 24 and not boss.full:
            screen.blit(boss.sprites[boss.frame_eat],boss.position)
            boss.eat(irene,gulp_sound)
        else:
            boss.idle()
            screen.blit(boss.sprites[boss.frame_idle],boss.position)
        if irene.status:
            if key[pygame.K_RIGHT]:
                screen.blit(irene.sprites[irene.frame],irene.position)
                irene.walk_right(x_bounds[1])
            elif key[pygame.K_LEFT]:
                screen.blit(irene.sprites[irene.frame],irene.position)
                irene.walk_left(x_bounds[0])
            else:
                irene.stop()
                screen.blit(irene.sprites[irene.frame],irene.position)
        if key[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()
        pygame.event.pump()
        
        pygame.display.flip()
            
    
    
    
    
    
    
    
    
    
    
    
    
    
if __name__ == '__main__': main()