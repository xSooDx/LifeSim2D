from organism import Animal, Plant

class Stats:
    
    def __init__(self):
        self.num_orgs = 0
        self.num_animals = 0
        self.num_plans = 0
        
    def analyseWorld(self, world):
        self.num_orgs=world.numObjects
        self.num_animals = 0
        self.num_plants = 0
        '''
            0-num per species
            1-avg max Life
            2-avg strength
            3-avg max energy
            4-avg reproduction rate
            5-avg splitChance
         '''
        self.animalSpecies = {}
        
        '''
            0-Num per species
            1 - avg max life
            2 - avg max health
        '''
        self.plantSpecies = {}
        
        for i in world:
            org =i.getComponent('organism')
            
            if org:
                if isinstance(org,Animal):
                    self.num_animals +=1
                    
                    if not org.species in self.animalSpecies:
                        self.animalSpecies[org.species] = [0,0,0,0,0,0]
                    t = self.animalSpecies[org.species]
                    t[0]+=1
                    t[1]+=org.life
                    t[2]+=org.strength
                    t[3]+=org.maxenergy
                    
                    t[4]+=org.reprrate
                    t[5]+=org.splitchance
                    
                elif isinstance(org,Plant):
                    
                    self.num_plants +=1
                    if not org.species in self.plantSpecies:
                        self.plantSpecies[org.species] = [0,0,0,0]
                    
                    t = self.plantSpecies[org.species]
                    t[0]+=1
                    t[1]+=org.life
                    t[2]+=org.reprrate
                    t[3]+=org.maxhealth
        
        for i in self.animalSpecies:
            t = self.animalSpecies[i]
            t[1]/=t[0]
            t[2]/=t[0]
            t[3]/=t[0]
            t[4]/=t[0]
            t[5]/=t[0]
            
        for i in self.plantSpecies:
            t = self.plantSpecies[i]
            t[1]/=t[0]
            t[2]/=t[0]

    def displayStats(self,p=1,a=1):
        print("Number of Organisms:",self.num_orgs)
        print("Number of Plants:",self.num_plants)
        print("Number of Animals:",self.num_animals)
        if a:
            print("____ANIMALS____")
            print("{:9}|{:9}|{:9}|{:9}|{:9}|{:9}|{:9}|{:9}|".format(
                "Species", "Color","Num", "Life","Str","Eng","RepRate","Split"
            ))
            color='RED'
            for i in sorted(self.animalSpecies.keys() ):
                if i == 1:
                    color='GRAY'
                elif i == 2:
                    color='YELLOW'
                elif i == 3:
                    color='CYAN'
                elif i == 4:
                    color='MAGENTA'
                elif i == 5:
                    color='ORANGE'
                elif i == 6:
                    color='BLUE'
                elif i == 7:
                    color='PINK'
                elif i == 8:
                    color='PURPLE'
                
                    
                t = self.animalSpecies[i]
                print("{:5}     {:9} {:9} {:9.2f} {:9.2f} {:9.2f} {:9.2f} {:9.2f}".format(i,color,t[0], t[1],t[2],t[3],t[4],t[5]))
        
        if p:   
            print("____PLANTS____")
            for i in sorted(self.plantSpecies.keys()):
                t = self.plantSpecies[i]
                print("Species {}: {} {:0.3f} {:0.3f}".format(i,t[0],t[1],t[2]))
                
        print()
        print("-------------------")
        print()
        