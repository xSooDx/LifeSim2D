import abc
import crossover as cross
import random
import math
import pygame
import color
from world import World, Component, DrawComponent, ObjectDestroyed

class OrganismDied(ObjectDestroyed):
    pass
    
    
class Organism(Component,abc.ABC):
    """
    Declare an interface for a type of product object.
    """
    def __init__(self,chromosome,species,factory):
        self.alive = True
        self.age=0
        self.chromosome= chromosome
        self.life = self.chromosome[0]
        self.species=species
        self.factory = factory

    def destroy(self):
        self.parent.destroy()
 
    def update(self):
        self.age+=1
        if self.age >= self.life:
            raise OrganismDied("old age")
    
    @abc.abstractmethod   
    def reproduce(self,mutate,energy=None):
        pass
        



class Plant(Organism):
    """
    Define a product object to be created by the corresponding concrete
    factory.
    Implement the AbstractProduct interface.
    """
    
    """
    chromosome order:
        0 - life
        1 - reprate
    """

    def __init__(self,chromosome,species,factory):  # chromosome has life and reproduction rate in that order
        Organism.__init__(self,chromosome,species,factory)
        self.reprrate = chromosome[1]

    def update(self):
        Organism.update(self)
        if not self.age % (self.reprrate or 1):
            self.reproduce(1)
        
    def reproduce(self,mutate,energy=None):
        chromosome = self.chromosome
        if(mutate):
            chromosome = cross.mutateorg(chromosome)
        
        n = self.parent.getEmptyNeighbourhood(3)
        
        if n:
            p = n[random.randint(0,len(n)-1)]
            #print(p)
            return self.factory.create(self.species,chromosome,p)
        else: return None
        
class Animal(Organism):
    """
    Define a product object to be created by the corresponding concrete
    factory.
    Implement the AbstractProduct interface.
    """
    
    """
    chromosome order:
        0 - life
        1 - strength        
        2 - maxenergy
        3 - reproduction rate
    """
    def __init__(self,chromosome,species,factory):
        Organism.__init__(self,chromosome,species,factory)
        self.strength = self.chromosome[1]
        self.maxenergy = self.chromosome[2]
        self.reprrate = self.chromosome[3]
        #self.foodaffinity = self.chromosome[4]
        self.energy = math.ceil(self.maxenergy * 0.7)
        self.reprval = 0
       # self.splitchance = self.chromosome[4]

    def update(self):
        Organism.update(self)
        self.energy-=1
        self.reprval += 1
        if self.energy <=0:
            raise OrganismDied("Starved")
        self.roam()
        if self.reprval > self. reprrate and self.energy > math.ceil(self.maxenergy * 0.75) and self.reproduce(1):
            pass
        else: self.eat()
     
    def roam(self):
        try:
            options = self.parent.getEmptyNeighbourhood()
            p = random.choice(options)
            if self.parent.move(p):
                return p
        except IndexError as e:
            pass
            
        return None
    
    def eat(self):
        food = []
        for i in self.parent.getNeighbours(2):
            org = i.getComponent('organism')
            if isinstance(org,Plant) or (isinstance(org,Animal) and not org.species==self.species):
                food.append(org)
        
        try:
            while food:
                i = random.randint(0,len(food)-1)
                f = food[i]
                food.pop(i)
                if isinstance(f,Plant) or self.strength >= f.strength:
                    try:
                        self.energy += f.energy
                    except: 
                        self.energy += f.age
                        
                    f.destroy()
                    #print(self,"ate",f)
                    return True
                    
        except IndexError as e:
            return False
            
        
    def reproduce(self,mutate,energy=None):
    
        mates= []
                
        for i in self.parent.getNeighbours():
            org = i.getComponent('organism')
            if isinstance(org,type(self)) and org.species==self.species:
                mates.append(org)
        
        try:
            mate = random.choice(mates)
        except IndexError as e:
            return None
            
        children = [] # the children on reproduction
        obj = cross.UniformCrossover()
        if(mate.energy< self.energy *0.3):
            obj = cross.OnePointCrossover()
        elif(mate.energy< self.energy*0.6):
            obj = cross.TwoPointCrossover()
        
        
        children = obj.crossover(self.chromosome,mate.chromosome)
        selectchromo = random.choice(children)
    
        if(mutate):
            selectchromo = cross.mutateorg(selectchromo)
    
        try:
            p = random.choice(self.parent.getEmptyNeighbourhood())
            c = self.factory.create(self.species, selectchromo, p)
            self.energy *= 0.5
            self.reprval =0
            #print(self, "reproduced with",mate,":" , c)
            return c
        except IndexError as e:
            return None
        

