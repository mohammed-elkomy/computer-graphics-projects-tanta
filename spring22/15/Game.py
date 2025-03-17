# -------------------------------------------------------------
# importing necessary libraries
import sys
import time
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
from math import *
import pygame
# -------------------------------------------------------------

# -------------------------------------------------------------
# constants
FONT_DOWNSCALE = .013
INTERVAL = 10
X_LIMIT = 20
Y_LIMIT = 20
Z_LIMIT = 20
raduis = .5
COIN_POSITION = []
COIN_NUMBER = 0

# to change number of coins edit range step
for x in np.arange(-10, 11, 2):
    for y in np.arange(-6, 7, 4):
        COIN_POSITION.append((x, y))
        COIN_NUMBER += 1

# dimention : left, right, top, bottom
start_diemntions = [-14, -10.95, 3, -3]
center_diemntions = [-10.95, 10.95, 7, -7]
out_diemntions = [10.95, 14, 3, -3]

# in the center of start part
player_initial_h_position = (start_diemntions[0] + start_diemntions[1]) / 2
step = .1

obstacles1_h_position = []          # red obstacles
for i in np.arange(-10, 13, 4):
    obstacles1_h_position.append(i)

obstacles2_h_position = []          # blue obstacles
for i in np.arange(-8, 10, 4):
    obstacles2_h_position.append(i)
# -------------------------------------------------------------

# -------------------------------------------------------------
# helpers
coin_rotate = 0
start_ang = 0
end_ang = 360
move_left = 1
move_right = 2
move_up = 3
move_down = 4
# -------------------------------------------------------------

# -------------------------------------------------------------
# states
current_move = 0
vertical_shift = 0
horizotal_shift = 0
score = 0
player_face = 0
delta_y_obstacles1 = .13
delta_y_obstacles2 = -.13
vertical_shift_obstacles1 = 0
vertical_shift_obstacles2 = 0
start_play = False
alive = True
winner = False
sound = True
win_sound = True
lose_sound = True
# -------------------------------------------------------------
# Texture
texture_names = [0, 1, 2, 3, 4]


def my_init():
    global X_LIMIT
    global y_LIMIT
    global Z_LIMIT

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-X_LIMIT, X_LIMIT, -X_LIMIT, X_LIMIT, -Z_LIMIT, Z_LIMIT)

    glMatrixMode(GL_MODELVIEW)
    loadTextures()
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)


def texture_setup(texture_image_binary, texture_name, width, height):

    glBindTexture(GL_TEXTURE_2D, texture_name)

    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

    glTexImage2D(GL_TEXTURE_2D,
                 0,  # mipmap
                 GL_RGBA,  # FOR BLENDING
                 width, height,
                 0,  # Texture border
                 # RGBA Exactly as in  pygame.image.tostring(image, "RGBA", True)
                 GL_RGBA,
                 GL_UNSIGNED_BYTE,
                 texture_image_binary)


def loadTextures():
    glEnable(GL_TEXTURE_2D)

    images = []
    images.append(pygame.image.load("pict.png"))
    images.append(pygame.image.load("background.png"))
    images.append(pygame.image.load("background2.png"))
    images.append(pygame.image.load("win.png"))
    images.append(pygame.image.load("loss.png"))

    textures = [pygame.image.tostring(image, "RGBA", True)
                for image in images]

    glGenTextures(len(images), texture_names)

    for i in range(len(images)):
        texture_setup(textures[i],
                      texture_names[i],
                      images[i].get_width(),
                      images[i].get_height())


def draw_text(string, x, y):
    global FONT_DOWNSCALE

    glLineWidth(4)
    glColor3ub(32, 212, 151)
    glLoadIdentity()
    glTranslate(x, y, 0)
    glScale(FONT_DOWNSCALE, FONT_DOWNSCALE, 1)
    string = string.encode()
    for c in string:
        glutStrokeCharacter(GLUT_STROKE_ROMAN, c)
    glLoadIdentity()


