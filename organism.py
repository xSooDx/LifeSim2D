import abc
import crossover as cross
import random

class OrganismFactory():
    """
    Declare an interface for operations that create abstract product
    objects.
    """
    __metaclass__=abc.ABCMeta
    @abc.abstractmethod
    def create(self,chromosome,mutate): # pass chromosome, mutaation boolean
        pass



class PlantFactory(OrganismFactory):
    """
    Implement the operations to create concrete product objects.

    """

    def create(self,chromosome,mutate):
        if(mutate):
            chromosome = cross.mutateorg(chromosome) # why red?
            
        return Plant(chromosome)


        

class AnimalFactory(OrganismFactory):
    """
    Implement the operations to create concrete product objects.
    """

    def create(self,chromosome,mutate):
        if(mutate):
            chromosome = cross.mutateorg(chromosome) # why red?
            
        return Animal(chromosome)
        

        
        


class Organism(abc.ABC):
    """
    Declare an interface for a type of product object.
    """
    def __init__(self,chromosome,species):
        self.alive = True
        self.age=0
        self.chromosome= chromosome
        self.life = self.chromosome[0]
        self.species=species
    @abc.abstractmethod
    def update(self):
        pass
    @abc.abstractmethod   
    def reproduce(self,mutate,specie1,specie2=None,energy=None):
        pass


class Plant(Organism):
    """
    Define a product object to be created by the corresponding concrete
    factory.
    Implement the AbstractProduct interface.
    """
    def __init__(self,chromosome,species):  # chromosome has life and reproduction rate in that order
        Organism.__init__(self,chromosome,species)
        self.reprrate = chromosome[1]

    def update(self):
        pass
        
    def reproduce(self,mutate,specie1,specie2=None,energy=None):
        if(mutate):
            chromosome = cross.mutateorg(specie1.chromosome)
        fact = PlantFactory()
        return fact.create(chromosome)
        
class Animal(Organism):
    """
    Define a product object to be created by the corresponding concrete
    factory.
    Implement the AbstractProduct interface.
    """
    def __init__(self,chromosome,species):
        Organism.__init__(self,chromosome,species)
        self.strength = self.chromosome[1]
        self.maxenergy = self.chromosome[2]
    
    def update(self):
        pass
        
    def reproduce(self,mutate,specie1,specie2=None,energy=None):
        
        if(specie1.specie == specie2.specie):
            children = [] # the children on reproduction
            if(energy>0 and energy< 30):
                obj = cross.OnePointCrossOver()
            elif(energy>30 and energy< 60):
                obj = cross.OnePointCrossOver()
            elif(energy>60):
                obj = cross.OnePointCrossOver()
            
            children = obj.crossover(specie1.chromosome,specie2.chromosome)
            selectchromo = random.choice(children)
        
            if(mutate):
                selectchromo = cross.mutateorg(selectchromo)
        
            fact  = AnimalFactory()
            return fact.create(selectchromo)
        else:
            pass


    
