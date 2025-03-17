from OpenGL.GL import *
from OpenGL.GLUT import *
import pygame
import level1

pygame.init()
pygame.mixer.init()
mom = pygame.mixer.Sound("sounds/mom.mp3")
conv = pygame.mixer.Sound("sounds/writing.mp3")


scene = 0


def my_init():
    loadTextures()
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)


texture_names = [0, 1, 2, 3]


def texture_setup(texture_image_binary, texture_name, width, height):
    glBindTexture(GL_TEXTURE_2D, texture_name)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_image_binary)


def loadTextures():
    glEnable(GL_TEXTURE_2D)
    images = []
    images.append(pygame.image.load("textures/duckwithchilds.png"))
    images.append(pygame.image.load("textures/alright_quacks.png"))
    images.append(pygame.image.load("textures/scene2.png"))
    images.append(pygame.image.load("textures/few_moments-removebg-preview.png"))
    textures = [pygame.image.tostring(image, "RGBA", True) for image in images]
    glGenTextures(len(images), texture_names)
    for i in range(len(images)):
        texture_setup(textures[i], texture_names[i], images[i].get_width(), images[i].get_height())


def draw():
    glClearColor(1, 1, 1, 1)
    glClear(GL_COLOR_BUFFER_BIT)

    glColor3f(1, 1, 1)  # IMPORTANT
    glPushMatrix()
    glBindTexture(GL_TEXTURE_2D, texture_names[0])  # draw back_ground
    glBegin(GL_QUADS)
    glTexCoord2f(0, 1)
    glVertex2d(-1, 1)

    glTexCoord2f(1, 1)
    glVertex2d(1, 1)

    glTexCoord2f(1, 0)
    glVertex2d(1, -1)

    glTexCoord2f(0, 0)
    glVertex2d(-1, -1)
    glEnd()

    glPopMatrix()
    glFlush()


def switch_scene1():  # alright quacks
    glPushMatrix()
    glBindTexture(GL_TEXTURE_2D, texture_names[1])
    glLoadIdentity()
    glTranslate(0.5, 0.6, 0)
    glScalef(2, 1, 1)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 1)
    glVertex2d(-0.70049, 0.30076)

    glTexCoord2f(1, 1)
    glVertex2d(-0.4, 0.3)

    glTexCoord2f(1.0, 0)
    glVertex2d(-0.4, 0.05)

    glTexCoord2f(0, 0)
    glVertex2d(-0.7, 0.05)

    glEnd()
    glPopMatrix()
    glFlush()


def switch_scene2():  # walk behind me
    glPushMatrix()
    glBindTexture(GL_TEXTURE_2D, texture_names[2])
    glLoadIdentity()
    glTranslate(0.3, 0.6, 0)
    glScalef(1.5, 1, 1)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 1)
    glVertex2d(-0.70049, 0.30076)

    glTexCoord2f(1, 1)
    glVertex2d(-0.4, 0.3)

    glTexCoord2f(1.0, 0)
    glVertex2d(-0.4, 0.05)

    glTexCoord2f(0, 0)
    glVertex2d(-0.7, 0.05)

    glEnd()
    glPopMatrix()
    glFlush()


def switch_scene3():  # Few moments
    glClearColor(1, 1, 1, 1)
    glClear(GL_COLOR_BUFFER_BIT)  # necessary

    glColor3f(1, 1, 1)
    glPushMatrix()
    glBindTexture(GL_TEXTURE_2D, texture_names[3])

    glScalef(.6, 0.6, 1)
    glBegin(GL_QUADS)

    glTexCoord2f(0, 1)
    glVertex2d(-1, 1)

    glTexCoord2f(1, 1)
    glVertex2d(1, 1)

    glTexCoord2f(1.0, 0)
    glVertex2d(1, -1)

    glTexCoord2f(0, 0)
    glVertex2d(-1, -1)

    glEnd()
    glPopMatrix()
    glFlush()


def handle_mouse_click(button, state, x, y):
    global scene
    # normalizing mouse coordinates:
    normalized_x = (x / glutGet(GLUT_WINDOW_WIDTH)) * 2 - 1
    normalized_y = -((y / glutGet(GLUT_WINDOW_HEIGHT)) * 2 - 1)

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN and -1 < normalized_x < 1 and -1 < normalized_y < 1:   # you clicked anywhere on screen
        if scene == 0:
            glLoadIdentity()
            glutDisplayFunc(switch_scene1)
            scene += 1
            conv.play(0, 4000, 0)
        elif scene == 1:
            glLoadIdentity()
            draw()
            glutDisplayFunc(switch_scene2)
            scene += 1

        elif scene == 2:
            glutDisplayFunc(switch_scene3)
            mom.play()
            scene += 1

        elif scene == 3:
            scene += 1
            level1.main()


def main():
    my_init()
    glutDisplayFunc(draw)  # first scene to be shown after clicking on play
    glutMouseFunc(handle_mouse_click)
    glutMainLoop()
