from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import pygame
from random import randint
#############################################@-Initialization-@########################################
current_keyboard_x = 350
current_Falling1 = randint(0, 620), randint(800, 900)
current_Falling2 = randint(0, 620), randint(800, 900)
current_Falling3 = randint(0, 620), randint(800, 900)
current_Falling4 = randint(0, 620), randint(1100, 1200)
current_Falling5 = randint(0, 620), randint(1100, 1200)
current_Falling6 = randint(0, 620), randint(1100, 1200)
current_Falling7 = randint(0, 620), randint(1400, 1500)
current_Falling8 = randint(0, 620), randint(1400, 1500)
current_Falling9 = randint(0, 620), randint(1400, 1500)
current_Falling10 = randint(0, 620), randint(1700, 1800)
current_Falling11 = randint(0, 620), randint(1700, 1800)
current_Falling12 = randint(0, 620), randint(1700, 1800)
addY1 = addY2 = addY3 = addY4 = addY5 = addY6 = addY7 = addY8 = addY9 = addY10 = addY11 = addY12 = addY0 = deltxy = 0
level = 1
score = 0
Shot = 0
list = []
texture_names = [0 , 1 , 2]
def init():
    glClearColor(.5, .7, .7, 1)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, 700, 0, 700 , -1, 1)
    glMatrixMode(GL_MODELVIEW)
    load_textures()
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
#############################################@-Texture-@#################################################
def texture_setup(texture_image_binary, texture_name, width, height):
    glBindTexture(GL_TEXTURE_2D, texture_name)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexImage2D(GL_TEXTURE_2D,
                 0,
                 GL_RGBA,
                 width, height,
                 0,
                 GL_RGBA,
                 GL_UNSIGNED_BYTE,
                 texture_image_binary)
def load_and_setup(image_path, idx):
    image = pygame.image.load(image_path)
    texture = pygame.image.tostring(image, "RGBA", True)
    texture_setup(texture, texture_names[idx], image.get_width(), image.get_height())
def load_textures():
    glEnable(GL_TEXTURE_2D)
    glGenTextures(len(texture_names), texture_names)
    load_and_setup("cannon.png", texture_names[0])
    load_and_setup("rock.png", texture_names[1])
    load_and_setup("fire.png", texture_names[2])
###########################################@-DRAWING-@####################################################
class RECTA:
    def __init__(self, left, right, bottom, top):
        self.left = left
        self.right = right
        self.bottom = bottom
        self.top = top
Player = RECTA(320, 380, 0, 100)
def DrawObject(ObjectLeft, ObjectRight, ObjectBottom, ObjectTop, z):
    glBindTexture(GL_TEXTURE_2D, texture_names[z])
    glBegin(GL_POLYGON)
    glTexCoord2f(0, 0)
    glVertex2d(ObjectLeft, ObjectBottom)
    glTexCoord2f(1, 0)
    glVertex2d(ObjectRight, ObjectBottom)
    glTexCoord2f(1, 1)
    glVertex2d(ObjectRight, ObjectTop)
    glTexCoord2f(0, 1)
    glVertex2d(ObjectLeft, ObjectTop)
    glEnd()
    glBindTexture(GL_TEXTURE_2D, -1)
def drawText(string, x, y):
    glLineWidth(2)
    glColor(1, 1, 1)
    glPushMatrix()
    glTranslate(x, y, 0)
    glScale(.2, .2, 1)
    string = string.encode()
    for c in string:
        glutStrokeCharacter(GLUT_STROKE_ROMAN, c)
    glPopMatrix()
###########################################@-TESTING-@#####################################################
def Test_Ball_Player(ObjectLeft, ObjectRight, ObjectBottom, ObjectTop, Player):
    left_overlap = Player.left <= ObjectLeft <= Player.right
    right_overlap =  Player.left <= ObjectRight <= Player.right
    horizontal_overlap = (left_overlap or right_overlap)
    bottom_overlap = Player.top >= ObjectBottom >= Player.bottom
    top_overlap = Player.top >= ObjectTop >= Player.bottom
    vertical_overlap = (bottom_overlap or top_overlap)
    return horizontal_overlap and vertical_overlap
