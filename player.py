from cmu_graphics import * 
import math

class Player:

    def __init__(self):
        self.x = 60
        self.y = app.height - 60
        self.radius = 5
        self.dx = .1
        self.dy = .1
        self.turnDirection = 0 # 1 player is rotating to right, -1 rotating to left
        self.walkDirection = 0
        self.moveSpeed = 3
        self.rotationSpeed = 5 * (math.pi/180)
        self.moving = False

        self.playerAngle = 90 * (math.pi / 180)

    
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
        self.moving = True

        
        
       
        
    
    def whileKeysPressed(self):
        if self.moving == True:
            moveStep = self.walkDirection * self.moveSpeed
            self.playerAngle += self.turnDirection * self.rotationSpeed
            print(self.playerAngle)
            self.x += math.cos(self.playerAngle) * moveStep
            self.y += math.sin(self.playerAngle) * moveStep


    def onKeyRelease(self, key):
        self.moving = False
        if key == 'w' or key == 's':
            self.walkDirection = 0
        if key == 'a' or key == 'd':
            self.turnDirection = 0

