import sys
from random import randint
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
import random

pygame.mixer.init()
# screen = pygame.display.set_mode()

#############################
#          Sounds        #
#############################

brick_sound = pygame.mixer.Sound('sounds/bricks.wav')
paddle_sound = pygame.mixer.Sound('sounds/paddle.wav')
wall_sound = pygame.mixer.Sound('sounds/wall.wav')
game_over = pygame.mixer.Sound('sounds/gameover1.wav')
coin = pygame.mixer.Sound('sounds/smb_coin.wav')
fire = pygame.mixer.Sound('sounds/smb_fireball.wav')

#############################
#          Constants        #
#############################
list_of_bricks = []
x_coin = []
y_coin = []
X_bricks = []
Y_bricks = []
list_of_coins = []
num_of_coins = 30
random_coins = [randint(0, 312) for _ in range(num_of_coins)]

FROM_RIGHT = 1
FROM_LEFT = 2
FROM_TOP = 3
FROM_BOTTOM = 4

lose = 0
lose_sound = 1

lives = 3

GB = 0
level_up = False

GRID_DIVISION = 30
no_of_bricks = 312

WINDOW_HEIGHT = 1200
WINDOW_WIDTH = 1200

FONT_DOWNSCALE = 0.25
DOWNSCALE = 1.0
BAT_SCALE = 1.0

x_mouse_coord = 100

WINDOW_WIDTH_INT = 1200
WINDOW_HEIGHT_INT = 1200

# No. of textures used in the game
textures_id = 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11
tex_index = random.randrange(3, 8)

#############################

####################################
#            Game State            #
####################################
INTERVAL = 1  # msec

current_mouse_x = 500

player_score = 0

current_delta_X = 3
current_delta_Y = 3

# GIFTS
x = random.randrange(0, WINDOW_WIDTH - 55)
y = WINDOW_HEIGHT
c = q0 = q1 = q2 = q3 = q4 = 0
control_l12 = False
fire1_collision = fire2_collision = False
REPEAT = False
speed_effect = 1
enable_fire = False


# Bricks Class
class brick:
    def __init__(self, x, y, width, height, strength, isLive=True):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.isLive = isLive
        self.strength = strength
        self.left = 1
        self.right = 1
        self.bottom = 1
        self.top = 1


# Rectangle Class
class Rectangle:
    def __init__(self, left, bottom, right, top):
        self.left = left
        self.bottom = bottom
        self.right = right
        self.top = top


def create_bricks():
    global no_of_bricks, list_of_bricks
    brick_X = 0.35
    brick_Y = 18.75
    strength = 1
    for i in range(0, no_of_bricks, 1):
        if brick_X > 38.75:
            brick_X = 0.35
            brick_Y += 1.5
            strength += 0.5

        list_of_bricks.append(brick(brick_X, brick_Y, 1.1, 1.1, strength))
        brick_X += 1.5
        draw_brick(list_of_bricks[i])  # passing brick with it's index


def create_coin():
    global num_of_coins, list_of_coins, x_coin, y_coin, random_coins, no_of_bricks, list_of_bricks
    coin_X = 0.35
    coin_Y = 18.75
    strength = 1
    for i in range(0, no_of_bricks, 1):
        if coin_X > 38.75:
            coin_X = 0.35
            coin_Y += 1.5
        x_coin.append(coin_X)
        y_coin.append(coin_Y)
        coin_X += 1.5

        list_of_coins.append(brick(x_coin[i] + 0.15, y_coin[i] + 0.1, 0.7, 0.7, 1))
        if i in random_coins:
            draw_coins(list_of_coins[i])


def draw_brick(brick):
    colors = get_color(brick.y)  # get brick line colors by passing the the row to fn get color

    if brick.isLive:
        glLoadIdentity()

        brick.left = brick.x * GRID_DIVISION
        brick.right = (brick.x + brick.width) * GRID_DIVISION
        brick.bottom = brick.y * GRID_DIVISION
        brick.top = (brick.y + brick.height) * GRID_DIVISION

        glColor3f(colors[0], colors[1], colors[1])
        glBegin(GL_QUADS)
        glVertex2f(brick.left, brick.bottom)
        glVertex2f(brick.right, brick.bottom)
        glVertex2f(brick.right, brick.top)
        glVertex2f(brick.left, brick.top)
        glEnd()


