import pygame
import traceback
import color
import random
from world import World
from organism import *
from stats import Stats

def initPopulation2(pf,af,ws):
    x = int(ws[0]/2)
    y = int(ws[1]/2)
    c1 = [100,100,100,10,5,4]
    c2 = [100,25,100,10,50,3]
    
    af.create(0,c1,[x,y])
    af.create(0,c1,[x+1,y])
    af.create(1,c2,[x+3,y+3])
    af.create(1,c2,[x-3,y+3])
    af.create(1,c2,[x-3,y-3])
    af.create(1,c2,[x,y-3])
    af.create(1,c2,[x+3,y])
    af.create(1,c2,[x,y+3])
    af.create(1,c2,[x-3,y])
    af.create(1,c2,[x+4,y+4])
    af.create(1,c2,[x-4,y+4])
    af.create(1,c2,[x-4,y-4])
    af.create(1,c2,[x,y-4])
    af.create(1,c2,[x+4,y])
    af.create(1,c2,[x,y+4])
    af.create(1,c2,[x-4,y])

class Engine:
    def __init__(self,size,caption, world_size = (100,100), fps=30,seed=3650):
        random.seed(seed)
        pygame.init()
        self.gameDisplay = pygame.display.set_mode(size)
        pygame.display.set_caption(caption)
        self.size=size
        self.stats = Stats()
        self.clock = pygame.time.Clock()
        self.world = World(world_size[0],world_size[1])
        self.af = AnimalFactory(self.world,self.gameDisplay)
        self.pf = PlantFactory(self.world,self.gameDisplay)
        self.pause = False
        self.state = 1  
        self.fps = fps
        self.frame=0
        initPopulation2(self.pf, self.af, world_size)
        
    def quit(self):
        pygame.quit()
        pass
        
    def input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.state = 0
            elif event.type == pygame.KEYDOWN:
                if self.fps< 120 and event.key in (pygame.K_KP_PLUS , pygame.K_PLUS):
                    self.fps+=5
                elif self.fps>5 and event.key in (pygame.K_KP_MINUS , pygame.K_MINUS):
                    self.fps-=5
                elif event.key == pygame.K_SPACE:
                    self.pause = not self.pause
        
    def draw(self):
        self.gameDisplay.fill(color.BLACK)
        self.world.draw()
        self.stats.displayStats(0,1)
        pygame.display.update()
        
    def update(self):
        self.world.update()
        if self.frame % 10 == 0:
            self.stats.analyseWorld(self.world)
        self.frame+=1
    
    def gameLoop(self):
        while self.state:
            try:
                self.input()
                if not self.pause:
                    self.update()
                    self.draw()
                self.clock.tick(self.fps)
            except Exception as e:
                print(e)
                traceback.print_exc()
                self.state = -1
                break
                
    
                
                
                
                
                
                
                