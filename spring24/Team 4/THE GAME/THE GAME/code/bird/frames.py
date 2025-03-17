import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import os

def init():
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glClearColor(1, 1, 1, 1)
    glMatrixMode(GL_PROJECTION)
    gluOrtho2D(-10.0, 50.0, -10.0, 50.0)
    glMatrixMode(GL_MODELVIEW)

# Load textures directly using OpenGL
texture_names = [i for i in range(0, 54)]
def texture_setup(texture_image_binary, texture_name, width, height):
    glBindTexture(GL_TEXTURE_2D, texture_name)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

    glTexImage2D(GL_TEXTURE_2D,
                 0,
                 GL_RGBA,
                 width, height,
                 0,
                 GL_RGBA,
                 GL_UNSIGNED_BYTE,
                 texture_image_binary)

def load_textures():
    global images
    glEnable(GL_TEXTURE_2D)
    # Load images from file system
    images = [pygame.image.load(os.path.join('', f'frame ({i}).png')) for i in range(1, 55)]

    # Convert images to the type needed for textures
    textures = [pygame.image.tostring(image, "RGBA", True) for image in images]

    # Generate texture names from array
    glGenTextures(len(images), texture_names)

    # Add textures to OpenGL
    for i in range(len(images)):
        texture_setup(textures[i], texture_names[i], images[i].get_width(), images[i].get_height())

current_frame = 0
bird_x_position = -10

def draw_bird():

    glBindTexture(GL_TEXTURE_2D, texture_names[current_frame])
    glPushMatrix()
    glTranslatef(bird_x_position, 40, 0)
    glScalef(4, 5.5, 1)

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

def draw_scene():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    draw_bird()
    glutSwapBuffers()

def timer_func(value):
    glutPostRedisplay()  # Trigger a redraw
    glutTimerFunc(50, timer_func, 0)  # Schedule the next redraw in 50 milliseconds

    # Update the current frame and bird position here if needed
    global current_frame, bird_x_position
    if current_frame + 1 < len(images):
        current_frame += 1
    else:
        current_frame = 0
    bird_x_position += 0.3  # Adjust the speed of movement

glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(1280, 720)
glutCreateWindow(b"Flying Birds Animation")
init()
load_textures()  # Load textures before entering the main loop
glutDisplayFunc(draw_scene)
glutTimerFunc(50, timer_func, 0)  # Start the timer for the initial redraw
glutMainLoop()