def draw_start():
    global X_LIMIT
    global Y_LIMIT

    glColor3ub(255, 255, 255)
    glBindTexture(GL_TEXTURE_2D, texture_names[2])
    glBegin(GL_POLYGON)
    glTexCoord2f(0, 0)
    glVertex2d(-X_LIMIT, -Y_LIMIT)
    glTexCoord2f(1, 0)
    glVertex2d(X_LIMIT, -Y_LIMIT)
    glTexCoord2f(1, 1)
    glVertex2d(X_LIMIT, Y_LIMIT)
    glTexCoord2f(0, 1)
    glVertex2d(-X_LIMIT, Y_LIMIT)
    glEnd()
    glutSwapBuffers()


def draw_loss():
    global X_LIMIT
    global Y_LIMIT
    global lose_sound

    if lose_sound:
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.Channel(0).play(pygame.mixer.Sound('lose.mp3'))
    # Channel(0) so it will play over start and game sound
    # the previous if condition won't be executed again and the sound will continue playing
    lose_sound = False

    glColor3ub(255, 255, 255)
    glBindTexture(GL_TEXTURE_2D, texture_names[4])
    glBegin(GL_POLYGON)
    glTexCoord2f(0, 0)
    glVertex2d(-X_LIMIT, -Y_LIMIT)
    glTexCoord2f(1, 0)
    glVertex2d(X_LIMIT, -Y_LIMIT)
    glTexCoord2f(1, 1)
    glVertex2d(X_LIMIT, Y_LIMIT)
    glTexCoord2f(0, 1)
    glVertex2d(-X_LIMIT, Y_LIMIT)
    glEnd()
    glutSwapBuffers()


def draw_win():
    global X_LIMIT
    global Y_LIMIT
    global win_sound

    if win_sound:
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.Channel(0).play(pygame.mixer.Sound('win.mp3'))
    # Channel(0) so it will play over start and game sound
    # the previous if condition won't be executed again and the sound will continue playing
    win_sound = False

    glColor3ub(255, 255, 255)
    glBindTexture(GL_TEXTURE_2D, texture_names[3])
    glBegin(GL_POLYGON)
    glTexCoord2f(0, 0)
    glVertex2d(-X_LIMIT, -Y_LIMIT)
    glTexCoord2f(1, 0)
    glVertex2d(X_LIMIT, -Y_LIMIT)
    glTexCoord2f(1, 1)
    glVertex2d(X_LIMIT, Y_LIMIT)
    glTexCoord2f(0, 1)
    glVertex2d(-X_LIMIT, Y_LIMIT)
    glEnd()
    glutSwapBuffers()


def draw_background():
    global X_LIMIT
    global Y_LIMIT
    glColor3ub(255, 41, 255)

    glColor3ub(255, 255, 255)
    glBindTexture(GL_TEXTURE_2D, texture_names[1])
    glBegin(GL_POLYGON)
    glTexCoord2f(0, 0)
    glVertex2d(-X_LIMIT, -Y_LIMIT)
    glTexCoord2f(1, 0)
    glVertex2d(X_LIMIT, -Y_LIMIT)
    glTexCoord2f(1, 1)
    glVertex2d(X_LIMIT, Y_LIMIT)
    glTexCoord2f(0, 1)
    glVertex2d(-X_LIMIT, Y_LIMIT)
    glEnd()


def draw_game_body():
    global start_diemntions
    global center_diemntions
    global out_diemntions

    # center
    glColor3ub(255, 255, 255)
    glBindTexture(GL_TEXTURE_2D, texture_names[0])
    glBegin(GL_POLYGON)
    glTexCoord2f(0, 1)
    glVertex2d(center_diemntions[0], center_diemntions[3])
    glTexCoord2f(1, 1)
    glVertex2d(center_diemntions[1], center_diemntions[3])
    glTexCoord2f(1, 0)
    glVertex2d(center_diemntions[1], center_diemntions[2])
    glTexCoord2f(0, 0)
    glVertex2d(center_diemntions[0], center_diemntions[2])
    glEnd()

    # start
    glColor3ub(105, 219, 143)
    glBegin(GL_POLYGON)
    glVertex2d(start_diemntions[0], start_diemntions[3])
    glVertex2d(start_diemntions[1], start_diemntions[3])
    glVertex2d(start_diemntions[1], start_diemntions[2])
    glVertex2d(start_diemntions[0], start_diemntions[2])
    glEnd()

    # out
    glColor3ub(105, 219, 143)
    glBegin(GL_POLYGON)
    glVertex2d(out_diemntions[0], out_diemntions[3])
    glVertex2d(out_diemntions[1], out_diemntions[3])
    glVertex2d(out_diemntions[1], out_diemntions[2])
    glVertex2d(out_diemntions[0], out_diemntions[2])
    glEnd()


