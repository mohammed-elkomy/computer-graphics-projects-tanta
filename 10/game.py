from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import random
import pygame
from pygame import mixer

FONT_DOWNSCALE = 0.13
FROM_RIGHT = 1
FROM_LEFT = 2
FROM_TOP = 3
FROM_BOTTOM = 4

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 500
SPEED=50
START=0

class Rectangle:
    def __init__(self, left, bottom, right, top):
        self.left = left
        self.bottom = bottom
        self.right = right
        self.top = top

current_delta_X = 100
current_delta_y = 350

current_apple = Rectangle(135, 135, 160, 160)
current_box = Rectangle(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
current_player = Rectangle(0, 0, 60, 50)

current_player_result = 0
current_player_chances=3
current_mouse_x = 0
current_player_level=1

def init():
    global texture
    glLoadIdentity()

    glClearColor( 1,1,1,1)
    glMatrixMode(GL_PROJECTION)
    glOrtho(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT, 0, 1)
    glMatrixMode(GL_MODELVIEW)

    texture = glGenTextures(3)  #

    glEnable(GL_BLEND)  # FOR BLENDING ADDED
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)  # FOR BLENDING ADDED


    # Create MipMapped Texture

    imgload = pygame.image.load("box.png")
    img = pygame.image.tostring(imgload, "RGBA", 1)
    width = imgload.get_width()
    height = imgload.get_height()
    glBindTexture(GL_TEXTURE_2D, texture[0])
    glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
    glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    gluBuild2DMipmaps(GL_TEXTURE_2D, 4, width, height, GL_RGBA, GL_UNSIGNED_BYTE, img)

######################################################################

    imgload = pygame.image.load("apple.png")
    img = pygame.image.tostring(imgload, "RGBA", 1)
    width = imgload.get_width()
    height = imgload.get_height()
    glBindTexture(GL_TEXTURE_2D, texture[1])
    glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
    glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    gluBuild2DMipmaps(GL_TEXTURE_2D, 4, width, height, GL_RGBA, GL_UNSIGNED_BYTE, img)

    ######################################################################

    imgload = pygame.image.load("tree.jpg")
    img = pygame.image.tostring(imgload, "RGBA", 1)
    width = imgload.get_width()
    height = imgload.get_height()
    glBindTexture(GL_TEXTURE_2D, texture[2])
    glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
    glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    gluBuild2DMipmaps(GL_TEXTURE_2D, 4, width, height, GL_RGBA, GL_UNSIGNED_BYTE, img)

    glEnable(GL_TEXTURE_2D)

    glBindTexture(GL_TEXTURE_2D, -1)

def draw_moving_apple(rect):
    glLoadIdentity()
    glBindTexture(GL_TEXTURE_2D, texture[1])

    glBegin(GL_QUADS)
    glTexCoord(0, 0)
    glVertex(rect.left, rect.bottom, 0)
    glTexCoord(1, 0)
    glVertex(rect.right, rect.bottom, 0)
    glTexCoord(1, 1)
    glVertex(rect.right, rect.top, 0)
    glTexCoord(0, 1)
    glVertex(rect.left, rect.top, 0)

    glEnd()

    glBindTexture(GL_TEXTURE_2D,-1)

def draw_Moving_Box(rect):
    glLoadIdentity()
    glBindTexture(GL_TEXTURE_2D, texture[0])

    glBegin(GL_QUADS)
    glTexCoord(0, 0)
    glVertex(rect.left, rect.bottom, 0)
    glTexCoord(1, 0)
    glVertex(rect.right, rect.bottom, 0)
    glTexCoord(1, 1)
    glVertex(rect.right, rect.top, 0)
    glTexCoord(0, 1)
    glVertex(rect.left, rect.top, 0)

    glEnd()

    glBindTexture(GL_TEXTURE_2D, -1)

def draw_back_ground():
    glLoadIdentity()
    glColor(1, 1, 1)

    glBindTexture(GL_TEXTURE_2D, texture[2])
    glBegin(GL_QUADS)
    glTexCoord(0, 0)
    glVertex(0, 0, -1)
    glTexCoord(1, 0)
    glVertex(WINDOW_WIDTH, 0, -1)
    glTexCoord(1, 1)
    glVertex(WINDOW_WIDTH, WINDOW_HEIGHT, -1)
    glTexCoord(0, 1)
    glVertex(0, WINDOW_HEIGHT, -1)
    glEnd()

    glBindTexture(GL_TEXTURE_2D,-1)


def draw_text(string, x, y):

        if (x == 390 and y == 250):
            glColor3f(1, 0, 0)
            glLineWidth(2)

        elif (x == 350 and y == 250):
            glColor3f(0, 1, 0)
            glLineWidth(2)

        elif (x == 8 and y == 160):

            glColor3f(1, 0, 0)
            glLineWidth(2)

        elif (x == 330 and y == 250):

            glColor3f(1, 0, 1)
            glLineWidth(1.5)

        else:
            glColor3f(0, 0, 1)
            glLineWidth(1.5)

        glPushMatrix()
        glTranslate(x, y, 0)
        glScale(FONT_DOWNSCALE, FONT_DOWNSCALE, 1)
        string = string.encode()
        for c in string:
            glutStrokeCharacter(GLUT_STROKE_ROMAN, c)
        glPopMatrix()


def check_apple_box_direction(_apple, _box):
    global FROM_RIGHT
    global FROM_LEFT
    global FROM_TOP
    global FROM_BOTTOM

    if _apple.right >= _box.right:
        return FROM_RIGHT
    if _apple.left <= _box.left:
        return FROM_LEFT
    if _apple.top >= _box.top:
        return FROM_TOP
    if _apple.bottom <= _box.bottom:
        return FROM_BOTTOM


