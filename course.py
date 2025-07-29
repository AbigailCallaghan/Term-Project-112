from cmu_graphics import * 
import math
class Course:
    def __init__(self):
        self.map = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
               [1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
               [1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1],
               [1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1],
               [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
               [1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
               [1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
               [1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1],
               [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
               [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
        
   
       
    
    def createMap(self, length, width, type):
        finalMap = []
        if type == 'straight':
            for row in range(length):
                newRow = [1]
                for col in range(width):
                    newRow.append(0)
                newRow.append(1)
                finalMap.append(newRow)
        elif type == 'curved up':
            for row in range(length):
                newRow = [1] * (length - row)
                for col in range(width + 1):
                    newRow.append(0)
                newRow += [1] * (row + 1)
                finalMap.append(newRow)
        elif type == 'curved down':
            for row in range(length):
                newRow = [1] * (row + 1)
                for col in range(width + 1):
                    newRow.append(0)
                newRow += [1] * (length - row)
                finalMap.append(newRow)
        self.map = finalMap
        print('final map', finalMap)


        
    def wallInPosition(self, app, x, y):
        return self.map[int(y // app.tileSize)][int(x//app.tileSize)]

    def drawMap(self, app):
        for row in range(len(self.map)):
             for col in range(len(self.map[0])):
                if self.map[row][col] == 1: 
                    drawRect(col * app.tileSize, row * app.tileSize, app.tileSize - 1, app.tileSize -1, fill = 'black')
                else:
                    drawRect(col * app.tileSize, row * app.tileSize, app.tileSize -1, app.tileSize -1, fill = 'white')

test = Course()
 
test.createMap(5, 2, 'curved down')


#[[1, 1, 1, 1, 0, 0, 0, 1]
# [1, 1, 1, 0, 0, 0, 1, 1]
 #[1, 1, 0, 0, 0, 1, 1, 1]
 #[1, 0, 0, 0, 1, 1, 1, 1]]