def Test_Ball_ShotBall(ObjectLeft, Objectright, ObjectBottom, Objecttop, Object2left, Object2right, Object2Bottom, Object2top):
    left_overlap = ObjectLeft  <= Object2left <= Objectright
    right_overlap = ObjectLeft  <= Object2right <= Objectright
    hprizontal_overlap = (left_overlap or right_overlap)
    top_overlap = Objecttop  >= Object2top >= ObjectBottom
    bottom_overlap = Objecttop  >= Object2Bottom >= ObjectBottom
    vertical_overlap = (top_overlap or bottom_overlap)
    return hprizontal_overlap and vertical_overlap
def keyboard_moving(key, x, y):
    global current_keyboard_x, Shot
    if key == GLUT_KEY_LEFT:
        current_keyboard_x = max(current_keyboard_x - 20, 40)
    if key == GLUT_KEY_RIGHT:
        current_keyboard_x = min(current_keyboard_x + 20, 660)
    if key == GLUT_KEY_UP:
        Shot = 1
###########################################@-DISPLAYING-@###################################################
def Display():
    global addY1 , addY2 , addY3, addY4 , addY5 , addY6 , addY7 , addY8 , addY9, addY10 , addY11 , addY12 ,addY0, current_Falling1, current_Falling2, current_Falling3, current_Falling4,\
        current_Falling5,current_Falling6, current_Falling7, current_Falling8, current_Falling9, current_Falling10 ,current_Falling11, current_Falling12, Shot, score, deltxy, level
    glClear(GL_COLOR_BUFFER_BIT)
    #########################################################Balls####################################################################
    addY1 -= .4
    addY2 -= .4
    addY3 -= .4
    addY4 -= .4
    addY5 -= .4
    addY6 -= .4
    addY7 -= .4
    addY8 -= .4
    addY9 -= .4
    addY10 -= .4
    addY11 -= .4
    addY12 -= .4
    DrawObject(current_Falling1[0]-deltxy, current_Falling1[0]+60+deltxy, current_Falling1[1]+addY1-deltxy, current_Falling1[1]+60+addY1+deltxy, 1)
    DrawObject(current_Falling2[0]-deltxy, current_Falling2[0]+60+deltxy, current_Falling2[1]+addY2-deltxy, current_Falling2[1]+60+addY2+deltxy, 1)
    DrawObject(current_Falling3[0]-deltxy, current_Falling3[0]+60+deltxy, current_Falling3[1]+addY3-deltxy, current_Falling3[1]+60+addY3+deltxy, 1)
    DrawObject(current_Falling4[0]-deltxy, current_Falling4[0] + 60+deltxy, current_Falling4[1] + addY4-deltxy,current_Falling4[1] + 60 + addY4+deltxy, 1)
    DrawObject(current_Falling5[0]-deltxy, current_Falling5[0] + 60+deltxy, current_Falling5[1] + addY5-deltxy,current_Falling5[1] + 60 + addY5+deltxy, 1)
    DrawObject(current_Falling6[0]-deltxy, current_Falling6[0] + 60+deltxy, current_Falling6[1] + addY6-deltxy,current_Falling6[1] + 60 + addY6+deltxy, 1)
    DrawObject(current_Falling7[0]-deltxy, current_Falling7[0] + 60+deltxy, current_Falling7[1] + addY7-deltxy,current_Falling7[1] + 60 + addY7+deltxy, 1)
    DrawObject(current_Falling8[0]-deltxy, current_Falling8[0] + 60+deltxy, current_Falling8[1] + addY8-deltxy, current_Falling8[1] + 60 + addY8+deltxy, 1)
    DrawObject(current_Falling9[0]-deltxy, current_Falling9[0] + 60+deltxy, current_Falling9[1] + addY9-deltxy, current_Falling9[1] + 60 + addY9+deltxy, 1)
    DrawObject(current_Falling10[0]-deltxy, current_Falling10[0] + 60+deltxy, current_Falling10[1] + addY10-deltxy, current_Falling10[1] + 60 + addY10+deltxy, 1)
    DrawObject(current_Falling11[0]-deltxy, current_Falling11[0] + 60+deltxy, current_Falling11[1] + addY11-deltxy, current_Falling11[1] + 60 + addY11+deltxy, 1)
    DrawObject(current_Falling12[0]-deltxy, current_Falling12[0] + 60+deltxy, current_Falling12[1] + addY12-deltxy, current_Falling12[1] + 60 + addY12+deltxy, 1)
    if Test_Ball_Player(current_Falling1[0], current_Falling1[0]+60, current_Falling1[1]+addY1, current_Falling1[1]+60+addY1, Player) == True :
        sys.exit(0)
    if addY1 <= -1100:
        addY1 = 0
        current_Falling1 = randint(0, 620), randint(800, 900)
    if Test_Ball_Player(current_Falling2[0], current_Falling2[0] + 60, current_Falling2[1] + addY2,current_Falling2[1] + 60 + addY2, Player) == True:
        sys.exit(0)
    if addY2 <= -1100 :
        addY2 = 0
        current_Falling2 = randint(0, 620), randint(800, 900)
    if Test_Ball_Player(current_Falling3[0], current_Falling3[0] + 60, current_Falling3[1] + addY3,current_Falling3[1] + 60 + addY3, Player) == True:
        sys.exit(0)
    if addY3 <= -1100:
        addY3 = 0
        current_Falling3 = randint(0, 620), randint(800, 900)
    if Test_Ball_Player(current_Falling4[0], current_Falling4[0] + 60, current_Falling4[1] + addY4,current_Falling4[1] + 60 + addY4, Player) == True:
        sys.exit(0)
    if addY4 <= -1400 :
        addY4 = 0
        current_Falling4 = randint(0, 620), randint(1100, 1200)
    if Test_Ball_Player(current_Falling5[0], current_Falling5[0] + 60, current_Falling5[1] + addY5,current_Falling5[1] + 60 + addY5, Player) == True:
        sys.exit(0)
    if addY5 <= -1400 :
        addY5 = 0
        current_Falling5 = randint(0, 620), randint(1100, 1200)
    if Test_Ball_Player(current_Falling6[0], current_Falling6[0] + 60, current_Falling6[1] + addY6,current_Falling6[1] + 60 + addY6, Player) == True:
        sys.exit(0)
    if addY6 <= -1400 :
        addY6 = 0
        current_Falling6 = randint(0, 620), randint(1100, 1200)
    if Test_Ball_Player(current_Falling7[0], current_Falling7[0] + 60, current_Falling7[1] + addY7, current_Falling7[1] + 60 + addY7, Player) == True:
        sys.exit(0)
    if addY7 <= -1700:
        addY7 = 0
        current_Falling7 = randint(0, 620), randint(1400, 1500)
    if Test_Ball_Player(current_Falling8[0], current_Falling8[0] + 60, current_Falling8[1] + addY8, current_Falling8[1] + 60 + addY8, Player) == True:
        sys.exit(0)
    if addY8 <= -1700:
        addY8 = 0
        current_Falling8 = randint(0, 620), randint(1400, 1500)
    if Test_Ball_Player(current_Falling9[0], current_Falling9[0] + 60, current_Falling9[1] + addY9, current_Falling9[1] + 60 + addY9, Player) == True:
        sys.exit(0)
    if addY9 <= -1700:
        addY9 = 0
        current_Falling9 = randint(0, 620), randint(1400, 1500)
    if Test_Ball_Player(current_Falling10[0], current_Falling10[0] + 60, current_Falling10[1] + addY10, current_Falling10[1] + 60 + addY10, Player) == True:
        sys.exit(0)
    if addY10 <= -2000 :
        addY10 = 0
        current_Falling10 = randint(0, 620), randint(1700, 1800)
    if Test_Ball_Player(current_Falling11[0], current_Falling11[0] + 60, current_Falling11[1] + addY11, current_Falling11[1] + 60 + addY11, Player) == True:
        sys.exit(0)
    if addY11 <= -2000:
        addY11 = 0
        current_Falling11 = randint(0, 620), randint(1700, 1800)
    if Test_Ball_Player(current_Falling12[0], current_Falling12[0] + 60, current_Falling12[1] + addY12, current_Falling12[1] + 60 + addY12, Player) == True:
        sys.exit(0)
    if addY12 <= -2000:
        addY12 = 0
        current_Falling12 = randint(0, 620), randint(1700, 1800)
    #########################################################SHOTBALL####################################################################
    if Shot == 1:
        addY0 += 1.3
        list.append(Player.left)
        list.append(Player.right)
        DrawObject( list[0] + 10, list[1] - 10, 100+addY0, 140+addY0, 2)
        if Test_Ball_ShotBall(current_Falling1[0], current_Falling1[0] + 60, current_Falling1[1] + addY1, current_Falling1[1] + 60 + addY1, list[0] + 20, list[1] - 20, 120+addY0, 160+addY0) == True:
            addY0 = 0
            addY1 = 0
            current_Falling1 = randint(0, 620), randint(800, 900)
            Shot = 0
            score += 1
        if Test_Ball_ShotBall(current_Falling2[0], current_Falling2[0] + 60, current_Falling2[1] + addY2, current_Falling2[1] + 60 + addY2, list[0] + 20, list[1] - 20, 120+addY0, 160+addY0) == True:
            addY0 = 0
            addY2 = 0
            current_Falling2 = randint(0, 620), randint(800, 900)
            Shot = 0
            score += 1
        if Test_Ball_ShotBall(current_Falling3[0], current_Falling3[0] + 60, current_Falling3[1] + addY3, current_Falling3[1] + 60 + addY3, list[0] + 20, list[1] - 20, 120+addY0, 160+addY0) == True:
            addY0 = 0
            addY3 = 0
            current_Falling3 = randint(0, 620), randint(800, 900)
            Shot = 0
            score += 1
        if Test_Ball_ShotBall(current_Falling4[0], current_Falling4[0] + 60, current_Falling4[1] + addY4, current_Falling4[1] + 60 + addY4, list[0] + 20, list[1] - 20, 120+addY0, 160+addY0) == True:
            addY0 = 0
            addY4 = 0
            current_Falling4 = randint(0, 620), randint(1100, 1200)
            Shot = 0
            score += 1
        if Test_Ball_ShotBall(current_Falling5[0], current_Falling5[0] + 60, current_Falling5[1] + addY5, current_Falling5[1] + 60 + addY5, list[0] + 20, list[1] - 20, 120+addY0, 160+addY0) == True:
            addY0 = 0
            addY5 = 0
            current_Falling5 = randint(0, 620), randint(1100, 1200)
            Shot = 0
            score += 1
        if Test_Ball_ShotBall(current_Falling6[0], current_Falling6[0] + 60, current_Falling6[1] + addY6, current_Falling6[1] + 60 + addY6, list[0] + 20, list[1] - 20, 120+addY0, 160+addY0) == True:
            addY0 = 0
            addY6 = 0
            current_Falling6 = randint(0, 620), randint(1100, 1200)
            Shot = 0
            score += 1
        if Test_Ball_ShotBall(current_Falling7[0], current_Falling7[0] + 60, current_Falling7[1] + addY7, current_Falling7[1] + 60 + addY7, list[0] + 20, list[1] - 20, 120+addY0, 160+addY0) == True:
            addY0 = 0
            addY7 = 0
            current_Falling7 = randint(0, 620), randint(1400, 1500)
            Shot = 0
            score += 1
        if Test_Ball_ShotBall(current_Falling8[0], current_Falling8[0] + 60, current_Falling8[1] + addY8, current_Falling8[1] + 60 + addY8, list[0] + 20, list[1] - 20, 120+addY0, 160+addY0) == True:
            addY0 = 0
            addY8 = 0
            current_Falling8 = randint(0, 620), randint(1400, 1500)
            Shot = 0
            score += 1
        if Test_Ball_ShotBall(current_Falling9[0], current_Falling9[0] + 60, current_Falling9[1] + addY9, current_Falling9[1] + 60 + addY9, list[0] + 20, list[1] - 20, 120+addY0, 160+addY0) == True:
            addY0 = 0
            addY9 = 0
            current_Falling9 = randint(0, 620), randint(1400, 1500)
            Shot = 0
            score += 1
        if Test_Ball_ShotBall(current_Falling10[0], current_Falling10[0] + 60, current_Falling10[1] + addY10, current_Falling10[1] + 60 + addY10, list[0] + 20, list[1] - 20, 120+addY0, 160+addY0) == True:
            addY0 = 0
            addY10 = 0
            current_Falling10 = randint(0, 620), randint(1700, 1800)
            Shot = 0
            score += 1
        if Test_Ball_ShotBall(current_Falling11[0], current_Falling11[0] + 60, current_Falling11[1] + addY11, current_Falling11[1] + 60 + addY11, list[0] + 20, list[1] - 20, 120+addY0, 160+addY0) == True:
            addY0 = 0
            addY11 = 0
            current_Falling11 = randint(0, 620), randint(1700, 1800)
            Shot = 0
            score += 1
        if Test_Ball_ShotBall(current_Falling12[0], current_Falling12[0] + 60, current_Falling12[1] + addY12, current_Falling12[1] + 60 + addY12, list[0] + 20, list[1] - 20, 120+addY0, 160+addY0) == True:
            addY0 = 0
            addY12 = 0
            current_Falling12 = randint(0, 620), randint(1700, 1800)
            Shot = 0
            score += 1
        if addY0 >= 600 :
            addY0 = 0
            Shot = 0
    else :
        list.clear()
    #########################################################cannon####################################################################
    DrawObject(Player.left, Player.right, Player.bottom, Player.top, 0)
    Player.right = current_keyboard_x + 30
    Player.left = current_keyboard_x - 30
    #########################################################Levels&Score####################################################################
    string = "Current_score:" + str(score)
    drawText(string, 10, 10)
    string = "Current_Level:" + str(level)
    drawText(string, 510, 10)
    if score >= 10 :
        addY1 -= .7
        addY2 -= .7
        addY3 -= .7
        addY4 -= .7
        addY5 -= .7
        addY6 -= .7
        addY7 -= .7
        addY8 -= .7
        addY9 -= .7
        addY10 -= .7
        addY11 -= .7
        addY12 -= .7
        level = 2
        deltxy=15
    if score >= 20:
        addY1 -= 1
        addY2 -= 1
        addY3 -= 1
        addY4 -= 1
        addY5 -= 1
        addY6 -= 1
        addY7 -= 1
        addY8 -= 1
        addY9 -= 1
        addY10 -= 1
        addY11 -= 1
        addY12 -= 1
        level = 3
        deltxy=30
    glutSwapBuffers()
def Timer(v):
    Display()
    glutTimerFunc(1, Timer, 1)
def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(700, 700)
    glutInitWindowPosition(350, 0)
    glutCreateWindow(b"Falling")
    glutDisplayFunc(Display)
    glutTimerFunc(1, Timer, 1)
    glutSpecialFunc(keyboard_moving)
    init()
    glutMainLoop()
main()