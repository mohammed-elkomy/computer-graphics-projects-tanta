from OpenGL.GL import *
from OpenGL.GLUT import *
import main
import numpy as np
import pygame
import sys
mouse_y = 1
mouse_x = 3

shell_x = 0
shell_y = 0
loc_yp = 0
loc_xp = 0
speed_of_shell = 5

firing1 = False
firing2 = False
state_1 = 1
state_2 = 0

ACTIVE = 1
IN_ACTIVE = 0

mouse_motion_1 = IN_ACTIVE
mouse_motion_2 = IN_ACTIVE

rotation_angle = 45
SHELL_RADIUS = 0.25
speed = 1
angle_1 = 0
angle_2 = 0
#########################
player_health_1 = 100
player_health_2 = 100
#########################
# Define the movement for the tanks
left_tank_x = 0
right_tank_x = 0
######################################

pygame.mixer.init()
effect = pygame.mixer.Sound("boom.mp3")


def wheels(loc_x, loc_y, loc_z):
    glLoadIdentity()
    main.reposition_camera()
    glColor3ub(107, 107, 107)
    glTranslate(loc_x, loc_y, loc_z)
    glScale(0.25, 0.125, 1)
    glutSolidCylinder(3, 3, 50, 10)


def path():
    global angle_1, loc_yp, right_tank_x, left_tank_x, shell_x, state_1, state_2, shell_y
    if state_1:
        x0 = 10.5 + right_tank_x
        shell_y = -7.5 - (5 / 3) * (shell_x - x0) - (13/126) * (shell_x - x0) * (shell_x - x0 / 2) - \
            (1/2772) * (shell_x - x0) * (shell_x - x0 / 2) * shell_x - \
            (1/29106) * (shell_x - x0) * (shell_x - x0 / 2) * shell_x * (shell_x + x0)
    if state_2:
        x1 = -10.5 + left_tank_x
        shell_y = -7.5 + (14 / 7) * (shell_x - x1) - (44 / 441) * (shell_x - x1) * (shell_x - x1 / 2) - \
            (16 / 9261) * (shell_x - x1) * (shell_x - x1 / 2) * shell_x - \
            (32 / 194481) * (shell_x - x1) * (shell_x - x1 / 2) * shell_x * (shell_x + x1)
    return shell_y


def update():
    global shell_x, firing1, firing2, state_1, state_2, loc_yp

    if firing1:
        shell_x -= 0.15
        if (-12.5+left_tank_x <= shell_x <= -9.5+left_tank_x) and (-8 <= shell_y <= -7):
            effect.play()
            decay_player2_health()
            firing1 = False
            state_1 = 0
            state_2 = 1
        if shell_y < -7.8:
            effect.play()
            firing1 = False
            state_1 = 0
            state_2 = 1
        if 0.65 < shell_x < 0.82 and shell_y < 1.2:
            effect.play()
            firing1 = False
            state_1 = 0
            state_2 = 1
    if firing2:
        shell_x += 0.15
        if (12.5+right_tank_x >= shell_x >= 9.5+right_tank_x) and (-8 <= shell_y <= -7):
            effect.play()
            decay_player1_health()
            firing2 = False
            state_2 = 0
            state_1 = 1
        if shell_y < -7.8:
            effect.play()
            firing2 = False
            state_2 = 0
            state_1 = 1
        if -0.65 > shell_x > -0.82 and shell_y < 1.2:
            effect.play()
            firing2 = False
            state_2 = 0
            state_1 = 1
    glutPostRedisplay()


def mouse_click(m_x, m_y):
    global mouse_y
    global mouse_x
    mouse_y = max(m_y, 100)
    mouse_x = max(m_x, 500)


def draw_shell():
    global shell_x, shell_y, loc_yp, loc_xp
    glLoadIdentity()
    main.reposition_camera()
    print(shell_x)
    print(shell_y)
    glColor3f(1, 0, 0)
    glTranslate(shell_x, path(), 0)
    glutSolidSphere(0.25, 25, 25)
    update()


def decay_player1_health():
    global player_health_1
    if player_health_1 == 100:
        player_health_1 = 75
    elif player_health_1 == 75:
        player_health_1 = 50
    elif player_health_1 == 50:
        player_health_1 = 25
    else:
        player_health_1 = 0


def decay_player2_health():
    global player_health_2
    if player_health_2 == 100:
        player_health_2 = 75
    elif player_health_2 == 75:
        player_health_2 = 50
    elif player_health_2 == 50:
        player_health_2 = 25
    else:
        player_health_2 = 0


def wall(loc_x, loc_y, loc_z):
    glLoadIdentity()
    main.reposition_camera()
    glColor3ub(117, 22, 63)
    glTranslate(loc_x, loc_y, loc_z)
    glScale(1.5, 1, 3)
    glutSolidCube(1)


def triangle(loc_x, loc_y, loc_z):
    glLoadIdentity()
    main.reposition_camera()
    glColor3ub(117, 22, 63)
    glTranslate(loc_x, loc_y, loc_z)
    glScale(0.5, 0.5, 0.5)
    glBegin(GL_POLYGON)
    glVertex3d(-1.5, 0, 0)
    glVertex3d(1.5, 0, 0)
    glVertex3d(0, 2, 0)
    glEnd()


