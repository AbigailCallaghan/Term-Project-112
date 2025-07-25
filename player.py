from cmu_graphics import * 
import math

class Player:

    def __init__(self):
        self.x = 84
        self.y = app.height - 30
        self.radius = 5
        self.dx = .1
        self.dy = .1
        self.playerAngle = 0

    
    def drawPlayer(self, app):
        drawCircle(self.x, self.y, self.radius, fill = 'red')
        drawLine(self.x, self.y, self.x + math.cos(self.playerAngle) *10 , self.y + math.sin(self.playerAngle) * 10, fill = 'red')

    def onKeyPress(self, app, key):
        if key == 'w':
            self.x += self.dx
            self.y += self.dy
        if key == 's':
            self.x -= self.dx
            self.y -= self.dy
        if key == 'a':
            self.playerAngle -=.1
            if self.playerAngle < 0:
                self.playerAngle += 2 * math.pi
            self.dx = math.cos(self.playerAngle) * 10
            self.dy = math.sin(self.playerAngle) * 10
        if key == 'd':
            self.playerAngle +=.1
            if self.playerAngle > 0:
                self.playerAngle -= 2 * math.pi
            self.dx = math.cos(self.playerAngle) * 10
            self.dy = math.sin(self.playerAngle) * 10
