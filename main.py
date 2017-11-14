'''
Created on Apr 28, 2015

@author: Saul Castro
Cs332L Spring 2015 
Final Project

Game class

Start fuction contains Main loop, 
game settings, controls 

todo
Level file format
stats class
options
controller + setup
sound effects

'''


import pygame, sys 
from stats import Stats
from user import User
from alien import *
from bullet import Bullet, AlienBullet
from level import Level, levelItem, levelMaker
from powerup import *
from mySounds import *
import random



class Game:
    LOST = -1
    WON = 1
    active = True
    
    gamesounds = 0
    soundOn = True
#     sound ids
    boomSound = 0
    laserSound = 1
    reloadSound = 2
    upSound = 3
    missleSound = 4
    mainGunSound = 5
    blasterSound = 6 
    
    
    width = 800
    height = 800
    fullscreen = True
    padding = 100
    currentLevel = 1
    timerEvent =  19
    fireEvent = 14
    
    user = 0
    stats = 0
    keys = []
    controllerMap = []
    controller = 0
    eFrames = []
    isPaused = True
    
    bg = []
    background_image = 0
    bgh = 0
    surface = 0
    
    LevelLength = 1500
    
    def __init__(self):
        pygame.init()
        
        if Game.fullscreen:
            Game.width = pygame.display.Info().current_w
            Game.height = pygame.display.Info().current_h
       
        Game.surface = pygame.display.set_mode([Game.width, Game.height])
        pygame.display.set_caption('Final Project')
        
        
        Game.bg.append(  pygame.image.load("./res/bg2k.jpg").convert() )
        Game.bg.append(  pygame.image.load("./res/bge.jpg").convert() )
#         Game.bg.append(  pygame.image.load("./res/bgm.jpg").convert() )
        
        
        Game.background_image = Game.bg[0]
        
        self.resetBg()
        
        # Initialize the joysticks
        pygame.joystick.init()
    
    
        self.createEframes()
        
        self.setupKeys()
        Game.controller  = self.setupController()
      
        Game.gamesounds = MySound()
  
        self.splash()
            
        result = 0
       
        while True:
            
            result = self.start()
            if result == Game.WON:  
                Game.stats.levelUp()    
                if Game.soundOn: 
                    Game.gamesounds.playSound(Game.upSound)
                    Game.background_image = Game.bg[Game.stats.level % len(Game.bg) ]
        
                    self.resetBg()
                      
            elif result == Game.LOST:  
                Game.stats.died()
               
                result = 0
                
                
                
    def printText(self, text, size=45):
        white = pygame.Color(255, 255, 255)
        f = pygame.font.get_default_font()
        myfont = pygame.font.SysFont(f, size, True , False)
        label = myfont.render(text, True, white)
        Game.surface.blit(label, (Game.width/3, Game.height/3))
         
        
    def splash(self):
      
        Game.surface.blit(Game.background_image, [0, Game.bgh])
        self.printText("Name goes here", size=100)
        pygame.display.update()
        while True:
                 #event check
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print('time to quit')
                    pygame.quit()
                    break
                elif event.type == pygame.JOYBUTTONDOWN or event.type == pygame.KEYDOWN:
                    return
                
           
        
    def resetBg(self):
        Game.bgh = -Game.background_image.get_height() + Game.height 
        
    def shiftBg(self, shift):
        Game.bgh += shift
        print( Game.bgh)
        
    def createEframes(self):  
        sprite_sheet = pygame.image.load("./res/SkybusterExplosion.jpg").convert()
        w = 170
        h = 170
        hpad = 75
        vpad = 35
        for i in range(5):
            for j in range(4):
                image = self.getImage(sprite_sheet,hpad +  j*(w + 2 * hpad), vpad+ i*(h + 2*vpad), w, h)
                Game.eFrames.append(image)

    def getImage(self, source, x, y, w, h):
            image = pygame.Surface([w, h]).convert()
            image.blit(source, (0, 0), (x, y, w, h))
            image.set_colorkey((0,0,0))
            return image
        
    def Countdown(self, text, time, delay = 1000):
        timer = pygame.event.Event(Game.timerEvent, mSecs = time, message = text)
        pygame.time.set_timer(Game.timerEvent, delay)
        
    def youWin(self):
        black = pygame.Color(0, 0, 0)
        white = pygame.Color(255, 255, 255)
