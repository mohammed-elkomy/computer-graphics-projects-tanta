from OpenGL.GL import *
from PIL.Image import open
import pygame


class Texture:

    def texture_setup(self, texture_image_binary, texture_name, width, height):
        glBindTexture(GL_TEXTURE_2D, texture_name)

        # texture init step [6]
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        # END: texture init step [6]

        glTexImage2D(GL_TEXTURE_2D,
                     0,  # mipmap
                     3,  # Bytes per pixel
                     width, height,
                     0,  # Texture border
                     GL_RGBA, GL_UNSIGNED_BYTE, texture_image_binary)  # texture init step [7]

    def load_and_setup(self, image_path, idx):
        # Load images from file system
        image = pygame.image.load(image_path)
        # Convert images to the type needed for textures
        texture = pygame.image.tostring(
            image, "RGBA", True)  # texture init step [3]
        self.texture_setup(texture, idx, image.get_width(), image.get_height())

    def load_textures(self):

        glEnable(GL_TEXTURE_2D)  # texture init step 1
        self.load_and_setup("textures/floor.jpg", 1)
        self.load_and_setup("textures/wall2.jpg", 2)
        self.load_and_setup("textures/phot.jpg", 3)
        self.load_and_setup("textures/side.jpg", 4)
        self.load_and_setup("textures/player/front head.png", 5)
        self.load_and_setup("textures/player/backhead.png", 6)
        self.load_and_setup("textures/player/righthead.png", 7)
        self.load_and_setup("textures/player/lefthead.png", 8)
        self.load_and_setup("textures/player/frontbody.png", 9)
        self.load_and_setup("textures/player/backbody.png", 10)
        self.load_and_setup("textures/player/rihgtarm.png", 11)
        self.load_and_setup("textures/player/leftarm.png", 12)
        self.load_and_setup("textures/player/front leg.png", 13)
        self.load_and_setup("textures/player/backoneleg.png", 14)
        self.load_and_setup("textures/player/right leg.png", 15)
        self.load_and_setup("textures/player/leftleg.png", 16)
        self.load_and_setup("textures/grenade.jpg", 17)
        self.load_and_setup("textures/sidegrenades.jpg", 18)
        self.load_and_setup("textures/win.jpg", 19)
        self.load_and_setup("textures/lose.jpg", 20)
        self.load_and_setup("textures/start.png", 21)