def draw_coins(brick):
    if brick.isLive:
        glLoadIdentity()

        brick.left = brick.x * GRID_DIVISION
        brick.right = (brick.x + brick.width) * GRID_DIVISION
        brick.bottom = brick.y * GRID_DIVISION
        brick.top = (brick.y + brick.height) * GRID_DIVISION

        glColor3d(1, 1, 1)
        glBegin(GL_QUADS)
        glTexCoord(0, 0)
        glVertex2f(brick.left, brick.bottom)
        glTexCoord(1, 0)
        glVertex2f(brick.right, brick.bottom)
        glTexCoord(1, 1)
        glVertex2f(brick.right, brick.top)
        glTexCoord(0, 1)
        glVertex2f(brick.left, brick.top)
        glEnd()


def draw_rectangle(rect):
    glLoadIdentity()
    glBegin(GL_QUADS)
    glVertex2f(rect.left, rect.bottom)
    glVertex2f(rect.right, rect.bottom)
    glVertex2f(rect.right, rect.top)
    glVertex2f(rect.left, rect.top)
    glEnd()


def draw_rectangle_textured(rect):
    glLoadIdentity()
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)
    glVertex2f(rect.left, rect.bottom)
    glTexCoord2f(1, 0)
    glVertex2f(rect.right, rect.bottom)
    glTexCoord2f(1, 1)
    glVertex2f(rect.right, rect.top)
    glTexCoord2f(0, 1)
    glVertex2f(rect.left, rect.top)
    glEnd()


###################################
#            Rectangles           #
###################################
ball = Rectangle(135, 135, 165, 165)
wall = Rectangle(0, 0, WINDOW_WIDTH, 1100)
whole_wall = Rectangle(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
bat = Rectangle(350, 55, 450, 70)
fireGun_left = Rectangle(bat.left, bat.top, bat.left + 10, bat.top + 10)
fireGun_right = Rectangle(bat.right - 10, bat.top, bat.right, bat.top + 10)


###################################
#             Gifts               #
###################################
def draw_gift(LEFT, BOTTOM, H):
    glLoadIdentity()
    rect = Rectangle(LEFT, BOTTOM, LEFT + H, BOTTOM + H)
    glBegin(GL_QUADS)
    glColor(1, 1, 1)
    glTexCoord2f(0, 0)
    glVertex(rect.left, rect.bottom, 0)
    glTexCoord2f(1, 0)
    glVertex(rect.right, rect.bottom, 0)
    glTexCoord2f(1, 1)
    glVertex(rect.right, rect.top, 0)
    glTexCoord2f(0, 1)
    glVertex(rect.left, rect.top, 0)
    glEnd()


def showGifts():
    global y, x, c, bat, REPEAT
    gift = Rectangle(x, y, x + 55, y + 55)
    if check_bat(gift, bat):
        check_changes()

    if y >= -55 and not check_bat(gift, bat):
        REPEAT = True
        y -= 5
        draw_gift(x, y, 55)
    else:
        REPEAT = False


l1 = fireGun_left.left
l2 = fireGun_right.left
b1 = fireGun_left.top
b2 = fireGun_right.top


def fireGUN():
    global bat, fireGun_left, fireGun_right
    glLoadIdentity()
    fireGun_left.left = bat.left
    fireGun_left.right = bat.left + 10
    fireGun_right.left = bat.right - 10
    fireGun_right.right = bat.right
    glPushMatrix()
    glBindTexture(GL_TEXTURE_2D, textures_id[2])
    draw_rectangle_textured(fireGun_left)
    draw_rectangle_textured(fireGun_right)
    glPopMatrix()


def fireShots():
    glLoadIdentity()
    global b1, b2, l1, l2, enable_fire, control_l12, fire1_collision, fire2_collision, fireGun_left, fireGun_right
    # l1,l2 position left
    # b1,b2 bottom
    fire1 = Rectangle(l1, b1, l1 + 20, b1 + 20)
    fire2 = Rectangle(l2, b2, l2 + 20, b2 + 20)
    check_coin_collision(fire1, "f")
    check_coin_collision(fire2, "f")
    if b2 == b1 and b1 == fireGun_left.top:
        fire.play()
    if check_brick_fire_collision(fire1):
        fire1_collision = True
    if check_brick_fire_collision(fire2):
        fire2_collision = True
    if not control_l12:
        l1 = fireGun_left.left
        l2 = fireGun_right.left

    if not fire1_collision:  # collision with fire 1
        if b1 <= WINDOW_HEIGHT:
            control_l12 = True
            b1 += 7
            glPushMatrix()
            glBindTexture(GL_TEXTURE_2D, textures_id[8])
            draw_gift(l1, b1, 20)
            glPopMatrix()
    else:
        l1 = fireGun_left.left
        b1 = fireGun_left.top
        glPushMatrix()
        glBindTexture(GL_TEXTURE_2D, textures_id[8])
        draw_gift(l1, b1, 20)
        glPopMatrix()

    if not fire2_collision:
        if b2 <= WINDOW_HEIGHT:
            control_l12 = True
            b2 += 7
            glPushMatrix()
            glBindTexture(GL_TEXTURE_2D, textures_id[8])
            draw_gift(l2, b2, 20)
            glPopMatrix()
    else:
        l2 = fireGun_right.left
        b2 = fireGun_left.top
        glPushMatrix()
        glBindTexture(GL_TEXTURE_2D, textures_id[8])
        draw_gift(l2, b2, 20)
        glPopMatrix()

    if (fire1_collision and fire2_collision) or (b2 > WINDOW_HEIGHT) or (b1 > WINDOW_HEIGHT):
        control_l12 = fire1_collision = fire2_collision = False
        b1 = fireGun_left.top
        b2 = b1
        glPushMatrix()
        glBindTexture(GL_TEXTURE_2D, textures_id[10])
        draw_gift(l1, b1, 20)
        draw_gift(l2, b2, 20)
        glPopMatrix()


def init():
    glClearColor(1, 1, 1, 1)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT, 0, 1)
    glMatrixMode(GL_MODELVIEW)