def draw_game_border():
    global start_diemntions
    global center_diemntions
    global out_diemntions
    
    glLineWidth(4)
    glColor3ub(0, 0, 0)

    # border
    glBegin(GL_LINE_STRIP)
    glVertex2d(start_diemntions[0], start_diemntions[3])
    glVertex2d(start_diemntions[1], start_diemntions[3])
    glVertex2d(start_diemntions[1], center_diemntions[3])
    glVertex2d(center_diemntions[1], center_diemntions[3])
    glVertex2d(center_diemntions[1], out_diemntions[3])
    glVertex2d(out_diemntions[1], out_diemntions[3])
    glVertex2d(out_diemntions[1], out_diemntions[2])
    glVertex2d(out_diemntions[0], out_diemntions[2])
    glVertex2d(center_diemntions[1], center_diemntions[2])
    glVertex2d(center_diemntions[0], center_diemntions[2])
    glVertex2d(start_diemntions[1], start_diemntions[2])
    glVertex2d(start_diemntions[0], start_diemntions[2])
    glVertex2d(start_diemntions[0], start_diemntions[3])
    glEnd()

    # corners
    glPointSize(4)
    glBegin(GL_POINTS)
    glVertex2d(start_diemntions[0], start_diemntions[3])
    glVertex2d(start_diemntions[1], start_diemntions[3])
    glVertex2d(start_diemntions[1], center_diemntions[3])
    glVertex2d(center_diemntions[1], center_diemntions[3])
    glVertex2d(center_diemntions[1], out_diemntions[3])
    glVertex2d(out_diemntions[1], out_diemntions[3])
    glVertex2d(out_diemntions[1], out_diemntions[2])
    glVertex2d(out_diemntions[0], out_diemntions[2])
    glVertex2d(center_diemntions[1], center_diemntions[2])
    glVertex2d(center_diemntions[0], center_diemntions[2])
    glVertex2d(start_diemntions[1], start_diemntions[2])
    glVertex2d(start_diemntions[0], start_diemntions[2])
    glVertex2d(start_diemntions[0], start_diemntions[3])
    glEnd()


def draw_coin():
    global coin_rotate

    glRotate(coin_rotate, 0, 1, 0)
    glScale(.7, 1, 1)

    glColor3ub(186, 122, 1)
    glutSolidTorus(.1, .5, 10, 10)
    glLoadIdentity()
    


def draw_coins():
    global coin_rotate
    global COIN_POSITION
    for i, z in COIN_POSITION:
        glLoadIdentity()
        glTranslate(i, z, 0)
        glScale(.5, .5, 0)
        draw_coin()
    coin_rotate += 3

def draw_player():
    global raduis
    global start_ang
    global end_ang
    global player_initial_h_position
    global player_face

    glColor(1, 1, 0)
    resolution = 1

    # toggling between two cases
    if start_ang == 30 and end_ang == 330:
        start_ang = 0
        end_ang = 360
    elif start_ang == 0 and end_ang == 360:
        start_ang = 30
        end_ang = 330

    move_player()
    glRotate(player_face, 0, 0, 1)
    glScale(.8, .8, 1)


    glBegin(GL_POLYGON)
    # to make to polygon connect to this point so it appears as oppenning it's mouth
    glVertex(0, 0, 0)
    for ang in np.arange(start_ang, end_ang, resolution):
        x = raduis * cos(ang * pi / 180)
        y = raduis * sin(ang * pi / 180)
        glVertex(x, y, 0)

    glEnd()


