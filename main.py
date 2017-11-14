'''
Created on 11/14/17

pypong prootype


Start fuction contains Main loop, 
game settings, controls 


'''


import pygame, sys 
from user import User
from ball import Ball
import random



class Game:
   
    active = True
    width = 800
    height = 800
    fullscreen = False
    padding = 100
    currentLevel = 1
    timerEvent =  19
    turn = 0
    
    ball = 0
    user = 0
    user2  = 0
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
        pygame.display.set_caption('Py Pong')
        
         
        # Game.background_image =  pygame.Surface([Game.width, Game.height])
        # Game.background_image.fill(pygame.Color(0,20,100))
        
        # 
        
        # Initialize the joysticks
        pygame.joystick.init()
    
    
        self.createEframes()
        
        self.setupKeys()
        Game.controller  = self.setupController()
      
        # Game.gamesounds = MySound()
  
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
      
        # Game.surface.blit(Game.background_image, [0, Game.bgh])
        Game.surface.fill(pygame.Color(0, 0, 0))
        self.printText("PyPong", size=60)
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
                 
                        
                
            Game.surface.fill(black)
            # Game.surface.blit(Game.background_image, [0, Game.bgh])
           
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
            Game.user = User(0)
            Game.user.setEframe(Game.eFrames)
        if Game.user2 == 0:
            Game.user2 = User(1)
            Game.user2.setEframe(Game.eFrames)
        if Game.ball == 0:
            Game.ball = Ball(int(Game.turn%2))
            Game.ball.setEframe(Game.eFrames)
            
#         user = Game.user
#         players.append(user)
#         user = User(700, 400)
#         players.append()

        items = pygame.sprite.Group()  
        items.add(Game.user)
        items.add(Game.user2)
        items.add(Game.ball)
        
        # if Game.stats == 0:
        #     Game.stats = Stats(Game.width, Game.height)
        # items.add(Game.stats)
            
          
       
          
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
                    
            # Game.surface.blit(Game.background_image, [0, 0])
            Game.surface.fill(pygame.Color(0,0,0))
            # label = myfont.render(Game.stats.getStatsString(), True, white)
            # Game.surface.blit(label, (Game.padding, 10))
            
    
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
          
            #check the ball hits
            #only need to check when the users hit the ball
            #wall bounce should be within ball update func
            ball = Game.ball
            hitList = pygame.sprite.spritecollide(ball, items, False)
            for a in hitList:
                if pygame.sprite.collide_circle(a, Game.user):
                    # Game.stats.crashed(a.power)
                    print("ball hit")
                   
                    
            items.update()
            items.draw(Game.surface)  
            levelPos += 1
    #         print( pos )
        
            #check if i'm dead
#             if Game.stats.power <= 0 and Game.active:
# #                 print('you lose no power')
#                 self.printText("You died...", 30) # Ships Remaining: " + str(Game.stats.lives))
#                 if Game.active: #make sure to set timer only once
#                     Game.active = False
#                     Game.user.bang()
#                     pygame.time.set_timer(Game.timerEvent, 1500)

     
                
            pygame.display.update()
            fpsClock.tick(FPS)
    
    
    
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