#####################################
#            Gifts effects           #
######################################
def check_changes():
    global y, x, \
        tex_index, bat, \
        BAT_SCALE, enable_fire, speed_effect, \
        q0, q1, q2, q3, q4
    gift = Rectangle(x, y, x + 55, y + 55)
    if check_bat(gift, bat):
        if tex_index == 3:
            q0 = 0
            if (bat.right - bat.left) <= WINDOW_WIDTH - 400:
                BAT_SCALE += 1
        elif tex_index == 4:
            q1 = 0
            if BAT_SCALE > 0.5:
                BAT_SCALE *= 0.75
        elif tex_index == 5:
            q2 = 0
            enable_fire = True
        elif tex_index == 6:
            q3 = 0
            speed_effect += 0.25
        elif tex_index == 7:
            q4 = 0
            if speed_effect > 0.25:
                speed_effect -= 0.25

        tex_index = random.randrange(3, 8)


def reverse_changes():
    global BAT_SCALE, enable_fire, \
        q0, q1, q2, q3, q4, \
        speed_effect, control_l12
    if q0 == 1000 and BAT_SCALE > 1:
        q0 = 0
        BAT_SCALE -= 1
    elif q1 == 1000 and BAT_SCALE != int(BAT_SCALE):
        q1 = 0
        BAT_SCALE /= 0.75
    elif q2 == 1000 and enable_fire is True:
        q2 = 0
        enable_fire = False
        control_l12 = False
    elif q3 == 1000 and speed_effect > 1:
        q3 = 0
        speed_effect -= 0.25
    elif q4 == 1000 and speed_effect != 1:
        q4 = 0
        speed_effect += 0.25

    q0 += 1
    q1 += 1
    q2 += 1
    q3 += 1
    q4 += 1


######################################
#             Callbacks              #
######################################

def mouse_callback(x_mouse_coord, y):
    global current_mouse_x
    current_mouse_x = x_mouse_coord


