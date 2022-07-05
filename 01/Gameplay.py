from random import randint
from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
import os

###############################
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
TOP_SCREEN = 800
TOP_GROUND = 75
dBar = 120
barWidth = 170
barHeight = 25
speed = 0
score = 0
FONT_DOWNSCALE = .17
coinWidth = 40
Coins = 0
with open('music_state', 'r') as f:
    sound = bool(f.readline())
################################
colors = [
    (148, 0, 211),
    (75, 0, 130),
    (0, 0, 255),
    (0, 255, 0),
    (255, 255, 0),
    (255, 127, 0),
    (255, 0, 0)
]
colorIndex = 0
###############################
names = [0, 1, 2, 3, 4, 5, 6, 7]
###############################
current_x = WINDOW_WIDTH / 2
current_y = TOP_GROUND + 40
gameOver = False
winning = False
displacement_amount = 0
start = False
store = True
###############random lists###############
randL = []
randCoin = []
for i in range(0, 100):
    a = randint(0, WINDOW_WIDTH - barWidth)
    randL.append(a)
    randCoin.append(randint(0, WINDOW_WIDTH - coinWidth))


##########################################

class RECT:
    def __init__(self, left, right, bottom, top):
        self.left = left
        self.bottom = bottom
        self.right = right
        self.top = top

    def draw_rect(self, red, green, blue, texture, x=1, y=1):
        glPushMatrix()
        glBindTexture(GL_TEXTURE_2D, texture)
        glColor3d(red, green, blue)
        glBegin(GL_POLYGON)
        glTexCoord2f(0, 0)
        glVertex2d(self.left, self.bottom)
        glTexCoord2f(x, 0)
        glVertex2d(self.right, self.bottom)
        glTexCoord2f(x, y)
        glVertex2d(self.right, self.top)
        glTexCoord2f(0, y)
        glVertex2d(self.left, self.top)
        glEnd()
        glBindTexture(GL_TEXTURE_2D, -1)
        glPopMatrix()


####################initialize polygons#######################
space = RECT(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT * 100)
ground = RECT(0, WINDOW_WIDTH, 0, TOP_GROUND)
player = RECT(WINDOW_WIDTH / 2 - 25, WINDOW_WIDTH / 2 + 25, TOP_GROUND, TOP_GROUND + 70)
end = RECT(WINDOW_WIDTH / 2 - 162, WINDOW_WIDTH / 2 + 162, WINDOW_HEIGHT / 2 - 150, WINDOW_HEIGHT / 2 + 200)


#################### Audio #######################

def death_sound():
    if sound:
        die = pygame.mixer.Sound("Textures/super-mario-death-sound-sound-effect.mp3")
        pygame.mixer.Sound.play(die)
        pygame.mixer.music.stop()


def coin_sound():
    if sound:
        coin = pygame.mixer.Sound("Textures/pressing_start_sound.wav")
        pygame.mixer.Sound.play(coin)
        pygame.mixer.music.stop()


def win_sound():
    if sound:
        won = pygame.mixer.Sound("Textures/Tada-sound.mp3")
        pygame.mixer.Sound.play(won)
        pygame.mixer.music.stop()


#########################################

##################init###################

def init():
    #################################
    load_textures()
    #################################
    pygame.mixer.init()
    ##################################
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT, 0, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


#################################################

###################drawing text##################

def draw_text(string, x, y):
    glColor3d(1, 1, 1)
    glLineWidth(2)
    glPushMatrix()
    glTranslate(x, y, 0)
    glScale(FONT_DOWNSCALE, FONT_DOWNSCALE, 1)
    string = string.encode()
    for c in string:
        glutStrokeCharacter(GLUT_STROKE_ROMAN, c)
    glPopMatrix()


#########################Texture setup##########################

def texture_setup(texture_image_binary, texture_name, width, height):
    glBindTexture(GL_TEXTURE_2D, texture_name)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, 3, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_image_binary)


def load_textures():
    glEnable(GL_TEXTURE_2D)
    images = []
    images.append(pygame.image.load("Textures/sawtooth.jpeg"))
    images.append(pygame.image.load("Textures/space.png"))
    images.append(pygame.image.load("Textures/spaceship.jpeg"))
    images.append(pygame.image.load("Textures/moon.png"))
    images.append(pygame.image.load("Textures/gameover.png"))
    images.append(pygame.image.load("Textures/0.jpeg"))
    images.append(pygame.image.load("Textures/win.webp"))
    images.append(pygame.image.load("Textures/winline.jpg"))
    textures = [pygame.image.tostring(image, "RGBA", True) for image in images]
    glGenTextures(len(images), names)
    for i in range(len(images)):
        texture_setup(textures[i], names[i], images[i].get_width(), images[i].get_height())


###################################################

######### draw randomized bars and coins###########

