from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from random import randint
from itertools import cycle

# ######### Constants ##############
SCREENWIDTH = 600
SCREENHEIGHT = 720
BASEY = SCREENHEIGHT * 0.2
###################################


def random_gap():
    return randint(int(BASEY) + 170, SCREENHEIGHT - 170)


def draw_rectangle_with_tex(left, right, bottom, top, tex, z=0):
    glPushMatrix()
    glBindTexture(GL_TEXTURE_2D, tex)

    glBegin(GL_QUADS)
    glTexCoord(0, 0)
    glVertex(left, bottom, z)
    glTexCoord(0, 1)
    glVertex(left, top, z)
    glTexCoord(1, 1)
    glVertex(right, top, z)
    glTexCoord(1, 0)
    glVertex(right, bottom, z)
    glEnd()

    glPopMatrix()


class Pipe:
    def __init__(self, tex):
        self.gap_size = 150
        self.width = 70
        self.gap_y = random_gap()
        self.left = SCREENWIDTH
        self.right = self.left + self.width
        self.upper_y = self.gap_y + self.gap_size * 0.5
        self.lower_y = self.gap_y - self.gap_size * 0.5
        self.count = False
        self.tex = tex  # It's alist contains two textures: tex[0] for lower pipe & tex[1] for upper pipe.

    def draw(self):
        # Lower pipe
        draw_rectangle_with_tex(self.left, self.right, -300, self.lower_y, self.tex[0])
        # Upper pipe
        draw_rectangle_with_tex(self.left, self.right, self.upper_y, SCREENHEIGHT + 400, self.tex[1])

    def move(self, shift):
        self.left += shift
        self.right += shift


class Bird:
    def __init__(self, tex, gravity=0.2, angular_s=0.5):
        # shape attributes
        self.height = 40
        self.width = 1.3 * self.height   # width is longer than height
        # position attributes
        self.right = SCREENWIDTH * 0.3
        self.left = self.right - self.width
        self.bottom = SCREENHEIGHT * 0.5
        self.top = self.bottom + self.height
        self.angle = 0
        # movement attributes
        self.fly_speed = 1.1
        self.velocity = 0
        self.gravity = gravity
        self.i_velocity = 0
        self.angular_s = angular_s
        self.i_angular_s = self.angular_s
        # animation Attributes
        self.swap = True
        self.tex = tex  # It's alist contains 3 textures for (3 states of the bird)
        self.tex_sequence = cycle([0, 1, 2, 1])   # sequence in which we want textures flow.
        self.tex_index = 0  # pointer to the current texture.
        self.tex_loop = 0   # each time the bird is drawn, It's increased by one. "help in controlling the speed of wings".

    def draw(self):
        glPushMatrix()
        glLoadIdentity()

        glTranslate((self.right + self.left) / 2, (self.bottom + self.top) / 2, 0)
        glRotate(self.angle, 0, 0, 1)
        glTranslate(-(self.right + self.left) / 2, -(self.bottom + self.top) / 2, 0)
        draw_rectangle_with_tex(self.left, self.right, self.bottom, self.top, 
                                self.tex[self.tex_index], 0.8)
        glPopMatrix()

        if self.swap:
            self.tex_loop += 1
            if (self.tex_loop % 12) == 0:
                self.tex_index = next(self.tex_sequence)

    def fly(self, fly_range=15):
        self.draw()
        # moving the bird up or down.
        self.bottom += self.fly_speed
        self.top += self.fly_speed

        # change direction of bird if necessary
        if self.bottom < SCREENHEIGHT * 0.5 - fly_range:
            self.fly_speed *= -1
        if self.bottom > SCREENHEIGHT * 0.5 + fly_range:
            self.fly_speed *= -1

    def move(self):
        if self.bottom > BASEY:
            self.bottom += self.velocity
            self.top += self.velocity
            # control angle variation
            if self.velocity >= 0:  # bird is going up.
                if self.angle < 30:
                    self.angle += self.angular_s
            elif self.angle > -90:  # bird is going down and angle > -90.
                self.angle -= self.angular_s * 0.3

        if self.top >= SCREENHEIGHT:
            self.velocity = 0

        self.velocity += self.gravity

        self.draw()

    def die(self):
        self.swap = False
        self.velocity += self.gravity
        self.angular_s += 0.3
        self.move()

    def reset(self):
        # position attributes
        self.right = SCREENWIDTH * 0.3
        self.left = self.right - self.width
        self.bottom = SCREENHEIGHT * 0.5
        self.top = self.bottom + self.height
        self.angle = 0
        # movement attributes
        self.velocity = self.i_velocity
        self.angular_s = self.i_angular_s
        self.swap = True


class Base:
    def __init__(self, tex, z=0.1):
        self.tex = tex
        self.z = z
        self.width = 2 * SCREENWIDTH + 5
        self.right = 2 * SCREENWIDTH
        self.left = self.right - self.width
        self.top = BASEY
        self.bottom = 0
    
    def draw(self):
        glPushMatrix()
        glBindTexture(GL_TEXTURE_2D, self.tex)

        glBegin(GL_QUADS)
        glTexCoord(0, 0)
        glVertex(self.left, self.bottom, self.z)
        glTexCoord(0, 1)
        glVertex(self.left, self.top, self.z)
        glTexCoord(2, 1)
        glVertex(self.right, self.top, self.z)
        glTexCoord(2, 0)
        glVertex(self.right, self.bottom, self.z)
        glEnd()

        glPopMatrix()

    def move(self, dx):
        if self.right <= SCREENWIDTH + 1:
            self.right = 2 * SCREENWIDTH
        self.right += dx
        self.left = self.right - self.width
        