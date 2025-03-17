from math import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import pygame
import time
import tank_model

x_ = 0
_x = 0
forward1 = True
forward2 = True
INTERVAL = 5

texture_names = [1, 2, 3]
global start_time

flag_1 = False
flag_2 = False
##########################################


def init():
    load_textures()
    glEnable(GL_BLEND)
    glEnable(GL_DEPTH_TEST)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-15, 15, -10, 10, 1, 30)  # ===>(1)
    glMatrixMode(GL_MODELVIEW)


def reposition_camera():
    gluLookAt(0, 0, 5, 0, 0, -1, 0, 1, 0)      # ===>(1)


def texture_setup(texture_image_binary, texture_name, width, height):
    """  Assign texture attributes to specific images.
    """
    glBindTexture(GL_TEXTURE_2D, texture_name)  # texture init step [5]

    # texture init step [6]
    # affects the active selected texture which is identified by texture_name
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    # END: texture init step [6]

    glTexImage2D(GL_TEXTURE_2D,
                 0,
                 3,
                 width, height,
                 0,  # Texture border
                 GL_RGBA,  # RGBA Exactly as in  pygame.image.tostring(image, "RGBA", True)
                 GL_UNSIGNED_BYTE,
                 texture_image_binary)  # texture init step [7]
    glBindTexture(GL_TEXTURE_2D, -1)


def load_textures():
    """  Open images and convert them to "raw" pixel maps and
             bind or associate each image with and integer reference number.
    """
    global texture_names
    glEnable(GL_TEXTURE_2D)  # texture init step [1]
    # Load images from file system
    images = []   # texture init step [2]
    images.append(pygame.image.load("op.jpeg"))  # repeat this for more images
    images.append(pygame.image.load("poster.jpg"))
    images.append(pygame.image.load("end_game.jpg"))

    # Convert images to the type needed for textures
    textures = [pygame.image.tostring(image, "RGBA", True)  # TODO change True to False
                for image in images]  # texture init step [3]

    # Generate textures names from array
    glGenTextures(len(images), texture_names[0])  # texture init step [4]

    # Add textures to openGL
    for i in range(len(images)):
        texture_setup(textures[i],  # binary images
                      texture_names[i],  # identifiers
                      images[i].get_width(),
                      images[i].get_height())


def background(i_d, dx, dy, dz):
    global texture_names
    glLoadIdentity()
    reposition_camera()
    glColor3f(1, 1, 1)
    glTranslate(dx, dy, dz)
    glScale(30, 20, 1)
    glBindTexture(GL_TEXTURE_2D, texture_names[i_d])
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)
    glVertex3f(-0.5, -0.5, 0)

    glTexCoord2f(1, 0)
    glVertex3f(0.5, -0.5, 0)

    glTexCoord2f(1, 1)
    glVertex3f(0.5, 0.5, 0)

    glTexCoord2f(0, 1)
    glVertex3f(-0.5, 0.5, 0)

    glEnd()
    glBindTexture(GL_TEXTURE_2D, -1)


def clouds(loc_x, loc_y, loc_z):
    glLoadIdentity()
    reposition_camera()
    glColor3ub(232, 232, 232)
    glTranslate(loc_x, loc_y, loc_z)
    glScale(1.5, 1, 1)
    resolution = 1
    glBegin(GL_POLYGON)
    for i0 in range(0, 360, resolution):
        x0 = cos(i0 * pi / 180)
        y0 = sin(i0 * pi / 180)
        glVertex2d(x0, y0)
    glEnd()
    glBegin(GL_POLYGON)
    for i1 in range(0, 360, resolution):
        x1 = cos(i1 * pi / 180) + 1.2
        y1 = sin(i1 * pi / 180)
        glVertex2d(x1, y1)
    glEnd()
    glBegin(GL_POLYGON)
    for i2 in range(0, 360, resolution):
        x2 = cos(i2 * pi / 180) + 1.2
        y2 = sin(i2 * pi / 180) - 1.6
        glVertex2d(x2, y2)
    glEnd()
    glBegin(GL_POLYGON)
    for i3 in range(0, 360, resolution):
        x3 = cos(i3 * pi / 180)
        y3 = sin(i3 * pi / 180) - 1.6
        glVertex2d(x3, y3)
    glEnd()
    glBegin(GL_POLYGON)
    for i4 in range(0, 360, resolution):
        x4 = cos(i4 * pi / 180) - 0.8
        y4 = 1.2*sin(i4 * pi / 180) - 0.8
        glVertex2d(x4, y4)
    glEnd()
    glBegin(GL_POLYGON)
    for i5 in range(0, 360, resolution):
        x5 = cos(i5 * pi / 180) + 1.8
        y5 = 1.2 * sin(i5 * pi / 180) - 0.8
        glVertex2d(x5, y5)
    glEnd()


