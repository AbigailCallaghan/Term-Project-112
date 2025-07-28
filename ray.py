from cmu_graphics import * 
import math
from player import Player
from course import Course

#makes sure angle is always between 0 and 2pi
def convertAngle(anlge): 
    angle = anlge % (2* math.pi)
    if anlge <= 0:
        anlge = (math.pi * 2) + angle
    return angle

def distance(x0, y0, x1, y1):
    return ((x0-x1)**2 + (y0 -y1)**2) **.5



class Ray:
    def __init__(self, angle, player, course):
        self.rayAngle = convertAngle(angle)
        self.player = player
        self.course = course
        self.facesDown = self.rayAngle > 0 and self.rayAngle < math.pi
        self.facesUp = self.rayAngle < 0 and self.rayAngle > math.pi or not self.facesDown
        self.facesRight = self.rayAngle < (math.pi/2) or self.rayAngle > (3 * math.pi/2)
        self.facesLeft = self.rayAngle > (math.pi/2) or self.rayAngle < (3 * math.pi/2) or not self.facesRight
        self.wallHitX = 0
        self.wallHitY = 0
        self.distance =0

    


    def cast(self, app):
        #check horizontal driection
        horizontalWallFound = False
        horizontalHitX = 0
        horizontalHitY = 0

        firstIntersectionInX = 0
        firstIntersectionInY = 0

        if self.facesUp: 
            firstIntersectionInY = (self.player.y // app.tileSize) * app.tileSize - 1
        elif self.facesDown:
            firstIntersectionInY = ((self.player.y // app.tileSize) * app.tileSize ) + app.tileSize

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
            if app.course.wallInPosition(app, nextHorizontalIntersectionX, nextHorizontalIntersectionY):
                horizontalWallFound = True
                horizontalHitX = nextHorizontalIntersectionX
                horizontalHitY = nextHorizontalIntersectionY
                break
            else:
                nextHorizontalIntersectionX += xA
                nextHorizontalIntersectionY += yA

        self.wallHitX = horizontalHitX
        self.wallHitY = horizontalHitY

        #check veritcal direction
        verticalWallFound = False
        verticalHitX = 0
        verticalHitY = 0

        if self.facesRight:
            firstIntersectionInX = ((self.player.x // app.tileSize) * app.tileSize) + app.tileSize
            xA = app.tileSize
        elif self.facesLeft:
            firstIntersectionInX = (self.player.x // app.tileSize) * app.tileSize - 1
            xA = -app.tileSize

        firstIntersectionInY = self.player.y + (firstIntersectionInX - self.player.x) * math.tan(self.rayAngle)
        nextVerticalX = firstIntersectionInX
        nextVerticalY = firstIntersectionInY
        yA = math.tan(self.rayAngle) * xA

        while (nextVerticalX <= app.width and nextVerticalX >= 0 and nextVerticalY <= app.height and nextVerticalY >=0):
            if self.course.wallInPosition(app, nextVerticalX, nextVerticalY):
                verticalWallFound = True
                verticalHitX = nextVerticalX
                verticalHitY = nextVerticalY
                break
            else:
                nextVerticalX += xA
                nextVerticalY += yA

        horizontalDistance = 0
        verticalDistance = 0
        if horizontalWallFound:
            horizontalDistance = distance(self.player.x, self.player.y, horizontalHitX, horizontalHitY)
        #else:
         #  horizontalDistance = 99999

        if verticalWallFound:
            verticalDistance = distance(self.player.x, self.player.y, verticalHitX, verticalHitY)
       # else:
        #  verticalDistance = 99999
        if horizontalDistance < verticalDistance:
            self.wallHitX = horizontalHitX
            self.wallHitY = horizontalHitY
            self.distance = horizontalDistance
        else:
            self.wallHitX = verticalHitX
            self.wallHitY = verticalHitY
            self.distance = verticalDistance

        self.distance *= math.cos(self.player.playerAngle - self.rayAngle)



    

    def drawRays(self, app):
       #drawLine(self.player.x, self.player.y, self.player.x + math.cos(self.rayAngle) * 50, self.player.y + math.sin(self.rayAngle) * 50, fill = 'red')
       drawLine(self.player.x, self.player.y, self.player.x + self.wallHitX, self.player.y + self.wallHitY, fill = 'red')
        