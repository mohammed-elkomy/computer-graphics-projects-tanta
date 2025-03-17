from OpenGL.GL import *
from Textures import *


class Rectangle:
    def __init__(self, width, height, x, y):
        self.width = width
        self.height = height
        self.right = x + width
        self.left = x
        self.top = y + height
        self.bottom = y

    def draw_texture(self, texture_index):
        drawHelper1(texture_index, self.left, self.right, self.top, self.bottom)

    def drawRectangle(self, color: tuple = (1, 1, 1)):
        glColor3f(color[0], color[1], color[2])
        glBegin(GL_QUADS)
        glVertex2f(self.left, self.bottom)
        glVertex2f(self.right, self.bottom)
        glVertex2f(self.right, self.top)
        glVertex2f(self.left, self.top)
        glEnd()



class MainCar:
    def __init__(self, x, y, trans_x, trans_y, theta, rgb):
        self.x = x
        self.y = y
        self.right = trans_x + (x / 2)
        self.left = trans_x - (x / 2)
        self.top = trans_y + (y / 2)
        self.bottom = trans_y - (y / 2)

        glPushMatrix()
        glTranslatef(trans_x, trans_y, 0)
        glRotatef(theta, 0, 0, 1)
        # Another draw-helper for the car
        drawHelper1(1, -x / 2, x / 2, y / 2, -y / 2)
        glPopMatrix()


class Car_Model:
    def __init__(self, left, bottom, right, top, car_Direction, obstacle_speed):
        self.left = left
        self.bottom = bottom
        self.right = right
        self.top = top
        self.car_Direction = car_Direction * obstacle_speed

    def draw_texture(self, texture_index):
        drawHelper1(texture_index, self.left, self.right, self.top, self.bottom)
