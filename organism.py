import abc
import crossover as cross
import random
import math
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
        
        n = self.parent.getEmptyNeighbourhood(2)
        
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
        3 - foodaffinity
    """
    def __init__(self,chromosome,species,factory):
        Organism.__init__(self,chromosome,species,factory)
        self.strength = self.chromosome[1]
        self.maxenergy = self.chromosome[2]
        self.foodaffinity = self.chromosome[3]
        self.energy = math.ceil(self.maxenergy * 0.5)

    def update(self):
        Organism.update(self)
        self.energy-=1
        if self.energy <=0:
            raise OrganismDied("Starved")
        self.roam()
        if self.energy > math.ceil(self.maxenergy * 0.75) and self.reproduce(0):
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
        for i in self.parent.getNeighbours():
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
                    print(self,"ate",f)
                    return True
                    
        except IndexError as e:
            return False
            
        
    def reproduce(self,mutate,energy=None):
        mates = []
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
        if(mate.energy>0 and mate.energy< 30):
            obj = cross.TwoPointCrossover()
        elif(mate.energy>30 and mate.energy< 60):
            obj = cross.OnePointCrossover()
        
        
        children = obj.crossover(self.chromosome,mate.chromosome)
        selectchromo = random.choice(children)
    
        if(mutate):
            selectchromo = cross.mutateorg(selectchromo)
    
        try:
            p = random.choice(self.parent.getEmptyNeighbourhood())
            c = self.factory.create(self.species, selectchromo, p)
            self.energy -= self.maxenergy * 0.4
            print(self, "reproduced with",mate,":" , c)
            return c
        except IndexError as e:
            return None
        
        
class PlantDrawComponent(DrawComponent):
    def draw(self):
        print("P",end="")

class AnimalDrawComponent(DrawComponent):
    def draw(self):
        print(self.parent.getComponent('organism').species,end="")
            
class OrganismFactory(abc.ABC):
    """
    Declare an interface for operations that create abstract product
    objects.
    """
    def __init__(self,world):
        assert isinstance(world,World)
        self.world = world
    
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
        
        dc = PlantDrawComponent()
        
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
        
        dc = AnimalDrawComponent()
        
        return self.world.addObject(World.WorldObjBuilder().setDrawComponent(dc).addComponent('organism',ac).build(),
                                       pos)
        

    
