import pygame
import traceback
from world import World

class Engine:
    def __init__(self,size,caption):
        pygame.init()
        self.gameDisplay = pygame.display.set_mode(size)
        pygame.display.set_caption(caption)
        self.clock = pygame.time.Clock()
        self.world = World()
        self.state = 1
        
    def quit(self):
        pygame.quit()
        pass
        
    def input(self):
        pass

    def draw(self):
        pass
        
    def update(self):
        pass
    
    def gameLoop(self):
        while self.state:
            try:
                self.input()
                self.update()
                self.draw()
            except Exception as e:
                print(e.msg)
                traceback.print_exc()
                self.state = -1
                break
                
                
                
                
                
                
                
                
                