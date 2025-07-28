from cmu_graphics import * 
import math
class Course:
    def __init__(self):
        self.map = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
               [1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
               [1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1],
               [1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1],
               [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
               [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
               [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
               [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
               [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
               [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
        
    def wallInPosition(self, app, x, y):
        return self.map[int(y // app.tileSize)][int(x//app.tileSize)]

    def drawMap(self, app):
        for row in range(len(self.map)):
             for col in range(len(self.map[0])):
                if self.map[row][col] == 1: 
                    drawRect(col * app.tileSize, row * app.tileSize, app.tileSize - 1, app.tileSize -1, fill = 'black')
                else:
                    drawRect(col * app.tileSize, row * app.tileSize, app.tileSize -1, app.tileSize -1, fill = 'white')