from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import pygame
import Global as G

def texture_setup(texture_image_string, texture_name, width, height):
    glBindTexture(GL_TEXTURE_2D, texture_name)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, 
                GL_UNSIGNED_BYTE, texture_image_string)
    
def load_textures():
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA,GL_ONE_MINUS_SRC_ALPHA)

    for path in G.paths: #  0  1  2  3  4  5  
        G.images.append(pygame.image.load(path))
    for stand in G.man_stand: #  6   7
        G.images.append(pygame.image.load(stand))
    for jump in G.man_jump: # 8     9
        G.images.append(pygame.image.load(jump))
    for right in G.man_path_right: # 10  11  12  13
        G.images.append(pygame.image.load(right))
    for left in G.man_path_left: # 14  15  16  17
        G.images.append(pygame.image.load(left))
    for fall in G.man_fall: # 18  19
        G.images.append(pygame.image.load(fall))

    for image in G.images:
        G.textures.append(pygame.image.tostring(image, "RGBA", True))
    
    glGenTextures(len(G.images),G.names)
    
    for i in range(len(G.images)):
        texture_setup(G.textures[i], G.names[i], G.images[i].get_width(), G.images[i].get_height())