def small_cube(loc_x, loc_y, loc_z):
    glLoadIdentity()
    reposition_camera()
    glColor3ub(192, 192, 192)
    glTranslate(loc_x, loc_y, loc_z)
    glScale(0.6, 0.8, 1.1)
    glutSolidCube(1)


def power(translate, scale, color):    # it is decay with boom
    glLoadIdentity()
    reposition_camera()
    glColor3ub(color[0], color[1], color[2])
    glTranslate(translate[0], translate[1], translate[2])
    glScale(scale[0], scale[1], scale[2])
    glutSolidCube(1)


def health_bar_1():
    global flag_1
    if tank_model.player_health_1 == 100:
        health_color = [255, 0, 0]
        translate = [9.5, 9, 0]
        scale = [10, 1, 1]
        power(translate, scale, health_color)
    elif tank_model.player_health_1 == 75:
        health_color = [200, 0, 0]
        translate = [10.75, 9, 0]
        scale = [7.5, 1, 1]
        power(translate, scale, health_color)
    elif tank_model.player_health_1 == 50:
        health_color = [150, 0, 0]
        translate = [12, 9, 0]
        scale = [5, 1, 1]
        power(translate, scale, health_color)
    elif tank_model.player_health_1 == 25:
        health_color = [100, 0, 0]
        translate = [13.25, 9, 0]
        scale = [2.5, 1, 1]
        power(translate, scale, health_color)
    else:
        health_color = [0, 0, 0]
        translate = [0, 0, 0]
        scale = [0, 0, 0]
        power(translate, scale, health_color)
        flag_1 = True


def health_bar_2():
    global flag_2
    if tank_model.player_health_2 == 100:
        health_color = [255, 0, 0]
        translate = [-9.5, 9, 0]
        scale = [10, 1, 1]
        power(translate, scale, health_color)
    elif tank_model.player_health_2 == 75:
        health_color = [200, 0, 0]
        translate = [-10.75, 9, 0]
        scale = [7.5, 1, 1]
        power(translate, scale, health_color)
    elif tank_model.player_health_2 == 50:
        health_color = [150, 0, 0]
        translate = [-12, 9, 0]
        scale = [5, 1, 1]
        power(translate, scale, health_color)
    elif tank_model.player_health_2 == 25:
        health_color = [100, 0, 0]
        translate = [-13.25, 9, 0]
        scale = [2.5, 1, 1]
        power(translate, scale, health_color)
    else:
        health_color = [0, 0, 0]
        translate = [0, 0, 0]
        scale = [0, 0, 0]
        power(translate, scale, health_color)
        flag_2 = True


def play_song():
    pygame.mixer.init()  # Format the sound library
    pygame.mixer.music.load("sound_game.mp3")    # Download audio file
    pygame.mixer.music.play(-1)   # Play the audio file


def game_timer(v):
    draw()
    print(v)
    glutTimerFunc(INTERVAL, game_timer, 1)


