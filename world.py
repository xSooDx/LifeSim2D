import abc
import crossover as cross
import random


# Linked List terminal nodes
class _lln:
    def __init__(self):
        self.next=None
        self.prev=None

# World Object Iterator
class _worldIterator:
    def __init__(self, head, tail):
        self.h = head
        self.t = tail
        pass
    
    def __next__(self):
        if not self.h.next == self.t:
            self.h = self.h.next
            return self.h
        raise StopIteration



        
# Game World Class
class World:
    # Builder class for world objects
    class WorldObjBuilder:
        def __init__(self):
            self.dc=None
            self.org=None
        
        # Add a drawable Component
        def setDrawComponent(self, dc):
            if isinstance(dc,DrawComponent) or dc == None:
                self.dc = dc
            else:
                raise TypeError("Not of type DrawComponent")
            return self
        
        # Add an organism component
        def setOrganism(self,org):
            self.org=org
            return self
        
        # Create and return object
        def build(self):
            return WorldObject(self.dc, self.org)
        
    def __init__(self, width = 100, height = 100):
        # Initialize head and tails of internal linklist
        h = _lln()
        t = _lln()
        h.next = t
        t.prev = h
        self.head= h
        self.tail= t
        self.numObjects = 0
        
        # Init grid
        self.width=width
        self.height=height
        self.map = [[0 for i in range(width)] for _ in  range(height)]
        
    # Iterator through world objects
    def __iter__(self):
        return _worldIterator(self.head, self.tail)
    
    # Draws all world objects if they have a draw component
    def drawWorld(self):
        for i in self.map:
            for j in i:
                print('|',end='')
                try:
                    j.draw()
                except: print(' ',end='')
            print('|')
            
    # Updates all world objects
    def updateWorld(self):
        for o in self:
            try:
                o.update()
            except Exception as e:
                # ignores if updateable component is missing
                print(e)
    
    
    def _testPos(self,pos):
        assert pos[0]>= 0 and pos[0] < self.width , "X Out of range"
        assert pos[1]>= 0 and pos[1] < self.height , "Y Out of range"
        assert self.map[pos[1]][pos[0]] == 0, "Position already Occupied"
        
    # Adds a world object to internal list
    def addObject(self, obj, pos):
        assert isinstance(obj,WorldObject), "Not a WorldObject"
        
        self._testPos(pos)
        
               
        # Check if obj is already part of world
        if obj.world==self:
            return obj
        obj.world=self
        
        #if list empty
        if self.head.next==self.tail:
            self.head.next = obj
         
        # Insert Object
        obj.prev = self.tail.prev
        obj.next = self.tail
        self.tail.prev.next = obj
        self.tail.prev= obj
        self.map[pos[1]][pos[0]]=obj
        obj.pos=pos
        
        self.numObjects+=1
        
        return obj
    
    def moveObject(self,obj,npos):
        assert isinstance(obj,WorldObject), "Not a world object"
        assert obj.world == self, "Object not part of this world"
        self._testPos(npos)
        
        tmp = obj.pos
        try:
            self.map[obj.pos[1]][obj.pos[0]]=0
            self.map[npos[1]][npos[0]]=obj
            obj.pos=npos
        except:
            self.map[tmp[1]][tmp[0]]=obj
            self.map[npos[1]][npos[0]]=0
            obj.pos=tmp
            
    def getNeighbours(self,pos,r=1):
        res=[]
        for i in range(-r,r+1):
            x = pos[0]+i
            for j in range(-r,r+1):
                y = pos[1]+j
                if i==0 and j==0:
                    pass
                else:
                    try:
                        if not self.map[y][x] == 0:
                            res.append(self.map[y][x])
                    except:
                        pass
                
            
        return res        
    
    # Destroy World Object inplace
    def destroyObject(self,obj):
        assert isinstance(obj,WorldObject), "Not a world object"
        assert obj.world == self, "Object not part of this world"
        assert not self.head.next == self.tail and self.numObjects > 0, "No object in world"
        
      
        obj.prev.next = obj.next
        obj.next.prev = obj.prev
        self.numObjects-=1
        
        p = obj.pos
        obj.pos=None
        self.map[p[1]][p[0]] =0
      
    pass
    
    
    
# Drawable component baseclass
class DrawComponent():#abc.ABC):
    #@abc.abstractmethod
    def __init__(self,a):
        self.ref=None
        self.a=a    
        
    def draw(self):
        print(self.a,end='')

#World Object Class
class WorldObject():
    def __init__(self,drawComponent=None, organism=None):
        self.next=None
        self.prev=None
        self.world=None
        if drawComponent is not None: drawComponent.ref=self
        if organism is not None: organism.ref=self
        self.drawComponent=drawComponent
        self.organism=organism
        self.pos=None
        
    def draw(self):
        self.drawComponent.draw()
        pass
    
    
    def update(self):
        print(self.organism)
    
    def getPos(self):
        return pos
    
    def getNeighbours(self):
        return self.world.getNeighbours(self.pos)
    
    pass
    