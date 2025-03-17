from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import pygame
# from Rectangles import *



""" STEPS
    1. glEnable(GL_TEXTURE_2D)
    2. Load images
    3. to_string
    4. glGenTextures
    5. glBindTexture
    6. glTexParameterf
    7. glTexImage2D
    8. glBindTexture
    9. glTexCoord 
"""

"""textures:world , main car , 12 cars"""
textureIdentifiers = [i for i in range(21)]


def setupHelper(texture_string, textureIdentifier, width, height):
    glEnable(GL_BLEND)  # FOR BLENDING
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)  # FOR BLENDING

    glBindTexture(GL_TEXTURE_2D, textureIdentifier)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    gluBuild2DMipmaps(GL_TEXTURE_2D, GL_RGBA, width, height, GL_RGBA, GL_UNSIGNED_BYTE,texture_string)


def loadHelper(path, index):
    image = pygame.image.load(path)

    binaryImage = pygame.image.tostring(image, "RGBA", True)
    setupHelper(binaryImage, textureIdentifiers[index], image.get_width(), image.get_height())


def drawHelper1 (textureIndex, left, right, top, bottom):
    glBindTexture(GL_TEXTURE_2D, textureIdentifiers[textureIndex])
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex(left, bottom, 0.5)
    glTexCoord2f(1, 0.0)
    glVertex(right, bottom, 0.5)
    glTexCoord2f(1, 1)
    glVertex(right, top, 0.5)
    glTexCoord2f(0.0, 1)
    glVertex(left, top, 0.5)
    glEnd()
    glBindTexture(GL_TEXTURE_2D, -1)


def load_setup_textures():
    glEnable(GL_TEXTURE_2D)

    glGenTextures(len(textureIdentifiers), textureIdentifiers)
    # TODO: Load all textures here
    #
    loadHelper("World Assets/Final-Start-Screen.jpg", 14)
    loadHelper("World Assets/Start Button.png", 15)

    loadHelper("World Assets/Win Screen.png", 16)
    loadHelper("World Assets/Lose Screen.png", 17)
    loadHelper("World Assets/Level UP Button.png", 18)
    loadHelper("World Assets/Final Restart Button.png", 19)
    loadHelper("World Assets/Exit Button.png", 20)

    loadHelper("World Assets/porche_911.png", 1)
    loadHelper("World Assets/world.png", 0)

    loadHelper("World Assets/car-yellow.png", 2)
    loadHelper("World Assets/car-red.png", 3)
    loadHelper("World Assets/car-purple.png", 4)

    loadHelper("World Assets/car-purple-2.png", 5)
    loadHelper("World Assets/car-pink.png", 6)
    loadHelper("World Assets/car-orange.png", 7)

    loadHelper("World Assets/car-green.png", 8)
    loadHelper("World Assets/car-blue.png", 9)
    loadHelper("World Assets/car-red.png", 10)

    loadHelper("World Assets/car-purple-2.png", 11)
    loadHelper("World Assets/car-pink.png", 12)
    loadHelper("World Assets/car-orange.png", 13)


def drawTextures(color, world):
    # TODO: Draw all textures here [ WORLD , MAIN CAR , OTHER CARS(12)]
    glColor(color[0], color[1], color[2])
    drawHelper1(0, world.left, world.right, world.top, world.bottom)
