from cmu_graphics import * 
import math
from player import Player

def convertAngle(anlge): 
    angle = anlge % (2* math.pi)
    if anlge < 0:
        anlge = (math.pi * 2) + angle
    return angle

def wallInPosition(app, x, y):
        xPos = math.floor(x/app.tileSize)
        yPos = math.floor(y/app.tileSize)
        print(xPos, yPos)
        if app.map[yPos][xPos] == 1: 
            return True
        else:
            return False

class Ray:
    def __init__(self, angle, player):
        self.rayAngle = convertAngle(angle)
        self.player = player
        self.facesDown = self.rayAngle > 0 and self.rayAngle < math.pi
        self.facesUp = self.rayAngle < 0 and self.rayAngle > math.pi
        self.facesRight = self.rayAngle < (math.pi/2) or self.rayAngle > (3 * math.pi/2)
        self.facesLeft = self.rayAngle > (math.pi/2) or self.rayAngle < (3 * math.pi/2)

        self.wallHitX = 0
        self.wallHitY = 0

    


    def cast(self, app):
        horizontalWallFound = False
        horizontalHitX = 0
        horizontalHitY = 0

        firstIntersectionInX = 0
        firstIntersectionInY = 0

        if self.facesUp: 
            firstIntersectionInY = ((self.player.y) // app.tileSize) * (app.tileSize - 1)
        elif self.facesDown:
            firstIntersectionInY = ((self.player.y) // app.tileSize) * (app.tileSize + 1)

        firstIntersectionInX = self.player.x + (firstIntersectionInY - self.player.y) / math.tan(self.rayAngle)

        nextHorizontalIntersectionX = firstIntersectionInX
        nextHorizontalIntersectionY = firstIntersectionInY
        xA = 0
        yA = 0
        if self.facesUp:
            yA = -app.tileSize
        elif self.facesDown:
            yA = app.tileSize
        xA = yA / math.tan(self.rayAngle)
        while (nextHorizontalIntersectionX <= app.width and nextHorizontalIntersectionX >= 0 and nextHorizontalIntersectionY <= app.height and nextHorizontalIntersectionY >=0):
            if wallInPosition(app, nextHorizontalIntersectionX, nextHorizontalIntersectionY):
                horizontalWallFound = True
                horizontalHitX = nextHorizontalIntersectionX
                horizontalHitY = nextHorizontalIntersectionY
            else:
                nextHorizontalIntersectionX += xA
                nextHorizontalIntersectionY += yA

        self.wallHitX = horizontalHitX
        self.wallHitY = horizontalHitY



   


    

    def drawRays(self, app):
        print('now called')
        drawLine(self.player.x, self.player.y, self.wallHitX, self.wallHitY, fill = 'red')
        