def move_player():
    global current_move
    global vertical_shift
    global horizotal_shift
    global start_diemntions
    global center_diemntions
    global out_diemntions
    global player_initial_h_position
    global raduis

    # player in start

    if start_diemntions[0] <= (horizotal_shift + player_initial_h_position) < start_diemntions[1] \
            and start_diemntions[3] <= vertical_shift <= start_diemntions[2]:
        if current_move == move_left:
            horizotal_shift = max(horizotal_shift + player_initial_h_position -
                                  step, raduis + start_diemntions[0]) - player_initial_h_position
        if current_move == move_right:
            horizotal_shift += step
        if current_move == move_up:
            vertical_shift = min(vertical_shift + step,
                                 start_diemntions[2] - raduis)
        if current_move == move_down:
            vertical_shift = max(vertical_shift - step,
                                 start_diemntions[3] + raduis)

    # player in center
    if center_diemntions[0] <= (horizotal_shift + player_initial_h_position) < center_diemntions[1] \
            and center_diemntions[3] <= vertical_shift <= center_diemntions[2]:

        if start_diemntions[2] <= vertical_shift <= center_diemntions[2] or \
                center_diemntions[3] <= vertical_shift <= start_diemntions[3]:
            if current_move == move_left:
                horizotal_shift = max(horizotal_shift + player_initial_h_position -
                                      step, center_diemntions[0] + raduis) - player_initial_h_position
            if current_move == move_right:
                horizotal_shift = min(horizotal_shift + player_initial_h_position +
                                      step, center_diemntions[1] - raduis) - player_initial_h_position

        else:
            if current_move == move_left:
                horizotal_shift -= step
            if current_move == move_right:
                horizotal_shift += step
        if current_move == move_up:
            vertical_shift = min(vertical_shift + step,
                                 center_diemntions[2] - raduis)
        if current_move == move_down:
            vertical_shift = max(vertical_shift - step,
                                 center_diemntions[3] + raduis)

    # player in out
    if out_diemntions[0] <= (horizotal_shift + player_initial_h_position) <= out_diemntions[1] \
            and out_diemntions[3] <= vertical_shift <= out_diemntions[2]:
        if current_move == move_left:
            horizotal_shift -= step
        if current_move == move_right:
            horizotal_shift = min(horizotal_shift + player_initial_h_position +
                                  step, out_diemntions[1] - .01 - raduis) - player_initial_h_position
        if current_move == move_up:
            vertical_shift = min(vertical_shift + step,
                                 out_diemntions[2] - raduis)
        if current_move == move_down:
            vertical_shift = max(vertical_shift - step,
                                 out_diemntions[3] + raduis)

    glTranslate(player_initial_h_position, 0, 0)
    glTranslate(horizotal_shift, vertical_shift, 0)


def draw_obstacales():
    global center_diemntions
    global vertical_shift_obstacles1
    global vertical_shift_obstacles2
    global delta_y_obstacles1
    global delta_y_obstacles2
    global obstacles1_h_position
    global obstacles2_h_position

    edge = .9
    # group 1 obstacles
    for i in obstacles1_h_position:
        glLoadIdentity()
        glTranslate(i, vertical_shift_obstacles1, 0)

        glColor3ub(123, 12, 32)
        glutSolidCube(edge)
        glColor3ub(0, 0, 0)
        glLineWidth(2)
        glutWireCube(edge)

    # group 2 obstacles
    for i in obstacles2_h_position:
        glLoadIdentity()
        glTranslate(i, vertical_shift_obstacles2, 0)

        glColor(0, 0, 1)
        glutSolidCube(.9)
        glColor3ub(0, 0, 1)
        glLineWidth(2)
        glutWireCube(.9)

    if vertical_shift_obstacles1 >= center_diemntions[2] - 1 * edge or vertical_shift_obstacles1 <= center_diemntions[3] + 1 * edge:
        delta_y_obstacles1 = -delta_y_obstacles1

    if vertical_shift_obstacles2 >= center_diemntions[2] - 1 * edge or vertical_shift_obstacles2 <= center_diemntions[3] + 1 * edge:
        delta_y_obstacles2 = -delta_y_obstacles2

    vertical_shift_obstacles1 += delta_y_obstacles1
    vertical_shift_obstacles2 += delta_y_obstacles2


