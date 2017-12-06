#from engine import Engine
import world as w
import time
from organism import*
world = w.World(20,20)
objBuilder = world.WorldObjBuilder()


af = AnimalFactory(world)
pf = PlantFactory(world)

b = af.create(1,[101,75,95,8],[5,3])
'''b = af.create(1,[99,74,89,8],[4,4])
b = af.create(2,[150,63,125,8],[13,6])
b = af.create(2,[145,61,129,8],[12,7])
b = af.create(3,[25,30,100,8],[15,1])
b = af.create(3,[20,27,100,8],[16,2])'''
b = pf.create(1,[100,10],[19,18])
b = pf.create(1,[100,10],[4,16])
b = pf.create(1,[100,10],[10,10])
b = pf.create(1,[100,10],[16,3])
print(pf.world)
print(b.pos)
print(b.world)
for i in world:
    print(i)
    
'''        
a = objBuilder.setDrawComponent(w.DrawComponent('a')).addComponent('organism', Plant([5,5],0)).build()
b = objBuilder.setDrawComponent(w.DrawComponent('b')).addComponent('organism', Animal([5,5,5,5],1)).build()
c = objBuilder.setDrawComponent(w.DrawComponent('c')).addComponent('organism', Plant([5,5],1)).build()
e = objBuilder.setDrawComponent(w.DrawComponent('e')).addComponent('organism', Plant([5,5],1)).build()
#d = objBuilder.setOrganism(o()).build()
world.addObject(a,[5,6])
world.addObject(b,[0,2])
world.addObject(c,[5,5])
#world.addObject(d,[3,3])
world.addObject(e,[4,4])
'''

while True:
    world.updateWorld()
    world.drawWorld()
    time.sleep(0.1)
    print()
    

'''
if __name__=='__main__':

    e = Engine((800,600),"hello")
    
    e.gameLoop()
    
    quit()
 '''  