def keyboard_callback(key, x, y):
    global current_keyboard_x
    if key == GLUT_KEY_LEFT:
        current_keyboard_x = max(current_keyboard_x - 50, 0)
    elif key == GLUT_KEY_RIGHT:
        current_keyboard_x = min(current_keyboard_x + 50, WINDOW_WIDTH)


######################################
#             Textures               #
######################################
def texture_setup(texture_image_binary, texture_id, width, height):
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glEnable(GL_BLEND)  # FOR BLENDING
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_image_binary)


def load_textures():
    global textures_id
    glEnable(GL_TEXTURE_2D)

    glGenTextures(len(textures_id), textures_id)

    load_and_setup("pics/1111.jpg", textures_id[0])
    load_and_setup("pics/golf_ball_large.png", textures_id[1])

    # #### gifts
    load_and_setup("pics/b1.png", textures_id[2])
    load_and_setup("pics/gift.png", textures_id[3])
    load_and_setup("pics/decreasing.png", textures_id[4])
    load_and_setup("pics/fireee.png", textures_id[5])
    load_and_setup("pics/speed.png", textures_id[6])
    load_and_setup("pics/slow.png", textures_id[7])
    load_and_setup("pics/fire.png", textures_id[8])

    load_and_setup("pics/dollar.jpg", textures_id[9])
    load_and_setup("pics/gameover.jpg", textures_id[10])
    load_and_setup("pics/levelup.jpg", textures_id[11])


def load_and_setup(image_path, idx):
    # Loading
    image = pygame.image.load(image_path)

    texture = pygame.image.tostring(image, "RGBA", True)

    texture_setup(texture, textures_id[idx], image.get_width(), image.get_height())
    # Setup Wrapping and Rendering


#######################################
#        Game Implementation          #
#######################################
def gameover():
    glBindTexture(GL_TEXTURE_2D, textures_id[10])
    glColor3d(1, 1, 1)
    draw_rectangle_textured(whole_wall)
    glBindTexture(GL_TEXTURE_2D, -1)
    final_score = " Final Score : " + str(player_score) + "  "
    draw_text_centre(final_score, 600, 1000)


