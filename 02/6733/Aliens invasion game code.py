from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import pygame
from random import randint

WindowDim = 10


translating_x = 1
translating_y = 1

minimum = 1
maximum = WindowDim

increasing = True
decreasing = False


HoldTime = 0

step = 0.3  # For Plane Movement

PlaneDim = 1
PlaneX = 0
PlaneY = -WindowDim + PlaneDim

PlaneBulletX = 0
PlaneBulletY = -WindowDim + PlaneDim

shooting = False  # I'm Not Shooting
attacking = False  # Aliens Are Not Attacking
losing = False  # I Didn't Lose

Score = 0
ScoreGoal = 5

AlienN = 5  # can be increased with the limit of the arrays sizes
AlienDim = 1
AlienX = [0, 0, 0, 0, 0, 0, 0]  # the array size limits the number of alien ships
AlienY = [0, 0, 0, 0, 0, 0, 0]  # the array size limits the number of alien ships
AlienBulletX = [0, 0, 0, 0, 0, 0, 0]  # the array size limits the number of alien ships
AlienBulletY = [WindowDim + 1, WindowDim + 1, WindowDim + 1, WindowDim + 1, WindowDim + 1, WindowDim + 1, WindowDim + 1]  # to make the alien bullets initially outside the frustem

texture_names = [0, 1, 2, 3]
spaceship = 0  # texture number 0
alien = 1  # texture number 1
lose = 2  # texture number 2
win = 3  # texture number 3


def DrawSquare(Dim, TexNum):
    glColor3f(1, 1, 1)
    glBindTexture(GL_TEXTURE_2D, texture_names[TexNum])
    glBegin(GL_QUADS)

    glTexCoord2f(0, 0)
    glVertex2f(-Dim, -Dim)

    glTexCoord2f(0, 1)
    glVertex2f(-Dim, Dim)

    glTexCoord2f(1, 1)
    glVertex2f(Dim, Dim)

    glTexCoord2f(1, 0)
    glVertex2f(Dim, -Dim)

    glEnd()

    glBindTexture(GL_TEXTURE_2D, -1)


def InitShapesPos(v):
    global AlienX, AlienY
    for i in range(v):  # Generate Five Random Positions
        AlienX[i] = randint(-WindowDim + 2, WindowDim - 1)  # All The X-Axis Except The Score Dim
        AlienY[i] = randint(-WindowDim + 2 + PlaneDim,
                            WindowDim - 2)  # All The Y-Axis Except The Score Dim and Plane Dim

    for j in range(v):
        for i in range(v):
            if i != j:
                if AlienX[j] - AlienDim <= AlienX[i] <= AlienX[j] + AlienDim:
                    if AlienY[j] - AlienDim <= AlienY[i] <= AlienY[j] + AlienDim:
                        InitShapesPos(AlienN)  # Internal Recursion Till We Get Perfect positions


def genShapePos(index):
    global AlienX, AlienY
    # Just Generate One New Position
    AlienX[index] = randint(-WindowDim + 2, WindowDim - 1)  # All The X-Axis Except The Score Dim
    AlienY[index] = randint(-WindowDim + 2 + PlaneDim, WindowDim - 2)  # All The Y-Axis Except The Score Dim and Plane Dim

    for i in range(AlienN):
        if i != index:
            if AlienX[index] - AlienDim <= AlienX[i] <= AlienX[index] + AlienDim:
                if AlienY[index] - AlienDim <= AlienY[i] <= AlienY[index] + AlienDim:
                    genShapePos(index)  # Internal Recursion


def my_init():
    loadTextures()

    glClearColor(1, 1, 1, 1)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-WindowDim, WindowDim, -WindowDim, WindowDim)

    glMatrixMode(GL_MODELVIEW)


def texture_setup(texture_image_binary, texture_name, width, height):
    glBindTexture(GL_TEXTURE_2D, texture_name)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

    glTexImage2D(GL_TEXTURE_2D,
                 0,  # mipmap
                 GL_RGBA,  # Bytes per pixel
                 width, height,
                 0,  # Texture border
                 GL_RGBA,  # RGBA Exactly as in  pygame.image.tostring(image, "RGBA", True)
                 GL_UNSIGNED_BYTE,
                 texture_image_binary)  # texture init step [7]


def loadTextures():
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_BLEND)  # FOR BLENDING
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)  # FOR BLENDING
    images = []
    images.append(pygame.image.load("spaceship.png"))  # For The Plane
    images.append(pygame.image.load("alien.png"))  # For The Shape
    images.append(pygame.image.load("lose.jpg"))  # For The Losing Screen
    images.append(pygame.image.load("win.jpg"))  # For The Wining Screen
    textures = [pygame.image.tostring(image, "RGBA", True)
                for image in images]

    glGenTextures(len(images), texture_names)

    for i in range(len(images)):
        texture_setup(textures[i],
                      texture_names[i],
                      images[i].get_width(),
                      images[i].get_height())


def Repeat(v):
    global AlienBulletX, AlienBulletY, AlienX, AlienY, attacking, HoldTime
    mainFunc()
    HoldTime += 1
    if HoldTime == 1000:  # Attack Every Second
        attacking = True
        HoldTime = 0
        for i in range(AlienN):
            AlienBulletX[i] = AlienX[i]
            AlienBulletY[i] = AlienY[i]
    glutTimerFunc(1, Repeat, 1)


