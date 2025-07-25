from cmu_graphics import * 
import math
from ray import Ray

class Raycaster:
    
    def __init__(self, player):
        self.rays = []
        self.player = player

    def castAllRays(self, app):
        self.rays = []
        rayAngle = self.player.playerAngle - (app.FOV / 2)
        print(rayAngle)
        for i in range(app.rayAmount):
            ray = Ray(rayAngle, self.player)
            ray.cast(app)
            self.rays.append(ray)
            rayAngle += app.FOV / app.rayAmount

    def drawAllRays(self, app):
        for ray in self.rays:
            ray.drawRays(app)