from cmu_graphics import * 
import math
from course import Course
#the player class was partially inspired by the raycasting tutorial
#specifically the player angle speeds and the increase to the player x and y
#the key press, mouse press, and other parts of move are all my own ideas

def distance(x0, y0, x1, y1):
    return ((x0-x1)**2 + (y0 -y1)**2) **.5

class Player:

    def __init__(self, app, course):
        self.course = course
        self.y, self.x = self.course.findClosestWhiteSpace(app, 'down')
        self.radius = 5
        self.dx = .1
        self.dy = .1
        self.turnDirection = 0 # 1 player is rotating to right, -1 rotating to left
        self.walkDirection = 0
        self.velocity = 0
        self.inputForce = 0
        self.rotationSpeed = 90 * (math.pi/180)
        self.moving = False
        self.totalDistance = 0
        self.playerAngle = 45 * (math.pi / 180) + 180

    
    def drawPlayer(self, app):
        drawCircle(self.x, self.y, self.radius, fill = 'red')
        drawLine(self.x, self.y, self.x + math.cos(self.playerAngle) *10 , 
                 self.y + math.sin(self.playerAngle) * 10, fill = 'red')

    def onKeyPress(self, app, key):
        if key == 'a' and app.playerChars[3] == 'Keys':
            self.turnDirection = -.25
            
        if key == 'd' and app.playerChars[3] == 'Keys':
            self.turnDirection = .25
        if key == 'space' and app.pushZone == True and app.coolDown == 0:
            print('called')
            self.inputForce += app.playerChars[2]
            app.coolDown = app.maxCoolDown
            print(app.coolDown)
            app.maxCoolDown += 100
        
        self.move(app)
        
    #I used AI to check that the physics was semi realistic after I wrote the code
    #there were a few tweaks to the physics
    #but the basic code remained the same
    def buggyForces(self, app):
        if self.velocity >= 0:
            slope = app.potentialMaps[app.mapKey][3]
            slope = math.radians(slope)
            weight = 9.8 * 68 * math.sin(slope)
            normal = 9.8 * 68
            friction = normal * .05
            drag = (self.velocity ** 2) * .5 * 1.225 * 2 * .47
            repellingForces = (friction + drag + weight) / (app.stepsPerSecond)
            total = -repellingForces
            if self.inputForce != 0:
                total = self.inputForce - repellingForces
                self.inputForce *= .6
            acceleration = total / 68
            self.velocity += acceleration
        else:
            self.velocity = 0  
    
    def move(self, app):
        self.buggyForces(app)
        isWall = self.course.wallInPosition(app, self.x + math.cos(self.playerAngle) * self.velocity, 
                                            self.y + math.sin(self.playerAngle) * self.velocity)
        self.playerAngle += self.turnDirection * self.rotationSpeed
        if isWall == 0:
            if self.x >=0 and self.y >=0:
                dx = math.cos(self.playerAngle) * self.velocity
                dy = math.sin(self.playerAngle) * self.velocity
                self.x += dx
                self.y += dy
                self.totalDistance += (dx ** 2 + dy **2) **.5
            
   

    def onMousePress(self, app, mouseX, mouseY):
        if (mouseY >= (app.height - app.steeringWheelHeight) and mouseY <= app.height - 20 and 
            mouseX >= (app.steeringWheelLeftCordinates[0] - 10) and (mouseX <= app.steeringWheelRightCordinates[0] + 10)):
            leftX = app.steeringWheelLeftCordinates[0]
            leftY = app.steeringWheelLeftCordinates[1]
            rightX = app.steeringWheelRightCordinates[0]
            rightY = app.steeringWheelRightCordinates[1]
            distanceBetweenLeft = distance(mouseX, mouseY, leftX, leftY)
            distanceBetweenRight = distance(mouseX, mouseY, rightX, rightY)
            #tells which direction you're trying to steer in
            #the closer you are to the center of the wheel, the less force you imput
            if distanceBetweenRight > distanceBetweenLeft:
                self.turnDirection -= (1/distanceBetweenLeft) * self.rotationSpeed
            else:
                self.turnDirection += (1/distanceBetweenRight) * self.rotationSpeed
            
            self.move(app)

    def whileKeysPressed(self):
        if self.moving == True:
            moveStep = self.walkDirection * self.moveSpeed
            self.playerAngle += self.turnDirection * self.rotationSpeed
            self.x += math.cos(self.playerAngle) * moveStep
            self.y += math.sin(self.playerAngle) * moveStep


