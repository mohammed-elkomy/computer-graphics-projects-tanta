import math
import random
from math import cos, sin, pi, radians, sqrt
from OpenGL.GL import *
# from OpenGL.GLU import *
from OpenGL.GLUT import *
from blend import *
from sys import *



################################################# Texture Fetch
DOG_STATE = "IDLE"
CAT_STATE = "IDLE"
def getDogTex(state):
    '''Chooses The Dog's Current Texture'''

    if state == "IDLE":
        return 1
    elif state == "Preparing":
        return 2
    elif state == "Throw":
        return 3

def getCatTex(state):
    '''Chooses The Cat's Current Texture'''

    if state == "IDLE":
        return 5
    elif state == "Preparing":
        return 6
    elif state == "Throw":
        return 7

def getBallTex():
    '''Chooses The Ball's Current Texture'''

    if CURRENT_TURN == "DOG":
        return 4
    else:
        return 8




############################################################# ADJUSTING THE ENVIRONMENT
def init():
    glClearColor(1, 1, 1, 1)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT, 0, 1)  # l,r,b,t,n,f
    glMatrixMode(GL_MODELVIEW)


########################################################################## TEXT
def draw_text(string, x, y, color=[1, 0.7, 0]):
    '''Draws Given String at given location'''

    glLoadIdentity()
    glLineWidth(2)

    glPushMatrix()
    glTranslate(x, y, 0)
    glScale(FONT_DOWNSCALE, FONT_DOWNSCALE, 1)
    string = string.encode()

    str_width = sum(glutStrokeWidth(GLUT_STROKE_ROMAN, c) for c in string)  # get total width of string
    str_height = max(glutStrokeHeight(GLUT_STROKE_ROMAN) for c in string)  # get total width of string
    glTranslate(-str_width // 2, -str_height // 2, 0)

    glColor(color[0], color[1], color[2], 1)
    for c in string:
        glutStrokeCharacter(GLUT_STROKE_ROMAN, c)

    glPopMatrix()





############################################################### COMPUTING ANGLE AND FORCE
mouse_x1 = 0
mouse_y1 = 0
mouse_x2 = 1
mouse_y2 = 1

delta_x = 0
delta_y = 0
theta = 0
force = 0

def angle():
    '''Finds the throwing angle'''
    global mouse_x1, mouse_y1, mouse_x2, mouse_y2, theta, delta_x, delta_y, force, msgTime, msgText, shot

    #  dy & dx
    delta_x = mouse_x2 - mouse_x1
    delta_y = mouse_y2 - mouse_y1

    # The Force is the distance between hold and release locations
    force = sqrt(pow(delta_x, 2) + pow(delta_y, 2))

    # Identify Which Quadrant you're in
    if delta_x > 0 and delta_y > 0:
        theta = 360 - math.degrees(math.atan(delta_y / delta_x))

    elif delta_x < 0 and delta_y > 0:
        theta = 180 + math.degrees(math.atan(delta_y / -delta_x))

    elif delta_x < 0 and delta_y < 0:
        theta = 180 - math.degrees(math.atan(-delta_y / -delta_x))

    elif delta_x > 0 > delta_y:
        theta = math.degrees(math.atan(-delta_y / delta_x))

    else: # if no dragging occured , output an in-game error message
        msgText = "CLICK AND DRAG TO SHOOT!"
        msgTime = 60
        shot = False

    theta -= 180


###################################################################### Callbacks
def mouseButton(key, state, xc, yc):
    global mouse_x1, mouse_y1, mouse_x2, mouse_y2, theta, delta_x, delta_y, force
    global shot, x, y, time, CURRENT_TURN, CAT_RESULT, DOG_RESULT, DOG_STATE, CAT_STATE

    if key == GLUT_LEFT_BUTTON and state == GLUT_DOWN:  ## PRESS AND HOLD
        mouse_x1 = xc
        mouse_y1 = yc

    elif key == GLUT_LEFT_BUTTON and state == GLUT_UP:  ## RELEASE
        mouse_x2 = xc
        mouse_y2 = yc
        if not shot:
            shot = True
            angle()
            ## Intialize the throw
            x = ball.X
            y = ball.Y
            time = 0

    if key == GLUT_RIGHT_BUTTON:  ## RESET
        if shot:
            shot = False
            ## Intialize the throw
            x = ball.X
            y = ball.Y
            time = 0
            ball.respawn("CAT")
            CURRENT_TURN = "CAT"
            CAT_RESULT = WINNING_CONDITION
            DOG_RESULT = WINNING_CONDITION

def keyboard_callback(key, x, y):
    global START,MAIN, END, CAT_RESULT, DOG_RESULT,msgTime, WINNING_CONDITION
    if START and (key == b's' or key == b'S'):  # Choosing which Scene to display
        START = 0
        MAIN = 1
        END = 0
        pygame.mixer.music.stop()
        pygame.mixer.music.load("Game.mp3")
        pygame.mixer.music.play()
    elif END and (key == b'n' or key == b'N'):
        MAIN = 1
        START = 0
        END = 0
        # RESETing Scores
        CAT_RESULT = WINNING_CONDITION
        DOG_RESULT = WINNING_CONDITION
        msgTime = 0
        pygame.mixer.music.stop()
        pygame.mixer.music.load("Game.mp3")
        pygame.mixer.music.play()


    elif key == b'q' or key == b'Q':
        sys.exit(0)



######################################################### COMPUTING THE PATH OF THE PROJECTILE(BALL)
x = 0
y = 0
time = 0
shot = False

def objPath(xc, yc, F, ang, t):
    '''Computes the balls path'''

    ## get the Velocity components
    velx = F * cos(ang)
    vely = F * sin(ang)

    ## current location
    distX = velx * t  ## Acc = 0 in X
    distY = (vely * t) + ((GRAVITY_ACC * (t) ** 2) / 2)  ##Gravity Acc for y

    newx = round(distX + xc)
    newy = round(distY + yc)
    return (newx, newy)


################################################################### CHECKING COLLISION
def check_collision():
    '''Checks collision between the ball and the players'''
    global CAT_RESULT
    global DOG_RESULT
    global shot, x, y, theta, force, time, CURRENT_TURN, msgTime, msgText

    # Dog Points
    # If the Dog hit the cat
    if CURRENT_TURN == "DOG" and ball.bottom <= CAT.top:
        if CAT.right >= ball.left >= CAT.left:
            ## Print message
            msgTime = 200
            msgText = "DOG HITTs !!!   CAT's Turn!"

            ## Dec result
            CAT_RESULT -= 1

            ## stop and begin the cat's turn
            shot = False
            ball.respawn("CAT")
            CURRENT_TURN = "CAT"

    # Cat Points
    # If the Dog hit the cat
    if CURRENT_TURN == "CAT" and ball.bottom <= DOG.top:
        if DOG.right >= ball.right >= DOG.left:
            ## Print message
            msgTime = 200
            msgText = "CAT HITTs !!!  DOG's Turn!"

            ## Dec result
            DOG_RESULT -= 1

            ## stop and begin the DOG's turn
            shot = False
            ball.respawn("DOG")
            CURRENT_TURN = "DOG"


def CollidedWithMiddleWall():
    '''Checks collision with the middle wall'''
    leftOverlap = middle_wall.right >= ball.left >= middle_wall.left
    rightOverlap = middle_wall.left <= ball.right <= middle_wall.right

    verticalCollision = ball.bottom <= middle_wall.top

    return verticalCollision and (leftOverlap or rightOverlap)


##############################################################Health Bars
def drawHealthBar(player):
    '''Draws the players' health bars'''
    if player == "CAT":
        bar = Rectangle(0,0,0,0)
        bar.left = WINDOW_WIDTH//15
        bar.right = (bar.left + WINDOW_WIDTH//3)
        bar.top = WINDOW_HEIGHT - 15
        bar.bottom = bar.top - 25

        glLineWidth(5)
        bar.draw_rect([0,0,0,1], GL_LINE_LOOP)   # Bar Frame

        bar.right = bar.left + (WINDOW_WIDTH//3) * CAT_RESULT/WINNING_CONDITION  # Remaining Health
        bar.draw_rect([1,0,0,1],GL_QUADS)
    else:
        bar = Rectangle(0, 0, 0, 0)
        bar.right = WINDOW_WIDTH - WINDOW_WIDTH // 15
        bar.left = (bar.right - WINDOW_WIDTH // 3)
        bar.top = WINDOW_HEIGHT - 15
        bar.bottom = bar.top - 25

        glLineWidth(5)
        bar.draw_rect([0, 0, 0, 1], GL_LINE_LOOP) # Bar Frame

        bar.left = bar.right - (WINDOW_WIDTH // 3) * DOG_RESULT / WINNING_CONDITION  # Remaining Health
        bar.draw_rect([1, 0, 0, 1], GL_QUADS)




########################################################## Writing a pop up message
msgTime = 0
msgText = ""
def makeMsg():
    '''Generates a Pop up Message for a certain amount of time'''
    global msgTime, msgText
    if msgTime == 0:
        return
    msg = Rectangle(WINDOW_WIDTH, 0, WINDOW_HEIGHT, 0)
    msg.draw_rect([0.5, 0.5, 0.5, 0.7], GL_QUADS)
    string = msgText
    draw_text(string, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50, [0, 0, 0])
    msgTime -= 1



def mainGame():
    ''' The Main Game '''
    global mouse_x1, mouse_y1, mouse_x2, mouse_y2, theta, delta_x, delta_y, force
    global CAT_RESULT, DOG_RESULT
    global x, y, time, shot, msgTime, msgText
    global DOG_STATE, CAT_STATE, LOSE
    global CURRENT_TURN,MAIN,END,START,WINNING_CONDITION

    if CURRENT_TURN == "DOG" and not shot:
        DOG_STATE = "Preparing"
        CAT_STATE = "IDLE"
    elif CURRENT_TURN == "CAT" and not shot:
        CAT_STATE = "Preparing"
        DOG_STATE = "IDLE"


    ###################################### Drawing the objects

    backGround = Rectangle(WINDOW_WIDTH,0,WINDOW_HEIGHT,0)
    backGround.draw_rect_tex(0)

    if shot:
        ball.draw_rect_tex(getBallTex())
    DOG.draw_rect_tex(getDogTex(DOG_STATE))
    CAT.draw_rect_tex(getCatTex(CAT_STATE))
    middle_wall.draw_rect_tex(9)

    ####################################### Health Bar

    drawHealthBar("CAT")
    drawHealthBar("DOG")

    ###################################### Checking collision

    check_collision()

    ###################################### Throwing
    if shot:
        if CURRENT_TURN == "DOG":  ## ADJUST CURRENT TEXTURE
            DOG_STATE = "Throw"
        else:
            CAT_STATE = "Throw"

        ## IF It didnt collide
        if ball.bottom > 0 and not CollidedWithMiddleWall() and ball.left > 0 and ball.right < WINDOW_WIDTH :  # Keep moving
            time += 0.05  ##Time with respect to the ball
            po = objPath(x, y, force, radians(theta), time)  ## gets its current position after the passed time using Newton's Eqns of motion

            ## Update the ball's current location
            ball.left = po[0] - BALL_SIZE//2
            ball.right = po[0] + BALL_SIZE//2
            ball.top = po[1] + BALL_SIZE//2
            ball.bottom = po[1] - BALL_SIZE//2
            ball.refresh()

        else:  # if the ball collided
            shot = False
            LOSE = True
            if CURRENT_TURN == "DOG":
                ball.respawn("CAT")
                CURRENT_TURN = "CAT"
            else:
                ball.respawn("DOG")
                CURRENT_TURN = "DOG"

    if LOSE:
        msgTime = 80
        msgText = "Hard Luck!"
        LOSE = 0


    makeMsg()

    if CAT_RESULT <= 0 or DOG_RESULT <= 0:  ## GAME ENDED

        ## SWITCH to Ending Scene
        END = 1
        MAIN = 0
        START = 0

        ## GET the winner
        if CURRENT_TURN == "DOG":
            CURRENT_TURN = "CAT"
            ball.respawn("CAT")
        else:
            CURRENT_TURN = "DOG"
            ball.respawn("DOG")

        pygame.mixer.music.stop()
        pygame.mixer.music.load("Game Over.mp3")
        pygame.mixer.music.play()


MAIN = 0
START = 1
END = 0

def StartingWindow():
    '''The Starting Window'''
    startScreen = Rectangle(WINDOW_WIDTH,0,WINDOW_HEIGHT,0)
    startScreen.draw_rect_tex(10)

    startScreen.draw_rect([1,0.8,0,0.7], GL_QUADS)

    startScreen.draw_rect_tex(11)



def EndingWindow():
    '''The Ending Window'''
    global CURRENT_TURN
    startScreen = Rectangle(0, WINDOW_WIDTH, WINDOW_HEIGHT, 0)
    startScreen.draw_rect([0, 0, 0, 1], GL_QUADS)


    string = CURRENT_TURN + " WINS !!"
    draw_text(string, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50, [1, 1, 1])
    string = "Press N For New Game"
    draw_text(string, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 , [1, 1, 1])

def display():
    global mouse_x1, mouse_y1, mouse_x2, mouse_y2, theta, delta_x, delta_y, force
    global CAT_RESULT
    global DOG_RESULT
    global x, y, time, shot, LOSE, msgTime, msgText
    global CURRENT_TURN,MAIN,START,END

    glClear(GL_COLOR_BUFFER_BIT)


    if START :
        StartingWindow()
    elif END:
        EndingWindow()
    else:
        mainGame()

    glutSwapBuffers()


def game_timer(v):
    display()
    glutTimerFunc(Time, game_timer, v)


glutInit()
pygame.mixer.init()
pygame.mixer.music.load("start menu.mp3")
pygame.mixer.music.play()

glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA)
glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
glutInitWindowPosition(0, 0)
glutCreateWindow(b"The Game")
glutDisplayFunc(display)
glutTimerFunc(Time, game_timer, 1)

glutMouseFunc(mouseButton)
glutKeyboardFunc(keyboard_callback)
init()
Texture_init()
glutMainLoop()
