from cmu_graphics import * 
import random

class Star:
    def __init__(self, x, y, opacity):
        self.x = x
        self.y = y
        self.opacity = opacity

    def drawLight(self):
        drawCircle(self.x, self.y, 10, 
                   fill = gradient('ivory', 'cornSilk', 'wheat', 'goldenrod', start='center'), 
                   opacity = self.opacity)
    
    def __eq__(self, other):
        return isinstance(other, Star) and self.x == other.x and self.y == other.y
    
    def __hash__(self):
        return hash(str(self))
        
class AllStars:

    def __init__(self, app):
        self.allStars = set()
        self.generateAllStars(app)
    
    def generateAllStars(self, app):
        print('')
        starAmount = random.randint(5, 10)
        for star in range(starAmount):
            self.allStars.add(self.generateRandomStar(app))
            
    def generateRandomStar(self, app):
        starX = random.randint(10, app.width -10)
        starY = random.randint(app.height-50, app.height)
        starOpacity = random.randint(75, 100)
        potentialStar = Star(starX, starY, starOpacity)
        if potentialStar not in self.allStars:
            return potentialStar
        else:
            return self.generateRandomStar(app)
    def addRandomStarAmount(self, app):
        starAmount = random.randint(1, 2)
        for star in range(starAmount):
            self.allStars.add(self.generateRandomStar(app))
        self.allStars.pop()
        
    def moveStars(self, app):
        for star in self.allStars:
            star.y -= 2
            star.opacity -=1
            if star.opacity <=0:
                self.allStars.remove(star)
                self.allStars.add(self.generateRandomStar(app))
        addStars = random.randint(0, 100)
        if addStars > 90:
            self.addRandomStarAmount(app)
    
    def drawAllStars(self):
        for star in self.allStars:
            star.drawLight()





    
