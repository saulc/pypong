'''
Created on May 12, 2015

@author: saul

stats class to keep track of game values for each player
future version may be linked to a user item to hold stats for mutiple players
'''
from item import Item
import pygame

class myPair:
    def __init__(self, name, value):
        self.name = name
        self.value = value
        
    def getName(self): return self.name
    
    def getValue(self): return self.value
    
    
class Stats(Item):
    
    black = pygame.Color(0, 0, 0)
    white = pygame.Color(255, 255, 255)
    green = pygame.Color(0,255,0)
    blue = pygame.Color(0, 0,255)
    red = pygame.Color(255,0, 0)
    orange = pygame.Color(200,0, 100)
 
    colors = [red, orange, green, blue]
    
    dpower = 10
    
    def __init__(self, swidth, sheight, score=0, level=1, lives=4, power= 10):
        super().__init__(0, 0)
        self.height = sheight
        self.width = swidth
        self.score = score
        self.shots = 0
        self.hits = 0
        self.kills = 0
        self.gotHit = 0
        self.crash = 0
        self.powerUps = 0
        self.power = power
        self.level = level
        self.lives = lives
        self.weponZero = 1000
        self.weponOne = 100
        self.weponTwo = 10
        self.wepons = [ self.weponZero, self.weponOne, self.weponTwo]
        
    def getStatsString(self):
        return 'Score: {0} | Lives: {1} | Level: {2} | Shield: {3}'.format(self.score, self.lives, self.level, self.power)
    
    def getFullStats(self):
        items = []
        items.append( myPair('Game Stats', ''))
        items.append( myPair('Score', self.score) )
        items.append( myPair('Level', self.level) ) 
        items.append( myPair('Lives', self.lives) )
        items.append( myPair('Shield', self.power) )
        items.append( myPair('Shots', self.shots) )
        items.append( myPair('Hits', self.hits) )
        items.append( myPair('Kills', self.kills) )
        items.append( myPair('Been Hit', self.gotHit) )
        items.append( myPair('Crashes', self.crash) )
        items.append( myPair('Power Ups', self.powerUps) )
        
        items.append( myPair('Main Weapon', 'Unlimited' ) )
        items.append( myPair('Left Gun', self.wepons[1]) )
        items.append( myPair('Right Gun', self.wepons[2]) )
    
        
        
        return items
    
    def setWepon(self, w, power):
        if w < len(self.wepons):
            self.wepons[w] = power
#         if w == 0: self.weponZero = power
#         elif w == 1: self.weponOne = power
#         elif w == 2: self.weponTwo = power
        
    def update(self):
        x = 150 #self.width // 3
        myHeight = self.height // 4 + 20
        w = 20
        pad = 10
        image = pygame.Surface([x, self.height])
        image.fill(Stats.black)
        image.set_alpha(128)
        #image.set_colorkey(Stats.black)
        
        for i in range (1, len(self.wepons)):
            h = self.wepons[i] /  myHeight
            h *= self.wepons[i]
#             print( str(h) + "  " + str(myHeight))
            pygame.draw.line(image, Stats.colors[i % len(Stats.colors)],
                          (w + i*(w + pad), myHeight - h), (w +i*(w + pad), myHeight), w)
       
        white = pygame.Color(255, 255, 255)
        f = pygame.font.get_default_font()
        myfont = pygame.font.SysFont(f, 36, True , False)
        label = myfont.render('Ammo:', True, white)
        image.blit(label, (0,0) )
        
        self.rect = image.get_rect()
        self.image = image
        
        self.rect.x = 20
        self.rect.y = self.height - 1.5 * myHeight
    
    def reset(self):
        self.power = Stats.dpower
        
    def shot(self, gun):
        if gun < len(self.wepons):
            self.wepons[gun] -= 1
        self.shots += 1
        
    def gotShot(self, power):
        self.gotHit += 1
        self.power -= power
    
    def crashed(self, power):
        self.crash += 1
        self.power -= power       
                                
    def hit(self):
        self.score += 10
        self.hits += 1
        
    def killed(self):
        self.score += 100
        self.kills += 1
        
    def misses(self):
        return self.shots - self.hits
    
    def powerup(self, pup):
        self.power += pup.power
        for i in range(len(self.wepons)):
            self.wepons[i] += pup.wepons[i]
        
        self.powerUps += 1
        self.score += 100
        
    def life(self):
        self.lives += 1
        self.score += 200
        
    def died(self):
        self.lives -=1
        self.power = self.dpower
        
    def levelUp(self):
        self.level += 1
        self.score += 10000
        
    def getScore(self):
        return self.score
    
    
        