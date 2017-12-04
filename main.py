#from engine import Engine
import world as w

world = w.World()
objBuilder = world.WorldObjBuilder()
a = objBuilder.setDrawComponent(w.DrawComponent('a')).setOrganism('a').build()
b = objBuilder.setDrawComponent(w.DrawComponent('b')).setOrganism('b').build()
c = objBuilder.setDrawComponent(w.DrawComponent('c')).setOrganism('c').build()
d = objBuilder.setDrawComponent(None).setOrganism(None).build()
world.addObject(a)
world.addObject(b)
world.addObject(c)
world.addObject(d)
world.drawWorld()
print()
world.updateWorld()
print()
world.destroyObject(a)
world.drawWorld()

'''
if __name__=='__main__':

    e = Engine((800,600),"hello")
    
    e.gameLoop()
    
    quit()
 '''  