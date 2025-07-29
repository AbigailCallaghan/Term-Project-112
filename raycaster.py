from cmu_graphics import * 
import math
from ray import Ray
from course import Course

class Raycaster:
    
    def __init__(self, player, course):
        self.rays = []
        self.player = player
        self.course = course

    def castAllRays(self, app):
        self.rays = []
        rayAngle = self.player.playerAngle - (app.FOV / 2)
       
        for i in range(app.rayAmount):
            
            ray = Ray(rayAngle, self.player, self.course)
            ray.cast(app)
            self.rays.append(ray)
            rayAngle += app.FOV / app.rayAmount

    def drawAllRays(self, app):
        count = 0
        
        for ray in self.rays:
            #ray.drawRays(app)
            slope = 15
            wallHeight = 30

            lineHeight = (wallHeight / ray.distance) * 415
            startOfDrawing = (app.height / 2) - (lineHeight / 2)
            endOfDrawing = lineHeight
            print('end', endOfDrawing, 'start', startOfDrawing, count)
            top = (abs(len(self.rays) - count)/ 100) * slope
            drawRect(count*app.resilution, startOfDrawing - 2*slope, app.resilution, endOfDrawing +2*slope, fill = 'navy')

            count +=1
        