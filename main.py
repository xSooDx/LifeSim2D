#from engine import Engine
import world as w

world = w.World(8,8)
objBuilder = world.WorldObjBuilder()
a = objBuilder.setDrawComponent(w.DrawComponent('a')).setOrganism('a').build()
b = objBuilder.setDrawComponent(w.DrawComponent('b')).setOrganism('b').build()
c = objBuilder.setDrawComponent(w.DrawComponent('c')).setOrganism('c').build()
e = objBuilder.setDrawComponent(w.DrawComponent('e')).setOrganism('e').build()
d = objBuilder.setDrawComponent(None).setOrganism(None).build()
world.addObject(a,[5,6])
world.addObject(b,[0,2])
world.addObject(c,[5,5])
world.addObject(d,[3,3])
world.addObject(e,[4,4])
world.drawWorld()
print()
world.updateWorld()
print()
world.moveObject(b,[4,6])
world.drawWorld()
print()
for i in world.getNeighbours([4,6]):
    i.draw()
    
world.destroyObject(a)
world.drawWorld()
print(world.map)
'''
if __name__=='__main__':

    e = Engine((800,600),"hello")
    
    e.gameLoop()
    
    quit()
 '''  