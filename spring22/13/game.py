from math import *
import numpy as np
from OpenGL.GL import *
from OpenGL.GLUT import *
from pygame import *

# ##############################################################
# ########### global variables and constants ###################
# ##############################################################

rot_sens = 1                 # increase this if the rotation is too slow or decrease it if you have high-end pc
arrow_sens = 0.06            # increase this if the arrow speed is too slow
rangle = 360                 # initial rotation angle
launch = 0                   # To check if the right click has been pressed or not
fail = 0                     # To check if an arrow collide with another arrow or not
newlevel = 1                 # new level checker
arrow_pos = 0                # the vertical speed of the arrow towards the circle center
arrowList = []               # A list to store the fired arrows
currentArrow = None          # The arrow that is in the bow right now
NumberOfArrows = 0           # number of fired arrows
max_arrows = 9               # maximum number of arrows
reqNum = max_arrows          # Required number of arrows for current level
level = 1                    # current level
gameSpeed = rot_sens         # the initial rotation speed
lose_counter = 0             # loses counter
trial = 3                    # remaining trials
gameOver = 1                 # To check if the trials has ended or not
time_interval = 4            # constant for any pc
lose_flag = None             # indicate if we start or win or lose to draw textures
texture = []                 # list of textures
newlevel = 1                 # new level checker


#########################################################################################################

def init():
    mixer.music.load("sounds/intro.mp3")
    mixer.music.play(-1)
    mixer.music.set_volume(0.4)


#########################################################################################################

def arrow_shape(head_pos):
    """
    This function draw arrow with head position "f" in Y-axis
    """
    glBegin(GL_POLYGON)
    glVertex2d(0.03, (head_pos - 0.06))
    glVertex2d(0, head_pos)
    glVertex2d(-0.03, (head_pos - 0.06))
    glEnd()
    glLineWidth(3)
    glBegin(GL_LINE_STRIP)
    glVertex2d(0, (head_pos - 0.06))
    glVertex2d(0, (head_pos - 0.23))
    glVertex2d(-0.03, (head_pos - 0.25))
    glVertex2d(0, (head_pos - 0.23))
    glVertex2d(0.03, (head_pos - 0.25))
    glVertex2d(0, (head_pos - 0.23))
    glVertex2d(0, (head_pos - 0.27))
    glVertex2d(-0.03, (head_pos - 0.29))
    glVertex2d(0, (head_pos - 0.27))
    glVertex2d(0.03, (head_pos - 0.29))
    glEnd()


#########################################################################################################

def circle(r, center=(0, 0)):
    """
     This funcrion draw solid circle with radius "r" and takes a tuple as a center point (x,y)
     """
    glBegin(GL_POLYGON)
    for ang in np.arange(0, 360, 10):
        x = r * cos(ang * pi / 180) + center[0]
        y = r * sin(ang * pi / 180) + center[1]
        glVertex2d(x, y)
    glEnd()
    

#########################################################################################################

def bow():
    """
     This function draws a bow at the bottom of the scene
    """
    glLineWidth(3)
    glBegin(GL_LINE_STRIP)
    glVertex2d(-0.2, -0.8)
    glVertex2d(-0.1, -0.7)
    glVertex2d(-0.05, -0.7)
    glVertex2d(0, -0.73)
    glVertex2d(0.05, -0.7)
    glVertex2d(0.1, -0.7)
    glVertex2d(0.2, -0.8)
    glColor3d(0.8, 0.4, 0.5)
    glVertex2d(0.2, -0.8)
    glVertex2d(0, -0.84)
    glVertex2d(-0.2, -0.8)

    glEnd()


#########################################################################################################

def rotate_center(rotation_angle):
    """
     This function is used rotate any thing around the center of the circle
    """
    glTranslatef(0, 0.35, 0)
    glRotatef(rotation_angle, 0, 0, 1)
    glTranslate(0, -0.35, 0)


#########################################################################################################

def check_collision(first_angle, second_angle):
    """
         This function is used to detect the collision
    """
    checker = 0
    left = second_angle - 7
    right = second_angle + 7
    if left < 0:
        left += 360
        if not (right <= first_angle <= left):
            checker = 1
    elif right > 360:
        right -= 360
        if not (right <= first_angle <= left):
            checker = 1
    elif left <= first_angle <= right:
        checker = 1
    return checker


