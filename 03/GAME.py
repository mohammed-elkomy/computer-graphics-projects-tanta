import random

import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

################
#  CONSTANTS   #
################
FONT_DOWNSCALE = 0.004
INTERVAL = 10  # speed
WINDOW_WIDTH = WINDOW_HEIGHT = 800
LAST_PLAY = False
POSITIONS_LIST = [0, 2, -2]  # NEW BALLS RANDOM POSITIONS
START_GAME = False
AT_START = True
PLAY = False
BEGIN = True

TEXTURE_NAMES = 0, 1, 2, 3, 4  # Texture Names List
POINTS = 0  # POINTS COUNTER
LEVEL = 1
# main ball PARAMETERS
MAIN_BALL_COLOR = [232, 99, 10]
MAIN_BALL_Y = 0
MAIN_BALL_CURR_X = 0  # curr main ball continuous position
MAIN_BALL_NEXT_X = 0  # next main ball discrete position
DIREC = "STOP"

# JUMPING
JUMPING = False
NEXT_JUMP = False
FALLING = False

# WALL PARAMETERS
WALL_Z = -140  # at infinity
SHOW_WALL = False
WALL_COLOR = [84, 99, 255]  # green

# generating stars position 1 time @ first
STARS_POSITIONS = []

# STATES
DEAD = False
PAUSE = False

# WINING PARAMETERS
LEVEL_UP = False  # if True: show winning window
GO_NEXT_LEVEL = False  # if True: CONTINUE
INC_LEVEL = False  # if True: increment LEVEL one time
# main goal to handle case of incrementing LEVELS more than 1 time while showing winning window
ENTERED_NEXT_LEVEL = False  # ^
# WINNING BOX ROTATION PARAMETERS
ROT_ANGLE = 0
ROT_DIREC = 1  # direction of rotation of the winning box <->

FINISH_Z = -400  # detecting the end of the level
STARS_DELTA_Y = 0
ROAD_DELTA_Z = 0
BALL_ROT_ANGLE = 0
for _i in range(100):
    _x = random.uniform(-2, 2)  # float no
    _y = random.uniform(-3, 3)
    STARS_POSITIONS.append((_x, _y))


################
#   TEXTURE    #
################
def init_textures():
    loadTextures()


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
                 3,  # Bytes per pixel
                 width, height,
                 0,  # Texture border
                 GL_RGBA,  # RGBA Exactly as in  pygame.image.tostring(image, "RGBA", True)
                 GL_UNSIGNED_BYTE,
                 texture_image_binary)  # texture init step [7]


def loadTextures():
    """  Open images and convert them to "raw" pixel maps and
             bind or associate each image with and integer reference number.
    """
    glEnable(GL_TEXTURE_2D)  # texture init step [1]

    # Load images from file system
    images = [pygame.image.load("road_tex6.png"),
              pygame.image.load("interface_off.jpg"),
              pygame.image.load("interface_on.jpg"),
              pygame.image.load("race-finish.png"),
              pygame.image.load("skky.png")]  # texture init step [2]

    # textures list contains all images in the needed format for textures
    textures = [pygame.image.tostring(image, "RGBA", True)
                for image in images]  # texture init step [3]

    # Generate textures names from TEXTURE_NAMES list
    glGenTextures(len(images), TEXTURE_NAMES)  # texture init step [4]

    # Add textures to openGL
    for i in range(len(images)):
        texture_setup(textures[i],  # binary images
                      TEXTURE_NAMES[i],  # identifiers
                      images[i].get_width(),
                      images[i].get_height())


####################################
#     Helper Funcs  and classes    #
####################################

# BALL CLASS #
class Ball:

    def __init__(self, x, y, z, radius, color):
        self.x = x
        self.y = y
        self.z = z
        self.radius = radius

        self.color = color

        self.scale = [0.5, 0.5, 0.5]

    def draw(self):
        glColor3ub(self.color[0], self.color[1], self.color[2])

        glLoadIdentity()
        reposition_camera()

        glTranslatef(self.x, self.y, self.z)
        glScale(self.scale[0], self.scale[1], self.scale[2])

        glutSolidSphere(1, 20, 10)


def change_wall_color():
    global WALL_COLOR, COLORS_LIST, MAIN_BALL_COLOR

    # list of objects without the curr color
    colors_except_curr_color = [each_color for each_color in COLORS_LIST if each_color not in MAIN_BALL_COLOR]

    # randomly select a color from this list
    WALL_COLOR = random.choice(colors_except_curr_color)


