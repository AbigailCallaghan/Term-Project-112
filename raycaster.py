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
            #slope = abs(count - app.rayAmount//100) + 1
            wallHeight = 32

            lineHeight = (wallHeight / ray.distance) * 415
            startOfDrawing = (app.height / 2) - (lineHeight / 2)
            endOfDrawing = lineHeight
            drawRect(count*app.resilution, startOfDrawing, app.resilution, endOfDrawing, fill = 'navy')

            count +=1
        