def check_apple_box_in_touch(_apple, _player):
    horizontal_check = _player.left <= _apple.left <= _apple.right <= _player.right
    vertical_check = _player.top - _apple.bottom >=0 and _player.top - _apple.bottom <=10
    return vertical_check and horizontal_check


def mouse_callback(x, y):
    global current_mouse_x
    current_mouse_x = x


def keyboard_callback(key,x,y):
    global SPEED
    global START
    if(key==b"a"):
        START=1
    if (key == b"b"):
        START = -1


def game_timer(v):
    Run_game()
    glutTimerFunc(SPEED, game_timer, 1)


def motion_apple():
    current_delta_X = random.randrange(-400, 400)
    current_apple.left = current_apple.left + current_delta_X
    current_apple.right = current_apple.right + current_delta_X
    while (current_apple.left < 1 or current_apple.right > 799):
        current_delta_X = random.randrange(-400, 400)
        current_apple.left = current_apple.left + current_delta_X
        current_apple.right = current_apple.right + current_delta_X


def lose():
    global SPEED
    glColor(1, 0, 0)
    glLineWidth(2)
    string ="Game over"
    draw_text(string, 390, 250)
    SPEED=-1

def win_game():
    global SPEED
    glColor(0, 1, 0)
    glLineWidth(1.5)
    string = "you win , congratulation"
    draw_text(string, 350, 250)
    SPEED = -1

def sound_pick_apple():
    PicK_apple = mixer.Sound("pop.ogg")
    PicK_apple.play()

def sound_falling_apple():
    fallen = mixer.Sound("flatten1.ogg")
    fallen.play()

def sound_win():
    win_sound = mixer.Sound("shimmer.ogg")
    win_sound.play()

def sound_lose():
    losing = mixer.Sound("explode1.ogg")
    losing.play()

def sound_next_level():
    next_level = mixer.Sound("levelup.ogg")
    next_level.play()


def Run_game():
    global Stop
    global current_delta_X
    global current_delta_y
    global SPEED
    global current_apple
    global current_player_level
    global current_player_result
    global current_player_chances

    glClear(GL_COLOR_BUFFER_BIT)
    draw_back_ground()

    string = "score : " + str(current_player_result)
    draw_text(string, 8, 240)

    string = "level : " + str(current_player_level)
    draw_text(string, 8, 200)

    string = "chance : " + str(current_player_chances)
    draw_text(string, 8, 160)

    string = "b to stop"
    draw_text(string, 685, 480)

    string = "a to resume"
    draw_text(string, 685, 460)

    if(START==0):  #the beginning of the game
        string = "press a to start"
        draw_text(string, 330, 250)

    if(START==1 ): #to run or resume game

        current_apple.top = current_apple.top + current_delta_y
        current_apple.bottom = current_apple.bottom + current_delta_y

        glColor3d(1, 1, 1)
        draw_moving_apple(current_apple)

        if check_apple_box_direction(current_apple, current_box) == FROM_RIGHT:
            current_delta_X = -1
        if check_apple_box_direction(current_apple, current_box) == FROM_LEFT:
            current_delta_X = 1
        if check_apple_box_direction(current_apple, current_box) == FROM_TOP:
            current_delta_y = -7
        if check_apple_box_direction(current_apple, current_box) == FROM_BOTTOM:
            current_delta_y = 1

        if (current_mouse_x <= 40):
            current_player.left = 0
            current_player.right = 80
        elif (current_mouse_x >= 760):
            current_player.right = 800
            current_player.left = 720
        else:
            current_player.left = current_mouse_x - 40
            current_player.right = current_mouse_x + 40


        draw_Moving_Box(current_player)

        if check_apple_box_in_touch(current_apple, current_player):
           current_player_result = current_player_result + 1
           sound_pick_apple()

           glColor3f(0,1,0)
           draw_Moving_Box(current_player)

           SPEED-=1
           if(SPEED<40):
               current_player_level=2
               if(SPEED==39):
                   sound_next_level()


           if (SPEED < 30):
               current_player_level = 3
               if (SPEED == 29):
                   sound_next_level()


           if (SPEED < 20):
               current_player_level = 4
               if (SPEED == 19):
                   sound_next_level()

           if(SPEED<10):
               current_player_level=5
               if (SPEED == 9):
                   sound_next_level()


           if(SPEED==5):
               sound_win()
               win_game()

           current_delta_y = 450
           motion_apple()


        if current_apple.top == 20 or current_apple.bottom==0:
            glColor(1, 0, 0)
            draw_Moving_Box(current_player)
            if(current_player_chances<1):
                sound_lose()
                lose()
            else:
                current_player_chances = current_player_chances-1
                current_delta_y = 490
                sound_falling_apple()
                motion_apple()

    if(START==-1):  #to stop game
        glColor3d(1, 1, 1)
        draw_moving_apple(current_apple)

        draw_Moving_Box(current_player)

    glutSwapBuffers()

pygame.init()
#clock = pygame.time.Clock()
#mixer.music.load("cat.ogg")
#mixer.music.play(-1)

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutInitWindowPosition(250, 100)
    glutCreateWindow(b"!!! catch the apple !!! -- Team 10")
    glutDisplayFunc(Run_game)
    glutKeyboardFunc(keyboard_callback)
    glutPassiveMotionFunc(mouse_callback)
    glutTimerFunc(SPEED, game_timer, 1)
    init()
    glutMainLoop()

if __name__ == "__main__":
    main()