def draw_wall(z, color_r=232, color_g=99, color_b=10):
    glColor3ub(color_r, color_g, color_b)
    glLoadIdentity()
    reposition_camera()
    glTranslate(0, 0, z)
    glScale(6, 1, 1)
    glutSolidCube(1)


def draw_star(x, y):
    global STARS_DELTA_Y
    glPointSize(4)
    glBegin(GL_POINTS)
    glVertex(x, y)
    glEnd()


def draw_2d_texture(x1, x2, y1, y2):
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


def draw_rectangle_xy(x1, x2, y1, y2):
    glBegin(GL_QUADS)

    glVertex(x1, y2)

    glVertex(x1, y1)

    glVertex(x2, y1)

    glVertex(x2, y2)
    glEnd()


def init_projection_ortho(z_near=-1, z_far=1):
    glLoadIdentity()
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-1, 1, -1, 1, z_near, z_far)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def init_projection():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1, 1, 100)
    glMatrixMode(GL_MODELVIEW)


def reposition_camera():
    gluLookAt(0, 3.5, 10,
              0, 0, 0,
              0, 1, 0)


def draw_axes():  # DELETE THIS LATER
    glBegin(GL_LINES)

    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(100, 0.0, 0.0)

    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(0.0, 100.0, 0.0)

    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, -100.0)
    glVertex3f(0.0, 0.0, 100.0)

    glEnd()


#################################################
#        (start + pause + end) STATES           #
#################################################

# reset parameters (constants) to default
def reset():
    global ROAD_DELTA_Z, TEXTURE_NAMES, POINTS, MAIN_BALL_Y, \
        LEVEL, MAIN_BALL_CURR_X, MAIN_BALL_NEXT_X, DIREC, \
        JUMPING, WALL_Z, SHOW_WALL, WALL_COLOR, DEAD, STARS_DELTA_Y, \
        MAIN_BALL_COLOR, START_GAME, NEXT_JUMP, FALLING, PAUSE, \
        ROT_ANGLE, FINISH_Z, LEVEL_UP, ROT_DIREC, GO_NEXT_LEVEL, INC_LEVEL, \
        ENTERED_NEXT_LEVEL, BALL_ROT_ANGLE

    ROAD_DELTA_Z = 0
    TEXTURE_NAMES = 0, 1, 2, 3, 4  # Texture Names List
    POINTS = 0  # POINTS COUNTER
    MAIN_BALL_Y = 0
    LEVEL = 1
    MAIN_BALL_CURR_X = 0  # curr main ball continuous position
    MAIN_BALL_NEXT_X = 0  # next main ball discrete position
    DIREC = "STOP"
    JUMPING = False
    NEXT_JUMP = False
    FALLING = False
    WALL_Z = -140  # at infinity
    SHOW_WALL = False
    WALL_COLOR = [84, 99, 255]  # green
    DEAD = False
    STARS_DELTA_Y = 0
    START_GAME = True
    BALLS_LIST.clear()
    BALLS_LIST.append(Ball(0, 0, -100, 0.5, COLORS_LIST[0]))
    MAIN_BALL_COLOR = COLORS_LIST[0]
    PAUSE = False
    ROT_ANGLE = 0
    FINISH_Z = -400
    LEVEL_UP = False
    INC_LEVEL = False
    GO_NEXT_LEVEL = False
    ENTERED_NEXT_LEVEL = False
    ROT_DIREC = 1
    BALL_ROT_ANGLE = 0


def draw_start():
    global LAST_PLAY, BEGIN, PLAY, AT_START, START_GAME, INTERVAL

    if LAST_PLAY and BEGIN:
        glBindTexture(GL_TEXTURE_2D, TEXTURE_NAMES[1])
        draw_2d_texture(-1, 1, -1, 1)
        PLAY = BEGIN = False
        START_GAME = True
        INTERVAL = 10

    elif PLAY and AT_START:
        glBindTexture(GL_TEXTURE_2D, TEXTURE_NAMES[2])
        draw_2d_texture(-1, 1, -1, 1)
        PLAY = False
        LAST_PLAY = True
        AT_START = False  # prevent from previewing start menu while playing if s is pressed

    elif BEGIN:
        glBindTexture(GL_TEXTURE_2D, TEXTURE_NAMES[1])
        draw_2d_texture(-1, 1, -1, 1)