def obstacles_collisions():
    global obstacles1_h_position
    global obstacles2_h_position
    global player_initial_h_position
    global vertical_shift_obstacles1
    global vertical_shift_obstacles2
    global vertical_shift
    global horizotal_shift
    global alive

    # detect collisions with obstacles1
    for position in obstacles1_h_position:
        if abs(horizotal_shift + player_initial_h_position - position) <= 1.3 * raduis and \
                abs(vertical_shift - vertical_shift_obstacles1) <= 1.3 * raduis:
            alive = False

    # detect collisions with obstacles2
    for position in obstacles2_h_position:
        if abs(horizotal_shift + player_initial_h_position - position) <= 1.3 * raduis and \
                abs(vertical_shift - vertical_shift_obstacles2) <= 1.3 * raduis:
            alive = False
    # abs is used to make the value of distance always positive even if the player in the negative part of screen
    # range distance is 1.3 * raduis and if the distance is less than that a collision is detected 


def eat_coin():
    global COIN_POSITION
    global player_initial_h_position
    global vertical_shift
    global horizotal_shift
    global raduis
    global score

    for coin_x, coin_y in COIN_POSITION:
        if abs(horizotal_shift + player_initial_h_position - coin_x) <= raduis and \
                abs(vertical_shift - coin_y) <= raduis:
            COIN_POSITION.remove((coin_x, coin_y))
            score += 1
            pygame.init()
            pygame.mixer.init()
            pygame.mixer.Channel(1).play(pygame.mixer.Sound('coin.mp3'))


def player_in_out():
    global player_initial_h_position
    global vertical_shift
    global horizotal_shift
    global out_diemntions

    if out_diemntions[0] <= (horizotal_shift + player_initial_h_position) <= out_diemntions[1] \
            and out_diemntions[3] <= vertical_shift <= out_diemntions[2]:
        return True

    return False


def keyboard_callback(key, x, y):
    global current_move
    global move_left
    global move_right
    global move_up
    global move_down
    global player_face

    if key == GLUT_KEY_LEFT:
        current_move = move_left
        player_face = 180

    if key == GLUT_KEY_RIGHT:
        current_move = move_right
        player_face = 0

    if key == GLUT_KEY_UP:
        current_move = move_up
        player_face = 90

    if key == GLUT_KEY_DOWN:
        current_move = move_down
        player_face = 270


def mouse2(button, state, x, y):
    global start_play
    global alive
    global winner

    if alive == False or winner == True:
        if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN and 255 < x < 545 and 615 < y < 730:
            sys.quit()

    if start_play == False:
        if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN and 230 < x < 575 and 568 < y < 630:
            start_play = True


num_frames = 0
start = time.time()


def game():
    global score
    global COIN_NUMBER
    global winner

    draw_background()
    draw_game_body()
    draw_game_border()
    draw_coins()
    draw_player()
    eat_coin()
    text1 = 'Score: ' + str(score) + ' \ ' + str(COIN_NUMBER)
    draw_obstacales()
    obstacles_collisions()
    draw_text(text1, -7, 7.5)
    if score == COIN_NUMBER and player_in_out():
        winner = True

    glutSwapBuffers()


def draw():
    global num_frames
    num_frames += 1
    # print(num_frames/(time.time()-start))=
    global alive
    global winner
    global sound

    glClearColor(1, 1, 1, 1)
    glClear(GL_COLOR_BUFFER_BIT)

    if sound:
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.Channel(0).play(pygame.mixer.Sound('start.mp3'))
    sound = False  # the previous if condition won't be executed again and the sound will continue playing

    if not start_play:
        draw_start()

    else:

        if alive == True and winner == False:
            game()

        if alive == False:
            draw_loss()

        if winner == True:
            draw_win()


def timer(v):
    draw()
    glutTimerFunc(INTERVAL, timer, 1)


def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowPosition(0, 0)
    glutInitWindowSize(800, 800)
    glutCreateWindow(b"7RAMY ELSOKAR")
    my_init()
    glutTimerFunc(INTERVAL, timer, 1)
    glutDisplayFunc(draw)
    glutSpecialFunc(keyboard_callback)
    glutMouseFunc(mouse2)
    glutMainLoop()


if __name__ == '__main__':
    main()
