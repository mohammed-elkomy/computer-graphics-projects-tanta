from random import randrange

import pygame
from OpenGL.GL import *
from numpy import *


class Heart:
    def __init__(self,texture_name=-1):
        self.heart_x = []
        self.heart_z = []
        self.texture_name = texture_name
        pygame.init()
        self.collision_sound = pygame.mixer.Sound("assets/sound/get_heart.wav")
    def generate_new_heart(self, num_of_rail, obstacles_x, fuel_x):

        if num_of_rail == 3:
            factor = 1
        else:
            factor = 2

        rail = randrange(num_of_rail)  # rail={0,1,2}
        while (rail - factor) * 8 == obstacles_x or (len(fuel_x) and (rail - factor) * 8 == fuel_x[0]):
            rail = randrange(num_of_rail)
        self.heart_x.append((rail - factor) * 8)

        self.heart_z.append(200)

    def draw_old_heart(self, speed):
        glPushMatrix()
        for i in range(len(self.heart_x)):
            glPushMatrix()
            glColor3d(1, 1, 0)
            glTranslate(self.heart_x[i], 0, self.heart_z[i])
            self.heart_z[i] -= speed
            glScale(4, 3.5, 0)
            self.heart_draw()
            glBindTexture(GL_TEXTURE_2D, -1)
            glPopMatrix()
        glPopMatrix()

    def delete_heart(self):
        self.heart_x.pop(0)
        self.heart_z.pop(0)

    def heart_draw(self):
        glBindTexture(GL_TEXTURE_2D, self.texture_name)
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0)
        glVertex(-.6, -.6)

        glTexCoord2f(1, 0)
        glVertex(.6, -0.6)

        glTexCoord2f(1, 1)
        glVertex(0.6, 0.6)

        glTexCoord2f(0, 1)
        glVertex(-.6, .6)
        glEnd()

    def collision_detection(self, space_ship_position, num_of_heart, speed):
        if len(self.heart_x) and self.heart_z[0] <= speed and abs(
                space_ship_position - self.heart_x[0]) <= 6:
            if num_of_heart < 3:
                num_of_heart += 1
            self.collision_sound.play()
            self.delete_heart()
            return num_of_heart
        if len(self.heart_x) and self.heart_z[0] < -6:
            self.delete_heart()
        return num_of_heart
