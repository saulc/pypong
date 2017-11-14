'''
Created on May 26, 2015

@author: saul

mixer wrapper class
'''

import pygame

class MySound:
    def __init__(self):
        pygame.mixer.init(frequency=22050, size=16, channels=2, buffer=4096)
        self.sounds = []
        sound = pygame.mixer.Sound("./sound/explosion.wav")
        self.sounds.append(sound)
        sound = pygame.mixer.Sound("./sound/laser.wav")
        self.sounds.append(sound)
        sound = pygame.mixer.Sound("./sound/reload.wav")
        self.sounds.append(sound)
        sound = pygame.mixer.Sound("./sound/line.wav")
        self.sounds.append(sound)
        sound = pygame.mixer.Sound("./sound/missle.wav")
        self.sounds.append(sound)
        sound = pygame.mixer.Sound("./sound/Blaster-Ricochet.wav")
        self.sounds.append(sound)
        sound = pygame.mixer.Sound("./sound/Blaster-Imperial.wav")
        self.sounds.append(sound)
        
     
    def playSound(self, i):
        self.sounds[i].play()
     
     
        
        
        