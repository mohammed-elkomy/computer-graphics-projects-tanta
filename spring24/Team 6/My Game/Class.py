from Initialization_Variable import *
import math


class Mouse:
    def __init__(self, window_height):
        self._x = 0
        self._y = 0
        self.window_height = window_height

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = glutGet(GLUT_WINDOW_HEIGHT) - value


class RECT:
    def __init__(self, left, bottom, right, top):
        self.left = left
        self.bottom = bottom
        self.right = right
        self.top = top

    def MakeRectFromCenter(self, _x, _y, Width, Height):
        w = Width / 2
        h = Height / 2
        self.left = _x - w
        self.bottom = _y - h
        self.right = _x + w
        self.top = _y + h

    def DrawRectangle(self):
        glLoadIdentity()
        glColor(1, 0, .2)  # White color
        glBegin(GL_QUADS)
        glVertex(self.left, self.bottom, 0)
        glVertex(self.right, self.bottom, 0)
        glVertex(self.right, self.top, 0)
        glVertex(self.left, self.top, 0)
        glEnd()

    def DrawRectangleWithPhoto(self, texture_name, z=-.9):
        glLoadIdentity()

        glColor(1, 1, 1, 1)
        glBindTexture(GL_TEXTURE_2D, texture_name)
        glBegin(GL_POLYGON)

        glTexCoord(0, 0)
        glVertex3d(self.left, self.bottom, z)

        glTexCoord(1, 0)
        glVertex3d(self.right, self.bottom, z)

        glTexCoord(1, 1)
        glVertex3d(self.right, self.top, z)

        glTexCoord(0, 1)
        glVertex3d(self.left, self.top, z)
        glEnd()
        glBindTexture(GL_TEXTURE_2D, -1)

    def XCenter(self):
        return (self.left + self.right) / 2

    def YCenter(self):
        return (self.top + self.bottom) / 2

    def DrawCircle(self, r):
        centerX = self.XCenter()
        centerY = self.YCenter()
        num_segments = 100
        glBegin(GL_TRIANGLE_FAN)
        glColor(1, 1, 1)  # White color
        glVertex2f(centerX, centerY)  # Center of the circle
        for i in range(num_segments + 1):
            angle = 2.0 * 3.141592653589793 * i / num_segments
            x = r * math.cos(angle) + centerX
            y = r * math.sin(angle) + centerY
            glVertex2f(x, y)
            glVertex3f(x, y, -.5)
        glEnd()


class Bullet:
    def __init__(self, _xMouse, _yMouse, _x, _y):
        self.xMouse = _xMouse
        self.yMouse = _yMouse
        self.xCenterPlayer = _x
        self.yCenterPlayer = _y
        self.xCenter = _x
        self.yCenter = _y
        self.Rect = RECT(self.xCenter - 10, self.yCenter - 10, self.xCenter + 10, self.yCenter + 10)


class Ghost_Class:

    def __init__(self, _z, _x, _y, GhostWidth, GhostHeight):
        self.z = _z
        self.Rect = RECT(0, 0, 0, 0)
        self.GhostWidth = GhostWidth
        self.GhostHeight = GhostHeight
        self.Rect.MakeRectFromCenter(_x, _y, self.GhostWidth, self.GhostHeight)

    def draw(self):
        self.Rect.DrawRectangleWithPhoto(20, self.z)

    def changeCenter(self, x, y):
        self.Rect.MakeRectFromCenter(x, y, self.GhostWidth, self.GhostHeight)


class HealthIcon_Class():
    def __init__(self, WINDOW_WIDTH, HealthIconFactor):
        self._x = randrange(0, WINDOW_WIDTH)
        self._y = randrange(0, 548)
        self.Rect = RECT(0, 0, 0, 0)
        self.Rect.MakeRectFromCenter(self._x, self._y, 338 * HealthIconFactor,
                                     510 * HealthIconFactor)

    def draw(self):
        glLoadIdentity()
        self.Rect.DrawRectangleWithPhoto(22, -.75)


class AmmoIcon_Class():
    def __init__(self, WINDOW_WIDTH, AmmoIconFactor):
        self._x = randrange(0, WINDOW_WIDTH)
        self._y = randrange(0, 548)
        self.Rect = RECT(0, 0, 0, 0)
        self.Rect.MakeRectFromCenter(self._x, self._y, 343 * AmmoIconFactor,
                                     513 * AmmoIconFactor)

    def draw(self):
        glLoadIdentity()
        self.Rect.DrawRectangleWithPhoto(21, -.75)
