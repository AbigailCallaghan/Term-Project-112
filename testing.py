def wallInPosition(map, tileSize, x, y):
        newX = int(x//tileSize)
        newY = int(y//tileSize)
        print(newX, newY, 'x, y')
        return map[newY][newX]

practice = [[1, 1, 1, 1, 1, 1, 1], 
            [1, 0, 0, 0, 0, 0, 1], 
            [1, 0, 0, 0, 0, 0, 1], 
            [1, 0, 0, 0, 0, 0, 1], 
            [1, 0, 0, 0, 0, 0, 1], 
            [1, 0, 0, 0, 0, 0, 1], 
            [1, 0, 0, 0, 0, 0, 1], 
            [1, 0, 0, 0, 0, 0, 1], 
            [1, 0, 0, 0, 0, 0, 1], 
            [1, 0, 0, 0, 0, 0, 1], 
            [1, 0, 0, 0, 0, 0, 1], 
            [1, 1, 1, 1, 1, 1, 1]]

print(wallInPosition(practice, 32, 64.2115757135358, 260.7725839762933))