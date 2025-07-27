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
        for ray in self.rays:
            ray.drawRays(app)