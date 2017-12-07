import pygame
import traceback
import color
import random
from world import World
from organism import *


class Engine:
    def __init__(self,size,caption, world_size = (100,100), fps=30,seed=1000):
        random.seed=seed
        pygame.init()
        self.gameDisplay = pygame.display.set_mode(size)
        pygame.display.set_caption(caption)
        self.size=size
        self.clock = pygame.time.Clock()
        self.world = World(world_size[0],world_size[1])
        self.af = AnimalFactory(self.world,self.gameDisplay)
        self.pf = PlantFactory(self.world,self.gameDisplay)
        self.state = 1  
        self.fps = fps
        self.frame=0
        initPopulation(self.pf, self.af, world_size, 10,20,4, 10, 15)
        
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
        
    def draw(self):
        self.gameDisplay.fill(color.BLACK)
        self.world.drawWorld()
        pygame.display.update()
        
    def update(self):
        self.world.updateWorld()
        self.frame+=1
    
    def gameLoop(self):
        while self.state:
            try:
                self.input()
                self.update()
                self.draw()
                self.clock.tick(self.fps)
            except Exception as e:
                print(e)
                traceback.print_exc()
                self.state = -1
                break
                
    
                
                
                
                
                
                
                