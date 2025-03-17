from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
from PIL import Image

class image_to_array:

    def generateMap(self , filename):
        with Image.open(filename).convert('L') as img:
            width, height = img.size
            pixels = img.load()
            array = [[1 if pixels[x, y] < 128 else 0 for x in range(width)] for y in range(height)]
        return array