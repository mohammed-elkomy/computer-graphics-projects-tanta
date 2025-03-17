import time
import random
import numpy as np
from random import randint
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import pygame
from pygame import mixer
from pygame import *
pygame.init()
pygame.mixer.pre_init(44100, -16, 2, 512)  #frequancy,audio bit depth, stereo audio, buffersize

####################################
########### constants ##############
####################################

GRID_DIVISION = 40
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
MAX_SPEED = 5
COLLISION_TIME = 0.1  # adjust this value as needed
WINDOW_WIDTH1 = 760
WINDOW_HEIGHT1 = 560
INTERVAL = 1
FONT_DOWNSCALE = 0.18
###
time_in_sec = 0
RIGHT = (1, 0)
LEFT = (-1, 0)
TOP = (0, 1)
BOTTOM = (0, -1)

timer_duration = 30

####################################
########### game state #############
####################################

# current_delta = RIGHT
# chech start, lose and run
start = True    # refer to intro
lose = False
run = False

# Player Position
x = GRID_DIVISION // 2
y = 1

# border
border = []

# path
path = []

collored_cell = 0
####################################
######## graphics helpers ##########
####################################

def init():
    glClearColor(0.0, 0.0, 0.0, 0.0)

    glMatrixMode(GL_PROJECTION)  # ortho or perspective NO BRAINER
    glLoadIdentity()
    glOrtho(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT, 0, 1)  # l,r,b,t,n,f
    glMatrixMode(GL_MODELVIEW)

####################################
############# Texture ##############
####################################
texture_names = 0, 1, 2, 3, 4, 5, 6, 7, 8

def texture_setup(texture_image_binary, texture_name, width, height):
    """  Assign texture attributes to specific images.
    """
    glBindTexture(GL_TEXTURE_2D, texture_name) # texture init step [5]

    # texture init step [6]
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)  # GL_MIRRORED_REPEAT , GL_CLAMP_TO_EDGE, GL_CLAMP_TO_BORDER
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    # END: texture init step [6]

    glTexImage2D(GL_TEXTURE_2D,
                 0,  # mipmap
                 3,  # Bytes per pixel
                 width, height,
                 0,  # Texture border
                 GL_RGBA, GL_UNSIGNED_BYTE, texture_image_binary) # texture init step [7]


def loadTextures():
    """  Open images and convert them to "raw" pixel maps and
             bind or associate each image with and integer refernece number.
    """
    glEnable(GL_TEXTURE_2D) # texture init step 1
    # Load images from file system
    images = [] # texture init step [2]
    images.append(pygame.image.load("img/Player.jpg"))
    images.append(pygame.image.load("img/Path Color.jfif"))
    images.append(pygame.image.load("img/Border.jpg"))
    images.append(pygame.image.load("img/Background.jfif"))
    images.append(pygame.image.load("img/Ball.jpg"))
    images.append(pygame.image.load("img/msg5941770979-4329.jpg"))
    images.append(pygame.image.load("img/Game Over.jfif"))
    images.append(pygame.image.load("img/you win.webp"))
    images.append(pygame.image.load("img/Start.jpg"))

    # Convert images to the type needed for textures
    textures = [pygame.image.tostring(image, "RGBA", True) for image in images] # texture init step [3]

    # Generate textures names from array
    glGenTextures(len(images), texture_names) # texture init step [4]

    # Add textures to openGL
    for i in range(len(images)):
        texture_setup(textures[i],
                      texture_names[i],
                      images[i].get_width(),
                      images[i].get_height())

####################################
############## Sounds ##############
####################################

sound_gameover = mixer.Sound('sound/mixkit-game-over-trombone-1940.ogg')
sound_collison_two_ball =mixer.Sound('sound/mixkit-small-hit-in-a-game-2072.ogg')
sound_collison_ball_border =mixer.Sound('sound/mixkit-golf-ball-hard-hit-2120.ogg')
sound_win =mixer.Sound('sound/mixkit-golf-ball-hard-hit-2120.ogg')
back_ground_music = mixer.Sound('sound/video-game-music.ogg')
if start == False:
    mixer.music.load('sound/mixkit-game-level-music-689.ogg')
    mixer.music.play(-1)
    mixer.music.set_volume(.9)
    # pygame.mixer.pre_init(44100, -16, 2, 512)


