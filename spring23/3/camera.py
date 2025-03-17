from pyrr import Vector3, vector3
from math import sin, cos, radians
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from grenades import *


class Camera:
    def __init__(self, width=900, height=800):
        self.locations = []
        self.camera_pos = Vector3([0.0, 0.0, 2.0])
        self.camera_front = Vector3([1.0, 0.0, 0.0])
        self.camera_right = Vector3([1.0, 0.0, 0.0])

        self.jaw = 0  # mouse in x

        self.pitch = 0  # mouse in y
        self.throw_direction = self.camera_front
        self.throw_avillable = True  # flag for grenade

        self.WIDTH, self.HEIGHT = width, height
        self.lastX, self.lastY = 0, 0

        self.look_up = False  # flag for h key
        self.angle = 90
        self.step = 0.0
        self.forward = False
        self.mouseAvaillabe = False  # if true --> the mouse is showing
        self.flag = "start"
        self.grenades = []

    # takes the changes of mouse positions and adjust it to the camera movement
    def process_mouse_movement(self, xoffset, yoffset, constrain_pitch=True):
        if constrain_pitch:
            if self.pitch > 80:
                self.pitch = 80
            if self.pitch < -30:
                self.pitch = -30
        self.jaw += xoffset
        self.pitch -= yoffset

        front = Vector3([0.0, 0.0, 0.0])
        front.x = cos(radians(self.jaw)) * cos(radians(self.pitch))
        front.y = sin(radians(self.pitch))
        front.z = sin(radians(self.jaw)) * cos(radians(self.pitch))

        self.camera_front = front
        self.camera_right = vector3.cross(self.camera_front, Vector3([0.0, 1.0, 0.0]))

    # Camera method for the W,A,S,D keyboard movement
    def collission(self, new_pos):
        location = [new_pos[0], new_pos[2]]
        for X in self.locations:
            if X[0] - 1.15 < location[0] and X[0] + 1.15 > location[0]:
                if X[1] - 1.15 < location[1] and X[1] + 1.15 > location[1]:
                    return True
        return False

    def process_keyboard(self, direction, velocity):
        if direction == "FORWARD":
            new_pos = self.camera_pos + self.camera_front * velocity
            self.step = self.step + (.1 if self.forward else -.1)

            if not self.collission(new_pos):
                self.camera_pos += self.camera_front * velocity
            self.angle = - self.jaw + 90
            self.throw_direction = self.camera_front
        if direction == "BACKWARD":
            new_pos = self.camera_pos - self.camera_front * velocity
            self.step = self.step + (0.1 if self.forward else -.1)

            if not self.collission(new_pos):
                self.camera_pos -= self.camera_front * velocity
            self.angle = -self.jaw - 90
            self.throw_direction = -self.camera_front
        if direction == "LEFT":
            new_pos = self.camera_pos - self.camera_right * velocity
            self.step = self.step + (0.1 if self.forward else -.1)

            if not self.collission(new_pos):
                self.camera_pos -= self.camera_right * velocity
            self.angle = -self.jaw + 180
            self.throw_direction = -self.camera_right  # left = - right
        if direction == "RIGHT":
            new_pos = self.camera_pos + self.camera_right * velocity
            self.step = self.step + (0.1 if self.forward else -.1)
            if not self.collission(new_pos):
                self.camera_pos += self.camera_right * velocity
            self.angle = -self.jaw + 180 + 180
            self.throw_direction = self.camera_right

        if self.step >= .7:
            self.forward = False
        if self.step <= -.7:
            self.forward = True

    def fix_cursor_out(self):
        self.lastX = int(self.WIDTH / 2)
        self.lastY = int(self.HEIGHT / 2)
        glutWarpPointer(self.lastX, self.lastY)

    # determine the change in mouse movement and updates the
    def mouse_look_clb(self, xpos, ypos):
        if self.mouseAvaillabe == False:
            if self.lastX == 0 and self.lastY == 0:
                self.lastX = int(self.WIDTH / 2)
                self.lastY = int(self.HEIGHT / 2)
                # x and y mouse position related to window's origin
                glutWarpPointer(self.lastX, self.lastY)

            xoffset = xpos - self.lastX  # updates the distance of mouse movement in x and y
            yoffset = self.lastY - ypos

            self.lastX = xpos
            self.lastY = ypos
            self.process_mouse_movement(xoffset, yoffset)
            self.fix_cursor_out()

    def throw(self, key, x, y):  # grenade throw
        if key == b' ':  # space
            self.throw_avillable = True  # controls the grenades

    def keyboard(self, key, x, y):
        global grenades
        if key == b'w':
            self.process_keyboard("FORWARD", 0.1)
        if key == b'd':
            self.process_keyboard("RIGHT", 0.1)
        if key == b'a':
            self.process_keyboard("LEFT", 0.1)
        if key == b's':
            self.process_keyboard("BACKWARD", 0.1)
        if key == b'h':
            self.look_up = not self.look_up  # to look at the maze from above
        if key == b' ':
            if self.throw_avillable == True:  # if working
                self.grenades.append(Grenades(self))  # make a grenade
                self.throw_avillable = False  # turn it off
        if key == b'p':
            self.flag = "play"
        if key == b'q':  # turns off the program
            os._exit(0)
        if key == b'\x1b':  # escape esc # to show the pointer from the program
            glutSetCursor(GLUT_CURSOR_LEFT_ARROW)
            self.mouseAvaillabe = True

        print(key)

    def setup_camera(self):
        if self.look_up == True:  # if i press h
            gluLookAt(1, 10, 1,
                      6, 0, 6,
                      0, 1, 0)
        else:
            gluLookAt(self.camera_pos[0] - self.camera_front[0], self.camera_front[1], self.camera_pos[2] - self.camera_front[2],
                      self.camera_pos[0] - .03, -0.2, self.camera_pos[2] - .03,
                      0, 1, 0)

    def activeMouse(self):  
        glutSetCursor(GLUT_CURSOR_NONE)
        self.lastX = int(self.WIDTH / 2)
        self.lastY = int(self.HEIGHT / 2)
        glutWarpPointer(self.lastX, self.lastY)
        self.mouseAvaillabe = False
