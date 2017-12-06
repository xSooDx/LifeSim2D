import abc
import crossover as cross
import random

class ObjectDestroyed(Exception):
    pass
    
class EmptyWorld(Exception):
    pass
    
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
            self.comps = {}
            
        # Add a drawable Component
        def setDrawComponent(self, dc):
            if isinstance(dc,Component):
                self.comps['draw'] = dc
            else:
                raise TypeError("Not of type Component")
            return self
        
        
        def addComponent(self,cname,comp):
            if isinstance(comp,Component):
                self.comps[cname] = comp
            else:
                raise TypeError("Not of type Component")
            return self
        
        # Create and return object
        def build(self):
            obj = WorldObject()
            for i in self.comps:
                obj.addComponent(i,self.comps[i])
            
            return obj
        
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
        if self.numObjects == 0:
            raise EmptyWorld()
        for o in self:
            #try:
                o.update()
            #except Exception as e:
                # ignores if updateable component is missing
            #    print(e)
    
    
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
    # Destroy World Object inplace
    def destroyObject(self,obj):
        assert isinstance(obj,WorldObject), "Not a world object"
        assert obj.world == self, "Object not part of this world"
        assert not self.head.next == self.tail and self.numObjects > 0, "No object in world"
        
      
        obj.prev.next = obj.next
        obj.next.prev = obj.prev
        self.numObjects-=1
        obj.world=None
        p = obj.pos
        obj.pos=None
        self.map[p[1]][p[0]]=0
    
    def moveObject(self,obj,npos):
        assert isinstance(obj,WorldObject), "Not a world object"
        assert obj.world == self, "Object not part of this world"
        self._testPos(npos)
        if obj.pos == npos: return True
        
        tmp = obj.pos
        try:
            self.map[obj.pos[1]][obj.pos[0]]=0
            self.map[npos[1]][npos[0]]=obj
            obj.pos=npos
            return True
        except:
            self.map[tmp[1]][tmp[0]]=obj
            self.map[npos[1]][npos[0]]=0
            obj.pos=tmp
            return False
            
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
    
    def getEmptyNeighbourhood(self,pos,r=1):
        res=[]
        for i in range(-r,r+1):
            x = pos[0]+i
            for j in range(-r,r+1):
                y = pos[1]+j
                if i==0 and j==0:
                    pass
                else:
                    try:
                        self._testPos((x,y))
                        if self.map[y][x] == 0:
                            res.append((x,y))
                    except:
                        pass
                
            
        return res   

    

class Component(abc.ABC):    
    def __init__(self):
        self.parent=None
        
    @abc.abstractmethod
    def update():
        pass
        

        
# Drawable component baseclass
class DrawComponent(Component):
    def __init__(self):
        super().__init__()
        
    def update(self):
        pass
        
    def draw(self):
        print(self.a,end='')

#World Object Class
class WorldObject():
    def __init__(self):
        self.next=None
        self.prev=None
        self.world=None        
        self.pos=None
        self.components = dict()
        
    def draw(self):
        self.getComponent('draw').draw()
        pass
    
    def getComponent(self,cname):
        return self.components.get(cname,None)
    
    def addComponent(self, cname, component):
        assert isinstance(component, Component), "Not a component"
        component.parent=self
        self.components[cname]=component
        
    
    def removeComponent(self, cname):
        try:
            self.components.remove(cname)
        except: pass
    
    def update(self):
        try:
            for i in self.components:
                self.components[i].update()
        except ObjectDestroyed as od:
            self.destroy()
            print(od)
            
    
    def getPos(self):
        return self.pos
    
    def getNeighbours(self,r=1):
        return self.world.getNeighbours(self.pos,r)
    
    def getEmptyNeighbourhood(self,r=1):
        return self.world.getEmptyNeighbourhood(self.pos,r)
    
    def destroy(self):
        return self.world.destroyObject(self)
        
    def move(self,pos):
        return self.world.moveObject(self,pos)
    