def draw():
    global x_    # for rectangle
    global _x    # for clouds
    global forward1   # for rectangle
    global forward2   # for clouds
    global start_time
    ##################################################
    glClearColor(0, 55, 55, 1)  # color of background
    glClear(GL_COLOR_BUFFER_BIT)
    glClear(GL_DEPTH_BUFFER_BIT)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    # Enable alpha testing to discard fragments with low alpha values
    glEnable(GL_ALPHA_TEST)
    glAlphaFunc(GL_GREATER, 0.1)  # Adjust threshold as needed
    # Display poster for 1.5 seconds
    if time.time() - start_time < 1.5:
        background(1, 0, 0, 0)
    elif flag_1:
        background(2, 0, 0, 0)
    elif flag_2:
        background(2, 0, 0, 0)
    else:
        glLoadIdentity()
        reposition_camera()
        ##################################################
        glLoadIdentity()
        reposition_camera()
        glColor3ub(24, 125, 54)
        glTranslate(0, -9.5, 0)
        glScale(30, 1, 30)
        glutSolidCube(1)  # green floor
        ##################################################
        glLoadIdentity()
        reposition_camera()
        tank_model.draw_1()  # right tank
        tank_model.draw_2()  # left tank
        ##################################################
        glLoadIdentity()
        reposition_camera()
        glColor3ub(77, 77, 77)
        glTranslate(0, -3.37, 0)
        glScale(1, 10, 30)
        glutSolidCube(1)  # long black dam
        ##################################################
        glLoadIdentity()
        reposition_camera()
        glColor3ub(77, 77, 77)
        glTranslate(0, -8.68, 0)
        glScale(1.5, 0.65, 30)
        glutSolidCube(1)  # the base of dam
        ##################################################
        clouds(-11.75 + _x, 5, -6)  # left cloud
        clouds(2 + _x, 7.5, -6)  # middle cloud
        clouds(11 + _x, 6.5, -6)  # right cloud
        ##################################################
        glLoadIdentity()
        reposition_camera()
        glColor3ub(255, 0, 0)
        glTranslate(9.5, 9, 0)
        glScale(10, 1, 1)
        glutWireCube(1)  # right constant rectangle
        ##################################################
        glLoadIdentity()
        reposition_camera()
        glColor3ub(255, 0, 0)
        glTranslate(-9.5, 9, 0)
        glScale(10, 1, 1)
        glutWireCube(1)  # left constant rectangle
        ##################################################
        glLoadIdentity()
        reposition_camera()
        glColor3ub(128, 72, 71)
        glTranslate(3 + x_, 4, 0)
        glScale(5.5, 1, 1)
        glutSolidCube(1)  # the cube that contain the three small cubes
        ##################################################
        small_cube(3 + x_, 4, 0)  # middle small cube
        small_cube(3.7 + x_, 4, 0)  # right small cube
        small_cube(2.3 + x_, 4, 0)  # left small cube
        ##################################################
        health_bar_1()
        health_bar_2()
        background(0, 0, 0, -15)
        ##################################################
    glutSwapBuffers()
    #################################################################
    if forward1:             # motion of rectangle that contain three cubes
        x_ = x_ + 0.05
    else:
        x_ = x_ - 0.05
    if x_ >= 9.25:
        forward1 = False
    if x_ <= -15.25:
        forward1 = True
    #################################################################
    if forward2:               # motion of clouds
        _x = _x + 0.035
    else:
        _x = _x - 0.035
    if _x >= 3:
        forward2 = False
    if _x <= -3:
        forward2 = True
    #################################################################


if __name__ == "__main__":
    glutInit()
    play_song()
    start_time = time.time()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    screen = glutInitWindowSize(1250, 700)
    glutInitWindowPosition(0, 0)
    glutCreateWindow(b'Tanks war')
    glutDisplayFunc(draw)
    glutTimerFunc(INTERVAL, game_timer, 1)
    glutKeyboardFunc(tank_model.key_pressed)
    glutPassiveMotionFunc(tank_model.mouse_click)
    init()
    glutMainLoop()
