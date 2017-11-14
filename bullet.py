'''
Created on Apr 30, 2015

@author: saul

bullet item base and subclasses for user and ememies.
'''
import pygame
from item import Item

class Bullet(Item):
    
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.image.load("./res/bullet.png").convert_alpha()
        #pygame.Surface([10, 10])
        #self.image.fill(pygame.Color(0,200,200))
 
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vy = -10
        self.power = 1
        self.type = 1
        
class AlienBullet(Bullet):
    
    def __init__(self, x, y):
        super().__init__(x, y)
        d = 20
        d2 = d//2
        self.radius = d
#         image = pygame.Surface([d, d])
#         pygame.draw.circle(image, pygame.Color(140,0,200),(d2,d2) , d2, 0)
#         image.set_colorkey(pygame.Color(0,0,0))
#         self.image = image
        self.image = pygame.image.load("./res/abullet.png").convert_alpha()
#         self.image.fill(pygame.Color(140,0,200))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vy = 10
        self.type = -1
       
    def update(self):
        super().update()
        if self.rect.y > 1200: self.kill()
       
        
        
class BigBullet(Bullet):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.image.load("./res/bullet2.png").convert_alpha()
#         pygame.Surface([8, 10])
#         self.image.fill(pygame.Color(0,200,100))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.power = 2
        self.type = 2
        
        
class Missile(Bullet):
    def __init__(self, x, y):
        super().__init__(x, y)
        frames = []
        image = pygame.image.load("./res/missle.png").convert_alpha()
        frames.append(image)
        image = pygame.image.load("./res/missle1.png").convert_alpha()
        frames.append(image)
        image = pygame.image.load("./res/missle2.png").convert_alpha()
        frames.append(image)
        image = pygame.image.load("./res/missle3.png").convert_alpha()
        frames.append(image)
        self.type = 3
        
        self.images = frames
        self.frame = 0
        self.image = frames[self.frame]
        self.rect = self.image.get_rect()
        
#         self.image = pygame.Surface([8, 15])
#         self.image.fill(pygame.Color(100,100,100))
#         self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.power = 5
        self.vy = -10
        
    def update(self):
        super().update()
#         print (self.frame)
        self.frame = (self.rect.y // 60)  % (len(self.images) - 1 ) + 1
        self.image = self.images[self.frame]
        
        
        
                
        
        