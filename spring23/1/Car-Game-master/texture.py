import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


#creating a list of texture names that will be used to identify each texture.
texture_names = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22]

# assigning a unique integer identifier to each texture using global constants, which makes it easier to refer to textures throughout the code.
STAR = 0
CAR = 1
HEALTH = 2
EXIT_RED = 3
EXIT_YELLOW = 4
START_RED = 5
START_YELLOW = 6
START_SCREEN = 7
CREDIT_SCREEN = 8
CREDIT_RED = 9
CREDIT_YELLOW = 10
BACK_YELLOW = 11
BACK_RED = 12
BOMB = 13
PLAY_AGAIN = 14
TRY_AGAIN_YEL = 15
TRY_AGAIN_RED = 16
EXIT2_YEL = 17
EXIT2_RED = 18
FINISH_LINE = 19
YOU_WIN = 20
HOME_YEL = 21
HOME_RED = 22

def load_texture():
    """
    enables 2D texture mapping for OpenGL, loads all the texture images and stores them as a list of texture binary data.
    It then generates a unique texture name for each image and sets up the texture parameters for each texture using the setup_texture() function.
    """
    glEnable(GL_TEXTURE_2D)

    images = []

    # Load images from files
    images.append(pygame.image.load("texture/star.png"))
    images.append(pygame.image.load("texture/car.png"))
    images.append(pygame.image.load("texture/health.png"))
    images.append(pygame.image.load("texture/exit_red.png"))
    images.append(pygame.image.load("texture/exit_yellow.png"))
    images.append(pygame.image.load("texture/start_red.png"))
    images.append(pygame.image.load("texture/start_yellow.png"))
    images.append(pygame.image.load("texture/start_screen.png"))
    images.append(pygame.image.load("texture/credits.png"))
    images.append(pygame.image.load("texture/credits_red.png"))
    images.append(pygame.image.load("texture/credits_yellow.png"))
    images.append(pygame.image.load("texture/back_yellow.png"))
    images.append(pygame.image.load("texture/back_red.png"))
    images.append(pygame.image.load("texture/bomb.png"))
    images.append(pygame.image.load("texture/game_over.png"))
    images.append(pygame.image.load("texture/try_again_yellow.png"))
    images.append(pygame.image.load("texture/try_again_red.png"))
    images.append(pygame.image.load("texture/exit2_yellow.png"))
    images.append(pygame.image.load("texture/exit2_red.png"))
    images.append(pygame.image.load("texture/finish_line.jpg"))
    images.append(pygame.image.load("texture/you_win.png"))
    images.append(pygame.image.load("texture/Home_yel.png"))
    images.append(pygame.image.load("texture/Home_red.png"))

    # Convert the images to raw binary image data
    textures = [pygame.image.tostring(img,"RGBA", 1) for img in images]

    # Generate texture IDs
    glGenTextures(len(images), texture_names)

    # Bind each texture and set texture parameters
    for i in range(len(images)):
        setup_texture(textures[i],
                      texture_names[i],
                      images[i].get_width(),
                      images[i].get_height())
        
def setup_texture(binary_img, texture_iden, width, height):
    """
    binds the texture to the texture identifier, sets texture parameters, and then loads the texture binary data.
    """
    glBindTexture(GL_TEXTURE_2D, texture_iden)

    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width,
                 height, 0, GL_RGBA, GL_UNSIGNED_BYTE, binary_img)
        