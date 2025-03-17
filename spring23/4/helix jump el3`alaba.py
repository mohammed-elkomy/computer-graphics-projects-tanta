from OpenGL.GL import *
from pygame import *
import pygame
from OpenGL.GLU import *
from OpenGL.GLUT import *
from math import *
import numpy as np
from random import *
import random

TEXTURE_NAMES = [0, 1, 2, 3, 4, 5, 6]
WINDOW_WIDTH = WINDOW_HEIGHT = 800
LEVEL_UP = False
y = 29.9
interval = 1
X = 0
v_velocity = 0
dtime = 0.0017
r_angle_safe = []
angle_air = []
r_angle_ball = 0
r_angle_glue = []

for _ in range(0, 25):
    r_angle_safe.append(0)
    r_angle_glue.append(0)
    angle_air.append(0)
lose = False
flag = True
c = y
SCORE = 0
START = 1
LEVEL = 1
sound_on = 1

pygame.mixer.init()
game_over_sound = pygame.mixer.Sound("gameover.wav")
Level_up_sound = pygame.mixer.Sound("levelup.wav")
hit = pygame.mixer.Sound("ball_hit.wav")
pygame.mixer.music.load("theme.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(.1)


def init_textures():
    load_textures()

    glEnable(GL_BLEND)  # FOR BLENDING
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)


def texture_setup(texture_image_binary, texture_name, width, height):
    """  Assign texture attributes to specific images.
    """
    glBindTexture(GL_TEXTURE_2D, texture_name)  # texture init step [5]

    # texture init step [6]
    # affects the active selected texture which is identified by texture_name
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T,
                    GL_REPEAT)  # GL_MIRRORED_REPEAT , GL_CLAMP_TO_EDGE, GL_CLAMP_TO_BORDER
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    # END: texture init step [6]

    glTexImage2D(GL_TEXTURE_2D,
                 0,  # mipmap
                 GL_RGBA,  # FOR BLENDING
                 width, height,
                 0,  # Texture border
                 GL_RGBA,  # RGBA Exactly as in  pygame.image.tostring(image, "RGBA", True)
                 GL_UNSIGNED_BYTE,
                 texture_image_binary)  # texture init step [7]


def load_textures():
    """  Open images and convert them to "raw" pixel maps and
             bind or associate each image with and integer reference number.
    """
    glEnable(GL_TEXTURE_2D)  # texture init step [1]

    # Load images from file system
    images = []  # texture init step [2]
    images.append(pygame.image.load("sky.png"))
    images.append(pygame.image.load("level_up.png"))
    images.append(pygame.image.load("game_over.png"))
    images.append(pygame.image.load("restart.png"))
    images.append(pygame.image.load("gonext.png"))
    images.append(pygame.image.load("start.png"))
    images.append(pygame.image.load("helix.png"))

    # textures list contains all images in the needed format for textures
    textures = [pygame.image.tostring(imagee, "RGBA", True)
                for imagee in images]  # texture init step [3]

    # Generate textures names from TEXTURE_NAMES list
    glGenTextures(len(images), TEXTURE_NAMES)  # texture init step [4]

    # Add textures to openGL
    for ii in range(len(images)):
        texture_setup(textures[ii],  # binary images
                      TEXTURE_NAMES[ii],  # identifiers
                      images[ii].get_width(),
                      images[ii].get_height())


def init_projection():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(35, 1, 1, 30)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glEnable(GL_DEPTH_TEST)


def init_camera():
    glLoadIdentity()

    gluLookAt(7 * sin(X), c, 7 * cos(X),
              0, c - 7, 0,
              0, 1, 0)


current_mouse_x = 0


def mouse_callback(x1, y1):
    global current_mouse_x, X
    current_mouse_x = x1
    current_mouse_x = current_mouse_x / WINDOW_WIDTH * 8 * pi
    if not lose and not LEVEL_UP:
        X = - current_mouse_x


def mouse2(button, state, x1, y1):
    if button == GLUT_LEFT_BUTTON and 245 <= x1 <= 557 and 644 <= y1 <= 754 and (START or lose or LEVEL_UP):
        restart()


def keyboard_callback(key1, x1, y1):
    global y, X
    if not lose:
        # if key1 == b"s":
        #     y -= .5
        # if key1 == b"w":
        #     y += .5
        if key1 == b"a":
            X -= .2
        if key1 == b"d":
            X += .2


def draw_3d_cylindrical(loc_y, theta1, theta2):
    glPushMatrix()
    glColor(1, 0, 0)
    glTranslate(0, loc_y, 0)
    glRotate(theta2, 0, 1, 0)
    resolution = .2
    glBegin(GL_QUAD_STRIP)
    x1 = 0
    z1 = 0

    for ang in np.arange(theta1, 2 * pi - theta1,
                         resolution):  # parametric form of a circle (r*cos(theta),r*sin(theta))
        x1 = 1 * sin(ang)  # pi / 180 from angle to rad
        z1 = 1 * cos(ang)  # pi / 180 from angle to rad

        glVertex3d(x1, 0, z1)
        glVertex3f(x1, -.15, z1)
    glEnd()
    glBegin(GL_QUADS)
    glVertex(sin(theta1), 0, cos(theta1))
    glVertex(sin(theta1), -.15, cos(theta1))
    glVertex(0, -.15, 0)
    glVertex(0, 0, 0)
    glEnd()
    glBegin(GL_QUADS)
    glVertex(0, -.15, 0)
    glVertex(0, 0, 0)
    # # glVertex(sin(2 * pi - theta1-.2), 0, cos(2 * pi - theta1-.2))
    # # glVertex(sin(2 * pi - theta1-.2), -.15, cos(2 * pi - theta1-.2))
    glVertex(x1, 0, z1)
    glVertex(x1, -.15, z1)
    glEnd()

    glPopMatrix()


def draw_Circular_sector(loc_y, theta1, theta2):
    glPushMatrix()
    glColor(1, 0, 0)
    glTranslate(0, loc_y, 0)
    glRotate(theta2, 0, 1, 0)
    glBegin(GL_POLYGON)
    resolution = .2
    if loc_y == 0:
        glColor3ub(0, 135, 95)
    if loc_y != 0:
        glVertex3d(0, 0, 0)
    for ang in np.arange(theta1, 2 * pi - theta1,
                         resolution):  # parametric form of a circle (r*cos(theta),r*sin(theta))
        x1 = 1 * sin(ang)  # pi / 180 from angle to rad
        z1 = 1 * cos(ang)  # pi / 180 from angle to rad
        glVertex3d(x1, 0, z1)  # 2 = coordL , d = float point NOT DIMENSION
    # if loc_y != 0:
    #     glVertex3d(0, 0, 0)
    glEnd()

    glPopMatrix()


def draw_cylinder(l1):
    glPushMatrix()

    glColor(1, 1, 1)
    # glTranslate(0, l1, 0)
    # glRotate(90, 1, 0, 0)
    glRotate(-90, 1, 0, 0)
    glutSolidCylinder(.5, l1, 50, 50)

    glPopMatrix()


def draw_sphere(x1, y1, r_angle):
    glPushMatrix()

    glColor(0, 0, 1)
    glTranslate(.8 * sin(x1), y1 + .07, .8 * cos(x1))

    glPushMatrix()

    glRotate(r_angle, 1, 1, 1)
    glutSolidSphere(.15, 30, 30)
    # glutSolidTeapot(.15) #todo try this

    glPopMatrix()
    glPopMatrix()


def game_timer(v):
    draw()
    # print(v)
    glutTimerFunc(interval, game_timer, v + 1)


def collision_detection():
    global LEVEL_UP
    global flag, lose
    if y <= 5.1:
        LEVEL_UP = True

    if y > 5:
        yy = floor(y) - 5
        if y - 5 <= yy + .07:
            # glue sector collision
            for ang in np.arange(3 - (.2 * LEVEL), 2 * pi - (3 - (.2 * LEVEL)), 0.005):
                x_check = round(sin(ang + (r_angle_safe[yy] + r_angle_glue[yy]) * pi / 180), 1) == round(sin(X), 1)
                z_check = round(cos(ang + (r_angle_safe[yy] + r_angle_glue[yy]) * pi / 180), 1) == round(cos(X), 1)
                if x_check and z_check:
                    lose = True
                    break
            # safe sector collision
            for ang in np.arange(angle_air[yy], 2 * pi - angle_air[yy], 0.005):
                x_check = round(sin(ang + r_angle_safe[yy] * pi / 180), 1) == round(sin(X), 1)
                z_check = round(cos(ang + r_angle_safe[yy] * pi / 180), 1) == round(cos(X), 1)
                if x_check and z_check:
                    flag = False
                    break


def ball_anim():
    global flag, c, y, v_velocity, SCORE, hit, sound_on
    # sounds
    if flag is False and sound_on:
        if not lose and not LEVEL_UP:
            hit.play()

    if not lose and not LEVEL_UP:
        sound_on = 0
    # print((flag,c,y))

    if flag is True:
        if floor(y) != floor(y - v_velocity * dtime):
            SCORE += 1
            SCORE += floor(v_velocity / 15)
        v_velocity = (40 - y)
        # v_velocity = v_velocity + 9.8 * dtime

        # camera stability

        if c > y:
            c = y

        y = y - v_velocity * dtime
        print(v_velocity)
        sound_on = 1

    elif flag is False and y < floor(y) + .76:  # ball bounce on red sectors
        # v_velocity = v_velocity + 9.8 * dtime

        v_velocity = (40 - y)
        y = y + v_velocity * dtime

    else:

        # ball goes down again
        flag = True


def restart():
    global X, y, angle_air, r_angle_safe, v_velocity, dtime, r_angle_ball, r_angle_glue, lose, flag, c
    global hit, LEVEL, SCORE, LEVEL_UP, START, game_over_sound, Level_up_sound, sound_on

    if lose:
        # back to level one and zero score
        LEVEL = 1
        SCORE = 0

    LEVEL_UP = False
    y = 29.9
    X = 0
    lose = False
    flag = True
    v_velocity = 0
    c = y
    START = 0
    for i in range(1, 25):
        r_angle_safe[i] = randrange(0, 180, 20)
        r_angle_glue[i] = randrange(0, 100, 20)
        angle_air[i] = random.uniform(.5, .75)

    # pygame.mixer.music.stop()
    # pygame.mixer.music.load("theme.mp3")
    # pygame.mixer.music.play(-1)
    # pygame.mixer.music.set_volume(.2)


def add_texture(x1, x2, y1, y2, index1=0, z_near=-1, z_far=1):
    glPushMatrix()
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()  # ortho or perspective NO BRAINER
    glLoadIdentity()
    glOrtho(-1, 1, -1, 1, z_near, z_far)
    glBindTexture(GL_TEXTURE_2D, TEXTURE_NAMES[index1])
    glBegin(GL_QUADS)

    glTexCoord2f(0, 1)
    glVertex(x1, y2)

    glTexCoord2f(0, 0)
    glVertex(x1, y1)

    glTexCoord2f(1, 0)
    glVertex(x2, y1)

    glTexCoord2f(1, 1)
    glVertex(x2, y2)
    glEnd()

    glBindTexture(GL_TEXTURE_2D, -1)
    glPopMatrix()
    glFlush()
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()


def new_init():
    init_projection()
    glEnable(GL_LIGHTING)


def white_material(rd=1.0, gd=1.0, bd=1.0, s=1.0, ra=.5, ga=.5, ba=.5):
    glPushMatrix()
    glPushAttrib(GL_ALL_ATTRIB_BITS)

    MaterialAmb = [ra, ga, ba, 1]  # r,g,b, alpha
    MaterialDif = [rd, gd, bd, 1]
    MaterialSpc = [s, s, s, 1]
    MaterialShn = [9]  # 0-128

    glMaterial(GL_FRONT_AND_BACK, GL_AMBIENT, MaterialAmb)
    glMaterial(GL_FRONT_AND_BACK, GL_DIFFUSE, MaterialDif)
    glMaterial(GL_FRONT_AND_BACK, GL_SPECULAR, MaterialSpc)
    glMaterial(GL_FRONT_AND_BACK, GL_SHININESS, MaterialShn)


def after_white_material():
    glPopAttrib()
    glPopMatrix()


def enableLight0():
    global X, y
    glEnable(GL_LIGHT0)

    LightPos = [100, 100, 100, 1]
    LightAmb = [1, 1, 1, 1.0]  # r,g,b, alpha
    LightDif = [1, 1, 1, 1.0]
    LightSpc = [1.0, 1.0, 1.0, 1.0]

    glLight(GL_LIGHT0, GL_POSITION, LightPos)
    glLight(GL_LIGHT0, GL_AMBIENT, LightAmb)
    glLight(GL_LIGHT0, GL_DIFFUSE, LightDif)
    glLight(GL_LIGHT0, GL_SPECULAR, LightSpc)


def draw_sectors_with_light():
    # for i in range(0, floor(y - 4)): #todo:try to un comment this and comment next line
    for i in range(0, 25):
        # safe sectors
        white_material(.6, 0, 0, 0, .8, 0, 0)
        draw_Circular_sector(i, angle_air[i], r_angle_safe[i])

        # draw_Circular_sector(i - .15, angle_air[i], r_angle_safe[i])

        # for 3d red (cylindrical)
        ################################

        after_white_material()
        white_material(.3, 0, 0, 0, .4, 0, 0)

        draw_3d_cylindrical(i, angle_air[i], r_angle_safe[i])
        after_white_material()

        ################################

        # glue sectors

        if i != 0:
            glPushMatrix()
            white_material(0, 1, 1, .5, 0, 1, 1)
            # to be visible
            glTranslate(0, 0.0001, 0)

            draw_Circular_sector(i, 3 - (.2 * LEVEL), r_angle_glue[i] + r_angle_safe[i])
            after_white_material()

            # for 3d glue (cylindrical)
            #######################
            white_material(0, .3, .3, .5, 0, .4, .4)
            glPushMatrix()
            glTranslate(0.0075 * sin(X), 0, 0.0075 * cos(X))
            draw_3d_cylindrical(i, 3 - (.2 * LEVEL), r_angle_glue[i] + r_angle_safe[i])
            after_white_material()

            glPopMatrix()
            ###########################
            glPopMatrix()


# regular draw text in ortho

def draw_text(string, x1, y1, FONT_DOWNSCALE=.4):
    glLineWidth(3)

    glPushMatrix()  # remove the previous transformations

    glTranslate(x1, y1, 0)

    glScale(FONT_DOWNSCALE, FONT_DOWNSCALE, 1)
    string = string.encode()  # conversion from Unicode string to byte string
    for c_ in string:
        glutStrokeCharacter(GLUT_STROKE_ROMAN, c_)

    glLineWidth(1)

    glPopMatrix()


#  draw text in 3d


def draw_text_3d_wrapper(string, x1, y1, r=.1, g=.1, b=.1, down_scale=.4):
    """
    This function defaults projection and modelview matrix to draw in the 2d plane and restores your original projection and modelview matrix
    :param down_scale: red
    :param r: red
    :param g: green
    :param b:blue
    :param string: any message
    :param x1: from -1 to 1 (we use default ortho)
    :param y1: from -1 to 1 (we use default ortho)

    your matrices will be the same after this call
    """

    glPushMatrix()
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()  # ortho or perspective NO BRAINER
    glLoadIdentity()
    glOrtho(0, 800, 0, 800, -1, 1)
    # glColor3d(r, g, b)
    draw_text(string, x1, y1, down_scale)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()

    # ending un in GL_MODELVIEW


def draw():
    global y, angle_air, r_angle_safe, v_velocity, dtime, r_angle_ball, r_angle_glue, lose, flag, c, SCORE, LEVEL_UP, START, game_over_sound, Level_up_sound, sound_on
    global hit, LEVEL
    glClearColor(0, 0, 0, 0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    # add_tex(-1, 1, 0, 0, 0.5, 1, z_near=-1000, z_far=10)
    if START:
        white_material()
        draw_text_3d_wrapper("HELIX JUMP", 250, 700)
        draw_text_3d_wrapper("HELIX JUMP", 251, 701)
        draw_text_3d_wrapper("HELIX JUMP", 252, 699)
        add_texture(-.4, .4, -.9, -.6, 5)
        add_texture(-.5, .5, -.5, .5, 6)
        add_texture(-1, 1, -1, 1, 0)
        after_white_material()

    else:
        add_texture(-1, 1, -1, 1, 0, z_near=-1000, z_far=10)

        white_material(-.7, -.7, 1, 0)

        draw_text_3d_wrapper("score:" + str(SCORE), 315, 700)
        draw_text_3d_wrapper("score:" + str(SCORE), 314, 701)
        draw_text_3d_wrapper("score:" + str(SCORE), 316, 699)
        draw_text_3d_wrapper("LEVEL:" + str(LEVEL), 22, 751, down_scale=.3)
        draw_text_3d_wrapper("LEVEL:" + str(LEVEL), 21, 750, down_scale=.3)
        draw_text_3d_wrapper("LEVEL:" + str(LEVEL), 20, 752, down_scale=.3)

        after_white_material()

        init_camera()
        # draw_axes()
        ########################

        white_material()
        draw_cylinder(25)
        after_white_material()

        ###################

        draw_sectors_with_light()
        # draw_circular_sectors()

        ##########################

        white_material(0, 0, .8, 1, 0, 0, .4)
        # white_material(0, 0, 0, 0, 0.5, 1, .5)
        draw_sphere(X, y - 5, r_angle_ball)
        after_white_material()

        ##################
        if not lose and not LEVEL_UP:
            collision_detection()
            ball_anim()
            r_angle_ball += 2

        elif lose and not LEVEL_UP:

            white_material()
            add_texture(-.4, .4, -.9, -.6, 3)
            add_texture(-1, 1, -1, 1, 2)
            after_white_material()

            if sound_on:
                # pygame.mixer.music.stop()
                game_over_sound.play()
                sound_on = 0

        if LEVEL_UP:

            white_material()
            add_texture(-.4, .4, -.9, -.6, 4)
            add_texture(-1, 1, -1, 1, 1)
            after_white_material()
            if sound_on:
                # pygame.mixer.music.stop()
                Level_up_sound.play()
                sound_on = 0
                LEVEL += 1
        #########################
    glutSwapBuffers()


if __name__ == '__main__':
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutCreateWindow(b"helix jump el3`laba")
    glutPositionWindow(0, 0)
    init_textures()
    # init_projection()
    mixer.init()

    new_init()
    enableLight0()
    glutMouseFunc(mouse2)

    glutKeyboardFunc(keyboard_callback)
    glutPassiveMotionFunc(mouse_callback)
    glutDisplayFunc(draw)
    glutTimerFunc(interval, game_timer, 1)
    glutMainLoop()