#########################################
#         draw text centre              #
#########################################
def draw_text_centre(string, x, y, S=FONT_DOWNSCALE, line_width=2.2):
    glLineWidth(line_width)
    glColor(1, 1, 1)
    glPushMatrix()
    glTranslate(x, y, 0)
    glScale(S, S, 1)
    string = string.encode()

    str_height = max(glutStrokeHeight(GLUT_STROKE_ROMAN) for c in string)
    str_width = sum(glutStrokeWidth(GLUT_STROKE_ROMAN, c) for c in string)

    glBegin(GL_LINE_LOOP)
    glVertex2d(-str_width // 2, -str_height // 2)
    glVertex2d(-str_width // 2, +str_height // 2)
    glVertex2d(+str_width // 2, +str_height // 2)
    glVertex2d(+str_width // 2, -str_height // 2)
    glEnd()

    glTranslate((-str_width // 2), -str_height // 3, 0)
    for c in string:
        glutStrokeCharacter(GLUT_STROKE_ROMAN, c)
    glPopMatrix()


def game_timer(v):
    global INTERVAL
    if not level_up:
        display()
    else:
        congrats()
    glutTimerFunc(INTERVAL, game_timer, 1)


def get_color(j):
    global R, GB
    R = 1
    glLoadIdentity()

    # >>>>>>>>>>>>>>>>>>>>>>  COLORS Green _ Blue  <<<<<<<<<<<<<<<<<<<<#
    if j == 18.75:
        GB = 0.5
        R = 0.5
    elif j == 20.25:
        GB = 0.8
    elif j == 21.75:
        GB = 0.72
    elif j == 23.75:
        GB = 0.64
    elif j == 24.75:
        GB = 0.56
    elif j == 26.25:
        GB = 0.48
    elif j == 27.75:
        GB = 0.4
    elif j == 29.25:
        GB = 0.32
    elif j == 30.75:
        GB = 0.24
    elif j == 32.25:
        GB = 0.16
    elif j == 33.75:
        GB = 0.1
    elif j == 35.25:
        GB = 0.5
        R = 0.5

    # glColor3f(R, GB, GB)
    return [R, GB]


####################################
#       Collision Detector         #
####################################
def check_ball_brick(ball, brick):
    collision_y = 0
    collision_x = 0
    horizontal_overlap = (brick.right >= ball.left >= brick.left) or (brick.right >= ball.right >= brick.left)

    if ball.top >= brick.bottom and horizontal_overlap:
        collision_y = True

    # Side Collision
    elif brick.bottom < ball.bottom < brick.top and horizontal_overlap:
        collision_x = True

    return [collision_y, collision_x]


def check_fire_brick(fire, brick):
    collision_y = False
    horizontal_overlap = (brick.right >= fire.left >= brick.left) or (brick.right >= fire.right >= brick.left)

    if fire.top >= brick.bottom and horizontal_overlap:
        collision_y = True

    return collision_y


def check_brick_fire_collision(fire):
    global player_score
    for i in range(0, no_of_bricks, 1):
        if list_of_bricks[i].isLive:
            delta = check_fire_brick(fire, list_of_bricks[i])

            if delta:
                list_of_bricks[i].strength -= 1
                if list_of_bricks[i].strength <= 0:
                    list_of_bricks[i].isLive = False
                player_score += 10
                brick_sound.play()
                return True

    return False


def congrats():
    global run_game
    glBindTexture(GL_TEXTURE_2D, textures_id[11])
    glColor3d(1, 1, 1)
    draw_rectangle_textured(whole_wall)
    glBindTexture(GL_TEXTURE_2D, -1)


def check_brick_ball_collision():
    global current_delta_Y, player_score, current_delta_X
    for i in range(0, no_of_bricks, 1):
        if list_of_bricks[i].isLive:
            delta = check_ball_brick(ball, list_of_bricks[i])

            if delta[0]:
                list_of_bricks[i].strength -= 3
                if list_of_bricks[i].strength <= 0:
                    list_of_bricks[i].isLive = False
                current_delta_Y = -3
                player_score += 10
                brick_sound.play()
            if delta[1]:
                list_of_bricks[i].strength -= 3
                if list_of_bricks[i].strength <= 0:
                    list_of_bricks[i].isLive = False
                current_delta_X = -current_delta_X
                player_score += 10
                brick_sound.play()


def check_coin_collision(element, elemntIndication):
    global player_score
    for i in range(0, no_of_bricks, 1):
        if list_of_coins[i].isLive:
            if elemntIndication == "b":
                coop = check_ball_brick(element, list_of_coins[i])
                if coop[0] or coop[1]:
                    list_of_coins[i].strength = 0
                    list_of_coins[i].isLive = False
                    player_score += 50
                    coin.play()
            elif elemntIndication == "f":
                coop = check_fire_brick(element, list_of_coins[i])
                if coop:
                    list_of_coins[i].strength = 0
                    list_of_coins[i].isLive = False
                    player_score += 50
                    coin.play()


def check_bat(element, bat):
    left_overlap = bat.left <= element.right <= bat.right
    right_overlap = bat.left <= element.left <= bat.right
    horizontal_overlap = (left_overlap or right_overlap)
    vertical_check1 = element.bottom <= bat.top
    vertical_check2 = element.bottom > bat.bottom
    vertical_check = vertical_check1 and vertical_check2

    return vertical_check and horizontal_overlap


def check_ball_wall(ball, wall):
    global FROM_RIGHT
    global FROM_LEFT
    global FROM_TOP
    global FROM_BOTTOM

    if ball.right >= wall.right:
        return FROM_RIGHT

    if ball.left <= wall.left:
        return FROM_LEFT

    if ball.top >= wall.top:
        return FROM_TOP

    if ball.bottom < wall.bottom and ball.top < wall.bottom:
        return FROM_BOTTOM


####################################
#            Display               #
####################################
def display():
    global current_delta_X, current_delta_Y
    global DOWNSCALE
    global x_mouse_coord
    global INTERVAL
    global lose, lose_sound
    global lives
    global player_score
    global list_of_bricks, no_of_bricks
    global tex_index
    global BAT_SCALE
    global enable_fire
    global REPEAT
    global y, x, c
    global level_up

    c += 1
    glClear(GL_COLOR_BUFFER_BIT)
    glClearColor(1, 1, 1, 1)
    ###############################
    # Background
    ###############################
    glBindTexture(GL_TEXTURE_2D, textures_id[0])
    glColor3d(1, 1, 1)
    draw_rectangle_textured(whole_wall)
    glBindTexture(GL_TEXTURE_2D, textures_id[9])
    glColor3d(1, 1, 1)
    create_coin()
    glBindTexture(GL_TEXTURE_2D, -1)
    create_bricks()
    ##################################
    #          Breaking Bricks       #
    ##################################
    draw_text_centre(f" Lives: {lives}  ", 120, 1150)
    str_score = " Score : " + str(player_score) + "  "
    draw_text_centre(str_score, 600, 1150)
    level1 = " level : 1 "
    draw_text_centre(level1, 1050, 1150)

    ###################################
    #              Bat                #
    ###################################
    glPushMatrix()
    glColor3f(1, 0, 0)
    draw_rectangle(bat)
    glPopMatrix()

    ########################################
    #              Ball                    #
    ########################################
    # draw the ball
    glPushMatrix()
    glBindTexture(GL_TEXTURE_2D, textures_id[1])
    glColor3d(1, 1, 1)
    draw_rectangle_textured(ball)
    glBindTexture(GL_TEXTURE_2D, -1)
    glPopMatrix()

    #################################
    #       Animate The Ball        #
    #################################
    if not lose:
        ball.left = ball.left + current_delta_X * speed_effect  # updating ball's coordinates
        ball.right = ball.right + current_delta_X * speed_effect
        ball.top = ball.top + current_delta_Y * speed_effect
        ball.bottom = ball.bottom + current_delta_Y * speed_effect

    if check_ball_wall(ball, wall) == FROM_RIGHT:
        current_delta_X = -current_delta_X
        wall_sound.play()

    if check_ball_wall(ball, wall) == FROM_LEFT:
        current_delta_X = -current_delta_X
        wall_sound.play()

    if check_ball_wall(ball, wall) == FROM_TOP:
        current_delta_Y = -current_delta_Y
        wall_sound.play()

    if check_ball_wall(ball, wall) == FROM_BOTTOM:  # bat lost the ball
        if lives > 1:
            lives -= 1
            current_delta_Y = 3
        else:
            lives = 0
            lose = 1
            if lose_sound:
                game_over.play()

                lose_sound = 0
    #######################################
    # Check Coin Collision
    #######################################
    check_coin_collision(ball, "b")

    # Mouse Control
    if not lose:
            bat.left = current_mouse_x - x_mouse_coord * BAT_SCALE  # to control the bat after changing it's size
            bat.right = current_mouse_x + x_mouse_coord * BAT_SCALE

    # GIFTS
    if not lose:
        # draw gifts
        glPushMatrix()
        glBindTexture(GL_TEXTURE_2D, textures_id[tex_index])
        if c == 1000:  # start ############optional
            showGifts()
        elif c > 1000:  # coding
            if REPEAT:
                showGifts()
            else:
                z = random.randrange(0, 700)
                if z == 90:
                    tex_index = random.randrange(3, 8)
                    x = random.randrange(0, WINDOW_WIDTH - 55)
                    y = WINDOW_HEIGHT
                    showGifts()

        glPopMatrix()

        # check_changes()
        if enable_fire:
            fireGUN()
            fireShots()

        reverse_changes()

    if lose:
        gameover()

    if check_bat(ball, bat):
        current_delta_Y = 3
        paddle_sound.play()

    #######################################
    # Check Brick Collision
    #######################################
    check_brick_ball_collision()

    if player_score == 4620:  # if the score = this value you had been bricked all bricks and gaining all coins then you will level up
        level_up = True
        congrats()

    glutSwapBuffers()


def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutInitWindowPosition(0, 0)
    glutCreateWindow("Breaking Out Game")
    load_textures()
    glutDisplayFunc(display)
    glutTimerFunc(INTERVAL, game_timer, 1)
    glutPassiveMotionFunc(mouse_callback)
    init()
    glutMainLoop()


main()
