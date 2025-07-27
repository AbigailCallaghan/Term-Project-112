from cmu_graphics import * 
import math
from player import Player
from raycaster import Raycaster
from course import Course

#using this https://www.youtube.com/watch?v=E18bSJezaUE tutorial for basic raycaster 
#it's in pygame so i'm translating it to cmu graphics
# i will be rewriting most of the code, I am just getting the basics so the code right now follows the tutorial pretty closely
def onAppStart(app):
    app.tileSize = 32
    app.rows = 10
    app.cols = 15
    app.width = app.cols * app.tileSize
    app.height = app.rows *app.tileSizeg
    
    app.FOV = 60 * (math.pi / 180)
    app.resilution = 10
    app.rayAmount = app.width // app.resilution
    app.course = Course()
    app.player = Player()
    app.raycaster = Raycaster(app.player, app.course)
    app.pY = app.height - 50
    app.lineLength = 30
    app.dx = 1
    app.dy = 1
    app.stepsPerSecond = 5


def redrawAll(app):
    drawRect(0, 0, app.width, app.height, fill = 'grey')
    app.course.drawMap(app)
    app.player.drawPlayer(app)
    app.raycaster.drawAllRays(app)



def angleInUnitCircle(angle):
    angle = angle % (2 *math.pi)
    if angle < 0:
        angle = (2 * math.pi) + angle
    return angle

def onStep(app):
    app.player.whileKeysPressed()

def onKeyPress(app, key):
    app.player.onKeyPress(app,key)
    app.raycaster.castAllRays(app)

def onKeyRelease(app, key):
    app.player.onKeyRelease(key)



def wallInPosition(app, x, y):
    xPos = math.floor(x/app.tileSize)
    yPos = math.floor(y/app.tileSize)
    if app.map[xPos,yPos] == 1: 
        return True
    else:
        return False


    
def main():
    runApp()

main()