def draw_pause():
    # text
    string = "F1 to CONTINUE"
    draw_text_center(string, 0, -0.36, 0.0003)  # PAUSE STATE

    # "||" inside a box
    glColor3f(1, 1, 1)
    draw_rectangle_xy(-.2, -.1, -.2, .2)
    draw_rectangle_xy(.2, .1, -.2, .2)
    glColor3ub(252, 217, 0)
    draw_rectangle_xy(-0.3, 0.3, -0.3, 0.3)

    # border for the previous box
    glColor3ub(232, 99, 10)
    draw_rectangle_xy(-0.32, 0.32, 0.32, -0.32)

    # box for "F1 to CONTINUE"
    glColor3ub(224, 77, 1)
    draw_rectangle_xy(-0.32, 0.32, -0.32, -0.44)


def draw_wining_box():
    glBegin(GL_POLYGON)
    glVertex(0, 0.6)
    glVertex(0.4, 0.3)
    glVertex(-0.4, 0.3)
    glEnd()

    glBegin(GL_POLYGON)
    glVertex(0, 0.2)
    glVertex(0.4, 0.5)
    glVertex(-0.4, 0.5)
    glEnd()


def winning():
    global ROT_ANGLE, LEVEL, ROT_DIREC

    if ROT_ANGLE == 10:
        ROT_DIREC = -1
    if ROT_ANGLE == -10:
        ROT_DIREC = 1

    if ROT_DIREC == 1:
        ROT_ANGLE = min(ROT_ANGLE + .2, 10)
    else:
        ROT_ANGLE = max(ROT_ANGLE - .2, -10)

    glRotate(ROT_ANGLE, 0, 0, 1)

    # text
    string = "UP TO LEVEL " + str(LEVEL)
    draw_text_center(string, 0, 0.4, 0.0004)

    # wining box --------------------------
    glColor3ub(113, 43, 117)
    draw_wining_box()
    # --------------------------------------

    glTranslate(0, -0.08, 0)  # to center it
    # border for wining box ----------------
    glColor3ub(233, 166, 166)
    glScale(1.2, 1.2, 1)
    draw_wining_box()
    # ---------------------------------------
    glLoadIdentity()

    string = "CONTINUE"
    draw_text_center(string, 0, 0, 0.001)

    string = "F1 to continue"
    draw_text_center(string, 0, -.18, 0.0004)
    # Some effects for box! (triangle)---------
    glColor3ub(213, 153, 191)
    glBegin(GL_POLYGON)
    glVertex(-0.38, -0.13)
    glVertex(0.38, -0.13)
    glVertex(-0.38, 0.08)
    glEnd()
    # -----------------------------------------

    # Box for continue-------------------------
    glColor3ub(193, 85, 154)
    draw_rectangle_xy(-0.4, 0.4, -0.15, 0.1)
    # -----------------------------------------

    # Box for f1-------------------------------
    glColor3ub(70, 36, 76)
    draw_rectangle_xy(-0.42, 0.42, -.25, 0.12)
    # -----------------------------------------


def draw_end():
    init_projection_ortho()
    gluLookAt(0, 0, 0, 0, 0, -1, 0, 1, 0)

    string = "GAME OVER!"
    # repeating with a little change in place (BOLD effect)
    draw_text_center(string, 0, 0.305, 0.0015)
    draw_text_center(string, 0, 0.3, 0.0015)
    draw_text_center(string, 0, 0.295, 0.0015)

    string = "RESTART"
    draw_text_center(string, 0, 0, 0.001)

    string = "F1 to restart"
    draw_text_center(string, 0, -.18, 0.0004)

    # NOTE : HERE order matters

    # triangle for some effects !!
    glColor3ub(255, 141, 41)
    glBegin(GL_POLYGON)
    glVertex(-0.38, -0.13)
    glVertex(0.38, -0.13)
    glVertex(-0.38, 0.08)
    glEnd()

    # Box for restart
    glColor3ub(241, 45, 45)
    draw_rectangle_xy(-0.4, 0.4, -0.15, 0.1)

    # Box for f1
    glColor3ub(178, 39, 39)
    draw_rectangle_xy(-0.42, 0.42, -.25, 0.12)


