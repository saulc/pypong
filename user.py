'''
Created on Apr 28, 2015

@author: saul

user class for controllable item
'''
import pygame
from item import Item
from bullet import *

class User(Item):
    def __init__(self, x, y):
        super().__init__(x, y)
        images =[]
        i = pygame.image.load("./res/user.png").convert_alpha()
        images.append(i)
        i = pygame.image.load("./res/userRight.png").convert_alpha()
        images.append(i)
        i = pygame.transform.flip(i, True, False)
        images.append(i)
        self.images = images
        self.image = images[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.radius = self.image.get_width()//2
        self.topSpeed = 25
        self.acc = 1
        self.gunzero = 1
        self.gunone = 2
        self.guntwo = 3
        self.guns = [1, 2, 3]
        self.gunspeed = 7
        self.firing = False
        self.power = 100
#         self.drones = pygame.sprite.Group()
        
#     def addDrones(self, drones):
#         self.drones.add(drones)
#         

    def update(self):
       
        i = 0
        if self.vx > 0:
            i = 1
        elif self.vx < 0:
            i = 2
        self.image = self.images[i]
        
        super().update()
#         pygame.draw.circle(surface, (0, 200, 0),
#                            (surface.get_width()//2,  surface.get_height()//2), self.radius-10, 1)
#         self.image = surface   
        
#         self.levelPos += 1
        if self.firing:
            self.gunone += 1
#             print ( str(self.gunone))
        


        
    def go(self, vx, vy):
        self.vx = int(vx * self.topSpeed)
        self.vy = int(vy * self.topSpeed)
        
        if self.vx > self.topSpeed: self.vx = self.topSpeed
        if self.vy > self.topSpeed: self.vy = self.topSpeed
        
            
    def goLeft(self):
        self.vx = -self.topSpeed
#         if self.vx > -self.topSpeed:
#             self.vx -= self.acc
        
    def goRight(self):
        self.vx = self.topSpeed
#         if self.vx < self.topSpeed:
#             self.vx += self.acc
    def goUp(self):
        self.vy = -self.topSpeed
        
    def goDown(self):
        self.vy = self.topSpeed
        
    def stopX(self):
        self.vx = 0
        
    def stopY(self):
        self.vy = 0
        
    def ceaseFire(self, gun):
        self.firing = False
        
    def tryFire(self, gun):
        v = self.gunone % self.gunspeed
        print (str (v))
        
        return v  == 0
            
    def fire(self, gun):
       
        print('fire gun: ' + str(gun))
        x = 0
        y = 0
        if gun == 0:
            x = self.rect.x + self.image.get_width()//2 -5
            y = self.rect.y
              
        elif gun == 1:
            x = self.rect.x + 40
            y = self.rect.y + self.image.get_height()//2
            
        elif gun == 2:
            x = self.rect.x + self.image.get_width() - 40 
            y = self.rect.y + self.image.get_height()//2
            
        guntype = self.guns[gun]   
        if guntype == 1:
            return Bullet(x, y)   
        
        elif guntype == 2:
            return BigBullet(x, y)
   
        elif guntype == 3:
            return Missile(x, y)
            
      
                
                
                
                
                
                
                
                
                
                
        
        