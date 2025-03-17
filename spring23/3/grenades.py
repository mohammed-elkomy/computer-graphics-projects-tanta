from pyrr import Vector3, vector, vector3
from math import sin, cos, radians
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from coins import *


class Grenades:
    def __init__(self, cam):
        self.cam = cam
        self.x = self.cam.camera_pos[0]
        self.y = -0.4
        self.z = self.cam.camera_pos[2]
        self.direction = self.cam.throw_direction
        self.pos = Vector3([self.x, self.y, self.z])

    def draw(self, monsters, grenades):
        glPushMatrix()
        glTranslate(self.pos[0] + self.direction[0] * 0.4,
                    self.y, self.pos[2] + self.direction[2] * 0.4)
        glScale(0.5, 0.5, 0.5)
        self.drawGernades()
        self.pos += self.direction * 0.05
        self.y -= 0.008
        if self.y < -1:
            grenades.remove(self)
        glPopMatrix()
        return self.collission_1(monsters, grenades)

    def collission_1(self, monsters, grenades):
        global coins_result
        for monster in monsters:
            if monster.x + 0.6 > self.pos[0] and monster.x - 0.6 < self.pos[0]:
                if monster.z + 0.6 > self.pos[2] and monster.z - 0.6 < self.pos[2] and self.y > -0.9:
                    grenades.remove(self)
                    monsters.remove(monster)
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound('sounds/hit.ogg'))
                    return True
        return False

    def drawGernades(self):
        glBindTexture(GL_TEXTURE_2D, 17)
        glColor3f(1, 1, 1)
        glBegin(GL_POLYGON)
        # front
        # basic body of gernades
        glTexCoord2f(0.25, 0.1)
        glVertex3f(-0.1, -0.3, 0.1)

        glTexCoord2f(0.75, 0.1)
        glVertex3f(0.1, 0.3, 0.1)

        glTexCoord2f(1, 0.5)
        glVertex3f(0.2, 0, 0.1)

        glTexCoord2f(0.75, 0.75)
        glVertex3f(0.1, 0.1, 0.1)

        glTexCoord2f(0.25, 0.75)
        glVertex3f(-0.1, 0.1, 0.1)

        glTexCoord2f(0, 0.5)
        glVertex3f(-0.2, 0, 0.1)

        glEnd()
        # above quad
        glBindTexture(GL_TEXTURE_2D, 17)
        glBegin(GL_QUADS)
        glTexCoord2f(0.25, 0.75)
        glVertex3f(-0.1, 0.1, 0.1)

        glTexCoord2f(0.75, 0.75)
        glVertex3f(0.1, 0.1, 0.1)

        glTexCoord2f(0.75, 0.85)
        glVertex3f(0.1, 0.2, 0.1)

        glTexCoord2f(0.25, 0.85)
        glVertex3f(-0.1, 0.2, 0.1)

        glEnd()
        # the triangle above the quad
        glBindTexture(GL_TEXTURE_2D, 17)
        glBegin(GL_QUADS)
        glTexCoord2f(0.25, 0.85)
        glVertex3f(-0.1, 0.2, 0.1)

        glTexCoord2f(0.75, 0.85)
        glVertex3f(0.1, 0.2, 0.1)

        glTexCoord2f(0.5, 1)
        glVertex3f(0, 0.3, 0.1)

        glEnd()

        glBindTexture(GL_TEXTURE_2D, 17)
        glColor3f(1, 1, 1)
        glBegin(GL_POLYGON)
        # back
        # basic body of gernades
        glTexCoord2f(0.25, 0.1)
        glVertex3f(-0.1, -0.3, 00.05)

        glTexCoord2f(0.75, 0.1)
        glVertex3f(0.1, 0.3, 0.05)

        glTexCoord2f(1, 0.5)
        glVertex3f(0.2, 0, 0.05)

        glTexCoord2f(0.75, 0.75)
        glVertex3f(0.1, 0.1, 0.05)

        glTexCoord2f(0.25, 0.75)
        glVertex3f(-0.1, 0.1, 0.05)

        glTexCoord2f(0, 0.5)
        glVertex3f(-0.2, 0, 0.05)

        glEnd()
        # above quad
        glBindTexture(GL_TEXTURE_2D, 17)
        glBegin(GL_QUADS)
        glTexCoord2f(0.25, 0.75)
        glVertex3f(-0.1, 0.1, 0.05)

        glTexCoord2f(0.75, 0.75)
        glVertex3f(0.1, 0.1, 0.05)

        glTexCoord2f(0.75, 0.85)
        glVertex3f(0.1, 0.2, 0.05)

        glTexCoord2f(0.25, 0.85)
        glVertex3f(-0.1, 0.2, 0.05)

        glEnd()
        # the triangle above the quad
        glBindTexture(GL_TEXTURE_2D, 17)
        glBegin(GL_QUADS)
        glTexCoord2f(0.25, 0.85)
        glVertex3f(-0.1, 0.2, 0.05)

        glTexCoord2f(0.75, 0.85)
        glVertex3f(0.1, 0.2, 0.05)

        glTexCoord2f(0.5, 1)
        glVertex3f(0, 0.3, 0.05)

        glEnd()
        # side left
        # under polygon part
        glBindTexture(GL_TEXTURE_2D, 18)

        glColor3f(1, 1, 0)
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0)
        glVertex3f(-0.1, -0.3, 0.05)

        glTexCoord2f(1, 0)
        glVertex3f(-0.1, -0.3, 0.1)

        glTexCoord2f(1, 1)
        glVertex3f(-0.2, 0, 0.1)

        glTexCoord2f(0, 1)
        glVertex3f(-0.2, 0, 0.05)

        glEnd()

        # right and left for above polygon part
        glBindTexture(GL_TEXTURE_2D, 18)

        glColor3f(1, 1, 0)
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0)
        glVertex3f(-0.2, 0, 0.05)

        glTexCoord2f(1, 0)
        glVertex3f(-0.2, 0, 0.1)

        glTexCoord2f(1, 1)
        glVertex3f(-0.1, 0.1, 0.1)

        glTexCoord2f(0, 1)
        glVertex3f(-0.1, 0.1, 0.05)

        glEnd()

        # part of quad above polygon
        glBindTexture(GL_TEXTURE_2D, 18)

        glColor3f(1, 1, 0)
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0)
        glVertex3f(-0.1, 0.1, 0.05)

        glTexCoord2f(1, 0)
        glVertex3f(-0.1, 0.1, 0.1)

        glTexCoord2f(1, 1)
        glVertex3f(-0.1, 0.2, 0.1)

        glTexCoord2f(0, 1)
        glVertex3f(-0.1, 0.2, 0.05)

        glEnd()
        # part of triangle
        glBindTexture(GL_TEXTURE_2D, 18)

        glColor3f(1, 1, 0)
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0)
        glVertex3f(-0.1, 0.2, 0.05)

        glTexCoord2f(1, 0)
        glVertex3f(-0.1, 0.2, 0.1)

        glTexCoord2f(1, 1)
        glVertex3f(0.15, 0.3, 0.1)

        glTexCoord2f(0, 1)
        glVertex3f(0.15, 0.3, 0.05)

        glEnd()

        # side right
        # under polygon part
        glBindTexture(GL_TEXTURE_2D, 18)

        glColor3f(1, 1, 0)
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0)
        glVertex3f(-0.1, -0.3, 0.1)

        glTexCoord2f(1, 0)
        glVertex3f(-0.1, -0.3, 0.05)

        glTexCoord2f(1, 1)
        glVertex3f(0.2, 0, 0.05)

        glTexCoord2f(0, 1)
        glVertex3f(0.2, 0, 0.1)

        glEnd()

        # right and left for above polygon part
        glBindTexture(GL_TEXTURE_2D, 18)

        glColor3f(1, 1, 0)
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0)
        glVertex3f(0.2, 0, 0.05)

        glTexCoord2f(1, 0)
        glVertex3f(0.2, 0, 0.1)

        glTexCoord2f(1, 1)
        glVertex3f(0.1, 0.1, 0.1)

        glTexCoord2f(0, 1)
        glVertex3f(0.1, 0.1, 0.05)

        glEnd()

        # part of quad above polygon
        glBindTexture(GL_TEXTURE_2D, 18)

        glColor3f(1, 1, 0)
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0)
        glVertex3f(0.1, 0.1, 0.05)

        glTexCoord2f(1, 0)
        glVertex3f(0.1, 0.1, 0.1)

        glTexCoord2f(1, 1)
        glVertex3f(0.1, 0.2, 0.1)

        glTexCoord2f(0, 1)
        glVertex3f(0.1, 0.2, 0.05)

        glEnd()
        # part of triangle
        glBindTexture(GL_TEXTURE_2D, 18)

        glColor3f(1, 1, 0)
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0)
        glVertex3f(0.1, 0.2, 0.05)

        glTexCoord2f(1, 0)
        glVertex3f(0.1, 0.2, 0.1)

        glTexCoord2f(1, 1)
        glVertex3f(0, 0.3, 0.1)

        glTexCoord2f(0, 1)
        glVertex3f(0, 0.3, 0.05)

        glEnd()
