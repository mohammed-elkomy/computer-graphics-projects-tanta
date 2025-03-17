from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
import pygame


def player(cam):
    glPushMatrix()
    glTranslate(cam.camera_pos[0], -0.4, cam.camera_pos[2])
    glRotate(cam.angle, 0, 1, 0)
    glScale(0.1, 0.1, 0.1)

    glBindTexture(GL_TEXTURE_2D, 5)


    glBegin(GL_QUADS)
    # Front Face
    glColor3f(1.0, 1.0, 1.0)  
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-1, 2, 0.5) # Bottom Left Of The Texture and Quad
    
    glTexCoord2f(1.0, 0.0)
    glVertex3f(1, 2, 0.5)  # Bottom Right Of The Texture and Quad
    
    glTexCoord2f(1.0, 1.0)
    glVertex3f(1, 4, 0.5)  # Top Right Of The Texture and Quad
    
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-1, 4, 0.5)  # Top Left Of The Texture and Quad
    glEnd()

    glBindTexture(GL_TEXTURE_2D, 6)

    glBegin(GL_QUADS)
    # Back Face
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-1, 2, -0.5)  # Bottom Right Of The Texture and Quad
    
    glTexCoord2f(1.0, 0.0)
    glVertex3f(-1, 4, -0.5)  # Top Right Of The Texture and Quad
    
    glTexCoord2f(1.0, 1.0)
    glVertex3f(1, 4, -0.5)  # Top Left Of The Texture and Quad
    
    glTexCoord2f(0.0, 1.0)
    glVertex3f(1, 2, -0.5)  # Bottom Left Of The Texture and Quad
    glEnd()

    glBegin(GL_QUADS)
    # Top Face
    glVertex3f(-1, 4, -0.5)  # Top Left Of The Texture and Quad
    glVertex3f(-1, 4, 0.5)  # Bottom Left Of The Texture and Quad
    glVertex3f(1, 4, 0.5)  # Bottom Right Of The Texture and Quad
    glVertex3f(1, 4, -0.5)  # Top Right Of The Texture and Quad

    # Bottom Face
    glVertex3f(-1, 2, -0.5)  # Top Right Of The Texture and Quad
    glVertex3f(1, 2, -0.5)  # Top Left Of The Texture and Quad
    glVertex3f(1, 2, 0.5)  # Bottom Left Of The Texture and Quad
    glVertex3f(-1, 2, 0.5)  # Bottom Right Of The Texture and Quad
    glEnd()
    glBindTexture(GL_TEXTURE_2D, 7)
    
    glBegin(GL_QUADS)
    # Right face
    glTexCoord2f(0.0, 0.0)
    glVertex3f(1, 2, -0.5)  # Bottom Right Of The Texture and Quad
    
    glTexCoord2f(1.0, 0.0)
    glVertex3f(1, 2, 0.5)  # Top Right Of The Texture and Quad
    
    glTexCoord2f(1.0, 1.0)
    glVertex3f(1, 4, 0.5)  # Top Left Of The Texture and Quad
    
    glTexCoord2f(0.0, 1.0)
    glVertex3f(1, 4, -0.5)  # Bottom Left Of The Texture and Quad
    glEnd()
    glBindTexture(GL_TEXTURE_2D, 8)
    
    glBegin(GL_QUADS)
    # Left Face
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-1, 2, -0.5)  # Bottom Left Of The Texture and Quad
    
    glTexCoord2f(1.0, 0.0)
    glVertex3f(-1, 2, 0.5)  # Bottom Right Of The Texture and Quad
    
    glTexCoord2f(1.0, 1.0)
    glVertex3f(-1, 4, 0.5)  # Top Right Of The Texture and Quad
    
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-1, 4, -0.5)  # Top Left Of The Texture and Quad
    glEnd()


    ##############################################################################body
    glBindTexture(GL_TEXTURE_2D, 9)
    glBegin(GL_QUADS)
    # Front body
    glTexCoord2f(0.25, 0.0)
    glVertex3f(-1, -2, 0.5)  # Bottom Left Of The Texture and Quad
    
    glTexCoord2f(0.75, 0.0)
    glVertex3f(1, -2, 0.5)  # Bottom Right Of The Texture and Quad
    
    glTexCoord2f(0.75, 1.0)
    glVertex3f(1, 2, 0.5)  # Top Right Of The Texture and Quad
    
    glTexCoord2f(0.25, 1.0)
    glVertex3f(-1, 2, 0.5)  # Top Left Of The Texture and Quad
    glEnd()
    glBindTexture(GL_TEXTURE_2D, 10)
    
    # Back body
    glBegin(GL_QUADS)
    glTexCoord2f(0.25, 0.0)
    glVertex3f(-1, -2, -0.5)  # Bottom Right Of The Texture and Quad
    
    glTexCoord2f(0.75, 0.0)
    glVertex3f(1, -2, -0.5)  # Top Right Of The Texture and Quad
    
    glTexCoord2f(0.75, 1.0)
    glVertex3f(1, 2, -0.5)  # Top Left Of The Texture and Quad
    
    glTexCoord2f(0.25, 1.0)
    glVertex3f(-1, 2, -0.5)  # Bottom Left Of The Texture and Quad
    glEnd()
    # Top body
    glBegin(GL_QUADS)
    glVertex3f(-1, 2, -0.5)  # Top Left Of The Texture and Quad
    glVertex3f(-1, 2, 0.5)  # Bottom Left Of The Texture and Quad
    glVertex3f(1, 2, 0.5)  # Bottom Right Of The Texture and Quad
    glVertex3f(1, 2, -0.5)  # Top Right Of The Texture and Quad
    glEnd()

    # Bottom body
    glBegin(GL_QUADS) 
    glVertex3f(-1, -2, -0.5)  # Top Right Of The Texture and Quad
    glVertex3f(1, -2, -0.5)  # Top Left Of The Texture and Quad
    glVertex3f(1, -2, 0.5)  # Bottom Left Of The Texture and Quad
    glVertex3f(-1, -2, 0.5)  # Bottom Right Of The Texture and Quad
    glEnd()

    glBindTexture(GL_TEXTURE_2D, 11)
    # Right body
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(1, -2, 0.5)  # Bottom Right Of The Texture and Quad
    
    glTexCoord2f(1.0, 0.0)
    glVertex3f(1, -2, -0.5)  # Top Right Of The Texture and Quad
    
    glTexCoord2f(1.0, 1.0)
    glVertex3f(1, 2, -0.5)  # Top Left Of The Texture and Quad
    
    glTexCoord2f(0.0, 1.0)
    glVertex3f(1, 2, 0.5)  # Bottom Left Of The Texture and Quad
    glEnd()

    glBindTexture(GL_TEXTURE_2D, 12)
    # Left body
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-1, -2, -0.5)  # Bottom Left Of The Texture and Quad
    
    glTexCoord2f(1.0, 0.0)
    glVertex3f(-1, -2, 0.5)  # Bottom Right Of The Texture and Quad
    
    glTexCoord2f(1.0, 1.0)
    glVertex3f(-1, 2, 0.5)  # Top Right Of The Texture and Quad
    
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-1, 2, -0.5)  # Top Left Of The Texture and Quad
    glEnd()

    glBindTexture(GL_TEXTURE_2D, 13)
    # Front body
    ##############right leg
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(0, -5, (0.5 - cam.step))  # Bottom Left Of The Texture and Quad
    
    glTexCoord2f(1.0, 0.0)
    glVertex3f(1, -5, (0.5 - cam.step))  # Bottom Right Of The Texture and Quad
    
    glTexCoord2f(1.0, 1.0)
    glVertex3f(1, -2, 0.5)  # Top Right Of The Texture and Quad
    
    glTexCoord2f(0.0, 1.0)
    glVertex3f(0, -2, 0.5)  # Top Left Of The Texture and Quad
    glEnd()

    glBindTexture(GL_TEXTURE_2D, 14)
    # Back body
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(0, -5, -(0.5 - cam.step))  # Bottom Right Of The Texture and Quad
    
    glTexCoord2f(1.0, 0.0)
    glVertex3f(1, -5, -(0.5 - cam.step))  # Top Right Of The Texture and Quad
    
    glTexCoord2f(1.0, 1.0)
    glVertex3f(1, -2, -0.5)  # Top Left Of The Texture and Quad
    
    glTexCoord2f(0.0, 1.0)
    glVertex3f(0, -2, -0.5)  # Bottom Left Of The Texture and Quad
    glEnd()

    glBindTexture(GL_TEXTURE_2D, 15)
    
    # Top leg
    glBegin(GL_QUADS)
    glVertex(0, -2, 0.5)
    glVertex(1, -2, 0.5)
    glVertex(1, -2, -0.5)
    glVertex(0, -2, -0.5)
    glEnd()
    
    # button leg
    glBegin(GL_QUADS)
    glVertex(0, -5, (0.5 - cam.step))
    glVertex(1, -5, (0.5 - cam.step))
    glVertex(1, -5, -(0.5 - cam.step))
    glVertex(0, -5, -(0.5 - cam.step))
    glEnd()

    glBindTexture(GL_TEXTURE_2D, 15)
    
    # right leg
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex(1, -5, (0.5 - cam.step))
    
    glTexCoord2f(1.0, 0.0)
    glVertex(1, -5, -(0.5 - cam.step))
    
    glTexCoord2f(1.0, 1.0)
    glVertex(1, -2, -0.5)
    
    glTexCoord2f(0.0, 1.0)
    glVertex(1, -2, 0.5)
    glEnd()
    
    # left leg
    glBegin(GL_QUADS)
    glTexCoord2f(1.0, 0.0)
    glVertex(0, -5, (0.5 - cam.step))
    
    glTexCoord2f(0.0, 0.0)
    glVertex(0, -5, -(0.5 - cam.step))
    
    glTexCoord2f(0.0, 1.0)
    glVertex(0, -2, -0.5)
    
    glTexCoord2f(1.0, 1.0)
    glVertex(0, -2, 0.5)

    glEnd()

    #####################left leg
    #########
    # rihgt side
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 1.0)
    glVertex(0, -2, 0.5)
    glTexCoord2f(1.0, 1.0)
    glVertex(0, -2, -0.5)
    glTexCoord2f(1.0, 0.0)
    glVertex(0, -5, -(0.5 + cam.step))
    glTexCoord2f(0.0, 0.0)
    glVertex(0, -5, (0.5 + cam.step))
    glEnd()
    glBindTexture(GL_TEXTURE_2D, 16)
    # left side
    glBegin(GL_QUADS)
    glTexCoord2f(1.0, 1.0)
    glVertex(-1, -2, 0.5)
    glTexCoord2f(0.0, 1.0)
    glVertex(-1, -2, -0.5)
    glTexCoord2f(0.0, 0.0)
    glVertex(-1, -5, -(0.5 + cam.step))
    glTexCoord2f(1.0, 0.0)
    glVertex(-1, -5, (0.5 + cam.step))
    glEnd()
    
    # top
    glBegin(GL_QUADS)
    glVertex(-1, -2, 0.5)
    glVertex(-1, -2, -0.5)
    glVertex(0, -2, -0.5)
    glVertex(0, -2, 0.5)
    # button
    glVertex(-1, -5, (0.5 + cam.step))
    glVertex(-1, -5, (-0.5 + cam.step))
    glVertex(0, -5, -(0.5 + cam.step))
    glVertex(0, -5, (0.5 + cam.step))
    glEnd()

    glBindTexture(GL_TEXTURE_2D, 13)
    # front
    glBegin(GL_QUADS)
    glTexCoord2f(1.0, 1.0)
    glVertex(-1, -2, 0.5)
    glTexCoord2f(0.0, 1.0)
    glVertex(0, -2, 0.5)
    glTexCoord2f(0.0, 0.0)
    glVertex(0, -5, (0.5 + cam.step))
    glTexCoord2f(1.0, 0.0)
    glVertex(-1, -5, (0.5 + cam.step))
    glEnd()

    glBindTexture(GL_TEXTURE_2D, 14)
    
    # back
    glBegin(GL_QUADS)
    glTexCoord2f(1.0, 1.0)
    glVertex(-1, -2, -0.5)
    glTexCoord2f(0.0, 1.0)
    glVertex(0, -2, -0.5)
    glTexCoord2f(0.0, 0.0)
    glVertex(0, -5, -(0.5 + cam.step))
    glTexCoord2f(1.0, 0.0)
    glVertex(-1, -5, -(0.5 + cam.step))
    glEnd()
    ###############################################################################right hand
    glBindTexture(GL_TEXTURE_2D, 11)
    # rihgt side
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex(1.5, -1.75, (0.5 + cam.step))
    glTexCoord2f(1.0, 0.0)
    glVertex(1.5, -1.75, -(0.5 + cam.step))
    glTexCoord2f(1.0, 1.0)
    glVertex(1.5, 1.9, -0.5)
    glTexCoord2f(0.0, 1.0)
    glVertex(1.5, 1.9, 0.5)
    glEnd()

    #########top left of right hand
    glBegin(GL_QUADS)
    glVertex(1, 1.9, 0.5)
    glVertex(1, 1.9, -0.5)
    glVertex(1.25, 2, -0.5)
    glVertex(1.25, 2, 0.5)
    glEnd()

    #### top right of left hand
    glBegin(GL_QUADS)
    glVertex(1.25, 2, 0.5)
    glVertex(1.25, 2, -0.5)
    glVertex(1.5, 1.9, -0.5)
    glVertex(1.5, 1.9, 0.5)
    glEnd()

    # button left for left  hand
    glBegin(GL_POLYGON)
    glVertex(1.25, -2, (0.5 + cam.step))
    glVertex(1.25, -2, -(0.5 + cam.step))
    glVertex(1.4, -1.9, -(0.5 + cam.step))
    glVertex(1.5, -1.75, -(0.5 + cam.step))
    glVertex(1.5, -1.75, (0.5 + cam.step))
    glVertex(1.4, -1.9, (0.5 + cam.step))
    glEnd()

    ################ front
    glBegin(GL_POLYGON)
    glTexCoord2f(0, 0)
    glVertex(1, -1.75, (0.5 + cam.step))
    glTexCoord2f(0.07, 0)
    glVertex(1.25, -2, (0.5 + cam.step))
    glTexCoord2f(0.12, 0.0)
    glVertex(1.4, -1.9, (0.5 + cam.step))
    glTexCoord2f(0.25, 0.0)
    glVertex(1.5, -1.75, (0.5 + cam.step))
    glTexCoord2f(0.25, 1.0)
    glVertex(1.5, 1.9, 0.5)
    glTexCoord2f(0.12, 1.0)
    glVertex(1.33, 1.98, 0.5)
    glTexCoord2f(0.07, 1.0)
    glVertex(1.2, 1.98, 0.5)
    glTexCoord2f(0.0, 1.0)
    glVertex(1, 1.9, 0.5)
    glEnd()

    # back right arm
    glBindTexture(GL_TEXTURE_2D, 10)
    glBegin(GL_POLYGON)
    glTexCoord2f(0, 0)
    glVertex(1, -1.75, -(0.5 + cam.step))
    glTexCoord2f(0.07, 0)
    glVertex(1.25, -2, -(0.5 + cam.step))
    glTexCoord2f(0.12, 0.0)
    glVertex(1.4, -1.9, -(0.5 + cam.step))
    glTexCoord2f(0.25, 0.0)
    glVertex(1.5, -1.75, -(0.5 + cam.step))
    glTexCoord2f(0.25, 1.0)
    glVertex(1.5, 1.9, -0.5)
    glTexCoord2f(0.12, 1.0)
    glVertex(1.33, 1.9, -0.5)
    glTexCoord2f(0.07, 1.0)
    glVertex(1.2, 1.9, -0.5)
    glTexCoord2f(0.0, 1.0)
    glVertex(1, 1.9, -0.5)
    glEnd()

    ####################################left arm
    # left side
    glBindTexture(GL_TEXTURE_2D, 12)

    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex(-1.5, -1.75, (0.5 - cam.step))
    glTexCoord2f(1.0, 0.0)
    glVertex(-1.5, -1.75, -(0.5 - cam.step))
    glTexCoord2f(1.0, 1.0)
    glVertex(-1.5, 1.9, -0.5)
    glTexCoord2f(0.0, 1.0)
    glVertex(-1.5, 1.9, 0.5)
    glEnd()

    # glBindTexture(GL_TEXTURE_2D, 16)
    #########top left of left hand
    glBegin(GL_QUADS)
    glVertex(-1.5, 1.9, 0.5)
    glVertex(-1.5, 1.9, -0.5)
    glVertex(-1.25, 2, -0.5)
    glVertex(-1.25, 2, 0.5)
    glEnd()

    #### top right of left hand
    glBegin(GL_QUADS)
    glVertex(-1.25, 2, 0.5)
    glVertex(-1.25, 2, -0.5)
    glVertex(-1, 1.9, -0.5)
    glVertex(-1, 1.9, 0.5)
    glEnd()

    # button left for left hand
    glBegin(GL_POLYGON)
    glVertex(-1.25, -2, (0.5 - cam.step))
    glVertex(-1.25, -2, -(0.5 - cam.step))
    glVertex(-1.4, -1.9, -(0.5 - cam.step))
    glVertex(-1.5, -1.75, -(0.5 - cam.step))
    glVertex(-1.5, -1.75, (0.5 - cam.step))
    glVertex(-1.4, -1.9, (0.5 - cam.step))
    glEnd()

    ################ front
    glBindTexture(GL_TEXTURE_2D, 9)
    glBegin(GL_POLYGON)
    glTexCoord2f(0, 0)
    glVertex(-1.5, -1.75, (0.5 - cam.step))
    glTexCoord2f(0.12, 0)
    glVertex(-1.25, -2, (0.5 - cam.step))
    glTexCoord2f(0.25, 0.0)
    glVertex(-1, -1.75, (0.5 - cam.step))
    glTexCoord2f(0.25, 1.0)
    glVertex(-1, 1.9, 0.5)
    glTexCoord2f(0.12, 1.0)
    glVertex(-1.2, 1.98, 0.5)
    glTexCoord2f(0.07, 1.0)
    glVertex(-1.35, 1.98, 0.5)
    glTexCoord2f(0.0, 1.0)
    glVertex(-1.5, 1.9, 0.5)
    glEnd()
    
    # back right arm
    glBindTexture(GL_TEXTURE_2D, 10)
    glBegin(GL_POLYGON)
    glTexCoord2f(0, 0)
    glVertex(-1.5, -1.75, -(0.5 - cam.step))
    glTexCoord2f(0.12, 0)
    glVertex(-1.25, -2, -(0.5 - cam.step))
    glTexCoord2f(0.25, 0.0)
    glVertex(-1, -1.75, -(0.5 - cam.step))
    glTexCoord2f(0.25, 1.0)
    glVertex(-1, 1.9, -0.5)
    glTexCoord2f(0.12, 1.0)
    glVertex(-1.2, 1.98, -0.5)
    glTexCoord2f(0.07, 1.0)
    glVertex(-1.35, 1.98, -0.5)
    glTexCoord2f(0.0, 1.0)
    glVertex(-1.5, 1.9, -0.5)
    glEnd()

    glPopMatrix()

