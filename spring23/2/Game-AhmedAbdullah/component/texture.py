import pygame

from OpenGL.GL import *

image_name = [
    'start.png',
    'background.png',
    'obstacle.jpeg',
    'heart.png',
    'fuel.png',
    'gameOver.png'
]
textureList = [0, 1, 2, 3, 4, 5]


class Texture:

    def init_textures(self):
        self.load_texture()
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    def load_texture(self):
        glEnable(GL_TEXTURE_2D)
        image_list = [pygame.image.load(f"assets/images/{image_name[i]}") for i in range(6)]
        textures = [pygame.image.tostring(image, "RGBA", True) for image in image_list]
        glGenTextures(len(image_list), textureList)
        for i in range(len(image_list)):
            self.texture_setup(textures[i],
                               i,
                               image_list[i].get_width(),
                               image_list[i].get_height())

    @staticmethod
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
                     texture_image_binary, )
        glBindTexture(GL_TEXTURE_2D, -1)
