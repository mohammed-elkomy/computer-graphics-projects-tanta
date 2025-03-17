from OpenGL.GL import *


class Rectangle:
    def __init__(self, x, y, length, width):
        self.left = x - length / 2
        self.right = x + length / 2
        self.top = y + width / 2
        self.bottom = y - width / 2
        self.x = x
        self.y = y

    def draw(self):
        glLoadIdentity()
        glBegin(GL_QUADS)
        glVertex(self.left, self.bottom, 0)  # Left - Bottom
        glVertex(self.right, self.bottom, 0)
        glVertex(self.right, self.top, 0)
        glVertex(self.left, self.top, 0)
        glEnd()


class Circle:
    # noinspection PyShadowingNames
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r
