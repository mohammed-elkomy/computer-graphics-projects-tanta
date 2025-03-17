from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from math import *
from texture import *
from numpy import sign
import pygame


class car:
    def __init__(self):
        """
        The __init__ method initializes the car's position and state attributes,
        as well as its physics attributes such as speed and acceleration.
        """
        # Coordinates
        self.left = 20
        self.bottom = 20
        self.right = 80
        self.top = 50
        
        # Car State
        self.health = 100
        self.coins = 0
        self.light = False
        # Car Pyhsics
        self.rot = 0  # is am rotating or not -->> can be 1 or -1
        self.rotAngle = 0  # what value of rotation
        self.currSpeed = 0  # 1 if 'w' or 's' else 0
        self.speed = 0     # to be increment
        self.forwardAcc = 0.02
        self.backwardAcc = -0.02
        # in case of inertia
        self.friction = -0.05
        self.collosion = False

    def draw(self):
        """
        This method uses the OpenGL library to draw the car onto the screen. It uses the texture module to apply a texture to the car.
        """
        glBindTexture(GL_TEXTURE_2D,CAR)
        glColor3f(1, 1, 1)
        glBegin(GL_POLYGON)
        glTexCoord(0,1)
        glVertex(self.left, self.top, 0)

        glTexCoord(0,0)
        glVertex(self.left, self.bottom, 0)

        glTexCoord(1,0)
        glVertex(self.right, self.bottom, 0)

        glTexCoord(1,1)
        glVertex(self.right, self.top, 0)
        glEnd()

        glBindTexture(GL_TEXTURE_2D, -1)

    def center(self):
        """
        This method calculates the center of the car, which is used in other methods to position and rotate it.
        """
        return [(self.right + self.left)/2, (self.top + self.bottom)/2]

    def animation(self):
        """
        This method updates the car's position and rotation based on its speed and any collision events.
        It also updates the car's rotation angle if the rot attribute is set.
        """
        if self.collosion:
            self.health -= int(10*abs(self.currSpeed)) # Health decrease proportoinal to currSpeed
            sign1 = 1 if self.currSpeed > 0 else -1
            self.currSpeed = -(self.currSpeed) - 0.15*sign1 # collsion in opposite direction
            self.speed = 0 # make final speed = 0
            self.collosion = False 
        
        # First of all we need to adjust rotation
        # To make car rotate around it self we need to do :
        # 1- Translate to Origin
        # 2- Rotate around z-Axis
        # 3- Translate Back
        glLoadIdentity()
        cen = self.center()
        glTranslate(cen[0], cen[1], 0)
        glRotate(self.rotAngle, 0, 0, 1)
        glTranslate(-cen[0], -cen[1], 0)
        #####################################
        # Now we need to adjust the Vertices
        theta = self.rotAngle*(pi/180)

        # Delta in y direction is proportional to Sin(theta) and currspeed
        # The greater currentspeed , the greater the shift
        self.top = self.top + sin(theta)*self.currSpeed
        self.bottom = self.bottom + sin(theta)*self.currSpeed

        # Delta in x direction is proportional to Cos(theta) and currspeed
        # The greater currentspeed , the greater the shift
        self.right = self.right + cos(theta)*self.currSpeed
        self.left = self.left + cos(theta)*self.currSpeed

        # Case 1 : if car has speed to be reaced
        if self.speed != 0:
            if abs(self.currSpeed - self.speed) <= 0.1:  # to avoid floating prection
                self.currSpeed = self.speed
            elif self.currSpeed < self.speed:
                self.currSpeed += self.forwardAcc
            elif self.currSpeed > self.speed:
                self.currSpeed += self.backwardAcc
        # Case 2 : Inertia
        elif self.speed == 0 and self.currSpeed != 0:
            if abs(self.currSpeed) <= 0.1:
                self.currSpeed = 0
            else:
                self.currSpeed += self.friction*sign(self.currSpeed)

        # We need to adjust rotAngle -->> if self.rot is active
        self.rotAngle += self.rot*self.currSpeed*0.5

    def load_texture(self):
        return
        
    def get_vertices(self):
        """
            This method calculates the four vertices of the car, which are used in collision detection.
            It first calculates the center of the car,
            then applies a rotation matrix to the vertices to adjust for the car's rotation.
        """
        # return type is a list
        # Step 1: Calculate the center of the car
        center = self.center()

        # Step 2: Calculate the four vertices of the car
        vertices = [
            [self.left, self.top],
            [self.left, self.bottom],
            [self.right, self.bottom],
            [self.right, self.top],
        ]

        # Steps 3-5: Move the car to the origin, rotate, and move back
        theta = radians(self.rotAngle)
        rot_matrix = [[cos(theta), -sin(theta)],
                      [sin(theta), cos(theta)]]

        rotated_vertices = []
        for vertex in vertices:
            # Move to origin
            moved_vertex = [vertex[0] - center[0], vertex[1] - center[1]]

            # Rotate around z-axis
            rotated_vertex = [0, 0]
            for i in range(2):
                for j in range(2):
                    rotated_vertex[i] += rot_matrix[i][j] * moved_vertex[j]

            # Move back
            rotated_vertex[0] += center[0]
            rotated_vertex[1] += center[1]
            rotated_vertices.append(rotated_vertex)


        # Step 6: Return the rotated vertices
        return rotated_vertices