def keyboard(key, x, y):
    global PlaneX, PlaneY, step, shooting, losing, PlaneBulletX, PlaneBulletY
    if key == b"w":
        PlaneY += step
    elif key == b"s":
        PlaneY -= step
    elif key == b"d":
        PlaneX += step
    elif key == b"a":
        PlaneX -= step
    elif key == b"k":

        PlaneBulletX = PlaneX
        PlaneBulletY = PlaneY

        shooting = True
    elif key == b"q":
        glutDestroyWindow()
    elif key == b"r" and losing:  # and condition is added so you can't reload while in game
        losing = False  # So You Can Get A New Try
        shooting = False
        Reset()

    return None


def Reset():
    global PlaneX, PlaneY, AlienBulletX, AlienBulletY, AlienX, AlienY, HoldTime, attacking
    HoldTime = 0  # So Aliens Wait For 1 second at first
    PlaneX = 0  # Bring The Plane Back To The Middle
    PlaneY = -WindowDim + PlaneDim  # Bring The Plane Back To The Middle
    InitShapesPos(AlienN)

    for i in range(AlienN):
        AlienBulletX[i] = AlienX[i]
        AlienBulletY[i] = AlienY[i]

    attacking = False


def shoot(x, y):
    glPointSize(5)
    glBegin(GL_POINTS)
    glColor3f(0, 0, 0)
    glVertex2f(x, y)
    glEnd()


def drawChar(string, x, y):
    glLineWidth(2)
    glColor(0.1, 0.1, 0)
    glPushMatrix()  # remove the previous transformations
    glTranslate(x, y, 0)
    glScale(0.005, 0.005, 1)  # DownScale According To Our Dimensions
    string = string.encode()
    for c in string:
        glutStrokeCharacter(GLUT_STROKE_ROMAN, c)
    glPopMatrix()


def mainFunc():
    global PlaneX, PlaneY, shooting, PlaneBulletX, PlaneBulletY, losing, AlienBulletX, AlienBulletY, Score ,translating_x ,translating_y,minimum ,increasing ,decreasing ,maximum


    glClear(GL_COLOR_BUFFER_BIT)
    if not losing and Score != ScoreGoal:

        drawChar("Score: " + str(Score) + "/" + str(ScoreGoal), -WindowDim + 0.5, WindowDim - 1)

        # Collision Detection (Plane vs Wall)
        if PlaneX + PlaneDim >= WindowDim:
            PlaneX = WindowDim - PlaneDim
        if PlaneX - PlaneDim <= -WindowDim:
            PlaneX = -WindowDim + PlaneDim
        if PlaneY + PlaneDim >= WindowDim:
            PlaneY = WindowDim - PlaneDim
        if PlaneY - PlaneDim <= -WindowDim:
            PlaneY = -WindowDim + PlaneDim
        # It's Better To Create Every Condition With It's Own "If" OtherWise There Will Be A Bug if two Conditions Are satisfied

        # Collision Detection (Bullet vs Alien)
        for i in range(AlienN):
            if AlienX[i] + AlienDim >= PlaneBulletX >= AlienX[i] - AlienDim:
                if AlienY[i] + AlienDim >= PlaneBulletY >= AlienY[i] - AlienDim:
                    shooting = False  # Make The Bullet Disappear
                    Score += 1
                    genShapePos(i)  # Generate New Position

        # Collision Detection (Aliens's Bullet vs Plane)
        for i in range(AlienN):
            if PlaneX + PlaneDim >= AlienBulletX[i] >= PlaneX - PlaneDim:
                if PlaneY + PlaneDim >= AlienBulletY[i] >= PlaneY - PlaneDim:
                    losing = True

        # collision Detection (plane vs Alien)
        for i in range(AlienN):
            if AlienX[i] - AlienDim <= PlaneX + .7 and AlienX[i] + AlienDim >= PlaneX - .7:
                if AlienY[i] - AlienDim <= PlaneY + .7 and AlienY[i] + AlienDim >= PlaneY - .7:
                    losing = True

        if shooting:  # from plane
            shoot(PlaneBulletX, PlaneBulletY)
            PlaneBulletY += 0.04

        if attacking:  # from alien
            glPushMatrix()
            glTranslate(0,.1,0)

            for i in range(AlienN):
                shoot(AlienBulletX[i], AlienBulletY[i])
                AlienBulletY[i] -= 0.025
            glTranslate(0,-.1,0)

            glPopMatrix()

        if increasing:
            translating_x += .01
            translating_y += .01

        if translating_x > maximum:
            decreasing = True
            increasing = False
        if decreasing:
            translating_x -= .01
            translating_y -= .01
        if translating_y < minimum:
            increasing = True
            decreasing = False

        glPushMatrix()
        glTranslate(PlaneX, PlaneY, 0)
        DrawSquare(PlaneDim, spaceship)
        glPopMatrix()

        # Doesn't Need 'glLoadIdentity' nor 'push/pop', as it's the last thing we draw anyway
        glPushMatrix()
        glTranslate(translating_x,0,0)

        for i in range(AlienN):
            glPushMatrix()
            glTranslate(AlienX[i], AlienY[i], 0)
            DrawSquare(AlienDim, alien)
            glPopMatrix()
        glPopMatrix()

    else:
        if losing:
            Score = 0
            DrawSquare(WindowDim, lose)
        else:
            DrawSquare(WindowDim, win)

    glutSwapBuffers()


glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowPosition(300, 20)
glutInitWindowSize(650, 650)
glutCreateWindow(b"Alien Invasion")
my_init()
InitShapesPos(AlienN)
glutDisplayFunc(mainFunc)
glutTimerFunc(1000, Repeat, 1)
glutKeyboardFunc(keyboard)
glutMainLoop()
