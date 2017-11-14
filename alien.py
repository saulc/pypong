'''
Created on Apr 28, 2015

@author: saul

Alien base class, for standard behavior
subclasses for varied behavior
'''
import pygame
from item import Item
from bullet import AlienBullet
from math import cos,sin, pi
import random

class Alien(Item):
    
    def __init__(self, x, y, maxy):
        super().__init__(x, y)
        self.image = pygame.image.load("./res/a1.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.maxy = maxy
        self.amp = 30
        self.speed= 1
        self.power = 5
        self.attack = 100
        self.aCount = random.randint(0, self.attack)
        self.angle = 30
    
    def tryFire(self):
#         if self.rect.y < 0: return False    #no shooting till on screen
        return self.aCount >= self.attack
    
    def fire(self):
        self.aCount = 0
        
        return AlienBullet(self.getCenter()[0]-25, self.getCenter()[1])
            
            
    def update(self):
        if not self.explode:
            self.vx = self.amp //  self.speed  * cos((self.aCount- self.attack//2)/pi)
            self.vy = self.speed
            
            #make them stop half way
#         if self.rect.y > self.maxy: 
#             self.vy = 0


#         if self.aCount % 5 == 0:
#             self.image = pygame.transform.rotate(self.image, self.angle)
        if self.aCount < self.attack:
            self.aCount += 1
        
        super().update()
        
     #true  alive
    def hit(self, hitPower):
        self.power -= hitPower
        return self.power > 0   
    
class Three(Alien):
    def __init__(self, x, y, maxy):
        super().__init__(x, y, maxy)
        self.image = pygame.image.load("./res/a3.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.amp = 33
        self.speed= 3 
        self.power = 12
        self.attack = 80
        
class Star(Alien):
    def __init__(self, x, y, maxy):
        super().__init__(x, y, maxy)
        self.image = pygame.image.load("./res/a4.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.amp = 60
        self.speed= 4
        self.power = 20
        self.attack = 20
        
class CommandShip(Alien):
    def __init__(self, x, y,maxy, drones=10):
        super().__init__(x, y, maxy)
        self.image = pygame.image.load("./res/a2.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.amp = 30
        self.speed= 2 
        self.power = 30
#         self.image.fill(pygame.Color(50,100,100))
        self.droneCount = drones
        self.drones = pygame.sprite.Group()
#         self.makeDrones()
        self.attack = 40
        self.aCount = 0
     
    def makeDrones(self):
        n = self.droneCount
        
        for i in range(0, n):
            self.drones.add(Drone(self.getCenter(), n=i, count=self.droneCount))
        
    def update(self):
#         if not self.explode:
#             self.vx = -self.rect.y +  self.amp * sin(self.rect.y * pi / 180)
#             self.vy = self.speed
         
        super().update()
        for d in self.drones:
            d.center = self.getCenter()
    
    
    
class Drone(Three):
    def __init__(self, center, n, count):
        super().__init__(0, 0, 2000)
#         
#         self.image = pygame.Surface([20, 20])
#         self.image.fill(pygame.Color(234,200,100))
#  
#         self.rect = self.image.get_rect()
#         
        self.center = center
        self.r = 150
        self.speed = 1
        self.angle = n * 360/count
#         self.power = 1
        
    def update(self):
        
        j = self.center[0]
        k = self.center[1]
        self.angle += self.speed
        a = self.angle
        r = self.r
        x = j + r* cos(a* pi /180)
        y = k + r* sin(a* pi / 180)
#         t = 'x: ' + str(x) + ' y: ' + str(y)
#         print(t)
        self.rect.x = int(x)
        self.rect.y = int(y)
        
   
#         super().update()
        
        
        
        
        
        
        