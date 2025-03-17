from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import pygame


def drawText(string, x, y, scale=0.23):

    glLineWidth(4)
    glColor(0, 0, 0)
    glLoadIdentity()
    glTranslate(x, y, 0)
    glScale(scale, scale, 1)
    string = string.encode()
    for c in string:
        glutStrokeCharacter(GLUT_STROKE_MONO_ROMAN, c)


def drawTextWithOutline(string, x, y, outline_thickness=2, scale=0.23):
    # glPushMatrix()
    glLineWidth(outline_thickness)
    glColor(0, 0, 0)
    
    for dx in [-1, 1]:
        for dy in [-1, 1]:
            glLoadIdentity()
            glTranslate(x + dx * outline_thickness, y + dy * outline_thickness, 0)  
            glScale(0.23, 0.23, 1)
            if isinstance(string, str):
                string = string.encode()  # Conversion from Unicode string to byte string
            for c in string:  # Render character by character starting from the origin
                glutStrokeCharacter(GLUT_STROKE_MONO_ROMAN, c)

    glColor(1, 1, 1)
    glLoadIdentity()
    glTranslate(x, y, 0)  
    glScale(scale, scale, 1)
    if isinstance(string, str):
        string = string.encode()  # Conversion from Unicode string to byte string
    for c in string:  # Render character by character starting from the origin
        glutStrokeCharacter(GLUT_STROKE_MONO_ROMAN, c)


def loadTexture(image_path, texture_name):

    texture_id = glGenTextures(1, texture_name)
    imgload = pygame.image.load(image_path)
    img = pygame.image.tostring(imgload, "RGBA", 1)
    width = imgload.get_width()
    height = imgload.get_height()
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
    glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    gluBuild2DMipmaps(GL_TEXTURE_2D, 4, width, height, GL_RGBA, GL_UNSIGNED_BYTE, img)  

    return texture_id
