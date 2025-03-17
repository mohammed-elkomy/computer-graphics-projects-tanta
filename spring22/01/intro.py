from OpenGL.GLUT import *
from OpenGL.GL import *
import pygame
import os

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
FONT_DOWNSCALE = .2
music = False
with open("music_state", 'w') as f:
    f.write('')
texture_names = [0, 1, 2, 3, 4, 5, 6]


def mouse(button, state, x, y):
    global music, WINDOW_WIDTH, WINDOW_HEIGHT
    if state == GLUT_UP and 0.55 * WINDOW_WIDTH > x > 0.45 * WINDOW_WIDTH and \
            0.7 * WINDOW_HEIGHT > y > 0.65 * WINDOW_HEIGHT:
        music = not music
        with open('music_state', 'w') as f:
            if music:
                f.write('1')
            else:
                f.write('')
    if state == GLUT_UP and 0.543 * WINDOW_WIDTH > x > 0.4 * WINDOW_WIDTH and \
            0.6 * WINDOW_HEIGHT > y > 0.55 * WINDOW_HEIGHT:
        import Gameplay
    if state == GLUT_UP and 0.54 * WINDOW_WIDTH > x > 0.4 * WINDOW_WIDTH and \
            0.8 * WINDOW_HEIGHT > y > 0.75 * WINDOW_HEIGHT:
        os._exit(0)


class RECT:
    def __init__(self, left, right, bottom, top):
        self.left = left
        self.bottom = bottom
        self.right = right
        self.top = top

    def draw_rect(self, red, green, blue, texture, x=1., y=1.):
        glPushMatrix()
        glBindTexture(GL_TEXTURE_2D, texture)
        glColor3d(red, green, blue)
        glBegin(GL_POLYGON)
        glTexCoord2f(0, 0)
        glVertex2d(self.left, self.bottom)
        glTexCoord2f(x, 0)
        glVertex2d(self.right, self.bottom)
        glTexCoord2f(x, y)
        glVertex2d(self.right, self.top)
        glTexCoord2f(0, y)
        glVertex2d(self.left, self.top)
        glEnd()
        glBindTexture(GL_TEXTURE_2D, -1)
        glPopMatrix()


def draw_text(string, x, y, font=FONT_DOWNSCALE):
    glColor3d(1, 1, 1)
    glLineWidth(3.2)
    glPushMatrix()
    glTranslate(x, y, 0)
    glScale(font, font, 1)
    string = string.encode()
    for c in string:
        glutStrokeCharacter(GLUT_STROKE_ROMAN, c)
    glPopMatrix()


space = RECT(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT)
hs_cup = RECT(40, 110, 695, 750)
name = RECT(0.25 * WINDOW_WIDTH, 0.75 * WINDOW_WIDTH, 0.55 * WINDOW_HEIGHT, 0.63 * WINDOW_HEIGHT)
play_button = RECT(0.4 * WINDOW_WIDTH, 0.55 * WINDOW_WIDTH, 0.4 * WINDOW_HEIGHT, 0.45 * WINDOW_HEIGHT)
music_on = RECT(0.4 * WINDOW_WIDTH, 0.55 * WINDOW_WIDTH, 0.3 * WINDOW_HEIGHT, 0.35 * WINDOW_HEIGHT)
music_off = RECT(0.4 * WINDOW_WIDTH, 0.55 * WINDOW_WIDTH, 0.3 * WINDOW_HEIGHT, 0.35 * WINDOW_HEIGHT)
Exit = RECT(0.4 * WINDOW_WIDTH, 0.45 * WINDOW_WIDTH, 0.2 * WINDOW_HEIGHT, 0.25 * WINDOW_HEIGHT)


def init():
    #################################
    load_textures_intro()
    ##################################
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT, 0, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def texture_setup(texture_image_binary, texture_name, width, height):
    glBindTexture(GL_TEXTURE_2D, texture_name)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, 3, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_image_binary)


def load_textures_intro():
    glEnable(GL_TEXTURE_2D)
    images = []
    images.append(pygame.image.load("Textures/space.png"))
    images.append(pygame.image.load("Textures/cup.png"))
    images.append(pygame.image.load("Textures/game_name.jpg"))
    images.append(pygame.image.load("Textures/play_button.png"))
    images.append(pygame.image.load("Textures/music_on.png"))
    images.append(pygame.image.load("Textures/music_off.png"))
    images.append(pygame.image.load("Textures/exit.png"))
    textures = [pygame.image.tostring(image, "RGBA", True) for image in images]
    glGenTextures(len(images), texture_names)
    for i in range(len(images)):
        texture_setup(textures[i], texture_names[i], images[i].get_width(), images[i].get_height())


def high_score():
    with open('high_scores', 'r') as f:
        return f.readline()


def draw():
    global space, hs_cup, music_on, music_off, music
    glClearColor(0, 0, 0, 0)
    glClear(GL_COLOR_BUFFER_BIT)
    space.draw_rect(1, 1, 1, texture_names[0])
    hs_cup.draw_rect(1, 1, 1, texture_names[1])
    name.draw_rect(1, 1, 1, texture_names[2])
    draw_text("EXIT", 0.46 * WINDOW_WIDTH, 0.208 * WINDOW_HEIGHT, 0.27)
    Exit.draw_rect(1, 1, 1, texture_names[6])
    play_button.draw_rect(1, 1, 1, texture_names[3])
    if music:
        music_on.draw_rect(1, 1, 1, texture_names[4], 1, 1)
    else:
        music_off.draw_rect(1, 1, 1, texture_names[5], 1, 1)
    draw_text(high_score(), 115, 715)
    glutSwapBuffers()


glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA)
glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
glutInitWindowPosition(400, 0)
glutCreateWindow("Intro")
glutMouseFunc(mouse)
glutDisplayFunc(draw)
glutIdleFunc(draw)
init()
glutMainLoop()
