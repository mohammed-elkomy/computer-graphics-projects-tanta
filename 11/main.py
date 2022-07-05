import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from random import randint

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 650
time_interval = 10
mouse_x = 0
eggy = -2

remain = 3
Score = 0

texture_names = [1, 2, 3, 4]


class RECTA:
    def __init__(self, left, bottom, right, top):
        self.left = left
        self.bottom = bottom
        self.right = right
        self.top = top


wall = RECTA(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
basket = RECTA(0, 0, 60, 35)
line = RECTA(0, 605, WINDOW_WIDTH, 610)
egg = RECTA(120, 560, 150, 605)
back = RECTA(0, -10, WINDOW_WIDTH, 610)


def init():
    glEnable(GL_BLEND)  # ADDED FOR BLENDING  # added by komy
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)  # ADDED FOR BLENDING # added by komy

    loadTextures()
    glClearColor(1.0, 1.0, 1.0, 0.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT, 0, 1)  # l,r,b,t,n,f
    glMatrixMode(GL_MODELVIEW)


def texture_setup(texture_image_binary, texture_name, width, height):
    glBindTexture(GL_TEXTURE_2D, texture_name)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

    glTexImage2D(GL_TEXTURE_2D,
                 0,
                 GL_RGBA, # added by komy
                 width, height,
                 0,
                 GL_RGBA,
                 GL_UNSIGNED_BYTE,
                 texture_image_binary)


def loadTextures():
    glEnable(GL_TEXTURE_2D)
    images = []
    images.append(pygame.image.load("egg.png"))
    images.append(pygame.image.load("black.jpg"))
    images.append(pygame.image.load("basket.png"))
    images.append(pygame.image.load("background.jpg"))

    textures = [pygame.image.tostring(image, "RGBA", True)
                for image in images]
    glGenTextures(len(images), texture_names)
    for i in range(len(images)):
        texture_setup(textures[i],
                      texture_names[i],
                      images[i].get_width(),
                      images[i].get_height())


def DrawRectangle(rect, B):
    glLoadIdentity()
    glColor3f(1, 1, 1)
    glBindTexture(GL_TEXTURE_2D, texture_names[B])
    glBegin(GL_QUADS)

    glTexCoord2f(0, 0)
    glVertex(rect.left, rect.bottom, 0)

    glTexCoord2f(1, 0)
    glVertex(rect.right, rect.bottom, 0)

    glTexCoord2f(1, 1)
    glVertex(rect.right, rect.top, 0)

    glTexCoord2f(0, 1)
    glVertex(rect.left, rect.top, 0)
    glEnd()


def drawText(string, x, y):
    glLineWidth(3)
    glColor(0, 0, 0)
    glLoadIdentity()
    glTranslate(x, y, 0)
    glScale(0.25, 0.25, 1)
    string = string.encode()
    for c in string:
        glutStrokeCharacter(GLUT_STROKE_ROMAN, c)


def keyboard(key, x, y):
    if key == b"q":
        sys.exit(0)


def MouseMotion(x, y):
    global mouse_x
    mouse_x = x


def Timer(v):
    Display()

    glutTimerFunc(time_interval, Timer, 1)


def check_ball_bat(_ball, _player):
    horizontal_check = _player.left <= _ball.left <= _ball.right <= _player.right
    vertical_check = _ball.bottom <= _player.top
    return vertical_check and horizontal_check


def Display():
    global egg
    global eggy
    global remain
    global Score
    glClear(GL_COLOR_BUFFER_BIT)
    DrawRectangle(back, 3)
    ########### TEXT ################
    string = "Score : " + str(Score)
    drawText(string, 5, 620)
    string = "remain : " + str(remain)
    drawText(string, 400, 620)
    ##################################
    glLoadIdentity()
    glColor(0, 0, 0)
    DrawRectangle(line, 1)
    ###################################
    ############ movement #############
    basket.left = mouse_x - 50
    basket.right = mouse_x + 50
    DrawRectangle(basket, 2)

    ################################
    ########### EGG ################
    glLoadIdentity()
    egg.top = egg.top + eggy
    egg.bottom = egg.bottom + eggy
    glColor(1, 0, 0)
    DrawRectangle(egg, 0)
    if remain >= 0:
        if check_ball_bat(egg, basket):
            x = randint(30, 570)
            egg = RECTA(x, 560, x + 30, 605)
            Score += 1
            if Score % 5 == 0:
                eggy -= 1
        elif egg.bottom <= wall.bottom:
            x = randint(30, 600)
            egg = RECTA(x, 560, x + 30, 605)
            remain -= 1

    else:
        sys.exit(0)

    glutSwapBuffers()


def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutInitWindowPosition(0, 0)
    glutCreateWindow(b"EGG")
    glutDisplayFunc(Display)
    glutTimerFunc(time_interval, Timer, 1)
    glutKeyboardFunc(keyboard)
    glutPassiveMotionFunc(MouseMotion)
    init()
    glutMainLoop()


main()