####################################
############## Init Balls ##########
####################################

BALL_RADIUS = 10
BALL_COLOR = (1, 1, 0)
BALL_SPEED = 2
NUM_BALLS = 3
cell_width = WINDOW_WIDTH / GRID_DIVISION
cell_height = WINDOW_HEIGHT / GRID_DIVISION
balls = []
for i in range(NUM_BALLS):
    ball_x = random.randint(3, GRID_DIVISION - 2)
    # print(ball_x)
    ball_y = random.randint(3, GRID_DIVISION - 2)
    # print(ball_y)
    ball_direction = [random.choice([-1, 1]), random.choice([-1, 1])]
    balls.append(
        [
            ball_x * cell_width,
            ball_y * cell_height,
            BALL_RADIUS,
            BALL_COLOR,
            BALL_SPEED,
            ball_direction,
        ]
    )

####################################
############## Draw Main ###########
####################################

def draw_cell(i, j,index):

    cell_width = WINDOW_WIDTH / GRID_DIVISION
    cell_height = WINDOW_HEIGHT / GRID_DIVISION
    glBindTexture(GL_TEXTURE_2D, texture_names[index])
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex2d(cell_width * i, cell_height * j)
    glTexCoord2f(1.0, 0.0)
    glVertex2d(cell_width * (i + 1), cell_height * j)
    glTexCoord2f(1.0, 1.0)
    glVertex2d(cell_width * (i + 1), cell_height * (j + 1))
    glTexCoord2f(0.0, 1.0)
    glVertex2d(cell_width * i, cell_height * (j + 1))
    glEnd()

# points of walls
for i in range(GRID_DIVISION):
    border.append((i, 0))
    border.append((i, GRID_DIVISION - 1))

for j in range(GRID_DIVISION):
    border.append((0, j))
    border.append((GRID_DIVISION - 1, j))


def draw_player(a, b):
    # glColor3f(1.0, 0, 1.0)
    draw_cell(a, b, 0)


def draw_path():
    for i, j in path:
        draw_cell(i, j, 1)


def draw_border():
    global collored_cell
    for i, j in border:
        draw_cell(i, j, 2)
        # collored_cell += 1


def draw_ball(ball):
    glBindTexture(GL_TEXTURE_2D, texture_names[4])
    glBegin(GL_POLYGON)
    glColor3f(1,1,1)
    # glColor3f(*ball[3])
    for i in range(360):
        rad = i * np.pi / 180
        x = (ball[0]) + (ball[2] * np.cos(rad)*1.5)
        y = (ball[1]) + (ball[2] * np.sin(rad)*1.5)
        glTexCoord2f(x / 50, y / 50)
        glVertex2f(x, y)
    glEnd()

def draw_balls():
    for ball in balls:
        draw_ball(ball)

####################################
########## Draw Texture ############
####################################

def texture_place_start():
    glColor3f(1, 1, 1)
    glPushMatrix()
    glBindTexture(GL_TEXTURE_2D, texture_names[8])
    glBegin(GL_QUADS)
    glTexCoord2f(0, 1)
    glVertex2d(0, WINDOW_HEIGHT)
    glTexCoord2f(1, 1)
    glVertex2d(WINDOW_WIDTH, WINDOW_HEIGHT)
    glTexCoord2f(1.0, 0)
    glVertex2d(WINDOW_WIDTH, 0)
    glTexCoord2f(0, 0)
    glVertex2d(0, 0)
    glEnd()
    glPopMatrix()


def draw_back_ground():
    glBindTexture(GL_TEXTURE_2D, texture_names[3])
    glBegin(GL_QUADS)
    glColor3f(1.0, 1.0, 1.0) #to make it green
    glTexCoord2f(0.0, 0.0)
    glVertex2d(0, 0)
    glTexCoord2f(1.0, 0.0)
    glVertex2d(WINDOW_WIDTH, 0)
    glTexCoord2f(1.0, 1.0)
    glVertex2d(WINDOW_WIDTH, WINDOW_HEIGHT )
    glTexCoord2f(0.0, 1.0)
    glVertex2d(0, WINDOW_HEIGHT)
    glEnd()