def draw_interface():
    global PLAY, BEGIN, LAST_PLAY, START_GAME, INTERVAL, \
        AT_START, DEAD, PAUSE, \
        ROT_ANGLE, FINISH_Z, LEVEL, INC_LEVEL

    init_projection_ortho()
    gluLookAt(0, 0, 0, 0, 0, -1, 0, 1, 0)
    glColor(1, 1, 1)

    # entering the game (AFTER pressing on run button) (conditions inside it)
    draw_start()

    if not START_GAME and not DEAD:
        if PAUSE:  # PAUSE ||
            draw_pause()
        else:  # up to next level
            if INC_LEVEL:
                LEVEL += 1
                INC_LEVEL = False
            winning()

    if DEAD:
        START_GAME = False
        draw_end()

    init_projection()
    reposition_camera()


##########################
#      Models            #
##########################
def road(x1, z1, x2, z2):
    global ROAD_DELTA_Z

    glBindTexture(GL_TEXTURE_2D, TEXTURE_NAMES[0])
    y = 0
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)
    glVertex3f(x2, y, z2)

    glTexCoord2f(0, 50)
    glVertex3f(x2, y, z1)

    glTexCoord2f(1, 50)
    glVertex3f(x1, y, z1)

    glTexCoord2f(1, 0)
    glVertex3f(x1, y, z2)
    glEnd()
    glBindTexture(GL_TEXTURE_2D, -1)  # disable textures effect


def draw_checkerboard():
    glColor3d(1, 1, 1)
    glBindTexture(GL_TEXTURE_2D, TEXTURE_NAMES[3])

    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)
    glVertex3f(-2.8, -0.49, -5)

    glTexCoord2f(0, 1)
    glVertex3f(-2.8, -0.49, 5)

    glTexCoord2f(1.0, 1)
    glVertex3f(2.8, -0.49, 5)

    glTexCoord2f(1, 0)
    glVertex3f(2.8, -0.49, -5)
    glEnd()
    glBindTexture(GL_TEXTURE_2D, -1)


def get_wall():
    global POINTS, WALL_Z, SHOW_WALL, MAIN_BALL_COLOR, COLORS_LIST, WALL_COLOR

    draw_wall(WALL_Z, WALL_COLOR[0], WALL_COLOR[1], WALL_COLOR[2])

    if START_GAME:
        if POINTS % 15 == int(0) and POINTS != 0:  # NEXT LEVEL !!? show a wall
            SHOW_WALL = True

        if SHOW_WALL:
            WALL_Z = min(WALL_Z + 1, 10)  # moving the wall

        if WALL_Z == 4:  # collision detection between the main ball & the wall
            MAIN_BALL_COLOR = [WALL_COLOR[0], WALL_COLOR[1], WALL_COLOR[2]]
            WALL_Z = -140  # put it @ infinity
            SHOW_WALL = False
            change_wall_color()


def draw_text(string, x, y, downscale):
    glLineWidth(2)
    glColor(1, 1, 1)
    glPushMatrix()

    glTranslate(x, y, 0)
    glScale(downscale, downscale, 1)
    string = string.encode()  # conversion from Unicode string to byte string
    # drawing text
    for c in string:
        glutStrokeCharacter(GLUT_STROKE_ROMAN, c)

    glPopMatrix()


