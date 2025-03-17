from OpenGL.GL import *
from coins import *
import pygame


class Monster:
    def __init__(self, x, z, angle):
        self.step = 0.0
        self.forward = False
        self.x = x
        self.z = z
        self.angle = angle

    def head(self):
        glBindTexture(GL_TEXTURE_2D, 4)
        # Front Face
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(-0.5, -0.5, 0.5)  # Bottom Left

        glTexCoord2f(1.0, 0.0)
        glVertex3f(0.5, -0.5, 0.5)  # Bottom Right

        glTexCoord2f(1.0, 1.0)
        glVertex3f(0.5, 0.5, 0.5)  # Top Right

        glTexCoord2f(0.0, 1.0)
        glVertex3f(-0.5, 0.5, 0.5)  # Top Left
        glEnd()
        # Back Face
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(-0.5, -0.5, -0.5)  # Bottom Right

        glTexCoord2f(1.0, 0.0)
        glVertex3f(-0.5, 0.5, -0.5)  # Top Right

        glTexCoord2f(1.0, 1.0)
        glVertex3f(0.5, 0.5, -0.5)  # Top Left

        glTexCoord2f(0.0, 1.0)
        glVertex3f(0.5, -0.5, -0.5)  # Bottom Left
        glEnd()
        # Top Face
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(-0.5, 0.5, -0.5)  # Top Left
        glTexCoord2f(1.0, 0.0)
        glVertex3f(-0.5, 0.5, 0.5)  # Bottom Left

        glTexCoord2f(1.0, 1.0)
        glVertex3f(0.5, 0.5, 0.5)  # Bottom Right

        glTexCoord2f(0.0, 1.0)
        glVertex3f(0.5, 0.5, -0.5)  # Top Right
        glEnd()
        # Bottom Face
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(-0.5, -0.5, -0.5)  # Top Right

        glTexCoord2f(1.0, 0.0)
        glVertex3f(0.5, -0.5, -0.5)  # Top Left

        glTexCoord2f(1.0, 1.0)
        glVertex3f(0.5, -0.5, 0.5)  # Bottom Left

        glTexCoord2f(0.0, 1.0)
        glVertex3f(-0.5, -0.5, 0.5)  # Bottom Right
        glEnd()

        # Right face
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(0.5, -0.5, -0.5)  # Bottom Right

        glTexCoord2f(1.0, 0.0)
        glVertex3f(0.5, 0.5, -0.5)  # Top Right

        glTexCoord2f(1.0, 1.0)
        glVertex3f(0.5, 0.5, 0.5)  # Top Left

        glTexCoord2f(0.0, 1.0)
        glVertex3f(0.5, -0.5, 0.5)  # Bottom Left
        glEnd()
        # Left Face
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(-0.5, -0.5, -0.5)  # Bottom Left

        glTexCoord2f(1.0, 0.0)
        glVertex3f(-0.5, -0.5, 0.5)  # Bottom Right

        glTexCoord2f(1.0, 1.0)
        glVertex3f(-0.5, 0.5, 0.5)  # Top Right

        glTexCoord2f(0.0, 1.0)
        glVertex3f(-0.5, 0.5, -0.5)  # Top Left
        glEnd()

    ###########################################################################################################
    def right_back1(self):
        # # Front Face
        glBegin(GL_QUADS)
        glVertex3f(0.5, -0.05, -0.4)  # Bottom Left
        glVertex3f(1, 0.05, -0.4)  # Bottom Right
        glVertex3f(1, 0.08, -0.4)  # Top Right
        glVertex3f(0.5, 0.05, - 0.4)  # Top Left
        glEnd()
        # # Back Face
        glBegin(GL_QUADS)
        glVertex3f(0.5, -0.05, -0.5)  # Bottom Left
        glVertex3f(1, 0.05, -0.5)  # Bottom Right
        glVertex3f(1, 0.08, -0.5)  # Top Right
        glVertex3f(0.5, 0.05, -0.5)  # Top Left
        glEnd()
        # # Top Face
        glBegin(GL_QUADS)
        glVertex3f(0.5, 0.05, -0.5)  # Top Left
        glVertex3f(0.5, 0.05, -0.4)  # Bottom Left
        glVertex3f(1, 0.08, -0.4)  # Bottom Right
        glVertex3f(1, 0.08, -0.5)  # Top Right
        glEnd()
        # # Bottom Face
        glBegin(GL_QUADS)
        glVertex3f(0.5, -0.05, -0.5)  # Top Left
        glVertex3f(0.5, -0.05, -0.4)  # Bottom Left
        glVertex3f(1, 0.05, -0.4)  # Bottom Right
        glVertex3f(1, 0.05, -0.5)  # Top Right
        glEnd()

        # # Right face
        glBegin(GL_QUADS)
        glVertex3f(1, 0.05, -0.4)  # Bottom Left
        glVertex3f(1, 0.05, -0.5)  # Bottom Right
        glVertex3f(1, 0.08, -0.5)  # Top Right
        glVertex3f(1, 0.08, -0.4)  # Top Left
        glEnd()
        # Left Face
        glBegin(GL_QUADS)
        glVertex3f(0.5, -0.05, -0.4)  # Bottom Left
        glVertex3f(0.5, -0.05, -0.5)  # Bottom Right
        glVertex3f(0.5, 0.05, -0.5)  # Top Right
        glVertex3f(0.5, 0.05, -0.4)  # Top Left
        glEnd()

    ###########################################################################################################
    def right_front1(self):
        # # # Front Face
        glBegin(GL_QUADS)
        glVertex3f(0.5, -0.05, 0.5)  # Bottom Left
        glVertex3f(1, 0.05, 0.5)  # Bottom Right
        glVertex3f(1, 0.08, 0.5)  # Top Right
        glVertex3f(0.5, 0.05, 0.5)  # Top Left
        glEnd()
        # # # Back Face
        glBegin(GL_QUADS)
        glVertex3f(0.5, -0.05, 0.4)  # Bottom Left
        glVertex3f(1, 0.05, 0.4)  # Bottom Right
        glVertex3f(1, 0.08, 0.4)  # Top Right
        glVertex3f(0.5, 0.05, 0.4)  # Top Left
        glEnd()
        # # # Top Face
        glBegin(GL_QUADS)
        glVertex3f(0.5, 0.05, 0.4)  # Top Left
        glVertex3f(0.5, 0.05, 0.5)  # Bottom Left
        glVertex3f(1, 0.08, 0.5)  # Bottom Right
        glVertex3f(1, 0.08, 0.4)  # Top Right
        glEnd()
        # # # Bottom Face
        glBegin(GL_QUADS)
        glVertex3f(0.5, -0.05, 0.4)  # Top Left
        glVertex3f(0.5, -0.05, 0.5)  # Bottom Left
        glVertex3f(1, 0.05, 0.5)  # Bottom Right
        glVertex3f(1, 0.05, 0.4)  # Top Right
        glEnd()

        # # # Right face
        glBegin(GL_QUADS)
        glVertex3f(1, 0.05, 0.5)  # Bottom Left
        glVertex3f(1, 0.05, 0.4)  # Bottom Right
        glVertex3f(1, 0.08, 0.4)  # Top Right
        glVertex3f(1, 0.08, 0.5)  # Top Left
        glEnd()
        # Left Face
        glBegin(GL_QUADS)
        glVertex3f(0.5, -0.05, 0.5)  # Bottom Left
        glVertex3f(0.5, -0.05, 0.4)  # Bottom Right
        glVertex3f(0.5, 0.05, 0.4)  # Top Right
        glVertex3f(0.5, 0.05, 0.5)  # Top Left
        glEnd()

    ###########################################################################################################
    def right_back2(self, step):
        # # Front Face
        glBegin(GL_QUADS)
        glVertex3f(1.5, -0.8, -(0.4 - step))  # Bottom Left
        glVertex3f(1.6, -0.8, -(0.4 - step))  # Bottom Right
        glVertex3f(1.1, 0.05, -0.4)  # Top Right
        glVertex3f(1, 0.05, - 0.4)  # Top Left
        glEnd()
        # # Back Face
        glBegin(GL_QUADS)
        glVertex3f(1.5, -0.8, -(0.5 - step))  # Bottom Left
        glVertex3f(1.6, -0.8, -(0.5 - step))  # Bottom Right
        glVertex3f(1.1, 0.05, -0.5)  # Top Right
        glVertex3f(1, 0.05, -0.5)  # Top Left
        glEnd()
        # # Top Face
        glBegin(GL_QUADS)
        glVertex3f(1, 0.05, -0.5)  # Top Left
        glVertex3f(1, 0.05, -0.4)  # Bottom Left
        glVertex3f(0.7, 0.05, -0.4)  # Bottom Right
        glVertex3f(0.7, 0.05, -0.5)  # Top Right
        glEnd()
        # # Bottom Face
        glBegin(GL_QUADS)
        glVertex3f(1.5, -0.8, -(0.5 - step))  # Top Left
        glVertex3f(1.5, -0.8, -(0.4 - step))  # Bottom Left
        glVertex3f(1.6, -0.8, -(0.4 - step))  # Bottom Right
        glVertex3f(1.6, -0.8, -(0.5 - step))  # Top Right
        glEnd()

        # # Right face
        glBegin(GL_QUADS)
        glVertex3f(1.6, -0.8, -(0.4 - step))  # Bottom Left
        glVertex3f(1.6, -0.8, -(0.5 - step))  # Bottom Right
        glVertex3f(1.1, 0.05, -0.5)  # Top Right
        glVertex3f(1.1, 0.05, -0.4)  # Top Left
        glEnd()
        # Left Face
        glBegin(GL_QUADS)
        glVertex3f(1.5, -0.8, -(0.4 - step))  # Bottom Left
        glVertex3f(1.5, -0.8, -(0.5 - step))  # Bottom Right
        glVertex3f(1, 0.05, -0.5)  # Top Right
        glVertex3f(1, 0.05, -0.4)  # Top Left
        glEnd()

    ###########################################################################################################
    def right_front2(self, step):
        glBegin(GL_QUADS)
        glVertex3f(1.5, -0.8, (0.5 + step))  # Bottom Left
        glVertex3f(1.6, -0.8, (0.5 + step))  # Bottom Right
        glVertex3f(1.1, 0.05, 0.5)  # Top Right
        glVertex3f(1, 0.05, 0.5)  # Top Left
        glEnd()
        # # Back Face
        glBegin(GL_QUADS)
        glVertex3f(1.5, -0.8, (0.4 + step))  # Bottom Left
        glVertex3f(1.6, -0.8, (0.4 + step))  # Bottom Right
        glVertex3f(1.1, 0.05, 0.4)  # Top Right
        glVertex3f(1, 0.05, 0.4)  # Top Left
        glEnd()
        # # Top Face
        glBegin(GL_QUADS)
        glVertex3f(1, 0.05, 0.4)  # Top Left
        glVertex3f(1, 0.05, 0.5)  # Bottom Left
        glVertex3f(0.7, 0.05, 0.5)  # Bottom Right
        glVertex3f(0.7, 0.05, 0.4)  # Top Right
        glEnd()
        # # Bottom Face
        glBegin(GL_QUADS)
        glVertex3f(1.5, -0.8, (0.4 + step))  # Top Left
        glVertex3f(1.5, -0.8, (0.5 + step))  # Bottom Left
        glVertex3f(1.6, -0.8, (0.5 + step))  # Bottom Right
        glVertex3f(1.6, -0.8, (0.4 + step))  # Top Right
        glEnd()

        # # Right face
        glBegin(GL_QUADS)
        glVertex3f(1.6, -0.8, (0.5 + step))  # Bottom Left
        glVertex3f(1.6, -0.8, (0.4 + step))  # Bottom Right
        glVertex3f(1.1, 0.05, 0.4)  # Top Right
        glVertex3f(1.1, 0.05, 0.5)  # Top Left
        glEnd()
        # Left Face
        glBegin(GL_QUADS)
        glVertex3f(1.5, -0.8, (0.5 + step))  # Bottom Left
        glVertex3f(1.5, -0.8, (0.4 + step))  # Bottom Right
        glVertex3f(1, 0.05, 0.4)  # Top Right
        glVertex3f(1, 0.05, 0.5)  # Top Left
        glEnd()

    ############################################################################################################
    def left_back1(self):
        # Front Face
        glBegin(GL_QUADS)
        glVertex3f(-1, 0.08, -0.4)  # Top left
        glVertex3f(-1, 0.05, -0.4)  # Bottom Left
        glVertex3f(-0.5, -0.05, -0.4)  # Bottom Right
        glVertex3f(-0.5, 0.05, -0.4)  # Top Right
        glEnd()
        # # Back Face
        glBegin(GL_QUADS)
        glVertex3f(-1, 0.08, -0.5)  # Top left
        glVertex3f(-1, 0.05, -0.5)  # Bottom Left
        glVertex3f(-0.5, -0.05, -0.5)  # Bottom Right
        glVertex3f(-0.5, 0.05, -0.5)  # Top Right
        glEnd()
        # Top Face
        glBegin(GL_QUADS)
        glVertex3f(-1, 0.08, -0.5)  # Top left
        glVertex3f(-1, 0.08, -0.4)  # Bottom Left
        glVertex3f(-0.5, 0.05, -0.4)  # Bottom Right
        glVertex3f(-0.5, 0.05, -0.5)  # Top Right
        glEnd()
        # # Bottom Face
        glBegin(GL_QUADS)
        glVertex3f(-1, 0.05, -0.5)  # Top left
        glVertex3f(-1, 0.05, -0.4)  # Bottom Left
        glVertex3f(-0.5, -0.05, -0.4)  # Bottom Right
        glVertex3f(-0.5, -0.05, -0.5)  # Top Right
        glEnd()
        # Right face
        glBegin(GL_QUADS)
        glVertex3f(-0.5, 0.05, -0.4)  # Top left
        glVertex3f(-0.5, -0.05, -0.4)  # Bottom Left
        glVertex3f(-0.5, -0.05, -0.5)  # Bottom Right
        glVertex3f(-0.5, 0.05, -0.5)  # Top Right
        glEnd()
        # Left Face
        glBegin(GL_QUADS)
        glVertex3f(-1, 0.08, -0.4)  # Top left
        glVertex3f(-1, 0.05, -0.5)  # Bottom Left
        glVertex3f(-1, 0.05, -0.5)  # Bottom Right
        glVertex3f(-1, 0.08, -0.4)  # Top Right
        glEnd()

    ###########################################################################################################
    def left_front1(self):
        # Front Face
        glBegin(GL_QUADS)
        glVertex3f(-1, 0.08, 0.5)  # Top left
        glVertex3f(-1, 0.05, 0.5)  # Bottom Left
        glVertex3f(-0.5, -0.05, 0.5)  # Bottom Right
        glVertex3f(-0.5, 0.05, 0.5)  # Top Right
        glEnd()
        # # Back Face
        glBegin(GL_QUADS)
        glVertex3f(-1, 0.08, 0.4)  # Top left
        glVertex3f(-1, 0.05, 0.4)  # Bottom Left
        glVertex3f(-0.5, -0.05, 0.4)  # Bottom Right
        glVertex3f(-0.5, 0.05, 0.4)  # Top Right
        glEnd()
        # Top Face
        glBegin(GL_QUADS)
        glVertex3f(-1, 0.08, 0.4)  # Top left
        glVertex3f(-1, 0.08, 0.5)  # Bottom Left
        glVertex3f(-0.5, 0.05, 0.5)  # Bottom Right
        glVertex3f(-0.5, 0.05, 0.4)  # Top Right
        glEnd()
        # # Bottom Face
        glBegin(GL_QUADS)
        glVertex3f(-1, 0.05, 0.4)  # Top left
        glVertex3f(-1, 0.05, 0.5)  # Bottom Left
        glVertex3f(-0.5, -0.05, 0.5)  # Bottom Right
        glVertex3f(-0.5, -0.05, 0.4)  # Top Right
        glEnd()
        # Right face
        glBegin(GL_QUADS)
        glVertex3f(-0.5, 0.05, 0.5)  # Top left
        glVertex3f(-0.5, -0.05, 0.5)  # Bottom Left
        glVertex3f(-0.5, -0.05, 0.4)  # Bottom Right
        glVertex3f(-0.5, 0.05, 0.4)  # Top Right
        glEnd()
        # Left Face
        glBegin(GL_QUADS)
        glVertex3f(-1, 0.08, 0.5)  # Top left
        glVertex3f(-1, 0.05, 0.4)  # Bottom Left
        glVertex3f(-1, 0.05, 0.4)  # Bottom Right
        glVertex3f(-1, 0.08, 0.5)  # Top Right
        glEnd()

    ###########################################################################################################
    def left_back2(self, step):
        glBegin(GL_QUADS)
        glVertex3f(-1.5, -0.8, -(0.4 + step))  # Bottom Left
        glVertex3f(-1.6, -0.8, -(0.4 + step))  # Bottom Right
        glVertex3f(-1.1, 0.05, -0.4)  # Top Right
        glVertex3f(-1, 0.05, - 0.4)  # Top Left
        glEnd()
        # # Back Face
        glBegin(GL_QUADS)
        glVertex3f(-1.5, -0.8, -(0.5 + step))  # Bottom Left
        glVertex3f(-1.6, -0.8, -(0.5 + step))  # Bottom Right
        glVertex3f(-1.1, 0.05, -0.5)  # Top Right
        glVertex3f(-1, 0.05, -0.5)  # Top Left
        glEnd()
        # # Top Face
        glBegin(GL_QUADS)
        glVertex3f(-1, 0.05, -0.5)  # Top Left
        glVertex3f(-1, 0.05, -0.4)  # Bottom Left
        glVertex3f(-0.7, 0.05, -0.4)  # Bottom Right
        glVertex3f(-0.7, 0.05, -0.5)  # Top Right
        glEnd()
        # # Bottom Face
        glBegin(GL_QUADS)
        glVertex3f(-1.5, -0.8, -(0.5 + step))  # Top Left
        glVertex3f(-1.5, -0.8, -(0.4 + step))  # Bottom Left
        glVertex3f(-1.6, -0.8, -(0.4 + step))  # Bottom Right
        glVertex3f(-1.6, -0.8, -(0.5 + step))  # Top Right
        glEnd()
        # # Right face
        glBegin(GL_QUADS)
        glVertex3f(-1.6, -0.8, -(0.4 + step))  # Bottom Left
        glVertex3f(-1.6, -0.8, -(0.5 + step))  # Bottom Right
        glVertex3f(-1.1, 0.05, -0.5)  # Top Right
        glVertex3f(-1.1, 0.05, -0.4)  # Top Left
        glEnd()
        # Left Face
        glBegin(GL_QUADS)
        glVertex3f(-1.5, -0.8, -(0.4 + step))  # Bottom Left
        glVertex3f(-1.5, -0.8, -(0.5 + step))  # Bottom Right
        glVertex3f(-1, 0.05, -0.5)  # Top Right
        glVertex3f(-1, 0.05, -0.4)  # Top Left
        glEnd()

    ###########################################################################################################
    def left_front2(self, step):
        glBegin(GL_QUADS)
        glVertex3f(-1.5, -0.8, (0.5 - step))  # Bottom Left
        glVertex3f(-1.6, -0.8, (0.5 - step))  # Bottom Right
        glVertex3f(-1.1, 0.05, 0.5)  # Top Right
        glVertex3f(-1, 0.05, 0.5)  # Top Left
        glEnd()
        # # Back Face
        glBegin(GL_QUADS)
        glVertex3f(-1.5, -0.8, (0.4 - step))  # Bottom Left
        glVertex3f(-1.6, -0.8, (0.4 - step))  # Bottom Right
        glVertex3f(-1.1, 0.05, 0.4)  # Top Right
        glVertex3f(-1, 0.05, 0.4)  # Top Left
        glEnd()
        # # Top Face
        glBegin(GL_QUADS)
        glVertex3f(-1, 0.05, 0.4)  # Top Left
        glVertex3f(-1, 0.05, 0.5)  # Bottom Left
        glVertex3f(-0.7, 0.05, 0.5)  # Bottom Right
        glVertex3f(-0.7, 0.05, 0.4)  # Top Right
        glEnd()
        # # Bottom Face
        glBegin(GL_QUADS)
        glVertex3f(-1.5, -0.8, (0.4 - step))  # Top Left
        glVertex3f(-1.5, -0.8, (0.5 - step))  # Bottom Left
        glVertex3f(-1.6, -0.8, (0.5 - step))  # Bottom Right
        glVertex3f(-1.6, -0.8, (0.4 - step))  # Top Right
        glEnd()
        # # Right face
        glBegin(GL_QUADS)
        glVertex3f(-1.6, -0.8, (0.5 - step))  # Bottom Left
        glVertex3f(-1.6, -0.8, (0.4 - step))  # Bottom Right
        glVertex3f(-1.1, 0.05, 0.4)  # Top Right
        glVertex3f(-1.1, 0.05, 0.5)  # Top Left
        glEnd()
        # Left Face
        glBegin(GL_QUADS)
        glVertex3f(-1.5, -0.8, (0.5 - step))  # Bottom Left
        glVertex3f(-1.5, -0.8, (0.4 - step))  # Bottom Right
        glVertex3f(-1, 0.05, 0.4)  # Top Right
        glVertex3f(-1, 0.05, 0.5)  # Top Left
        glEnd()

    ####################################################################################################
    def right_middle1(self):
        # Front Face
        glBegin(GL_QUADS)
        glVertex3f(0.5, -0.05, 0.05)  # Bottom Left
        glVertex3f(1, 0.05, 0.05)  # Bottom Right
        glVertex3f(1, 0.08, 0.05)  # Top Right
        glVertex3f(0.5, 0.05, 0.05)  # Top Left
        glEnd()
        # # Back Face
        glBegin(GL_QUADS)
        glVertex3f(0.5, -0.05, -0.05)  # Bottom Left
        glVertex3f(1, 0.05, -0.05)  # Bottom Right
        glVertex3f(1, 0.08, -0.05)  # Top Right
        glVertex3f(0.5, 0.05, -0.05)  # Top Left
        glEnd()
        # # Top Face
        glBegin(GL_QUADS)
        glVertex3f(0.5, 0.05, -0.05)  # Top Left
        glVertex3f(0.5, 0.05, 0.05)  # Bottom Left
        glVertex3f(1, 0.08, 0.05)  # Bottom Right
        glVertex3f(1, 0.08, -0.05)  # Top Right
        glEnd()
        # # Bottom Face
        glBegin(GL_QUADS)
        glVertex3f(0.5, -0.05, -0.05)  # Top Left
        glVertex3f(0.5, -0.05, 0.05)  # Bottom Left
        glVertex3f(1, 0.05, 0.05)  # Bottom Right
        glVertex3f(1, 0.05, -0.05)  # Top Right
        glEnd()
        # # Right face
        glBegin(GL_QUADS)
        glVertex3f(1, 0.05, 0.05)  # Bottom Left
        glVertex3f(1, 0.05, -0.05)  # Bottom Right
        glVertex3f(1, 0.08, -0.05)  # Top Right
        glVertex3f(1, 0.08, 0.05)  # Top Left
        glEnd()
        # Left Face
        glBegin(GL_QUADS)
        glVertex3f(0.5, -0.05, 0.05)  # Bottom Left
        glVertex3f(0.5, -0.05, -0.05)  # Bottom Right
        glVertex3f(0.5, 0.05, -0.05)  # Top Right
        glVertex3f(0.5, 0.05, 0.05)  # Top Left
        glEnd()

    ####################################################################################################
    def right_middle2(self, step):
        # # Front Face
        glBegin(GL_QUADS)
        glVertex3f(1.5, -0.8, (0.05 - step))  # Bottom Left
        glVertex3f(1.6, -0.8, (0.05 - step))  # Bottom Right
        glVertex3f(1.1, 0.05, 0.05)  # Top Right
        glVertex3f(1, 0.05, 0.05)  # Top Left
        glEnd()
        # # Back Face
        glBegin(GL_QUADS)
        glVertex3f(1.5, -0.8, -(0.05 + step))  # Bottom Left
        glVertex3f(1.6, -0.8, -(0.05 + step))  # Bottom Right
        glVertex3f(1.1, 0.05, -0.05)  # Top Right
        glVertex3f(1, 0.05, -0.05)  # Top Left
        glEnd()
        # # Top Face
        glBegin(GL_QUADS)
        glVertex3f(1, 0.05, -0.05)  # Top Left
        glVertex3f(1, 0.05, 0.05)  # Bottom Left
        glVertex3f(0.7, 0.05, 0.05)  # Bottom Right
        glVertex3f(0.7, 0.05, -0.05)  # Top Right
        glEnd()
        # # Bottom Face
        glBegin(GL_QUADS)
        glVertex3f(1.5, -0.8, -(0.05 + step))  # Top Left
        glVertex3f(1.5, -0.8, (0.05 - step))  # Bottom Left
        glVertex3f(1.6, -0.8, (0.05 - step))  # Bottom Right
        glVertex3f(1.6, -0.8, -(0.05 + step))  # Top Right
        glEnd()

        # # Right face
        glBegin(GL_QUADS)
        glVertex3f(1.6, -0.8, (0.05 - step))  # Bottom Left
        glVertex3f(1.6, -0.8, -(0.05 + step))  # Bottom Right
        glVertex3f(1.1, 0.05, -0.05)  # Top Right
        glVertex3f(1.1, 0.05, 0.05)  # Top Left
        glEnd()
        # Left Face
        glBegin(GL_QUADS)
        glVertex3f(1.5, -0.8, (0.05 - step))  # Bottom Left
        glVertex3f(1.5, -0.8, -(0.05 + step))  # Bottom Right
        glVertex3f(1, 0.05, -0.05)  # Top Right
        glVertex3f(1, 0.05, 0.05)  # Top Left
        glEnd()

    ####################################################################################################
    def left_middle1(self):
        # Front Face
        glBegin(GL_QUADS)
        glVertex3f(-1, 0.08, 0.05)  # Top left
        glVertex3f(-1, 0.05, 0.05)  # Bottom Left
        glVertex3f(-0.5, -0.05, 0.05)  # Bottom Right
        glVertex3f(-0.5, 0.05, 0.05)  # Top Right
        glEnd()
        # # Back Face
        glBegin(GL_QUADS)
        glVertex3f(-1, 0.08, -0.05)  # Top left
        glVertex3f(-1, 0.05, -0.05)  # Bottom Left
        glVertex3f(-0.5, -0.05, -0.05)  # Bottom Right
        glVertex3f(-0.5, 0.05, -0.05)  # Top Right
        glEnd()

        # Top Face
        glBegin(GL_QUADS)
        glVertex3f(-1, 0.08, -0.05)  # Top left
        glVertex3f(-1, 0.08, 0.05)  # Bottom Left
        glVertex3f(-0.5, 0.05, 0.05)  # Bottom Right
        glVertex3f(-0.5, 0.05, -0.05)  # Top Right
        glEnd()

        # # Bottom Face
        glBegin(GL_QUADS)
        glVertex3f(-1, 0.05, -0.05)  # Top left
        glVertex3f(-1, 0.05, 0.05)  # Bottom Left
        glVertex3f(-0.5, -0.05, 0.05)  # Bottom Right
        glVertex3f(-0.5, -0.05, -0.05)  # Top Right
        glEnd()

        # Right face
        glBegin(GL_QUADS)
        glVertex3f(-0.5, 0.05, 0.05)  # Top left
        glVertex3f(-0.5, -0.05, 0.05)  # Bottom Left
        glVertex3f(-0.5, -0.05, -0.05)  # Bottom Right
        glVertex3f(-0.5, 0.05, -0.05)  # Top Right
        glEnd()

        # Left Face
        glBegin(GL_QUADS)
        glVertex3f(-1, 0.08, 0.05)  # Top left
        glVertex3f(-1, 0.05, -0.05)  # Bottom Left
        glVertex3f(-1, 0.05, -0.05)  # Bottom Right
        glVertex3f(-1, 0.08, 0.05)  # Top Right
        glEnd()

    ####################################################################################################
    def left_middle2(self, step):
        glBegin(GL_QUADS)
        glVertex3f(-1.5, -0.8, (0.05 + step))  # Bottom Left
        glVertex3f(-1.6, -0.8, (0.05 + step))  # Bottom Right
        glVertex3f(-1.1, 0.05, 0.05)  # Top Right
        glVertex3f(-1, 0.05, 0.05)  # Top Left
        glEnd()
        # # Back Face
        glBegin(GL_QUADS)
        glVertex3f(-1.5, -0.8, -(0.05 - step))  # Bottom Left
        glVertex3f(-1.6, -0.8, -(0.05 - step))  # Bottom Right
        glVertex3f(-1.1, 0.05, -0.05)  # Top Right
        glVertex3f(-1, 0.05, -0.05)  # Top Left
        glEnd()
        # # Top Face
        glBegin(GL_QUADS)
        glVertex3f(-1, 0.05, -0.05)  # Top Left
        glVertex3f(-1, 0.05, 0.05)  # Bottom Left
        glVertex3f(-0.7, 0.05, 0.05)  # Bottom Right
        glVertex3f(-0.7, 0.05, -0.05)  # Top Right
        glEnd()
        # # Bottom Face
        glBegin(GL_QUADS)
        glVertex3f(-1.5, -0.8, -(0.05 - step))  # Top Left
        glVertex3f(-1.5, -0.8, (0.05 + step))  # Bottom Left
        glVertex3f(-1.6, -0.8, (0.05 + step))  # Bottom Right
        glVertex3f(-1.6, -0.8, -(0.05 - step))  # Top Right
        glEnd()
        # # Right face
        glBegin(GL_QUADS)
        glVertex3f(-1.6, -0.8, (0.05 + step))  # Bottom Left
        glVertex3f(-1.6, -0.8, -(0.05 - step))  # Bottom Right
        glVertex3f(-1.1, 0.05, -0.05)  # Top Right
        glVertex3f(-1.1, 0.05, 0.05)  # Top Left
        glEnd()
        # Left Face
        glBegin(GL_QUADS)
        glVertex3f(-1.5, -0.8, (0.05 + step))  # Bottom Left
        glVertex3f(-1.5, -0.8, -(0.05 - step))  # Bottom Right
        glVertex3f(-1, 0.05, -0.05)  # Top Right
        glVertex3f(-1, 0.05, 0.05)  # Top Left
        glEnd()
    ####################################################################################################

    def set_monster(self):
        glPushMatrix()
        glTranslate(self.x, -0.5, self.z)  # set monster
        glScale(0.5, 0.5, 0.5)
        glRotate(self.angle, 0, 1, 0)
        self.head()
        self.right_back1()
        self.right_front1()
        self.left_back1()
        self.left_front1()
        self.right_middle1()
        self.left_middle1()
        self.right_back2(self.step)
        self.right_front2(self.step)
        self.left_back2(self.step)
        self.left_front2(self.step)
        self.right_middle2(self.step)
        self.left_middle2(self.step)
        glPopMatrix()
        self.step = self.step + (0.02 if self.forward else -.02)

        if self.step >= 0.12:
            self.forward = False
        if self.step <= -0.12:
            self.forward = True
    ####################################################################################################
    def collission_1(self, cam):
        global coins_result
        if cam.camera_pos[0] + 0.6 > self.x and cam.camera_pos[0] - 0.6 < self.x:
            if cam.camera_pos[2] + 0.6 > self.z and cam.camera_pos[2] - 0.6 < self.z:
                return True
