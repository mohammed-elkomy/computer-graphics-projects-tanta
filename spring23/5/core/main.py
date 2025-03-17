# Make Directories Stable :
import os



from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math, numpy as np, time
from Rectangles import *
from Textures import *
from Collision import *
import pygame
from Sounds import *

# WINDOW PROPERTIES
WINDOW_WIDTH, WINDOW_HEIGHT = 1200, 900

# ROADS WIDTHS AND HEIGHTS
LOWER_ROAD_HEIGHT = UPPER_ROAD_HEIGHT = 200
MIDDLE_ROAD = (250, 150)
UPPER_LEFT_ROAD_WIDTH = UPPER_RIGHT_ROAD_WIDTH = 250

# CAR PROPERTIES
MAX_CAR_SPEED = 5
d = 0.965
CAR_ROTATION_SPEED = 2
CAR_WIDTH = 80
CAR_LENGTH = 40

CAR_SPEED = MAX_CAR_SPEED * (1-d)/d
time_interval = 1
keys_pressed = set()
car_pos = [100, 250]
car_angle = [0.0]
car_vel = [0.0, 0.0]
obstacle_speed = 0.2  # Changes on linux
game_over = [0]



# * =================================== Init PROJECTION ===================================== * #


def init():
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT)
    glMatrixMode(GL_MODELVIEW)


# * ========================= Rectangle ( width, height ,  x ,  y ) ========================= * #

# ! World Rectangle
world = Rectangle(WINDOW_WIDTH, WINDOW_HEIGHT, 0, 0)

# * ========================= car model ( left, bottom , right ,  top , direction ) ========================= * #


# road 1
car_Obj_1_0 = Car_Model(100, 160, 180, 205, 3, obstacle_speed)
car_Obj_1_1 = Car_Model(400, 160, 480, 205, 3, obstacle_speed)
car_Obj_1_2 = Car_Model(800, 160, 880, 205, 3, obstacle_speed)

# road 2
car_Obj_2_0 = Car_Model(100, 300, 180, 345, -4, obstacle_speed)
car_Obj_2_1 = Car_Model(400, 300, 480, 345, -4, obstacle_speed)
car_Obj_2_2 = Car_Model(900, 300, 980, 345, -4, obstacle_speed)

# road 3
car_Obj_3_0 = Car_Model(500, 520, 580, 565, 4, obstacle_speed)
car_Obj_3_1 = Car_Model(900, 520, 980, 565, 4, obstacle_speed)
car_Obj_3_2 = Car_Model(200, 520, 280, 565, 4, obstacle_speed)

# road 4
car_Obj_4_0 = Car_Model(600, 650, 680, 695, -9, obstacle_speed)
car_Obj_4_1 = Car_Model(200, 650, 280, 695, -9, obstacle_speed)
car_Obj_4_2 = Car_Model(1100, 650, 1180, 695, -9, obstacle_speed)


# * ================================= Draw other cor state  ================================= * #


def drawState(carObj, texture_index):
    glColor(1, 1, 1)  # White color
    carObj.draw_texture(texture_index)

    carObj.left = carObj.left + carObj.car_Direction
    carObj.right = carObj.right + carObj.car_Direction

    if carObj.left >= WINDOW_WIDTH and carObj.car_Direction > 0:
        carObj.left = -80
        carObj.right = 0

    if carObj.right <= 0 and carObj.car_Direction < 0:
        carObj.left = WINDOW_WIDTH
        carObj.right = WINDOW_WIDTH + 80


# * ===============================================  Start & End  ========================================== * #

# signal
start = 1  # start = 1 : mean (Still At Start) , start = 0 : mean (Enter gameplay)
end = None  # end = 1 : when win , end = 0 : when lose

# buttons properties
button_width = 120
button_height = 40

# start view buttons
start_button = Rectangle(button_width, button_height,
                         (WINDOW_WIDTH / 2) - (button_width / 2),
                         (WINDOW_HEIGHT / 2) - (button_height / 2) + 100)

# end view buttons
continue_button = Rectangle(button_width, button_height,
                            (WINDOW_WIDTH / 2) - (10 + button_width),
                            (WINDOW_HEIGHT / 2) - (button_height / 2) + 100)

quit_button = Rectangle(button_width, button_height, (WINDOW_WIDTH / 2) + 10,
                        (WINDOW_HEIGHT / 2) - (button_height / 2) + 100)


def draw_start():
    world.draw_texture(14)
    start_button.draw_texture(15)


def draw_end():
    if end == 1:  # winner
        movement_sound.stop()
        win.play()
        world.draw_texture(16)
        continue_button.draw_texture(18)

    if end == 0:  # loser
        movement_sound.stop()
        world.draw_texture(17)
        continue_button.draw_texture(19)

    quit_button.draw_texture(20)