#         surface.fill(black)

       
        f = pygame.font.get_default_font()
        myfont = pygame.font.SysFont(f, 65, True , False)
        label = myfont.render("You Win!", True, white)
        Game.surface.blit(label, (Game.width//3, Game.height//3))

        
            

        
    def menu(self):
        black = pygame.Color(0, 0, 0)
        white = pygame.Color(255, 255, 255)
        FPS = 10 #30 frames per second
        fpsClock = pygame.time.Clock()
        
        pygame.font.init()
        text = ['Main Menu', 'Start game', 'Options', 'Exit']
        selected = 1
        
            
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print('time to quit')
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    print('key pressed')
                    k = event.key 
                    if k == pygame.K_LEFT:
                        print('change')
                    elif k == pygame.K_RIGHT:
                        print('change')
                    elif k == pygame.K_UP:
                        selected -= 1
                        if selected < 1: selected = len(text) - 1
                    elif k == pygame.K_DOWN:
                        selected += 1
                        if selected >= len(text): selected = 1
                    elif k == pygame.K_SPACE:
                        return selected
                if not Game.controller == 0:
                    if event.type == pygame.JOYBUTTONDOWN and event.button == 3: 
                        return selected
                 
                        
                
#             Game.surface.fill(black)
            Game.surface.blit(Game.background_image, [0, Game.bgh])
           
            for i in range(0, len(text)):       
                f = pygame.font.get_default_font()
                myfont = pygame.font.SysFont(f, 65, i == selected , False)
                label = myfont.render(text[i], True, white)
                Game.surface.blit(label, (Game.width//3, 200 + i*100))
            if not Game.stats == 0: 
                stat = Game.stats.getFullStats()
                for z in range(len(stat)):   
                    f = pygame.font.get_default_font()
                    myfont = pygame.font.SysFont(f, 35, z == 0 , False)
                    temp = str(stat[z].getName()) + ': ' + str(stat[z].getValue())
                    label = myfont.render(temp, True, white)
                    Game.surface.blit(label, (2 * Game.width//3, 200 + z*40))
                
            pygame.display.update()
            fpsClock.tick(FPS)
        
        
    def start(self):
        white = pygame.Color(255, 255, 255)
        
        #set the FPS for this game
        FPS = 30 #30 frames per second
        fpsClock = pygame.time.Clock()
       
#         players = []

        #reset a lost game
        if not Game.active:
            Game.active = True
            Game.user = 0   #reset player
        
        #reset the user
        if Game.user == 0:
            Game.user = User(x=500, y=600)
            Game.user.setEframe(Game.eFrames)
            
#         user = Game.user
#         players.append(user)
#         user = User(700, 400)
#         players.append()

        items = pygame.sprite.Group()  
        items.add(Game.user)
        alienList = pygame.sprite.Group()
        bulletList = pygame.sprite.Group()
        alienBulletList = pygame.sprite.Group()
        powerUpList = pygame.sprite.Group()
        
        if Game.stats == 0:
            Game.stats = Stats(Game.width, Game.height)
        items.add(Game.stats)
            
             
#         currentLevel = 1
#         level = Level(Game.stats.level)
        LevelLength = Game.LevelLength
#         LevelLength = level.getLength()
        if Game.bgh + LevelLength >= Game.padding :
            self.resetBg()
        levelPos = 0

       
          
        pygame.font.init()
        f = pygame.font.get_default_font()
        myfont = pygame.font.SysFont(f, 35, True , False)
      
      
        
        
           #main loop
        while True: 
            while Game.isPaused:
                _m = self.menu()
                print(_m)
                if _m == 1: Game.isPaused = False
                elif _m == 3: pygame.quit()
                    
            Game.surface.blit(Game.background_image, [0, Game.bgh + levelPos])
            label = myfont.render(Game.stats.getStatsString(), True, white)
            Game.surface.blit(label, (Game.padding, 10))
            
            if levelPos< 50: 
                self.printText("Hope you are ready...")
            elif levelPos< 100: 
                self.printText("Here they come!")
    #         surface.fill(black)
    
            #event check
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print('time to quit')
                    pygame.quit()
                    break
                
                
                if event.type == pygame.JOYAXISMOTION:
                    axes = Game.controller.get_numaxes()
                    tol = .02
                    if axes >= 2: #only need one joystick for now.
                        xaxis = Game.controller.get_axis( 0 )
                        if -tol < xaxis < tol: xaxis = 0
                        yaxis = Game.controller.get_axis( 1 )
                        if -tol <  yaxis < tol: yaxis = 0
                        Game.user.go(xaxis, yaxis)
                        
                elif event.type == pygame.JOYBUTTONDOWN:
                    Game.keys[Game.controllerMap[event.button]](True)         
                elif event.type == pygame.JOYBUTTONUP:
                    Game.keys[Game.controllerMap[event.button]](False)    
                elif event.type == pygame.KEYDOWN:
                    Game.keys[event.key](True)
                elif event.type == pygame.KEYUP:
                    Game.keys[event.key](False)
                elif event.type == Game.fireEvent:
                    print('firing ')
                    g = event.gun
                    if Game.stats.wepons[g] > 0: #check ammo
                        if Game.soundOn:
                            if g==2: Game.gamesounds.playSound(Game.missleSound)
                            elif g==1: Game.gamesounds.playSound(Game.blasterSound)
                        b = Game.user.fire(g)
                        bulletList.add(b)
                        items.add(b)
                        Game.stats.shot(g)
                elif event.type == Game.timerEvent:
                    pygame.time.set_timer(Game.timerEvent, 0)
                    print('timer fired')
                    return Game.LOST
                
            #main weapon continuous firing
            if Game.user.firing and Game.user.tryFire(0):
                b = Game.user.fire(0)
                bulletList.add(b)
                items.add(b)
                Game.stats.shot(0)
                if Game.soundOn: Game.gamesounds.playSound(Game.mainGunSound)
            
            # check if i shot anything     
            for b in bulletList:      
                if b.rect.y < -100:        #remove bullets when they go off screen
                    bulletList.remove(b)
                    items.remove(b)  
                hitList = pygame.sprite.spritecollide(b, alienList, False)
                for et in hitList:
                    if not et.hit(b.power):
                        et.bang()
                        if Game.soundOn: Game.gamesounds.playSound(Game.boomSound)
                        alienList.remove(et)
                        Game.stats.killed()
                        
                        #Add power ups after some kills
                        if Game.stats.kills % 10*Game.currentLevel == 0:
                            p = PowerUps(et.getCenter()[0], et.getCenter()[1], 0)
                            powerUpList.add(p)
                            items.add(p)
#                         alienList.remove(et)
#                         items.remove(et)     
    #                     if type(et) is CommandShip:
    #                         user.addDrones(et.drones)
    
                        bulletList.remove(b)
                        items.remove(b)  
                        Game.stats.hit()
                        
                     #bullet to bullet hits
                hitList = pygame.sprite.spritecollide(b, alienBulletList, False)
                for et in hitList:
                    #if not et.hit(b.power):
                        #et.bang()
                        if Game.soundOn: Game.gamesounds.playSound(Game.boomSound)
                        et.kill()
                        bulletList.remove(b)
                        items.remove(b)  
                   # Game.stats.hit()
                    
            #check if they shot me
            hitList = pygame.sprite.spritecollide(Game.user, alienBulletList, False)
            for b in hitList:
                if pygame.sprite.collide_circle(b, Game.user):
                   
                    Game.stats.gotShot(b.power)
                    alienBulletList.remove(b)
                    items.remove(b)
            
            #check if I crash
            hitList = pygame.sprite.spritecollide(Game.user, alienList, False)
            for a in hitList:
                if pygame.sprite.collide_circle(a, Game.user):
                    Game.stats.crashed(a.power)
                    alienList.remove(a)
                    a.bang()
                    if Game.soundOn: Game.gamesounds.playSound(Game.boomSound)
            
              #check if get a power up!
            hitList = pygame.sprite.spritecollide(Game.user, powerUpList, False)
            for p in hitList:
                if pygame.sprite.collide_circle(p, Game.user):
                    Game.stats.powerup(p)
                    p.kill()
                    if Game.soundOn: Game.gamesounds.playSound(Game.reloadSound)
            
            #try to fire
            for a in alienList:
                if a.tryFire():
                    b = a.fire()
                    alienBulletList.add(b)
                    items.add(b)
                    if Game.soundOn: Game.gamesounds.playSound(Game.laserSound)
            
        
                    
            items.update()
            items.draw(Game.surface)  
            levelPos += 2
    #         print( pos )
    
    
         #add aliens  based on my position and current level
            item = self.makeItem(LevelLength, levelPos)
            if not item == 0:
                alienList.add( item )
                items.add( item )
                
                
                
#             #add aliens when they are near my position
#             if level.peek() != 0 and levelPos >= level.peek().y:
#                 item = self.makeItem(level.next(), levelPos)
#                 alienList.add( item )
#                 items.add( item )
           


            #check if i won the level
            if levelPos > LevelLength:
                self.shiftBg(levelPos)
                 
                return Game.WON
            elif levelPos > LevelLength-Game.padding:
                self.printText("Level up! Score:" + str(Game.stats.score))
               
               
            #check if i'm dead
            if Game.stats.power <= 0 and Game.active:
#                 print('you lose no power')
                self.printText("You died...", 30) # Ships Remaining: " + str(Game.stats.lives))
                if Game.active: #make sure to set timer only once
                    Game.active = False
                    Game.user.bang()
                    pygame.time.set_timer(Game.timerEvent, 1500)

     
                
            pygame.display.update()
            fpsClock.tick(FPS)
    
    
    def makeItem(self,ll, pos):
            if pos % (10*(10 - Game.currentLevel))  != 0 or pos/ll > .7: return 0
            
         
            aliens = []
            p = Game.padding
            x =  random.randint(2, Game.width//(p*2)-2)
            print('x : ' + str(x) )
            x *= p*2
            howMany =  random.randint(1, Game.currentLevel + 1)
            width =  random.randint(1, 4)
            rows = howMany // width
            mh = Game.height//4
            print('adding ' + str(howMany) + 'Item(s) in ' + str(width) + ' Cols')
            for k in range(rows):
                t =  random.randint(1, 4)
                for j in range(width):
                    y = -p - (k + 1) * (p)
                    #y = 100
                    if t == 1:
                        a = Alien(x + j * p, y , mh)
                    elif t == 2:
                        a = CommandShip(x+ j * p, y, mh, drones=0)
#                         for d in range(a.droneCount):
#                             print("drone added")
#                             b = Drone(a.getCenter(), n=d, count=a.droneCount) 
#                             a.drones.add(b)
#                             b.setEframe(Game.eFrames)
#                             aliens.append( b )
                    elif t == 3:
                        a = Three(x+ j * p, y, mh)
                    elif t == 4:
                        a = Star(x+ j *p, y, mh)
                    else: a = Alien(x+ j * p, y, mh)
                    
                    a.setEframe(Game.eFrames)
                    aliens.append( a )
            return aliens
    
    
    
#     def makeItem(self, i, pos):
#             print('adding ' + str(i.type) + ' alien! ' + str( i.howMany ))
#             aliens = []
#             p = Game.padding
#             x =  random.randint(2, Game.width//(p*2)-2)
#             print('x : ' + str(x) )
#             x *= p
#          
#             total = i.howMany // i.groupWidth
#             mh = Game.height//4
#             for k in range(total):
#                 t = i.type
#                 for j in range(i.groupWidth):
#                     y = -p - (k + 1) * (i.space + p)
#                     #y = 100
#                     if t == 1:
#                         a = Alien(x + j * p, y , mh)
#                     elif t == 2:
#                         a = CommandShip(x+ j * p, y, mh, drones=5)
# #                         for d in range(a.droneCount):
# #                             print("drone added")
# #                             b = Drone(a.getCenter(), n=d, count=a.droneCount) 
# #                             a.drones.add(b)
# #                             b.setEframe(Game.eFrames)
# #                             aliens.append( b )
#                     elif t == 3:
#                         a = Three(x+ j * p, y, mh)
#                     elif t == 4:
#                         a = Star(x+ j *p, y, mh)
#                     else: a = Alien(x+ j * p, y, mh)
#                     
#                     a.setEframe(Game.eFrames)
#                     aliens.append( a )
#             return aliens
    
     
    
    #button/ controller functions
    def buttonLeft(self, pressed):
      
        if pressed:
            print('button left pressed')
            Game.user.goLeft()
        else: 
            print("Button left released")
            Game.user.stopX()
            
                
    def buttonRight(self, pressed):
        if pressed:
            Game.user.goRight()
        else: 
            Game.user.stopX()
            
    def buttonUp(self, pressed):
        if pressed:
            Game.user.goUp()
        else: 
            Game.user.stopY()
            
    def buttonDown(self, pressed):
        if pressed:
            Game.user.goDown()
        else: 
            Game.user.stopY()
     
    def buttonSpace(self, pressed):
        Game.user.firing = pressed
            
    def fireOne(self, pressed):
        if pressed:
            e = pygame.event.Event(Game.fireEvent, gun=1)
            pygame.event.post(e)
             
    def fireTwo(self, pressed):
        if pressed:
            e = pygame.event.Event(Game.fireEvent, gun=2)
            pygame.event.post(e)
            
    def buttonNothing(self, pressed):
        pass
    
    def boom(self, pressed):
        if pressed:  
            Game.stats.power = 0
#             Game.user.bang()
            
        
    def pause(self, pressed):
        if pressed:
            Game.isPaused = not Game.isPaused 
        
    def setupKeys(self):
        for i in range(512):
            Game.keys.append(self.buttonNothing)
            
            
        Game.keys[pygame.K_DOWN] = self.buttonDown
        Game.keys[pygame.K_UP] = self.buttonUp
        Game.keys[pygame.K_LEFT] = self.buttonLeft
        Game.keys[pygame.K_RIGHT] = self.buttonRight
        Game.keys[pygame.K_SPACE] = self.buttonSpace
        Game.keys[pygame.K_z] = self.fireOne
        Game.keys[pygame.K_x] = self.fireTwo
        Game.keys[pygame.K_b] = self.boom
        Game.keys[pygame.K_ESCAPE] = self.pause


    def setupController(self):
        c = 0
        if pygame.joystick.get_count() > 0:
            c = pygame.joystick.Joystick(0)
            c.init()
            print("controller found! " + c.get_name())
        else: return c
        
        for i in range(c.get_numbuttons()):
            Game.controllerMap.append( 0 )
        
        Game.controllerMap[4] = pygame.K_UP
        Game.controllerMap[5] = pygame.K_RIGHT
        Game.controllerMap[6] = pygame.K_DOWN
        Game.controllerMap[7] = pygame.K_LEFT
        Game.controllerMap[14] = pygame.K_SPACE
        Game.controllerMap[8] = pygame.K_z
        Game.controllerMap[9] = pygame.K_x
        Game.controllerMap[3] = pygame.K_ESCAPE
        
        return c
 
              
    
if __name__ == '__main__':          
#     levelMaker(4, 5000, 1, 10, 200, 52)       
    Game()