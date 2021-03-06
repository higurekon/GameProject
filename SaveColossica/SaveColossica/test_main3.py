'''
Created on Jun 8, 2014

@author: PC
'''


import pygame
from pygame.locals import *
import sys,os
import spritesheet
import math
import random

workspace = "C:/Users/PC/Google Drive/Game Project/Workspace"

x_bounds = [0,1200]
y_bounds = [0,800]

#### Irene's Rects 

width = 448
height = 450
irenewidth = width
ireneheight = height
irene_rects = {"walk":[(width*0,0,width,height),(width*1,0,width,height),(width*2,0,width,height),(width*3,0,width,height),(width*4,0,width,height),(width*5,0,width,height),(width*6,0,width,height),(width*7,0,width,height),(width*8,0,width,height)],
               "jump":[(width*0,height,width,height),(width*1,height,width,height),(width*2,height,width,height),(width*3,height,width,height),(width*4,height,width,height),(width*5,height,width,height),(width*6,height,width,height)],
               "idle":[(width*0,5+height*2,width,height-5)]}

### Frog's Rects

width = 542
height = 233
frogwidth = width
frogheight = height
frog_rects = {"hop":[(width*0,height*0,368,height),(width*1,height*0,338,height),(width*2,height*0,436,height),(width*3,height*0,462,height),(width*4,height*0,368,height)],
              "hop full":[(width*0,height*1,368,height),(width*1,height*1,338,height),(width*2,height*1,436,height),(width*3,height*1,462,height),(width*4,height*1,368,height)],
              "birth":[(width*0,height*2,368,height),(width*1,height*2,368,height),(width*2,height*2,368,height),(width*3,height*2,368,height),(width*4,height*2,368,height),(width*5,height*2,368,height),(width*6,height*2,368,height),(width*7,height*2,368,height),(width*8,height*2,368,height)],
              "idle":[(width*0,height*0,368,height)],
              "idle full":[(width*0,height*1,368,height)],
              "eat":[(width*0,height*5,368,height),(width*1,height*5,368,height),(width*2,height*5,368,height),(width*3,height*5,368,height),(width*4,height*5,368,height),(width*5,height*5,368,height),(width*6,height*5,368,height)],
              "croak":[(width*0,height*7,368,height),(width*1,height*7,368,height),(width*2,height*7,368,height),(width*3,height*7,368,height),(width*4,height*7,368,height)],
              "croak full":[(width*0,height*8,368,height),(width*1,height*8,368,height),(width*2,height*8,368,height),(width*3,height*8,368,height),(width*4,height*8,368,height)],
              "hatch":[],
              "born":[],
              "tongue":[]}

#### Lengthen Frames

# IRENE
temp = []
for x,i in enumerate(irene_rects["walk"]):
    if x in [2,3,6]:
        temp.extend([i,i,i,i,i,i])
    else:
        temp.extend([i,i,i,i,i,i]) 
irene_rects["walk"] = temp
temp = []
for i in irene_rects["jump"]: 
    temp.extend([i,i,i,i,i,i]) 
irene_rects["jump"] = temp
temp = []
for i in irene_rects["idle"]: 
    temp.extend([i]) 
irene_rects["idle"] = temp

# FROG
temp = []
for i in frog_rects["hop"]: 
    temp.extend([i,i,i,i,i,i]) 
frog_rects["hop"] = temp
temp = []
for i in frog_rects["eat"]: 
    temp.extend([i,i,i,i,i,i,i,i,i,i,i]) 
frog_rects["eat"] = temp

