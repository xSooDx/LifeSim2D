import abc
import random

class Crossover():
    """
    Declare an interface common to all supported algorithms. Context
    uses this interface to call the algorithm defined by a
    ConcreteStrategy.
    """
    __metaclass__=abc.ABCMeta
    #takes two chromosomes as parameters and return two new chromosomes
    @abc.abstractmethod
    def crossover(self,chromosome1,chromosome2):
        pass


class OnePointCrossover(Crossover):
    

    def crossover(self,chromosome1,chromosome2):
        #print("1pc")
        length = len(chromosome1)
        halflength = int(length/2)
        newchromosome1 = [0]*length
        newchromosome1[:halflength] = chromosome1[:halflength] 
        newchromosome1[halflength:] = chromosome2[halflength:] 
        newchromosome2 = [0]*length
        newchromosome2[:halflength] = chromosome2[:halflength] 
        newchromosome2[halflength:] = chromosome1[halflength:] 
        return [newchromosome1,newchromosome2]


class TwoPointCrossover(Crossover):

    def crossover(self,chromosome1,chromosome2):
        #print("2pc")
        length = len(chromosome1)
        thirdlength = int(length/3)
        newchromosome1 = [0]*length
        newchromosome1[:thirdlength] = chromosome1[:thirdlength]
        newchromosome1[thirdlength:2*thirdlength] = chromosome2[thirdlength:2*thirdlength]
        newchromosome1[2*thirdlength:] = chromosome1[2*thirdlength:]
        newchromosome2 = [0]*length
        newchromosome2[:thirdlength] = chromosome2[:thirdlength]
        newchromosome2[thirdlength:2*thirdlength] = chromosome1[thirdlength:2*thirdlength]
        newchromosome2[2*thirdlength:] = chromosome2[2*thirdlength:]
        return [newchromosome1,newchromosome2]
        
        
class UniformCrossover(Crossover):
    
    def crossover(self,chromosome1,chromosome2):
        #print("Uc")
        length = len(chromosome1)
        newchromosome1 = [0]*length
        newchromosome2 = [0]*length
        for i in range(length):
            if(i%2==0):
                newchromosome1[i] = chromosome1[i]
                newchromosome2[i] = chromosome2[i]
            else:
                newchromosome1[i] = chromosome2[i]
                newchromosome2[i] = chromosome1[i]
        return [newchromosome1,newchromosome2]
        
  
def mutateorg(chromosome):
    #print(chromosome)
    length  = len(chromosome)
    index = random.randint(0,length-1)
    chromosome[index] += random.choice([1,1,2,1,1,1,1,1,2,1,1,2,5,1,1,1,1,2,10,1,2,1,1,1,1,1,2,1,1,2,5])* random.choice([1,-1]) # change value by 1
    if chromosome[index] < 0: chromosome[index] = 0
    #print(chromosome)
    #print()
    return chromosome         
            


_crossovers = {0:UniformCrossover(), 1:OnePointCrossover(), 2:TwoPointCrossover()}
_clen = len(_crossovers)
def getCrossover( i ):
    return _crossovers[ i%_clen ]
        