# section : handle click buttons process
def reset_game():
    # reset main car
    car_angle[0] = 0
    car_vel[0] = car_vel[1] = 0
    car_pos[0], car_pos[1] = 100, 250


# function that detect clicking at any button
def click_signal(button, click_type, x, y):
    if button.left <= x <= button.right and \
            WINDOW_HEIGHT - button.top <= y <= WINDOW_HEIGHT - button.bottom and \
            click_type == GLUT_LEFT_BUTTON:
        return True


def MouseMotion(click, state, x, y):
    global start
    global end

    if start == 1:
        if click_signal(start_button, click, x, y):
            button_sound.play()
            start = 0
            time.sleep(0.5)

    if end == 1 or end == 0:
        if click_signal(quit_button, click, x, y):  # Quit
            pygame.mixer.music.stop()
            glutDestroyWindow(glutGetWindow())
            time.sleep(0.5)
            button_sound.play()

        elif click_signal(continue_button, click, x, y):  # play-again or level-up
            pygame.mixer.music.stop()
            time.sleep(0.5)
            button_sound.play()
            reset_game()
            end = None  # back again to gameplay


# * ===============================================  DRAW FUNCTION ========================================== * #

def draw():
    global car_pos, car_angle, car_vel, keys_pressed, obstacle_speed, game_over, end,d
    glClear(GL_COLOR_BUFFER_BIT)

    if start == 1:
        draw_start()

    elif end == 1 or end == 0:
        draw_end()

    else:

        glClear(GL_COLOR_BUFFER_BIT )
        drawTextures((1, 1, 1), world)
        # * ========================= Draw cars ========================= * #
        obs_list = [car_Obj_1_0, car_Obj_1_1, car_Obj_1_2,
                    car_Obj_2_0, car_Obj_2_1, car_Obj_2_2,
                    car_Obj_3_0, car_Obj_3_1, car_Obj_3_2,
                    car_Obj_4_0, car_Obj_4_1, car_Obj_4_2]
        car = MainCar(CAR_WIDTH, CAR_LENGTH, car_pos[0], car_pos[1], car_angle[0], [0.6, 0.8, 0.5])
        j = 2
        for i in obs_list:
            drawState(i, j)
            if obstacle_collision(i, car_pos, car_vel, car_angle, CAR_LENGTH, CAR_WIDTH,
                                  game_over):  # if car collided three times
                end = 0
            j += 1

        # * ========================= Main car ========================= * #
        if 'left' in keys_pressed:
            car_angle[0] += CAR_ROTATION_SPEED
        if 'right' in keys_pressed:
            car_angle[0] -= CAR_ROTATION_SPEED
        if 'up' in keys_pressed:
            car_vel[0] += CAR_SPEED * math.cos(math.radians(car_angle[0]))
            car_vel[1] += CAR_SPEED * math.sin(math.radians(car_angle[0]))
            movement_sound.play()

        if 'up' not in keys_pressed:
            movement_sound.stop()

        if 'down' in keys_pressed:
            car_vel[0] -= CAR_SPEED * math.cos(math.radians(car_angle[0]))
            car_vel[1] -= CAR_SPEED * math.sin(math.radians(car_angle[0]))
            back_sound.play()
        if 'down' not in keys_pressed:
            back_sound.stop()


        car_pos[0] += car_vel[0]
        car_pos[1] += car_vel[1]
        car_vel[0] *= d
        car_vel[1] *= d

        # Collision detection to the side walls
        if wall_collision(car_pos, car_vel, car_angle, CAR_LENGTH, CAR_WIDTH, game_over):  # if car collided three times
            end = 0

        if arrival_line(car_pos, CAR_LENGTH):  # if car reach parking
            for i in obs_list:
                i.car_Direction *= 5
            end = 1
            game_over[0] = 0


    glutSwapBuffers()


def keyboard(key, x, y):
    global keys_pressed

    if key == b'a':
        keys_pressed.add('left')
    elif key == b'd':
        keys_pressed.add('right')
    elif key == b'w':
        keys_pressed.add('up')
    elif key == b's':
        keys_pressed.add('down')

def keyboard_up(key, x, y):
    global keys_pressed

    if key == b'a':
        keys_pressed.remove('left')
    elif key == b'd':
        keys_pressed.remove('right')
    elif key == b'w':
        keys_pressed.remove('up')
    elif key == b's':
        keys_pressed.remove('down')


def Timer(v):
    draw()
    glutTimerFunc(time_interval, Timer, 1)


def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutInitWindowPosition(500, 100)
    glutCreateWindow(b"FORSA GAME")
    glutDisplayFunc(draw)
    glutIdleFunc(draw)
    glutKeyboardFunc(keyboard)
    glutKeyboardUpFunc(keyboard_up)
    glutMouseFunc(MouseMotion)
    glutTimerFunc(time_interval, Timer, 1)
    init()
    load_setup_textures()
    glutMainLoop()


main()