class frog:
    def __init__(self,workspace,infile,rects,colorkey,scale,width,height,direction): # "rects" is a library of rects now.
        self.sprite_lib = {}
        spritesheeter = spritesheet.spritesheet(workspace+infile)
        if "hop" in rects:
            self.spritemaker(spritesheeter,workspace,infile,scale,colorkey,rects,direction,"hop")    
        if "eat" in rects:
            self.spritemaker(spritesheeter,workspace,infile,scale,colorkey,rects,direction,"eat")
        if "birth" in rects:
            self.spritemaker(spritesheeter,workspace,infile,scale,colorkey,rects,direction,"birth")
        if "idle" in rects:
            self.spritemaker(spritesheeter,workspace,infile,scale,colorkey,rects,direction,"idle")
        self.width = width
        self.height = y_bounds[1]-height
        self.x = x_bounds[1]-width
        self.y = y_bounds[1]-height 
        self.frame = 0
        self.timer = 50
        self.sprites = self.sprite_lib["idle right"]
        self.position = self.sprites[self.frame].get_rect().move(self.x,self.y)
        self.state = "idle right"
        self.direction = "right"
        self.offset = 0
        self.done = False
        self.alive = True
    def spritemaker(self,spritesheeter,workspace,infile,scale,colorkey,rects,direction,anim):
        self.sprite_lib[anim+" right"] = []
        self.sprite_lib[anim+" left"] = []
        for i,rect in enumerate(rects[anim]):
            sprite = spritesheeter.image_at(rect,colorkey)
            if scale is not None:
                width,height = sprite.get_size()
                sprite = pygame.transform.scale(sprite,(int(width*scale),int(height*scale)))
            if direction == "left":
                flip = "right"
            else:
                flip = "left"
            self.sprite_lib[anim+" "+direction].append(sprite)
            self.sprite_lib[anim+" "+flip].append(pygame.transform.flip(sprite,True,False))
    def actions(self):
        if self.state == "hop left":
            self.direction = "left"
            self.frame += 1
            if self.frame == len(self.sprites)-1:
                self.done = True
        if self.state == "hop right":
            self.direction = "right"
            self.frame += 1
            if self.frame == len(self.sprites)-1:
                self.done = True
        if self.state == "eat left":
            self.direction = "left"
            self.frame += 1
            if self.frame == len(self.sprites)-1:
                self.done = True
        if self.state == "eat right":
            self.direction = "right"
            self.frame += 1
            if self.frame == len(self.sprites)-1:
                self.done = True
        if self.state in ["idle right","idle left"]:
            pass
    def move_side(self,speed,direction):
        width,height = self.sprites[self.frame].get_size()
        if direction == "right":
            if self.x+width <= x_bounds[1] and self.frame < len(self.sprites):
                self.x = self.x+speed
                self.position = self.sprites[self.frame].get_rect().move(self.x,self.y)
        else:
            if self.x >= x_bounds[0] and self.frame < len(self.sprites):
                self.x = self.x-speed
                self.position = self.sprites[self.frame].get_rect().move(self.x,self.y)
    def resetTimer(self):
        self.timer = 50
    def resetFrame(self):
        self.frame = 0

class player:
    def __init__(self,workspace,infile,rects,colorkey,scale,width,height,direction): # "rects" is a library of rects now.
        self.sprite_lib = {}
        if "jump" in rects:
            self.spritemaker(workspace,infile,scale,colorkey,rects,direction,"jump")    
        if "walk" in rects:
            self.spritemaker(workspace,infile,scale,colorkey,rects,direction,"walk")
        if "idle" in rects:
            self.spritemaker(workspace,infile,scale,colorkey,rects,direction,"idle")
        self.width = width
        self.height = y_bounds[1]-height
        self.x = 0
        self.y = y_bounds[1]-height
        self.frame = 0
        self.sprites = self.sprite_lib["idle right"]
        self.position = self.sprites[self.frame].get_rect().move(self.x,self.y)
        self.state = "idle right"
        self.direction = "right"
        self.gravity = len(self.sprite_lib["jump right"])
        self.alive = True
    def spritemaker(self,workspace,infile,scale,colorkey,rects,direction,anim):
        spritesheeter = spritesheet.spritesheet(workspace+infile)
        self.sprite_lib[anim+" right"] = []
        self.sprite_lib[anim+" left"] = []
        for rect in rects[anim]:
            sprite = spritesheeter.image_at(rect,colorkey)
            if scale is not None:
                sprite = pygame.transform.scale(sprite,scale)
            if direction == "left":
                flip = "right"
            else:
                flip = "left"
            self.sprite_lib[anim+" "+direction].append(sprite)
            self.sprite_lib[anim+" "+flip].append(pygame.transform.flip(sprite,True,False))
    def move_up(self,threshold):
        if self.y >= 0:
            self.y = self.y - threshold
            self.position = self.sprites[self.frame].get_rect().move(self.x,self.y)
    def move_down(self,threshold): ### Eventually replace this with collision with ground object.
        if self.y < self.height:
            self.y = self.y + threshold
            self.position = self.sprites[self.frame].get_rect().move(self.x,self.y)
    def move_right(self,speed):
        if self.x+self.width <= x_bounds[1] and self.frame < len(self.sprites):
            self.x = self.x+speed
            self.position = self.sprites[self.frame].get_rect().move(self.x,self.y)
    def move_left(self,speed):
        if self.x >= x_bounds[0] and self.frame < len(self.sprites):
            self.x = self.x-speed
            self.position = self.sprites[self.frame].get_rect().move(self.x,self.y)
    def walk(self,direction):
        if self.state not in ["walk "+direction,"grabbed"]:
            self.state = "walk "+direction
            self.sprites = self.sprite_lib[self.state]
            self.reset()
            self.direction = direction
        if self.x+self.width <= x_bounds[1] or self.x >= x_bounds[0]:
            self.frame += 1-len(self.sprites)*(self.frame==(len(self.sprites)-1))
    def jump(self,direction):
        if self.state not in ["jump left","jump right","grabbed"]:
            self.reset()
        if self.state != "jump "+direction: ##### Have better definition for grounded state
            self.state = "jump "+direction
            self.sprites = self.sprite_lib[self.state]
            self.direction = direction
        if self.gravity >= -len(self.sprite_lib["jump right"]):
            self.move_up(self.gravity)
            self.gravity -= 3
        if self.frame < len(self.sprites)-1:
            self.frame += 1
        else:
            self.state = "idle "+direction
            self.reset()
    def reset(self):
        self.frame = -1
        self.gravity = len(self.sprite_lib["jump right"])
    def idle(self):
        if self.direction == "left":
            self.state = "idle left"
        else:
            self.state = "idle right"
        self.sprites = self.sprite_lib[self.state]
        self.reset()

