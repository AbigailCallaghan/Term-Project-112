from cmu_graphics import * 
import math
from player import Player
from raycaster import Raycaster
def onAppStart(app):
    app.tileSize = 64
    app.rows = 10
    app.cols = 15
    app.width = app.cols * app.tileSize
    app.height = app.rows *app.tileSize
    app.FOV = 90 * (math.pi / 180)
    app.resilution = 4
    app.rayAmount = app.width // app.resilution
    app.map = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
               [1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
               [1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1],
               [1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1],
               [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
               [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
               [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
               [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
               [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
               [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
    app.player = Player()
    app.raycaster = Raycaster(app.player)
    app.pY = app.height - 50
    app.lineLength = 30
    app.dx = 1
    app.dy = 1


def redrawAll(app):
    drawRect(0, 0, app.width, app.height, fill = 'grey')
    drawMap(app)
    app.player.drawPlayer(app)
    app.raycaster.drawAllRays(app)



def angleInUnitCircle(angle):
    angle = angle % (2 *math.pi)
    if angle < 0:
        angle = (2 * math.pi) + angle
    return angle


def onKeyPress(app, key):
    app.player.onKeyPress(app,key)
    app.raycaster.castAllRays(app)

    


def wallInPosition(app, x, y):
    xPos = math.floor(x/app.tileSize)
    yPos = math.floor(y/app.tileSize)
    if app.map[xPos,yPos] == 1: 
        return True
    else:
        return False

def drawMap(app):
    for row in range(len(app.map)):
        for col in range(len(app.map[0])):
            if app.map[row][col] == 1: 
                drawRect(col * app.tileSize, row * app.tileSize, app.tileSize - 1, app.tileSize -1, fill = 'black')
            else:
                drawRect(col * app.tileSize, row * app.tileSize, app.tileSize -1, app.tileSize -1, fill = 'white')
    
def main():
    runApp()

main()