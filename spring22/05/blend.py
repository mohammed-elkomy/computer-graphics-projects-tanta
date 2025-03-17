from OpenGL.GL import *
from OpenGL.GLUT import *
import pygame
######################################################## CONSTANTSSSS
WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080
FONT_DOWNSCALE = 0.3251
GRAVITY_ACC = -9.8

LOSE = False
Time = 5


WINNING_CONDITION = 3
DOG_RESULT = WINNING_CONDITION
CAT_RESULT = WINNING_CONDITION
CURRENT_TURN = "DOG"

## Dimensions must be relative to the window's dimensions
PLAYER_WIDTH = WINDOW_WIDTH//6
PLAYER_HEIGHT = WINDOW_HEIGHT//5
BALL_SIZE = ((50*(WINDOW_WIDTH)/800) + ((50*(WINDOW_HEIGHT)/600)))/2



"""
Texture steps (init)
1) glEnable(GL_TEXTURE_2D)
2) pygame.image.load("1.png")
3) pygame.image.tostring(image, "RGBA", True)
4) glGenTextures(len(images), texture_names) # create identifiers for textures
5) glBindTexture(GL_TEXTURE_2D, texture_name) # modify THIS IDENTIFIER
6) glTexParameterf (many of those) # set the parameters
7) glTexImage2D # feed the binary image to opengl
              (Usage)
1) glBindTexture(GL_TEXTURE_2D, texture_name) # use THIS IDENTIFIER
2) glTexCoord(0, 0) repeat this
"""

"""
TO enable texture transparency
1) set the third parameter in glTexImage2D to GL_RGBA
2) make sure to use "RGBA" >>> pygame.image.tostring(image, "RGBA", True) here
3) make sure GL_RGBA is the 7th parameter
4)  glEnable(GL_BLEND) 
"""


def Texture_init():
    loadTextures()
    glEnable(GL_BLEND)  # FOR BLENDING
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)  # FOR BLENDING


texture_names = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]  # TODO IMPORTANT must be numbers


def texture_setup(texture_image_binary, texture_name, width, height):
    """  Assign texture attributes to specific images.
    """

    glBindTexture(GL_TEXTURE_2D, texture_name)  # texture init step [5]

    # texture init step [6]
    # affects the active selected texture which is identified by texture_name
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)  # GL_MIRRORED_REPEAT , GL_CLAMP_TO_EDGE, GL_CLAMP_TO_BORDER
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    # END: texture init step [6]

    glTexImage2D(GL_TEXTURE_2D,
                 0,  # mipmap
                 GL_RGBA,  # FOR BLENDING
                 width, height,
                 0,  # Texture border
                 GL_RGBA,
                 GL_UNSIGNED_BYTE,
                 texture_image_binary)  # texture init step [7]
    glBindTexture(GL_TEXTURE_2D, -1)  # texture init step [5]



def loadTextures():
    """  Open images and convert them to "raw" pixel maps and
             bind or associate each image with and integer refernece number.
    """
    glEnable(GL_TEXTURE_2D)  # texture init step [1]
    # Load images from file system
    images = []  # texture init step [2]
    images.append(pygame.image.load("bg1 - Copy.jpg"))      # 0

    images.append(pygame.image.load("DOG.png"))             # 01
    images.append(pygame.image.load("DOG_preparing.png"))   # 02
    images.append(pygame.image.load("DOG_Throw.png"))       # 03
    images.append(pygame.image.load("Bone.png"))            # 04

    images.append(pygame.image.load("CAT.png"))             # 05
    images.append(pygame.image.load("CAT_preparing.png"))   # 06
    images.append(pygame.image.load("CAT_Throw.png"))       # 07
    images.append(pygame.image.load("Can.png"))             # 08

    images.append(pygame.image.load("midWall.png"))         # 09
    images.append(pygame.image.load("Start.png"))           # 10
    images.append(pygame.image.load("StartText.png"))       # 11

    # Convert images to the type needed for textures
    textures = [pygame.image.tostring(image, "RGBA", True)
                for image in images]  # texture init step [3]

    # Generate textures names from array
    glGenTextures(len(images), texture_names)  # texture init step [4]

    # Add textures to openGL
    for i in range(len(images)):
        texture_setup(textures[i],  # binary images
                      texture_names[i],  # identifiers
                      images[i].get_width(),
                      images[i].get_height())




################################################# RECTANGLE CLAAAAAASSSSS

class Rectangle:
    global DOG, CAT
    def __init__(self, right, left, top, bottom):
        self.top = top
        self.bottom = bottom
        self.right = right
        self.left = left
        self.X = (left + right) / 2
        self.Y = (top + bottom) / 2

    def draw_rect(self, color, type):   # Draw a normal Rectangle
        glColor(color[0], color[1], color[2], color[3])
        glBegin(type)
        glVertex(self.left, self.bottom, 0)
        glVertex(self.right, self.bottom, 0)
        glVertex(self.right, self.top, 0)
        glVertex(self.left, self.top, 0)
        glEnd()

    def draw_rect_tex(self, texture_name):  #Draw a Rectangle with Texture
        glColor(1,1,1,1)
        glBindTexture(GL_TEXTURE_2D, texture_name)
        glBegin(GL_POLYGON)

        glTexCoord(0, 0)
        glVertex2d(self.left, self.bottom)

        glTexCoord(1, 0)
        glVertex2d(self.right, self.bottom)

        glTexCoord(1, 1)
        glVertex2d(self.right, self.top)

        glTexCoord(0, 1)
        glVertex2d(self.left, self.top)
        glEnd()
        glBindTexture(GL_TEXTURE_2D, -1)


    def refresh(self):     #  Manually Refresh the values of X and Y after changing any of the 4 attributes
        self.X = (self.left + self.right) / 2
        self.Y = (self.top + self.bottom) / 2

    def respawn(self, player):  # Method made only for the ball to Initialize the ball's position near one of the two players
        if player == "DOG":
            self.left = DOG.left
            self.bottom = DOG.top - BALL_SIZE//2
            self.right = self.left + BALL_SIZE
            self.top = self.bottom + BALL_SIZE
            self.X = (self.left + self.right) / 2
            self.Y = (self.top + self.bottom) / 2

        else:  ##CAT
            self.left = CAT.right - BALL_SIZE//2
            self.bottom = CAT.top
            self.top = self.bottom - BALL_SIZE
            self.right = self.left + BALL_SIZE
            self.X = (self.left + self.right) / 2
            self.Y = (self.top + self.bottom) / 2



##  DOG Object
DOG = Rectangle(0, 0, 0, 0)
DOG.left = WINDOW_WIDTH - WINDOW_WIDTH//6
DOG.bottom = 0
DOG.right = DOG.left + PLAYER_WIDTH
DOG.top = DOG.bottom + PLAYER_HEIGHT

## CAT Object
CAT = Rectangle(0, 0, 0, 0)
CAT.left = 0
CAT.bottom = 0
CAT.right = CAT.left + PLAYER_WIDTH
CAT.top = CAT.bottom + PLAYER_HEIGHT

## Middle Wall Obj
middle_wall = Rectangle(0, 0, 0, 0)
middle_wall.left = WINDOW_WIDTH // 2 - 50
middle_wall.bottom = 0
middle_wall.right = WINDOW_WIDTH // 2 + 50
middle_wall.top = WINDOW_HEIGHT // 2

## Ball Obj
ball = Rectangle(0, 0, 0, 0)
ball.respawn(CURRENT_TURN)