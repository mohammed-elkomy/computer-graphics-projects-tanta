from random import randrange

import pygame
from OpenGL.GL import *
from numpy import *


class Fuel:
    def __init__(self, texture_name=-1):
        self.fuel_x = []
        self.fuel_z = []
        self.texture_name = texture_name
        pygame.init()
        self.collision_sound = pygame.mixer.Sound("assets/sound/get_fuel.mp3")

    def generate_new_fuel(self, num_of_rail, obstacles_x):
        if num_of_rail == 3:
            factor = 1
        else:
            factor = 2
        rail = randrange(num_of_rail)  # rail={0,1,2}
        while (rail - factor) * 8 == obstacles_x:
            rail = randrange(num_of_rail)
        self.fuel_x.append((rail - factor) * 8)
        self.fuel_z.append(200)

    def draw_old_fuel(self, speed):
        glPushMatrix()
        for i in range(len(self.fuel_x)):
            glPushMatrix()
            glColor3d(1, 1, 0)
            glTranslate(self.fuel_x[i], 0, self.fuel_z[i])
            self.fuel_z[i] -= speed
            glScale(2.5, 3, 0)
            self.draw_fuel()
            glBindTexture(GL_TEXTURE_2D, -1)
            glPopMatrix()
        glPopMatrix()

    def delete_fuel(self, ):
        self.fuel_z.pop(0)
        self.fuel_x.pop(0)

    def draw_fuel(self):
        glBindTexture(GL_TEXTURE_2D, self.texture_name)
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0)
        glVertex(-1, -1)

        glTexCoord2f(1, 0)
        glVertex(1, -1)

        glTexCoord2f(1, 1)
        glVertex(1, 1)

        glTexCoord2f(0, 1)
        glVertex(-1, 1)
        glEnd()

    def fuel_level_bar(self, fuel_level=0.0, state=''):
        if fuel_level <= 0:
            state = 'gameOver'
            gameOver_sound = pygame.mixer.Sound("assets/sound/gameOver.mp3")
            gameOver_sound.play()
            return state
        else:
            glColor3d(1 - fuel_level / 100, fuel_level / 100, 0.0)
            glLoadIdentity()
            glBegin(GL_POLYGON)
            glVertex2d(-0.9, 0.55)
            glVertex2d(-0.9 + (0.55 * fuel_level / 100), 0.55)
            glVertex2d(-0.9 + (0.55 * fuel_level / 100), 0.50)
            glVertex2d(-0.9, 0.50)
            glEnd()
            return state

    def collision_detection(self, space_ship_position, fuel_level, speed):
        if len(self.fuel_x) and self.fuel_z[0] <= speed and abs(
                space_ship_position - self.fuel_x[0]) <= 6:
            self.collision_sound.play()
            self.delete_fuel()
            fuel_level = 100.0
        elif len(self.fuel_x) and self.fuel_z[0] < -6:
            self.delete_fuel()
        return fuel_level
