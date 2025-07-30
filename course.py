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
        finalMap.insert(0, [1] * len(finalMap[0]))
        finalMap.append([1] * len(finalMap[0]))
        return finalMap

    def findClosestWhiteSpace(self, app, direction):
        if direction == 'down':
            for row in range(len(self.map) -1, -1, -1):
                for col in range(len(self.map[0])):
                    if self.map[row][col] == 0:
                        row *= app.tileSize
                        row += app.tileSize /2
                        col *= app.tileSize
                        col += app.tileSize /2
                        return row, col
        if direction == 'up':
            for row in range(len(self.map)):
                for col in range(len(self.map[0])):
                    if self.map[row][col] == 0:
                        return row, col
        return 'all walls'
    
    def findClosestWhiteSpacePartialMap(self, app, direction, map):
        if direction == 'down':
            for row in range(len(map) -1, -1, -1):
                for col in range(len(map[0])):
                    if self.map[row][col] == 0:
                        row *= app.tileSize
                        row += app.tileSize /2
                        col *= app.tileSize
                        col += app.tileSize /2
                        return int(row//app.tileSize), int(col//app.tileSize)
        if direction == 'up':
            for row in range(len(map)):
                for col in range(len(map[0])):
                    if map[row][col] == 0:
                        return row, col
        return 'all walls'
    
    def combineMaps(self, app, directionOne, lengthOne, widthOne, directionTwo, lengthTwo, widthTwo):
        mapOne = self.createMap(lengthOne, widthOne, directionOne)
        mapTwo = self.createMap(lengthTwo, widthTwo, directionTwo)
        mapOneCols = len(mapOne[0])
        mapTwoCols = len(mapTwo[0])
        rowMapOneWhiteSpace, colMapOneWhiteSpace = self.findClosestWhiteSpacePartialMap(app, 'up', mapOne)
        rowMapTwoWhiteSpace, colMapTwoWhiteSpace = self.findClosestWhiteSpacePartialMap(app, 'down', mapTwo)
        #for the first one this doesn't matter, but the maps are spliced at the end
        if app.mapKey != 0:
            print('called')
            mapOne.append([1] * len(mapOne[0]))
        print(len(mapOne))

        #cols aren't equal
        if mapOneCols < mapTwoCols:
            difference = mapTwoCols - mapOneCols
            beforeRow = colMapTwoWhiteSpace - colMapOneWhiteSpace
            afterRow = difference - beforeRow
            for row in range(len(mapOne)):
                for i in range(difference):
                    mapOne[row].append(1)
        elif mapTwoCols < mapOneCols:
            difference = mapOneCols - mapTwoCols
            beforeRow = colMapOneWhiteSpace - colMapTwoWhiteSpace
            afterRow = difference - beforeRow
            for row in range(len(mapTwo)):
                for i in range(beforeRow):
                   # mapTwo[row].append(1)
                    mapTwo[row].insert(0, 1)
                for k in range(afterRow):
                  mapTwo[row].append(1)
        # doesn't matter if rows are unequal, only widths since a grid is being generated
        
        self.map = mapTwo[:-1] + mapOne[1:]


        
    def wallInPosition(self, app, x, y):
        newX = int(x//app.tileSize)
        newY = int(y//app.tileSize)
        
        return self.map[newY][newX]
    
    def wallInPositionClone(self, app, x, y):
        newX = int(x//app.tileSize)
        newY = int(y//app.tileSize)
        print(newX, newY, 'x, y')
        return self.map[newY][newX]

    def drawMap(self, app):
        for row in range(len(self.map)):
             for col in range(len(self.map[0])):
                if self.map[row][col] == 1:
                    drawRect(col * app.tileSize, row * app.tileSize, app.tileSize - 1, app.tileSize -1, fill = 'black')
                else:
                    drawRect(col * app.tileSize, row * app.tileSize, app.tileSize -1, app.tileSize -1, fill = 'white')

test = Course()
test2 = Course()
test.map = test.createMap(10, 5, 'straight')

