from random import randrange

import pygame
from OpenGL.GL import *


class Obstacle:
    def __init__(self, texture_name=-1):
        self.obstacle_x = []
        self.obstacle_z = []
        self.counter = 0
        self.texture_name = texture_name
        self.phase = []

    def generate_obstacle(self, num_of_rail, speed):
        self.counter += 1
        if self.counter == 5 and speed <= 4:
            speed += 3 / (7 * speed)
            self.counter = 0

        if num_of_rail == 3:
            factor = 1
        else:
            factor = 2

        rail = randrange(num_of_rail)
        # if state num of rail =3 then obstacle_x is  -8 or 0 or 8 
        # if state num of rail =3 then obstacle_x is -16 or -8 or 0 or 8 or 16 
        self.obstacle_x.append((rail - factor) * 8)
        if num_of_rail == 5:
            rail_2 = randrange(num_of_rail)
            while rail_2 == rail:
                rail_2 = randrange(num_of_rail)
            self.obstacle_x.append((rail_2 - factor) * 8)
            self.obstacle_z.append(200)
            self.phase.append(randrange(360))

        self.phase.append(randrange(360))
        self.obstacle_z.append(200)
        return speed

    def draw_obstacles(self, speed):
        glPushMatrix()
        for i in range(len(self.obstacle_x)):
            glPushMatrix()
            glColor3d(1, 1, 0)
            glTranslate(self.obstacle_x[i], 0, self.obstacle_z[i])
            glRotate(self.phase[i], 1, 0, 1)
            self.obstacle_z[i] -= speed
            glScale(2.5, 2.5, 2.5)
            self.create_obstacle()
            glBindTexture(GL_TEXTURE_2D, -1)
            self.phase[i] += 3
            glPopMatrix()
        glPopMatrix()

    def delete_obstacle(self, n):
        for i in range(n):
            self.obstacle_x.pop(0)
            self.obstacle_z.pop(0)
            self.phase.pop(0)

    def create_obstacle(self):
        # Front Face
        glBindTexture(GL_TEXTURE_2D, self.texture_name)
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(-1.0, -1.0, 1.0)  # Bottom Left

        glTexCoord2f(1.0, 0.0)
        glVertex3f(1.0, -1.0, 1.0)  # Bottom Right

        glTexCoord2f(1.0, 1.0)
        glVertex3f(1.0, 1.0, 1.0)  # Top Right

        glTexCoord2f(0.0, 1.0)
        glVertex3f(-1.0, 1.0, 1.0)  # Top Left
        glEnd()

        # Back Face
        glBindTexture(GL_TEXTURE_2D, self.texture_name)
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(-1.0, -1.0, -1.0)  # Bottom Right
        glTexCoord2f(1.0, 0.0)
        glVertex3f(-1.0, 1.0, -1.0)  # Top Right
        glTexCoord2f(1.0, 1.0)
        glVertex3f(1.0, 1.0, -1.0)  # Top Left
        glTexCoord2f(0.0, 1.0)
        glVertex3f(1.0, -1.0, -1.0)  # Bottom Left
        glEnd()

        # Top Face
        glBindTexture(GL_TEXTURE_2D, self.texture_name)
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(-1.0, 1.0, -1.0)  # Top Left
        glTexCoord2f(1.0, 0.0)
        glVertex3f(-1.0, 1.0, 1.0)  # Bottom Left
        glTexCoord2f(1.0, 1.0)
        glVertex3f(1.0, 1.0, 1.0)  # Bottom Right
        glTexCoord2f(0.0, 1.0)
        glVertex3f(1.0, 1.0, -1.0)  # Top Right
        glEnd()

        # Bottom Face
        glBindTexture(GL_TEXTURE_2D, self.texture_name)
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(-1.0, -1.0, -1.0)  # Top Right
        glTexCoord2f(1.0, 0.0)
        glVertex3f(1.0, -1.0, -1.0)  # Top Left
        glTexCoord2f(1.0, 1.0)
        glVertex3f(1.0, -1.0, 1.0)  # Bottom Left
        glTexCoord2f(0.0, 1.0)
        glVertex3f(-1.0, -1.0, 1.0)  # Bottom Right
        glEnd()

        # Right face
        glBindTexture(GL_TEXTURE_2D, self.texture_name)
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(1.0, -1.0, -1.0)  # Bottom Right
        glTexCoord2f(1.0, 0.0)
        glVertex3f(1.0, 1.0, -1.0)  # Top Right
        glTexCoord2f(1.0, 1.0)
        glVertex3f(1.0, 1.0, 1.0)  # Top Left
        glTexCoord2f(0.0, 1.0)
        glVertex3f(1.0, -1.0, 1.0)  # Bottom Left
        glEnd()

        # Left Face
        glBindTexture(GL_TEXTURE_2D, self.texture_name)
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(-1.0, -1.0, -1.0)  # Bottom Left
        glTexCoord2f(1.0, 0.0)
        glVertex3f(-1.0, -1.0, 1.0)  # Bottom Right
        glTexCoord2f(1.0, 1.0)
        glVertex3f(-1.0, 1.0, 1.0)  # Top Right
        glTexCoord2f(0.0, 1.0)
        glVertex3f(-1.0, 1.0, -1.0)  # Top Left
        glEnd()

    def collision_detection(self, space_ship_position, num_of_heart, speed, state, flash):

        if len(self.obstacle_x) and state == '3' and self.obstacle_z[0] <= speed and abs(
                space_ship_position - self.obstacle_x[0]) <= 6:
            if flash == 0:
                flash = 100
                num_of_heart -= 1
                self.sound_crash(num_of_heart)
                self.delete_obstacle(1)
                print('crash ' * 5 + '\n' + '#' * 50)

        elif len(self.obstacle_x) > 1 and state == '5':
            if self.obstacle_z[0] <= speed and abs(space_ship_position - self.obstacle_x[0]) <= 6 or self.obstacle_z[
                1] <= speed \
                    and abs(space_ship_position - self.obstacle_x[1]) <= 6:
                if flash == 0:
                    flash = 100
                    num_of_heart -= 1
                    self.sound_crash(num_of_heart)
                    if self.obstacle_z[0] == self.obstacle_z[1]:
                        self.delete_obstacle(1)
                    self.delete_obstacle(1)
                    print('crash ' * 15 + '\n' + '#' * 50)

        if len(self.obstacle_x) and self.obstacle_z[0] < -6:
            if state == "5" and self.obstacle_z[1] < -6:
                self.delete_obstacle(2)
            else:
                self.delete_obstacle(1)
        return num_of_heart, flash

    def sound_crash(self, num_of_heart):
        if num_of_heart != 0:
            crash_sound = pygame.mixer.Sound("assets/sound/crash.mp3")
            crash_sound.play()
        else:
            gameOver_sound = pygame.mixer.Sound("assets/sound/gameOver.mp3")
            gameOver_sound.play()
