from engine import Engine
import sys


if __name__=="__main__":

    programName = sys.argv[0]
    arguments = sys.argv[1:]        
    argCount = len(arguments)
    sw,sh,ww,wh,fps = (1000,1000,100,100,30)
    caption = "Life Simulator"
    try:
        sw = arguments[0]
        sh = arguments[1]
        ww = arguments[2] 
        wh = arguments[3]
        fps = arguments[4]
    except :
        pass    
    
    game = Engine((sw,sh),caption,(ww,wh),fps)
    
    game.gameLoop()
    
    game.quit()
    quit()