def draw_bars_coins():
    global dBar, TOP_GROUND, randL, barHeight, player, gameOver, speed, displacement_amount, Coins, finish
    glPushMatrix()
    for co in range(len(randL)):
        bar = RECT(randL[co], randL[co] + barWidth, TOP_GROUND + dBar, TOP_GROUND + dBar + barHeight)
        bar.draw_rect(1, 1, 1, names[0], 10, 1)
        if player.bottom <= bar.top + displacement_amount and player.left <= bar.right and player.top >= bar.bottom + \
                displacement_amount and player.right >= bar.left:
            gameOver = True
            death_sound()
            break
        coin = RECT(0, 0, 0, 0)
        if not (randL[co] < randCoin[co] < randL[co] + barWidth):
            coin = RECT(randCoin[co], randCoin[co] + coinWidth, dBar, dBar + 40)
            coin.draw_rect(1, 1, 1, names[5])
        if player.bottom <= coin.top + displacement_amount and player.left <= coin.right and player.top >= \
                coin.bottom + displacement_amount and player.right >= coin.left:
            Coins += 10
            coin_sound()
            randCoin[co] = 900  # goes outside the frustum
        dBar += 170 + barHeight
    finish = dBar
    dBar = 170
    glPopMatrix()


#################################################

###### preform mouse and keyboard movement ######

def mouse_movement():
    global player, colors, current_x, current_y
    glPushMatrix()
    r, g, b = colors[colorIndex]
    player.draw_rect(r, g, b, names[2])
    if start:
        if current_x < 25:
            player.left = 0
            player.right = 50
        elif current_x > WINDOW_WIDTH - 25:
            player.right = WINDOW_WIDTH
            player.left = WINDOW_WIDTH - 50
        else:
            player.left = current_x - 25
            player.right = current_x + 25
        if current_y < TOP_GROUND + 35:
            player.bottom = TOP_GROUND
            player.top = TOP_GROUND + 70
        elif current_y > TOP_SCREEN - 35:
            player.bottom = TOP_SCREEN - 70
            player.top = TOP_SCREEN
        else:
            player.bottom = current_y - 35
            player.top = current_y + 35

    glPopMatrix()


##############################################

#############storing highscores###############

def height_score(scores):
    lines = []
    with open('high_scores', 'r') as f:
        for line in f:
            lines.append(int(line.rstrip()))
    lines.append(int(scores))
    lines.sort(reverse=True)
    with open('high_scores', 'w') as f:
        for line in lines:
            f.write(str(line) + '\n')


##########################################################

#########control signals with mouse and keyboard##########

def mouse(x, y):
    global current_x, current_y
    current_x = x
    current_y = y
    current_y = -current_y + WINDOW_HEIGHT - speed


def keyboard(key, xx, yy):
    global start
    if key == b'i':
        start = True
    elif key == b'q':
        os._exit(0)


###########################################

################Ending RECTs###############

def game_over():
    global end
    glPushMatrix()
    end.draw_rect(1, 1, 1, names[4])
    glPopMatrix()


def win():
    global end
    glPushMatrix()
    end.draw_rect(1, 1, 1, names[6])
    glPopMatrix()


def line_end():
    glPushMatrix()
    end_line = RECT(0, WINDOW_WIDTH, finish + 100, finish + 225)
    end_line.draw_rect(1, 1, 1, names[7], 3, 1)
    glPopMatrix()


###################################################

###############ending line collision###############


def check_win():
    if (abs(displacement_amount + TOP_GROUND - player.top) >= finish) and not gameOver:
        return True
    return False


##################################################

####################main draw#####################

def draw():
    global player, space, ground, colorIndex, colors, speed, end, gameOver, displacement_amount, score, Coins, store, \
        winning
    glClear(GL_COLOR_BUFFER_BIT)
    glClearColor(0, 0, 0, 0)
    score = -displacement_amount / 5
    score += Coins
    if not gameOver and not winning:
        displacement_amount += speed
        glTranslate(0, speed, 0)
        glPushMatrix()
        space.draw_rect(1, 1, 1, names[1], 1, 100)
        ground.draw_rect(1, 1, 1, names[3], 4, .5)
        draw_bars_coins()
        line_end()
        glLoadIdentity()
        mouse_movement()
        draw_text('Score: ' + str(int(score)), 0, 780)
        glPopMatrix()
        ########################################
        # colorIndex += 1
        # if colorIndex == len(colors):
        #     colorIndex = 0
        if speed >= -20 and start:
            speed -= .001
        else:
            draw_text('Press [i] to Start, [q] to exit', 0.28 * WINDOW_WIDTH, 0.9 * WINDOW_HEIGHT)
    elif gameOver and not winning:
        glLoadIdentity()
        game_over()
        draw_text('Your score is : ' + str(int(score)), WINDOW_WIDTH / 2 - 120, WINDOW_HEIGHT / 2 - 220)
        if store:
            height_score(score)
            store = False
    winning = check_win()
    if winning:
        glLoadIdentity()
        win()
        draw_text('Your score is : ' + str(int(score)), WINDOW_WIDTH / 2 - 120, WINDOW_HEIGHT / 2 - 220)
        if store:
            win_sound()
            height_score(score)
            store = False
    glutSwapBuffers()


###############################################

glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA)
glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
glutInitWindowPosition(400, 0)
glutCreateWindow("Gameplay")
glutDisplayFunc(draw)
glutIdleFunc(draw)
glutKeyboardFunc(keyboard)
glutPassiveMotionFunc(mouse)
init()
glutMainLoop()

''' 
Note that speed of translating the space depends on graphics card you can change the speed by adding more
 negative amount to the number 
 
 '''