#########################################################################################################

class Arrow:
    arrow_head = None
    angle = None

    def __init__(self, arrow_head):
        self.arrow_head = arrow_head

    def draw(self, angle):
        rotate_center(self.angle - angle)
        arrow_shape(0.2)
        glLoadIdentity()


#########################################################################################################

def mouse_func(button, state, x, y):
    """
    This function to press buttons like(start, yes, no)
    """
    global launch
    global gameOver
    global texture
    if gameOver == 0 and button == 0 and state == 1:
        launch = 1
    elif gameOver == 1 and button == 0 and state == 1:
        if lose_flag is None and 187 <= x <= 433 and 450 <= y <= 550:
            gameOver = 0
            launch = 0
            glDeleteTextures(1, texture)
            mixer.music.stop()
            mixer.music.set_volume(1)
        elif 313 <= x <= 377 and 515 <= y <= 543:
            gameOver = 0
            launch = 0
            glDeleteTextures(1, texture)
            mixer.music.stop()
        elif 400 <= x <= 465 and 515 <= y <= 543:
            os._exit(0)


#########################################################################################################

def draw_text(my_text, x1, y1, size=0.0009):
    glPushMatrix()
    glTranslate(x1 - 0.02, y1 - 0.03, 0)
    font_downscale = size
    glScale(font_downscale, font_downscale, 1)
    enco = str(my_text).encode()
    for c in enco:
        glutStrokeCharacter(GLUT_STROKE_ROMAN, c)
    glPopMatrix()


#########################################################################################################

# this section for textures (load, draw)
def load_texture(path):
    global texture
    texture = glGenTextures(2)
    imgload = image.load(path)
    img = image.tostring(imgload, "RGBA", True)
    width = imgload.get_width()
    height = imgload.get_height()
    glBindTexture(GL_TEXTURE_2D, texture[0])
    glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexImage2D(GL_TEXTURE_2D, 0, 3, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img)

    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture[0])


def draw_texture():
    global texture
    glClear(GL_COLOR_BUFFER_BIT)
    glColor(1, 1, 1)
    glBegin(GL_QUADS)
    glTexCoord(0, 0)
    glVertex2f(-1, -1)

    glTexCoord(1, 0)
    glVertex2f(1, -1)

    glTexCoord(1, 1)
    glVertex2f(1, 1)

    glTexCoord(0, 1)
    glVertex2f(-1, 1)

    glEnd()
    glDeleteTextures(texture)


#########################################################################################################

def Timer(v):
    myGame()
    glutTimerFunc(time_interval, Timer, 1)


#########################################################################################################