def Game_Over():
    glBindTexture(GL_TEXTURE_2D, texture_names[6])
    glColor(1, 1, 1)
    glBegin(GL_QUADS)

    glTexCoord2f(0.0, 0.0)
    glVertex2d(0, 0)
    glTexCoord2f(1.0, 0.0)
    glVertex2d(WINDOW_WIDTH, 0)
    glTexCoord2f(1.0, 1.0)
    glVertex2d(WINDOW_WIDTH, WINDOW_HEIGHT)
    glTexCoord2f(0.0, 1.0)
    glVertex2d(0, WINDOW_HEIGHT)

    glEnd()

def You_Win():
    glBindTexture(GL_TEXTURE_2D, texture_names[7])
    glColor(1, 1, 1)
    glBegin(GL_QUADS)

    glTexCoord2f(0.0, 0.0)
    glVertex2d(0, 0)
    glTexCoord2f(1.0, 0.0)
    glVertex2d(WINDOW_WIDTH, 0)
    glTexCoord2f(1.0, 1.0)
    glVertex2d(WINDOW_WIDTH, WINDOW_HEIGHT)
    glTexCoord2f(0.0, 1.0)
    glVertex2d(0, WINDOW_HEIGHT)

    glEnd()

####################################
######## Time Remaining ############
####################################

def draw_text(string, x, y):
    glLineWidth(3)
    glColor(1, 1, 1)
    glPushMatrix()
    glTranslate(x, y, 0)
    glScale(FONT_DOWNSCALE, FONT_DOWNSCALE, 1)
    string = string.encode()
    for c in string:
        glutStrokeCharacter(GLUT_STROKE_ROMAN, c)
    glPopMatrix()

