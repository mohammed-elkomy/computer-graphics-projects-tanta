import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys
import os

WINDOW_HEIGHT = 800
WINDOW_WIDTH = 1200
textures_id = 0, 1, 2


class Rectangle:
    def __init__(self, left, bottom, right, top):
        self.left = left
        self.bottom = bottom
        self.right = right
        self.top = top


def init():
    glClearColor(1, 1, 1, 1)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT, 0, 1)
    glMatrixMode(GL_MODELVIEW)


whole_wall = Rectangle(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
exit_label = Rectangle(WINDOW_WIDTH * 0.46, WINDOW_HEIGHT * 0.25, WINDOW_WIDTH * 0.54, WINDOW_HEIGHT * 0.4)
start_game = Rectangle(WINDOW_WIDTH * 0.45, WINDOW_HEIGHT * 0.4, WINDOW_WIDTH * 0.55, WINDOW_HEIGHT * 0.5)


######################################
#             Textures               #
######################################
def texture_setup(texture_image_binary, texture_id, width, height):
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glEnable(GL_BLEND)  # FOR BLENDING
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_image_binary)


def load_textures():
    global textures_id
    glEnable(GL_TEXTURE_2D)

    glGenTextures(len(textures_id), textures_id)

    load_and_setup("pics/intro2.jpg", textures_id[0])
    load_and_setup("pics/startt.png", textures_id[1])
    load_and_setup("pics/exittex.png", textures_id[2])


def load_and_setup(image_path, idx):
    # Loading
    image = pygame.image.load(image_path)

    texture = pygame.image.tostring(image, "RGBA", True)

    texture_setup(texture, textures_id[idx], image.get_width(), image.get_height())
    # Setup Wrapping and Rendering


def draw_rectangle_textured(rect):
    glLoadIdentity()
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)
    glVertex2f(rect.left, rect.bottom)
    glTexCoord2f(1, 0)
    glVertex2f(rect.right, rect.bottom)
    glTexCoord2f(1, 1)
    glVertex2f(rect.right, rect.top)
    glTexCoord2f(0, 1)
    glVertex2f(rect.left, rect.top)
    glEnd()


def display_2():
    glClear(GL_COLOR_BUFFER_BIT)
    glClearColor(1, 1, 1, 1)
    glBindTexture(GL_TEXTURE_2D, textures_id[0])
    glColor3d(1, 1, 1)
    draw_rectangle_textured(whole_wall)
    glBindTexture(GL_TEXTURE_2D, -1)

    glBindTexture(GL_TEXTURE_2D, textures_id[2])
    glColor3d(1, 1, 1)
    draw_rectangle_textured(exit_label)
    glBindTexture(GL_TEXTURE_2D, -1)

    glBindTexture(GL_TEXTURE_2D, textures_id[1])
    glColor3d(1, 1, 1)
    draw_rectangle_textured(start_game)
    glBindTexture(GL_TEXTURE_2D, -1)
    glutSwapBuffers()


def mouse_callback(button, state, x_mouse_coord, y_mouse_coord):
    global WINDOW_HEIGHT, WINDOW_WIDTH
    if state == GLUT_UP:
        print(x_mouse_coord)
        print(y_mouse_coord)
        if (WINDOW_WIDTH * 0.55 >= x_mouse_coord >= WINDOW_WIDTH * 0.45) and \
                (WINDOW_HEIGHT * 0.5 <= y_mouse_coord <= WINDOW_HEIGHT * 0.6):
            import Main_Code
        elif (WINDOW_WIDTH * 0.54 >= x_mouse_coord >= WINDOW_WIDTH * 0.46) and \
                (WINDOW_HEIGHT * 0.6 <= y_mouse_coord <= WINDOW_HEIGHT * 0.75):

            os._exit(0)


def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutInitWindowPosition(0, 0)
    glutCreateWindow("Breaking Out Game")
    load_textures()
    glutDisplayFunc(display_2)
    glutMouseFunc(mouse_callback)
    init()
    glutMainLoop()


main()