def main():
    pygame.init()

    screen = pygame.display.set_mode((x_bounds[1], y_bounds[1]))
    background = pygame.image.load(workspace+'/1397522201169.gif').convert()
    background = pygame.transform.scale(background,(x_bounds[1],y_bounds[1]))
    screen.blit(background,(0,0))
    
    clock = pygame.time.Clock()
    irene = player(workspace,"/Revision For Lines_01_Without Lines_white.png",irene_rects,(255,255,255),(int(irenewidth*0.5),int(ireneheight*0.5)),int(irenewidth*0.5),int(ireneheight*0.5),"right")
    
    frog1 = frog(workspace,"/Revision for Line_Frog Without Lines.png", frog_rects,(0,0,0),1.7,int(frogwidth*1.7),int(frogheight*1.7),"right")
    
    while 1:
        clock.tick(60)
        screen.blit(background,(0,0))
        
    # FROG
        
        if (irene.x - (frog1.x+frog1.width)) < 50 and ((irene.x+irene.width) - frog1.x) > -50:
            if frog1.state not in ["hop left","hop right"]: 
                if frog1.state == "idle "+frog1.direction:
                    frog1.resetFrame()
                if (irene.x+irene.width - frog1.x) < 0:
                    frog1.state = "eat left"
                    frog1.sprites = frog1.sprite_lib[frog1.state]
                elif (irene.x - (frog1.x+frog1.width)) > 0:
                    frog1.state = "eat right"
                    frog1.sprites = frog1.sprite_lib[frog1.state]
        if frog1.state in ["eat left","eat right"]:
            if frog1.done:
                frog1.resetTimer()
                frog1.resetFrame()
                frog1.done = False
                frog1.state = "idle "+frog1.direction
                frog1.sprites = frog1.sprite_lib[frog1.state]
        elif frog1.state in ["idle left","idle right"]:
            frog1.timer -= 1
            if frog1.timer == 0:
                frog1.direction = random.choice(["left","right"])
                frog1.state = "hop "+frog1.direction
                frog1.sprites = frog1.sprite_lib[frog1.state]
        elif frog1.state in ["hop left","hop right"]:
            frog1.move_side(7,frog1.direction)
            print frog1.x
            if frog1.done:    
                frog1.state = "idle "+frog1.direction 
                frog1.resetTimer()
                frog1.resetFrame()
                frog1.done = False
        frog1.actions()
        screen.blit(frog1.sprites[frog1.frame],frog1.position)
        
    # IRENE
    #Handle Input Events
        key = pygame.key.get_pressed()
        if irene.alive:
            if key[pygame.K_RIGHT]:
                if irene.state not in ["jump left","jump right"]:
                    irene.walk("right")
                    irene.move_right(5)
                if irene.state in ["jump left","jump right"]:
                    irene.jump("right")
                    irene.move_right(7)
            elif key[pygame.K_LEFT]:
                if irene.state not in ["jump left","jump right"]:
                    irene.walk("left")
                    irene.move_left(5)
                if irene.state in ["jump left","jump right"]:
                    irene.jump("left")
                    irene.move_left(7)
                
            else:
                if irene.state in ["jump left","jump right"]:
                    irene.jump(irene.direction)
                else:
                    irene.idle()
            for event in pygame.event.get():
                if event.type == KEYDOWN and event.key == K_SPACE:
                    irene.jump(irene.direction)
                    
            screen.blit(irene.sprites[irene.frame],irene.position)

            
        if key[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()
        pygame.event.pump()
         
        
                 
        pygame.display.flip()
            
    
    
    
    
    
    
    
    
    
    
    
    
    
if __name__ == '__main__': main()

