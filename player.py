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
        self.rotationSpeed = 1 * (math.pi/180)
        self.moving = False
        self.course = Course()
        self.playerAngle = 45 * (math.pi / 180) + 180

    
    def drawPlayer(self, app):
        drawCircle(self.x, self.y, self.radius, fill = 'red')
        drawLine(self.x, self.y, self.x + math.cos(self.playerAngle) *10 , self.y + math.sin(self.playerAngle) * 10, fill = 'red')

    

    def onKeyPress(self, app, key):
        if key == 'w':
            self.walkDirection = 1
           
        if key == 's':
            self.walkDirection = -1
           
        if key == 'a':
            self.turnDirection = -1
            
        if key == 'd':
            self.turnDirection = 1
        if key == 'space':
            print('called')
            self.inputForce += 20
    
    def buggyForces(self):
        if self.velocity > 0:
            normal = 9.8 * 150
            friction = normal * .7
            drag = (self.velocity ** 2) * .5 * 1.225 * 76.505653 * .47
            total = self.inputForce - friction - drag
            acceleration = total / 150
            print(acceleration)
            self.velocity += acceleration
        else:
            self.velocity = 1
       
    
    def move(self):
        self.buggyForces()
        isWall = self.course.wallInPosition(app, self.x + math.cos(self.playerAngle) * self.velocity, self.y + math.sin(self.playerAngle) * self.velocity)
        self.playerAngle += self.turnDirection * self.rotationSpeed
        if self.playerAngle > 180:
            self.playerAngle = 0
        if isWall == 0:
            self.x += math.cos(self.playerAngle) * self.velocity
            self.y += math.sin(self.playerAngle) * self.velocity


    def onMouseMove(self, app, mouseX, mouseY):
        if mouseX >= app.width // 2:
            self.turnDirection += .1
        if mouseX < app.width // 2:
            self.turnDirection += -.1
        if self.playerAngle > 360:
            self.playerAngle = 0
       
        self.move()



        
        
       
        
    
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