def key_pressed(key, x, y):
    global mouse_motion_1, mouse_motion_2, firing1, shell_y, shell_x, firing2, state_1, state_2
    global left_tank_x, right_tank_x
    if key == b'x' or key == b'X':
        sys.exit()
    if state_1:
        mouse_motion_1 = ACTIVE
        mouse_motion_2 = IN_ACTIVE
        firing1 = False
    if state_2:
        mouse_motion_1 = IN_ACTIVE
        mouse_motion_2 = ACTIVE
        firing2 = False
    if key == b'w' or key == b'W':
        if right_tank_x <= 3:
            right_tank_x += 0.5
    # Move right tank left within the allowed range
    elif key == b's' or key == b'S':
        if right_tank_x >= -8:
            right_tank_x -= 0.5
    if key == b'd' or key == b'D':
        if left_tank_x <= 8:
            left_tank_x += 0.5
    elif key == b'a' or key == b'A':
        if left_tank_x >= -3:
            left_tank_x -= 0.5
    if key == b' ':
        if (mouse_motion_1 == ACTIVE and not firing1) or (mouse_motion_2 == ACTIVE and not firing2):
            if mouse_motion_1 == ACTIVE:
                firing1 = True
                shell_x = 10.5 + right_tank_x
                shell_y = -7.5
            elif mouse_motion_2 == ACTIVE:
                firing2 = True
                shell_x = -10.5 + left_tank_x
                shell_y = -7.5


def calculate_angle(x0, y0):
    global rotation_angle, state_1, state_2, angle_1, angle_2
    rotation_angle = np.degrees(np.arctan2(x0, y0*3))   # Calculate angle in degrees
    if state_1:
        angle_1 = rotation_angle
    if state_2:
        angle_2 = rotation_angle
    return rotation_angle


def draw_1():
    global angle_1, state_2, state_1, right_tank_x
    wheels(13+right_tank_x, -9, -1.5)    # right wheel
    wheels(10+right_tank_x, -9, -1.5)        # left wheel
    #######################################################
    glLoadIdentity()
    main.reposition_camera()
    glColor3ub(107, 107, 107)
    glTranslate(11.5+right_tank_x, -9, 0)
    glScale(3, 0.75, 3)
    glutSolidCube(1)     # body of wheel
    #######################################################
    glLoadIdentity()
    main.reposition_camera()
    glColor3ub(200, 200, 200)
    glTranslate(10.7+right_tank_x, -7.5, 0)
    if state_1:
        # rotating around z depending on mouse position(x,y)
        glRotate(180-calculate_angle(mouse_x, mouse_y), 0, 0, 1)  # Rotate around z-axis
    else:
        glRotate(180 - angle_1, 0, 0, 1)
    glScale(2.5, 0.3, 0.25)
    glutSolidCube(1)         # the bulb
    #######################################################
    triangle(12.25+right_tank_x, -8.65, 1.5)  # right of front triangle
    triangle(10.75+right_tank_x, -8.65, 1.5)  # left of front triangle
    triangle(12.25+right_tank_x, -8.65, -1.5)  # right of back triangle
    triangle(10.75+right_tank_x, -8.65, -1.5)  # left of back triangle
    ########################################################
    wall(11.5+right_tank_x, -8.15, 0)   # body of tank
    #######################################################
    glLoadIdentity()
    main.reposition_camera()
    glColor3ub(0, 22, 100)
    glTranslate(11.5+right_tank_x, -7.5, 0)
    glScale(1, 0.75, 1)
    glutSolidSphere(0.5, 50, 50)     # head of tank
    #####################################################################
    if firing1:
        draw_shell()


def draw_2():
    global angle_2, state_2, state_1, left_tank_x
    wheels(-13+left_tank_x, -9, -1.5)    # right wheel
    wheels(-10+left_tank_x, -9, -1.5)        # left wheel
    #######################################################
    glLoadIdentity()
    main.reposition_camera()
    glColor3ub(107, 107, 107)
    glTranslate(-11.5+left_tank_x, -9, 0)
    glScale(3, 0.75, 3)
    glutSolidCube(1)     # body of wheel
    #######################################################
    glLoadIdentity()
    main.reposition_camera()
    glColor3ub(200, 200, 200)
    glTranslate(-10.7+left_tank_x, -7.5, 0)
    if state_2:
        # rotating around z depending on mouse position(x,y)
        glRotate(calculate_angle(mouse_x, mouse_y), 0, 0, 1)  # Rotate around z-axis
    else:
        glRotate(angle_2, 0, 0, 1)
    glScale(2.5, 0.3, 0.25)
    glutSolidCube(1)              # the bulb
    #######################################################
    triangle(-12.25+left_tank_x, -8.65, 1.5)  # right of front triangle
    triangle(-10.75+left_tank_x, -8.65, 1.5)  # left of front triangle
    triangle(-12.25+left_tank_x, -8.65, -1.5)  # right of back triangle
    triangle(-10.75+left_tank_x, -8.65, -1.5)  # left of back triangle
    ########################################################
    wall(-11.5+left_tank_x, -8.15, 0)   # body of tank
    #######################################################
    glLoadIdentity()
    main.reposition_camera()
    glColor3ub(0, 22, 100)
    glTranslate(-11.5+left_tank_x, -7.5, 0)
    glScale(1, 0.75, 1)
    glutSolidSphere(0.5, 50, 50)            # head of tank
    #####################################################################
    if firing2:
        draw_shell()