def draw_text_center(string, x, y, downscale):
    str_width = 0
    glLineWidth(2)
    glColor(1, 1, 1)
    glPushMatrix()

    glTranslate(x, y, 0)
    glScale(downscale, downscale, 1)
    string = string.encode()  # conversion from Unicode string to byte string

    # to center text, just calculate the string with and height and shift
    str_height = glutStrokeHeight(GLUT_STROKE_ROMAN)
    for c in string:
        str_width += glutStrokeWidth(GLUT_STROKE_ROMAN, c)

    glTranslate(-str_width // 2, -str_height // 2, 0)  # //3 instead of /2 to look better
    # drawing text
    for c in string:
        glutStrokeCharacter(GLUT_STROKE_ROMAN, c)

    glPopMatrix()


def draw_sky():
    global STARS_DELTA_Y

    init_projection_ortho(-1, 401)
    gluLookAt(0, 0, 0, 0, 0, -1, 0, 1, 0)
    glColor(1, 1, 1)

    glTranslate(0, -STARS_DELTA_Y, -400)  # moving stars

    for pos in STARS_POSITIONS:  # drawing stars
        draw_star(pos[0], pos[1])

    init_projection()
    reposition_camera()


##############################
#      BALLS LIST            #
##############################
COLORS_LIST = [[232, 99, 10], [248, 6, 204], [84, 99, 255]]

ball = Ball(0, 0, -100, 0.5, COLORS_LIST[0])
BALLS_LIST = [ball]


##################################################################
#    Generating new balls, Collision Detection and Movement      #
##################################################################
def move_main_ball():
    global MAIN_BALL_CURR_X, MAIN_BALL_NEXT_X, MAIN_BALL_Y, JUMPING, NEXT_JUMP, FALLING
    # NOTES:
    # next state moves by whole step (discrete) while  curr moves by smaller steps (continuous)
    # the next_state here to avoid float comparison error later in collision detection)
    # also avoid going over a single step (= 2)

    if DIREC == "LEFT":
        MAIN_BALL_CURR_X = max(MAIN_BALL_CURR_X - 0.2, MAIN_BALL_NEXT_X)

    if DIREC == "RIGHT":
        MAIN_BALL_CURR_X = min(MAIN_BALL_CURR_X + 0.2, MAIN_BALL_NEXT_X)

    # handling case of pressing up button continuously
    # prevent it from being up all the time
    if NEXT_JUMP and not JUMPING:
        JUMPING = True
        NEXT_JUMP = False

    if JUMPING and not FALLING:
        MAIN_BALL_Y = min(MAIN_BALL_Y + 0.1, 1.50)  # rising
        if MAIN_BALL_Y == 1.50:  # reached the jump limit !!?
            FALLING = True
    elif FALLING:
        if MAIN_BALL_Y > 0:  # falling
            MAIN_BALL_Y = max(MAIN_BALL_Y - 0.1, 0)
        else:
            JUMPING = False
            FALLING = False


def ball_generation():
    global MAIN_BALL_CURR_X, MAIN_BALL_Y, BALLS_LIST, \
        COLORS_LIST, POINTS, START_GAME, MAIN_BALL_COLOR, \
        DEAD

    ball_color = random.choice(COLORS_LIST)
    # drawing balls
    for moving_ball in BALLS_LIST:
        moving_ball.draw()

    if START_GAME:
        for moving_ball in BALLS_LIST:
            # Collision occurred !!?
            if MAIN_BALL_CURR_X == moving_ball.x and round(moving_ball.z) == 4 and \
                    round(MAIN_BALL_Y) == moving_ball.y:

                # like generating another ball with the same color
                if moving_ball.color == MAIN_BALL_COLOR:
                    POINTS += 1
                    if POINTS % 15 == 0:  # Next Level !!?
                        BALLS_LIST.append(Ball(0, 0, -100, 0.5, ball_color))
                    moving_ball.x = random.choice(POSITIONS_LIST)
                    moving_ball.z = -100

                else:  # died
                    DEAD = True
                    # POINTS = 0

            elif round(moving_ball.z) >= 7:  # the moving ball has passed the main ball
                # like generating new ball with new color
                moving_ball.x = random.choice(POSITIONS_LIST)
                moving_ball.z = -100
                moving_ball.color = ball_color

            else:  # the ball is still coming ??! continue
                if not DEAD:
                    moving_ball.z += 0.9


def draw():
    global MAIN_BALL_CURR_X, MAIN_BALL_Y, MAIN_BALL_NEXT_X, \
        JUMPING, START_GAME, LEVEL, \
        STARS_DELTA_Y, ROAD_DELTA_Z, \
        FINISH_Z, LEVEL_UP, GO_NEXT_LEVEL, \
        INC_LEVEL, ENTERED_NEXT_LEVEL, BALL_ROT_ANGLE

    glClearColor(0, 0, 0, 1)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    if GO_NEXT_LEVEL:
        FINISH_Z = -400

    # Start || Pause || End !!?
    draw_interface()
    ######################################################
    #                       MODELS                       #
    ######################################################
    # stars
    draw_sky()

    # sky background texture
    glColor(1, 1, 1)
    init_projection_ortho(-1, 401)

    glBindTexture(GL_TEXTURE_2D, TEXTURE_NAMES[4])
    glTranslate(0, 0, -400)
    draw_2d_texture(-1, 1, -1, 1)
    glBindTexture(GL_TEXTURE_2D, -1)

    init_projection()
    reposition_camera()

    # Road
    glLoadIdentity()
    reposition_camera()
    glColor(1, 1, 1)  # yellow
    glTranslate(0, -0.5, ROAD_DELTA_Z)
    road(3, 100, -3, -20000)

    # main ball
    glLoadIdentity()
    reposition_camera()
    glColor3ub(MAIN_BALL_COLOR[0], MAIN_BALL_COLOR[1], MAIN_BALL_COLOR[2])
    glTranslatef(MAIN_BALL_CURR_X, MAIN_BALL_Y, 4)
    glScale(0.5, 0.5, 0.5)
    glRotate(BALL_ROT_ANGLE, 1, 0, 0)
    glutWireSphere(1, 30, 10)

    # End of the level !!?
    glLoadIdentity()
    reposition_camera()
    glTranslate(0, 0, FINISH_Z)
    draw_checkerboard()

    # Text
    init_projection_ortho()
    gluLookAt(0, 0, 0, 0, 0, -1, 0, 1, 0)
    string = "Score: " + str(POINTS)
    draw_text_center(string, 0, 0.85, 0.001)  # Score

    # Controls
    string = "F1 to continue"
    draw_text(string, -0.99, 0.95, 0.0003)  # Controls

    string = "F2 to Pause"
    draw_text(string, -0.99, 0.9, 0.0003)  # Controls

    string = "UP arrow to Jump"
    draw_text(string, -0.99, 0.85, 0.0003)  # Controls

    string = "Level: " + str(LEVEL)
    draw_text(string, -0.99, 0.8, 0.0003)

    init_projection()
    reposition_camera()
    ######################################################
    #                       MOVEMENT                     #
    ######################################################
    # generating the moving balls and a wall
    ball_generation()
    get_wall()
    if FINISH_Z == 2.5 and not ENTERED_NEXT_LEVEL:  # 2.5 means end of the level
        START_GAME = False  # the cause of drawing winning box (interface function)
        LEVEL_UP = True
        INC_LEVEL = True  # increase level by 1

    if LEVEL_UP:  # prevent from entering previous if (so, level is increased ONLY 1 time)
        ENTERED_NEXT_LEVEL = True

    if GO_NEXT_LEVEL:  # if f1 is pressed (continue)
        LEVEL_UP = False
        ENTERED_NEXT_LEVEL = False
        FINISH_Z = -400
        ROAD_DELTA_Z = 0
        BALL_ROT_ANGLE = 0
        GO_NEXT_LEVEL = False

    print(FINISH_Z)

    if FINISH_Z != 2.5 and START_GAME:  # still moving!
        # finish condition for winning | start game for pause and dead
        move_main_ball()
        FINISH_Z = min(.3 + FINISH_Z, 2.5)  # move checkerboard
        ROAD_DELTA_Z += .3
        STARS_DELTA_Y += 0.0005
        BALL_ROT_ANGLE += 5

    glutSwapBuffers()


###################################################################
def game_timer(v):
    draw()
    glutTimerFunc(INTERVAL, game_timer, v + 1)


def keyboard_callback(key, x, y):
    global MAIN_BALL_NEXT_X, \
        START_GAME, DIREC, PLAY, \
        DEAD, PAUSE, NEXT_JUMP, LEVEL_UP, \
        GO_NEXT_LEVEL

    if key == GLUT_KEY_F1:  # RUN
        PAUSE = False
        PLAY = True
        if DEAD:  # RESTART
            reset()
        if LEVEL_UP:  # CONTINUE
            GO_NEXT_LEVEL = True
        START_GAME = True

    if key == GLUT_KEY_F2 and not DEAD and not LEVEL_UP:  # STOP (|| Pause state)
        PAUSE = True
        START_GAME = False

    if key == GLUT_KEY_LEFT:
        MAIN_BALL_NEXT_X = max(MAIN_BALL_NEXT_X - 2, -2)
        DIREC = "LEFT"

    elif key == GLUT_KEY_RIGHT:
        MAIN_BALL_NEXT_X = min(MAIN_BALL_NEXT_X + 2, 2)
        DIREC = "RIGHT"

    elif key == GLUT_KEY_UP:
        NEXT_JUMP = True


##################################
if __name__ == "__main__":  # RUN THISSS SCRIPT
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH)
    glutInitWindowSize(800, 800)
    glutInitWindowPosition(0, 0)
    glutCreateWindow(b"ROCKET ROAD")

    glutTimerFunc(INTERVAL, game_timer, 1)
    glutDisplayFunc(draw)
    glutSpecialFunc(keyboard_callback)

    init_textures()
    init_projection()
    glutMainLoop()