def draw_timer():
    global timer_duration, lose
    start_time = 30000 # 30000 almost equal 30 Sec

    for i in range (1,0,-1) :
        time_remaining = int(timer_duration - (pygame.time.get_ticks() - start_time))

    if time_remaining <= 0:
        time_remaining = 0
        lose = True
        sound_gameover.play()

    timer_text = "Time: " + str(time_remaining//1000)
    draw_text(timer_text, (WINDOW_WIDTH1 - 720), (WINDOW_HEIGHT1+190))# Set the timer duration


####################################
######## Collision detection #######
####################################

def update_balls():
    global lose
    for i in range(NUM_BALLS):
        ball1 = balls[i]
        ball1[0] += ball1[4] * ball1[5][0]
        ball1[1] += ball1[4] * ball1[5][1]

        # check if ball hits the walls
        if (
            ball1[0] - ball1[2] == cell_width
            or ball1[0] + ball1[2] == WINDOW_WIDTH - cell_width
        ):
            ball1[5][0] *= -1
            if start == False:
               sound_collison_ball_border.play()
        if (
            ball1[1] - ball1[2] == cell_width
            or ball1[1] + ball1[2] == WINDOW_HEIGHT - cell_width
        ):
            ball1[5][1] *= -1
            if start == False:
               sound_collison_ball_border.play()

        # check if ball intersects with path
        for cell in path:
            print()
            cx, cy = (
                cell[0] * cell_width + cell_width / 2,
                cell[1] * cell_height + cell_height / 2,
            )
            dx, dy = ball1[0] - cx, ball1[1] - cy
            distance = np.sqrt(dx**2 + dy**2)
            if distance < ball1[2] + cell_width / 2:
                lose = True
                if start == False:
                    mixer.music.stop()
                    sound_gameover.play()

        # collision with border
        for cell in border:
            cx, cy = (
                cell[0] * cell_width + cell_width / 2,
                cell[1] * cell_height + cell_height / 2,
            )
            dx, dy = ball1[0] - cx, ball1[1] - cy
            distance = np.sqrt(dx**2 + dy**2)
            if distance < ball1[2] + cell_width / 2:
                ball1[5][0] *= -1
                ball1[5][1] *= -1

        # check for collision with other balls
        for j in range(i + 1, NUM_BALLS):
            ball2 = balls[j]
            dx, dy = ball1[0] - ball2[0], ball1[1] - ball2[1]
            distance = np.sqrt(dx**2 + dy**2)
            if distance < ball1[2] + ball2[2]:
                # calculate new velocities after collision
                if start == False:
                   sound_collison_two_ball.play()
                v1 = np.array(ball1[5]) * ball1[4]
                v2 = np.array(ball2[5]) * ball2[4]
                m1 = np.pi * ball1[2] ** 2  # assuming density is 1
                m2 = np.pi * ball2[2] ** 2
                v1_new = v1 - 2 * m2 / (m1 + m2) * np.dot(
                    v1 - v2, np.array(ball1[0:2]) - np.array(ball2[0:2])
                ) / distance**2 * (np.array(ball1[0:2]) - np.array(ball2[0:2]))
                v2_new = v2 - 2 * m1 / (m1 + m2) * np.dot(
                    v2 - v1, np.array(ball2[0:2]) - np.array(ball1[0:2])
                ) / distance**2 * (np.array(ball2[0:2]) - np.array(ball1[0:2]))
                ball1[5] = list(v1_new / np.linalg.norm(v1_new))
                ball2[5] = list(v2_new / np.linalg.norm(v2_new))
                ball1[4] = np.linalg.norm(v1_new)
                ball2[4] = np.linalg.norm(v2_new)

                # move the balls apart
                overlap_vec = get_overlap_vector(ball1, ball2)
                if overlap_vec is not None:
                    ball1[0] -= overlap_vec[0] * 0.5
                    ball1[1] -= overlap_vec[1] * 0.5
                    ball2[0] += overlap_vec[0] * 0.5
                    ball2[1] += overlap_vec[1] * 0.5

####################################

def get_overlap_vector(ball1, ball2):
    """
    Returns the minimum translation vector needed to separate two balls.
    If the balls do not overlap, returns None.
    """
    dx, dy = ball1[0] - ball2[0], ball1[1] - ball2[1]
    distance = np.sqrt(dx**2 + dy**2)
    if distance >= ball1[2] + ball2[2]:
        return None

    # get the axes of separation
    axes = []
    for angle in range(0, 360, 10):
        axes.append(np.array([np.cos(np.radians(angle)), np.sin(np.radians(angle))]))

    # project the balls onto the axes and check for overlap
    overlap = float("inf")
    overlap_axis = None
    for axis in axes:
        projection1 = project_onto_axis(ball1, axis)
        projection2 = project_onto_axis(ball2, axis)
        if not overlap_on_axis(projection1, projection2):
            return None
        else:
            o = get_overlap_on_axis(projection1, projection2)
            if o < overlap:
                overlap = o
                overlap_axis = axis

    # calculate the minimum translation vector
    mtv = overlap_axis * overlap
    return mtv


def project_onto_axis(ball, axis):
    """
    Projects a ball onto an axis and returns the min and max projection values.
    """
    center = np.array(ball[:2])
    radius = ball[2]
    projection = np.dot(center, axis)
    min_proj = projection - radius
    max_proj = projection + radius
    return (min_proj, max_proj)


def overlap_on_axis(projection1, projection2):
    """
    Checks if two 1D projections overlap.
    """
    return (projection1[0] <= projection2[1]) and (projection2[0] <= projection1[1])


def get_overlap_on_axis(projection1, projection2):
    """
    Returns the overlap distance between two 1D projections.
    Assumes that the projections overlap.
    """
    return min(projection1[1], projection2[1]) - max(projection1[0], projection2[0])

##############################################

def game():
        global path, border, lose, collored_cell, start
        if start == False:
            draw_back_ground()
            draw_balls()
            
            if not lose:
                draw_timer()
                update_balls()

            # check losing
            if (x, y) in path:
                if (x, y) not in border:
                    lose = True
            # Check if the player has touched the border
            if (x, y) in border:
                # Append the points in the path and border to the border list
                for point in path:
                    if point not in border:
                        border.append(point)
                        collored_cell += 1
                        print(collored_cell)
                path.clear()
                #glColor(1, 1, 0)  # Set color to white
                draw_border()
                #glColor(1, 1, 1)
                draw_path()
                #glColor(1, 0, 1)
                draw_player(x, y)

            else:
                #glColor(1, 1, 0)  # Set color to white
                draw_border()
                #glColor(1, 1, 1)
                draw_path()
                #glColor(1, 0, 1)
                draw_player(x, y)

####################################
############# Game State ###########
####################################

def intro():
    global start
    if start ==True:

       texture_place_start()
       back_ground_music.play()

    else:
        game()

def check_Win():
    global collored_cell, sound_win
    if collored_cell >= 500:
        mixer.music.stop()
        sound_win.play()
        return True

def game_state():
    global lose
    if lose:
        Game_Over()
    elif check_Win():
        You_Win()

####################################
############# display ##############
####################################

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glClearColor(0, 0, 0, 0)

    intro()
    game()
    game_state()

    glutSwapBuffers()

####################################
############### Timers #############
####################################

def game_timer(v):
    display()
    glutTimerFunc(INTERVAL, game_timer, 1)

####################################
############ Keyboard ##############
####################################

def keyboard(key, xx, yy):
    global start
    if key == b's':
        start = False
        back_ground_music.stop()
    elif key == b'q':
        os._exit(0)


def keyboard_callback(key, X, Y):
    global x, y, lose
    if not lose:
        path.append((x, y))
        if key == GLUT_KEY_LEFT and x > 0:
            x -= 1
        elif key == GLUT_KEY_RIGHT and x < GRID_DIVISION - 1:
            x += 1
        elif key == GLUT_KEY_UP and y < GRID_DIVISION - 1:
            y += 1
        elif key == GLUT_KEY_DOWN and y > 0:
            y -= 1
####################################
############ flood Fill ##############
####################################





####################################
############  ##############
####################################
if __name__ == "__main__":
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutInitWindowPosition(0, 0)
    glutCreateWindow(b"2d Xonix")

    loadTextures()
    glutDisplayFunc(display)
    # glutDisplayFunc(Game_Over)
    # glutDisplayFunc(game)
    # glutDisplayFunc(texture_place_start)

    glutTimerFunc(INTERVAL, game_timer, 1)
    glutSpecialFunc(keyboard_callback)
    glutKeyboardFunc(keyboard)
    init()
    glutMainLoop()

####################################
############# DRAW Time Remaing #########
####################################
# Set the timer duration
# timer_duration = 30
#
# # Function to render text on the screen
# def draw_text(string, x, y):
#     glLineWidth(2)
#     glColor(0, 0, 1)
#     glPushMatrix()
#     glTranslate(x, y, 0)
#     glScale(FONT_DOWNSCALE, FONT_DOWNSCALE, 1)
#     string = string.encode()
#     for c in string:
#         glutStrokeCharacter(GLUT_STROKE_ROMAN, c)
#     glPopMatrix()
#
# def timer(seconds):
#     global lose
#     time_remaining = seconds
#     while time_remaining > 0:
#         timer_text = "Time: " + str(time_remaining)
#         draw_text(timer_text, (WINDOW_WIDTH - 3), (WINDOW_HEIGHT - 1))
#         # time.sleep(1)
#         pygame.time.delay(1000)
#         time_remaining -= 1
#
#     lose = True

###another function
# Function to draw the timer on the screen
# def draw_timer():
#     global timer_duration, lose
#     start_time = time.time()
#     time_remaining = int(timer_duration - (time.time() - start_time))
#     if time_remaining <= 0:
#         time_remaining = 0
#         lose = True
#     timer_text = "Time: " + str(time_remaining)
#     draw_text(timer_text, (WINDOW_WIDTH - 3), (WINDOW_HEIGHT-1))# Set the timer duration