def myGame():
    # this section is used to define the global variables:
    global rangle
    global launch
    global arrow_pos
    global arrowList
    global currentArrow
    global NumberOfArrows
    global reqNum
    global level
    global max_arrows
    global gameSpeed
    global fail
    global lose_counter
    global trial
    global gameOver
    global rot_sens
    global arrow_sens
    global lose_flag
    global newlevel

    # this section is used for setting the background and making the shapes smooth
    glClearColor(1, 1, 0.9, 0.1)
    glClear(GL_COLOR_BUFFER_BIT)
    glEnable(GL_BLEND)
    glEnable(GL_POLYGON_SMOOTH)
    glEnable(GL_LINE_SMOOTH)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    # the Beginning of the game:
    # the first condition to check if the game is over or not if it's over, it draws the following statements.
    # if it isn't over it begins the game
    if gameOver == 1:
        glColor3d(1, 0, 0)
        if lose_flag is None:
            load_texture("images/start.png")
        elif lose_flag == 1:
            load_texture("images/over.png")
        else:
            load_texture("images/win.png")
        draw_texture()
    else:
        glColor3d(0, 0, 0)
        bow()

        if rangle > 360:
            rangle %= 360

        # center circle:
        glColor3d(0, 0, 0)
        circle(0.3, (0, 0.35))

        # This is used to add the built-in arrows to the arrow list
        if newlevel:
            NumberOfArrows += (level + 1)
            random_angle = 360 / (level + 1)
            for i in range((level + 1)):
                new_arrow = Arrow(0.2)
                new_arrow.angle = i * random_angle
                arrowList.append(new_arrow)

        # This is used to create new arrow:
        if currentArrow is None:
            currentArrow = Arrow(-0.6)
            arrowList.append(currentArrow)
            NumberOfArrows += 1

        # This condition checks if an arrow has launched or not
        if launch == 0: # hasn't launched so the arrow still in the bow
            glColor3d(0, 0, 0)
            arrow_shape(-0.6)
            newlevel = 0
        else:           # it has launched
            # this condition checks if the current arrow has reached its orbit or not
            if currentArrow.arrow_head + arrow_pos <= 0.2:  # it hasn't reached its orbit so the arrow will go up
                glTranslate(0, arrow_pos, 0)
                arrow_pos += arrow_sens
                glColor3d(0, 0, 0)
                arrow_shape(-0.6)
            else:      # it has reached its orbit
                currentArrow.angle = rangle
                launch = 0
                arrow_pos = 0

                # To check collision:
                for i in range((NumberOfArrows - 1)):
                    if check_collision(currentArrow.angle, arrowList[i].angle):
                        fail = 1
                        break

                # This condition check if there is a collision or not to decide what will happen next
                if fail != 1:  # No collision
                    mixer.music.load("sounds/arrow.mp3")
                    mixer.music.play()
                    glColor3d(0, 0, 0)
                    currentArrow.draw(rangle)
                    currentArrow = None
                    reqNum -= 1
                else:      # collision happened!
                    mixer.music.load("sounds/collison.mp3")
                    mixer.music.play()

                    # This condition checks trial counter to decide whether the game is over or not
                    if trial > 0:    # there are remaining trials so the game is not over
                        trial -= 1
                        reqNum = max_arrows
                    else:           # the game is over so we need to start from zero
                        gameOver = 1

                        # clean start
                        trial = 3
                        level = 1
                        max_arrows = 9
                        reqNum = max_arrows
                        lose_counter += 1
                        gameSpeed = rot_sens
                    arrowList.clear()
                    NumberOfArrows = 0
                    currentArrow = None
                    fail = 0
                    lose_flag = 1
                    newlevel = 1
        glLoadIdentity()

        # Draw rotating arrows:
        glColor3d(0, 0, 0)
        for i in range((NumberOfArrows - 1)):
            arrowList[i].draw(rangle)
            glLoadIdentity()

        # This condition checks the required arrows to win:
        if reqNum != 0:  # it hasn't reached the required number of arrows needed to win
            glColor3d(1, 1, 1)
            draw_text(reqNum, 0, 0.35)
        else:           # it has reached the required number so it will go to the next level:
            arrowList.clear()
            NumberOfArrows = 0
            max_arrows -= 1
            reqNum = max_arrows
            level += 1
            gameSpeed += 0.01
            mixer.music.load("sounds/levelup.mp3")
            mixer.music.play()
            newlevel = 1

        # This condition checks if the player has won "reached level 10"
        if level == 10:
            mixer.music.load("sounds/vectory.mp3")
            mixer.music.play(-1)
            lose_flag = 0
            level = 1
            trial = 3
            max_arrows = 9
            reqNum = max_arrows
            gameSpeed = rot_sens
            gameOver = 1
            newlevel = 1

        # This section is for the up bar "level, lose counter, and trial counter":
        glColor3d(0, 0, 1)
        draw_text("Level: " + str(level), -0.9, 0.9)
        glColor3d(1, 0, 0)
        draw_text("Lose: " + str(lose_counter), -0.9, 0.75)
        if trial > 0:
            glPointSize(18)
            glBegin(GL_POINTS)
            for i in range(1, (trial + 1), 1):
                glVertex2d(0.9 - (i * 0.09), 0.85)
            glEnd()
            glPointSize(1)
        rangle += gameSpeed
    glutSwapBuffers()


#########################################################################################################

def main():
    glutInit()
    mixer.init()
    init()
    glutInitWindowSize(600, 600)
    glutInitWindowPosition(250, 50)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
    glutCreateWindow(b"Arrow Hit")
    glutDisplayFunc(myGame)
    glutTimerFunc(time_interval, Timer, 1)
    glutMouseFunc(mouse_func)
    glutMainLoop()


if __name__ == "__main__":
    main()
