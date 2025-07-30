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
    app.course = Course()
    app.mapKey = 0
    app.nextBottom =0
    app.player = Player(app, app.course)
    createMap(app)
    app.rows = len(app.course.map)
    app.cols = len(app.course.map[0])
    app.width = app.cols * app.tileSize
    app.height = app.rows *app.tileSize
    app.FOV = 60 * (math.pi / 180)
    app.resilution = 1
    app.rayAmount = app.width // app.resilution
    steeringWheelDimensions(app)
    app.raycaster = Raycaster(app.player, app.course)
    app.pY = app.height - 50
    app.lineLength = 30
    app.drawMap = True
    app.manual = False
    app.stepsPerSecond = 30


def redrawAll(app):
    drawRect(0, 0, app.width, app.height, fill = 'black')
    if app.drawMap == True:
        app.course.drawMap(app)
        app.player.drawPlayer(app)
        app.raycaster.drawAllRays(app)
    else:
        app.raycaster.drawAllRays(app)
        drawSteeringWheel(app)

def steeringWheelDimensions(app):
    distanceFromSides = app.width/6
    app.steeringWheelHeight = 40
    distanceFromGround = app.height - app.steeringWheelHeight
    app.steeringWheelLeftCordinates = (distanceFromSides, distanceFromGround + 10)
    app.steeringWheelRightCordinates = (app.width - distanceFromSides, distanceFromGround + 10)

def drawSteeringWheel(app):
    steeringWheelColor = 'darkSlateGray'
    drawRect(app.steeringWheelLeftCordinates[0], app.steeringWheelLeftCordinates[1]-10, app.width - 2* app.steeringWheelLeftCordinates[0], 20, fill = steeringWheelColor)
    drawCircle(app.steeringWheelLeftCordinates[0],  app.steeringWheelLeftCordinates[1], 10, fill = steeringWheelColor)
    drawCircle(app.width - app.steeringWheelLeftCordinates[0], app.steeringWheelLeftCordinates[1], 10, fill = steeringWheelColor)
    drawRect(app.width/2, app.steeringWheelLeftCordinates[1] + 20, 30, app.steeringWheelHeight, fill = steeringWheelColor, align = 'center')

def onStep(app):
    #app.player.move()
    app.raycaster.castAllRays(app)
    app.player.turnDirection = 0
    switchMaps(app)
    if app.manual == False:
        app.player.move(app)

def angleInUnitCircle(angle):
    angle = angle % (2 * math.pi)
    if angle < 0:
        angle = (2 * math.pi) + angle
    return angle

def onKeyPress(app, key):
    app.player.onKeyPress(app,key)
    app.raycaster.castAllRays(app)



def onMousePress(app, mouseX, mouseY):
    if app.manual == False:
        app.player.onMousePress(app, mouseX, mouseY)

def createMap(app):
    potentialMaps = {2: ['straight', 10, 6], 1: ['curved up', 8, 5], 0: ['straight', 10, 5]}
    if app.mapKey + 1 < len(potentialMaps):
        mapOneDirection = potentialMaps[app.mapKey][0]
        mapTwoDirection = potentialMaps[app.mapKey + 1][0]
        mapOneLength = potentialMaps[app.mapKey][1]
        mapTwoLength = potentialMaps[app.mapKey + 1][1]
        mapOneWidth = potentialMaps[app.mapKey][2]
        mapTwoWidth = potentialMaps[app.mapKey + 1][2]
        app.nextBottom = mapOneLength + 1
        app.course.combineMaps(app, mapOneDirection, mapOneLength, mapOneWidth, mapTwoDirection, mapTwoLength, mapTwoWidth)
        #need to reset player position for y, x is fine
        app.player.y, placeHolder =  app.course.findClosestWhiteSpace(app, 'down')


def switchMaps(app):
    trueYCoord = int(app.player.y//app.tileSize)
    if trueYCoord == (app.rows- (app.nextBottom + 1)):
        app.mapKey +=1
        createMap(app)
    
def main():
    runApp()

main()