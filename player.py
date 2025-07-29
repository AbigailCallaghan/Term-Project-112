from cmu_graphics import * 
import math
from course import Course

class Player:

    def __init__(self, course):
        self.x = 50
        self.y = app.height - 60
        self.radius = 5
        self.dx = .1
        self.dy = .1
        self.turnDirection = 0 # 1 player is rotating to right, -1 rotating to left
        self.walkDirection = 0
        self.velocity = 1
        self.inputForce = 0
        self.rotationSpeed = 45 * (math.pi/180)
        self.moving = False
        self.course = Course()
        self.playerAngle = 45 * (math.pi / 180) + 180

    
    def drawPlayer(self, app):
        drawCircle(self.x, self.y, self.radius, fill = 'red')
        drawLine(self.x, self.y, self.x + math.cos(self.playerAngle) *10 , self.y + math.sin(self.playerAngle) * 10, fill = 'red')

    

    def onKeyPress(self, app, key):
        print(key, self.velocity)
        if key == 'w':
            self.walkDirection = 1
           
        if key == 's':
            self.walkDirection = -1
           
        if key == 'a':
            self.turnDirection = -1
            
        if key == 'd':
            self.turnDirection = 1
        if key == 'space':
            self.inputForce += 400
        self.move(app)
    
    def buggyForces(self, app):
        if self.velocity >= 0:
            normal = 9.8 * 68
            friction = normal * .05
            drag = (self.velocity ** 2) * .5 * 1.225 * 76.505653 * .47
            self.inputForce = (self.inputForce - friction - drag) if self.inputForce >= 0 else 0
            acceleration = self.inputForce / 68
            self.velocity += acceleration * (1/app.stepsPerSecond)
        else:
            self.velocity = 0
       
    
    def move(self, app):
        self.buggyForces(app)
        isWall = self.course.wallInPosition(app, self.x + math.cos(self.playerAngle) * self.velocity, self.y + math.sin(self.playerAngle) * self.velocity)
        self.playerAngle += self.turnDirection * self.rotationSpeed
       # if self.playerAngle > 180:
       #     self.playerAngle = 0
        if isWall == 0:
            self.x += math.cos(self.playerAngle) * self.velocity
            self.y += math.sin(self.playerAngle) * self.velocity


    def onMouseMove(self, app, mouseX, mouseY):
       # print(self.playerAngle, 'angle')
        #if mouseX >= app.width // 2:
         #   self.turnDirection += .01
        #if mouseX < app.width // 2:
        #    self.turnDirection += -.01
        if self.playerAngle > 360:
            self.playerAngle = 0
       
        self.move(app)



        
        
       
        
    
    def whileKeysPressed(self):
        if self.moving == True:
            moveStep = self.walkDirection * self.moveSpeed
            self.playerAngle += self.turnDirection * self.rotationSpeed
            self.x += math.cos(self.playerAngle) * moveStep
            self.y += math.sin(self.playerAngle) * moveStep


    def onKeyRelease(self, key):
        self.moving = False
        if key == 'w' or key == 's':
            self.walkDirection = 0
        if key == 'a' or key == 'd':
            self.turnDirection = 0

