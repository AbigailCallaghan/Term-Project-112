from cmu_graphics import * 
import math
from ray import Ray
from course import Course
#the raycaster class was also inspired by the ray casting tutorial tutorial https://www.youtube.com/watch?v=E18bSJezaUE 


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
            slope = 15
            wallHeight = 100
            url = 'https://piskel-imgstore-b.appspot.com/img/c6646700-6c9b-11f0-b29a-6f0689713f11.gif'

            #for slopes need to apply based off of numrays
            lineHeight = (wallHeight / ray.distance) * 415
            startOfDrawing = (app.height / 2) - (lineHeight / 2)
            endOfDrawing = lineHeight
            top = .1*count
            if app.drawMap == True:
                ray.drawRays(app)
            
            else:
               #drawImage(url, count*app.resilution, startOfDrawing, width = app.resilution, height =endOfDrawing)
                drawRect(count*app.resilution, startOfDrawing - 20, app.resilution, endOfDrawing, fill = rgb(ray.color, ray.color, ray.color))
            count +=1
        