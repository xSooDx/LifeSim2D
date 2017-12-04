import abc

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



        
#Game World Class
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
        
    def __init__(self):
        # Initialize head and tails of internal linklist
        h = _lln()
        t = _lln()
        h.next = t
        t.prev = h
        self.head= h
        self.tail= t
        self.numObjects = 0
        
    # Iterator through world objects
    def __iter__(self):
        return _worldIterator(self.head, self.tail)
    
    # Draws all world objects if they have a draw component
    def drawWorld(self):
        for o in self:
            try:
                o.draw()
            except AttributeError as e:
                # ignore if draw component is missing
                pass
       
    # Updates all world objects
    def updateWorld(self):
        for o in self:
            try:
                o.update()
            except Exception as e:
                # ignores if updateable component is missing
                print(e)
    
    # Adds a world object to internal list
    def addObject(self,obj):
        
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
        self.numObjects+=1
        
        
        return obj
    
    # Destroy World Object inplace
    def destroyObject(self,obj):
        assert not self.head.next == self.tail and self.numObjects > 0
        if obj.world == self:
            obj.prev.next = obj.next
            obj.next.prev = obj.prev
            self.numObjects-=1
        else: raise ValueError("object not part of this world")
    pass
    
# Drawable component baseclass
class DrawComponent():#abc.ABC):
    #@abc.abstractmethod
    def __init__(self,a):
        self.a=a    
    def draw(self):
        print(self.a)

#World Object Class
class WorldObject():
    def __init__(self,drawComponent=None, organism=None):
        self.next=None
        self.prev=None
        self.world=None
        self.drawComponent=drawComponent
        self.organism=organism
        
    def draw(self):
        self.drawComponent.draw()
        pass
    
    
    def update(self):
        print(self.organism)
    
    pass
    