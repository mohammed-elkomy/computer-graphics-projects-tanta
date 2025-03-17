from OpenGL.GL import *
from OpenGL.GLUT import *
import pygame
import scenes

pygame.init()
pygame.mixer.init()
mouse = pygame.mixer.Sound("sounds/click.mp3")

flag = True


def init():
    glClearColor(1.0, 1.0, 1.0, 0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    loadTextures()
    glEnable(GL_BLEND)  # FOR BLENDING
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)  # FOR BLENDING
    glMatrixMode(GL_MODELVIEW)


texture_names = [0, 1, 2]


def texture_setup(texture_image_binary, texture_name, width, height):
    glBindTexture(GL_TEXTURE_2D, texture_name)
    # affects the active selected texture which is identified by texture_name
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexImage2D(GL_TEXTURE_2D,
                 0,  # mipmap
                 GL_RGBA,  # FOR BLENDING
                 width, height, 0,  # Texture border
                 GL_RGBA,  # RGBA Exactly as in  pygame.image.tostring(image, "RGBA", True)
                 GL_UNSIGNED_BYTE, texture_image_binary)


def loadTextures():
    glEnable(GL_TEXTURE_2D)
    # Load images from file system
    images = []
    images.append(pygame.image.load("textures/BGFINISH.png"))
    images.append(pygame.image.load("textures/PLAY3.jpg"))
    images.append(pygame.image.load("textures/QUIT3.jpg"))

    # Convert images to the type needed for textures
    textures = [pygame.image.tostring(image, "RGBA", True) for image in images]

    # Generate textures names from array
    glGenTextures(len(images), texture_names)

    # Add textures to openGL
    for i in range(len(images)):
        texture_setup(textures[i],  # binary images
                      texture_names[i],  # identifiers
                      images[i].get_width(), images[i].get_height())


def draw():
    glClear(GL_COLOR_BUFFER_BIT)

    glColor3f(1, 1, 1)
    glPushMatrix()
    glBindTexture(GL_TEXTURE_2D, texture_names[0])  # background
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

    glBindTexture(GL_TEXTURE_2D, texture_names[1])  # play
    glBegin(GL_QUADS)
    glTexCoord2f(0, 1)
    glVertex2d(-0.15782, 0.30415)

    glTexCoord2f(1, 1)
    glVertex2d(0.15179, 0.30415)

    glTexCoord2f(1.0, 0)
    glVertex2d(0.15179, 0.17345)

    glTexCoord2f(0, 0)
    glVertex2d(-0.15782, 0.17345)

    glEnd()

    glBindTexture(GL_TEXTURE_2D, texture_names[2])  # quit
    glBegin(GL_QUADS)
    glTexCoord2f(0, 1)
    glVertex2d(-0.15782, -0.08078)

    glTexCoord2f(1, 1)
    glVertex2d(0.15179, -0.08078)

    glTexCoord2f(1.0, 0)
    glVertex2d(0.15179, -0.21148)

    glTexCoord2f(0, 0)
    glVertex2d(-0.15782, -0.21148)

    glEnd()
    glPopMatrix()
    glFlush()


def handle_mouse_click(button, state, x, y):
    global flag

    normalized_x = (x / glutGet(GLUT_WINDOW_WIDTH)) * 2 - 1
    normalized_y = -((y / glutGet(GLUT_WINDOW_HEIGHT)) * 2 - 1)

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN and flag is True:
        if -0.15782 < normalized_x < 0.15179 and 0.17345 < normalized_y < 0.30415:  # you clicked on play
            glLoadIdentity()
            print("You clicked on play!")
            mouse.play()
            glClear(GL_COLOR_BUFFER_BIT)
            glutIdleFunc(scenes.main())

        elif -0.15782 < normalized_x < 0.15179 and -0.21148 < normalized_y < -0.08078:  # you clicked on quit
            mouse.play()
            print("You clicked on quit!")
            glutTimerFunc(300, exit, 0)

    flag = False  # deactivates handle click mouse on play & quit


if __name__ == "__main__":
    glutInit()
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(1280, 720)
    glutCreateWindow(b"Super Duck")
    init()
    glutDisplayFunc(draw)
    glutMouseFunc(handle_mouse_click)
    glutMainLoop()