class OrganismDrawComponent(DrawComponent):
    def __init__(self,gameScreen,size):
        super().__init__()
        self.screen=gameScreen
        self.size = size
        self.color = color.WHITE
        
    def draw(self):
        pos = self.parent.pos
        pos = (pos[0]*self.size[0],pos[1]*self.size[1])
        pygame.draw.rect(self.screen,self.color,(pos[0],pos[1],self.size[0],self.size[1]))
        
class PlantDrawComponent(OrganismDrawComponent):
    def __init__(self,gameScreen,world):
        super().__init__(gameScreen,world)
        self.color = color.LIGHT_GREEN
        


class AnimalDrawComponent(OrganismDrawComponent):
    def __init__(self,gameScreen,world,species):
        super().__init__(gameScreen,world)
       
        if species == 1:
            self.color=color.GRAY
        elif species == 2:
            self.color=color.YELLOW
        elif species == 3:
            self.color=color.CYAN
        elif species == 4:
            self.color=color.MAGENTA
        elif species == 5:
            self.color=color.ORANGE
        elif species == 6:
            self.color=color.BLUE
        elif species == 7:
            self.color=color.PINK
        elif species == 8:
            self.color=color.PURPLE
        elif species == 9:
            self.color=color.MARINE_GREEN
        else:
            self.color=color.RED

            
class OrganismFactory(abc.ABC):
    """
    Declare an interface for operations that create abstract product
    objects.
    """
    def __init__(self, world, screen):
        assert isinstance(world,World)
        self.world = world
        self.screen = screen
        self.size = (screen.get_width()/world.width, screen.get_height()/world.height)
        
    @abc.abstractmethod
    def create(self,species,chromosome,pos,mutate=0): # pass chromosome, mutaation boolean
        pass

        
class PlantFactory(OrganismFactory):
    """
    Implement the operations to create concrete product objects.

    """
    def create(self,species,chromosome,pos,mutate=0):
        if(mutate):
            chromosome = cross.mutateorg(chromosome) # why red?
            
        pc = Plant(chromosome,species,self)
        
        
        
        dc = PlantDrawComponent(self.screen,self.size)
        
        return self.world.addObject(World.WorldObjBuilder().setDrawComponent(dc).addComponent('organism',pc).build(),
                                       pos)
        
        

        

class AnimalFactory(OrganismFactory):
    """
    Implement the operations to create concrete product objects.
    """
    
    def create(self,species,chromosome,pos,mutate=0):
        if(mutate):
            chromosome = cross.mutateorg(chromosome) # why red?
            
        ac = Animal(chromosome,species,self)
        
        dc = AnimalDrawComponent(self.screen,self.size,species)
        
        return self.world.addObject(World.WorldObjBuilder().setDrawComponent(dc).addComponent('organism',ac).build(),
                                       pos)
        


def initPopulation(plantFactory, animalFactory, w_size, cluster_radius=5, plant_clusters=5, num_plants=5, animal_species=5, num_animals=5, mutate = 0):
    for i in range(plant_clusters):
        x = random.randrange(w_size[0])
        y = random.randrange(w_size[1])
        base_c = genPlantChromosome()
        t = num_plants
        while t:
                try:
                    x1 = random.randrange(max(0,x-cluster_radius),min(w_size[0],x+cluster_radius+1))
                    y1 = random.randrange(max(0,y-cluster_radius),min(w_size[1],y+cluster_radius+1))
                    c = base_c
                    if(mutate):
                        c = cross.mutateorg(base_c)
                    plantFactory.create(0,c,[x1,y1])
                    t-=1
                except Exception as e:
                    #print("plants",e)
                    pass

                    
    for i in range(animal_species):
        x = random.randrange(w_size[0])
        y = random.randrange(w_size[1])
        base_c = genAnimalChromosome()
        t = num_animals
        while t:
                try:
                    x1 = random.randrange(max(0,x-cluster_radius),min(w_size[0],x+cluster_radius+1))
                    y1 = random.randrange(max(0,y-cluster_radius),min(w_size[1],y+cluster_radius+1))
                    c = base_c
                    if(mutate):
                        c = cross.mutateorg(base_c)
                    
                    animalFactory.create(i,c,[x1,y1])
                    t-=1
                except Exception as e:
                    #print(e)
                    pass

def genAnimalChromosome():
    return [random.randint(30,100),random.randint(30,100),random.randint(30,100),random.randint(5,100)]
    
def  genPlantChromosome():
    return [random.randint(25,90),random.randint(1,85)]

