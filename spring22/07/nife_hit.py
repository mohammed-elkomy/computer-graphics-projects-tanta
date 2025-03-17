from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from numpy import *
import pygame

texture_names = [0, 1, 2, 3, 4]  # images used
axrng = 1  # background dimensions
INTERVAL = 80
N_knife = 15  # number of knifes
hit_cntr = 0
circle_rot = 0
r = 0.3
circle_trans = 0.5
c_k_anim = 1
knife_out = False
again = False
tryflg = False
t_delay = 0
step = 10


def texture_setup(texture_image_binary, texture_name, width, height):
    glBindTexture(GL_TEXTURE_2D, texture_name)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T,
                    GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

    glTexImage2D(GL_TEXTURE_2D,
                 0,
                 GL_RGBA,  # komy
                 width, height,
                 0,
                 GL_RGBA, GL_UNSIGNED_BYTE, texture_image_binary)


def loadTexture():
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_BLEND)  #
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)  # komy

    images = []
    images.append(pygame.image.load("background.jpeg"))
    images.append(pygame.image.load("knife.png"))
    images.append(pygame.image.load("background circle.jpeg"))
    images.append(pygame.image.load("win.jpg"))
    images.append(pygame.image.load("lose_case.jpg"))

    texture = [pygame.image.tostring(image, "RGBA", True)
               for image in images]
    glGenTextures(len(images), texture_names)
    for s in range(len(images)):
        texture_setup(texture[s], texture_names[s], images[s].get_width(), images[s].get_height())


def background(h):
    """that function is called by the image index -h- to be drawn"""
    glColor3d(1, 1, 1)
    if h == 1:
        glBindTexture(GL_TEXTURE_2D, texture_names[0])  # background of the game
    elif h == 2:
        glBindTexture(GL_TEXTURE_2D, texture_names[3])  # pic of win case
    else:
        glBindTexture(GL_TEXTURE_2D, texture_names[4])  # pic of lose case

    # background rendering:
    glBegin(GL_QUADS)
    glTexCoord2f(0, axrng)
    glVertex2d(-axrng, axrng)
    glTexCoord2f(axrng, axrng)
    glVertex2d(axrng, axrng)
    glTexCoord2f(axrng, 0)
    glVertex2d(axrng, -axrng)
    glTexCoord2f(0, 0)
    glVertex2d(-axrng, -axrng)
    glEnd()
    glBindTexture(GL_TEXTURE_2D, -1)  # komy


def init():
    loadTexture()


def draw_knife(H):
    global r, c, c_k_anim, knife_out, circle_trans
    # r: radius, c: position of HUD knifes, c_k_anim: animation of crashed knife

    glLoadIdentity()

    if H.crash:  # if the knife crashed
        if (H.top + H.tran < (circle_trans - r)) & H.k_c_crash:
            glTranslate(0, H.tran, 0)
        else:  # animation of the crashing knife
            glTranslate(0.7 * c_k_anim, 0.7 * c_k_anim, 0)
            glRotate(180, 0, 0, 1)
            H.top = circle_trans - r  # H.top+0.9 -----> -0.7+0.9 ----> 0.2
            H.bottom = 0
            if c_k_anim <= 1 and c_k_anim >= -1:
                c_k_anim -= .1
                knife_out = True

    else:  # the knife is taking off
        if (H.top + H.tran < (circle_trans - r)) & H.k_c_crash:
            glTranslate(0, H.tran, 0)
        else:
            H.top = circle_trans - r  # H.top+0.9 -----> -0.7+0.9 ----> 0.2
            H.bottom = 0  # H.bottom+0.9 ------> -0.9+0.9--->0
            H.tran = 0
            H.k_c_crash = False

        if not H.k_c_crash:  # repostioning the knife w.r.t the circle
            glTranslate(0, circle_trans, 0)
            glRotate(H.rot, 0, 0, 1)
            glTranslate(0, -circle_trans, 0)
    glBindTexture(GL_TEXTURE_2D, texture_names[1])  # knife shape
    glBegin(GL_POLYGON)
    glTexCoord2f(0, 0)
    glVertex2d(H.left, H.bottom)
    glTexCoord2f(1, 0)
    glVertex2d(H.right, H.bottom)
    glTexCoord2f(1, 1)
    glVertex2d(H.right, H.top)
    glTexCoord2f(0, 1)
    glVertex2d(H.left, H.top)
    glEnd()
    c = .8
    for i in range(hit_cntr, N_knife):  # remaining knifes.
        glLoadIdentity()
        glTranslate(.9, c, 0)
        glRotate(60, 0, 0, 1)
        glBindTexture(GL_TEXTURE_2D, texture_names[1])
        glScale(.1, .1, .1)
        glColor3d(1, 1, 1)
        glBegin(GL_POLYGON)
        glTexCoord2f(1, 1)
        glVertex2d(0.2, 0.9)
        glTexCoord2f(0, 1)
        glVertex2d(-0.2, 0.9)
        glTexCoord2f(0, 0)
        glVertex2d(-0.2, -1)
        glTexCoord2f(1, 0)
        glVertex2d(0.2, -1)
        glEnd()
        c = c - .1

    glBindTexture(GL_TEXTURE_2D, -1)  # komy


def Try_again(s=10):  # func to intialazation all values to restart the game, BUT with another difficulty
    global hit_cntr, circle_rot, r, circle_trans, c_k_anim, knife_out, rect, again, t_delay, tryflg, step
    step = s
    hit_cntr = 0
    circle_rot = 0
    r = 0.3
    circle_trans = 0.5
    t_delay = 0
    c_k_anim = 1
    knife_out = False
    again = False
    tryflg = False
    rect.clear()
    for i in range(N_knife):  # reconstructing knives
        i = Rectangle()
        rect.append(i)


def drawText(string, x, y, choose_view):
    glLineWidth(3)
    glColor(1, 0, 0)
    glLoadIdentity()
    glTranslate(x, y, 0)
    if choose_view == 1:  # for score
        glScale(0.0004, 0.0004, 1)
    else:
        glScale(0.001, 0.001, 1)  # for win

    string = string.encode()
    for c in string:
        glutStrokeCharacter(GLUT_STROKE_ROMAN, c)


def game_timer(v):
    moving()
    glutTimerFunc(INTERVAL, game_timer, 1)  # TODO: replace 1 by v+1


class Rectangle:  # the knife class

    def __init__(self, left=-0.03, bottom=-0.9, right=0.03, top=-0.7, rot=0, tran=0, k_c_crash=True, done=False,
                 crash=False):
        self.left = left  # khnife
        self.bottom = bottom  # khnife
        self.right = right  # khnife
        self.top = top  # khnife
        self.rot = rot  # for hit_cntr the knife in circle by the same speed circle
        self.tran = tran  # for launch the knife from its first position to circle
        self.k_c_crash = k_c_crash  # the condition to convert hit_cntr of knife from vertical movement to Circular motion
        self.done = done  # the state of knife been thrown
        self.crash = crash  # crash state of two knifes


rect = []
for i in range(N_knife):  # inittializing knifes objects with the ini values.
    e = Rectangle()
    rect.append(e)


def detctor(objt):
    for i in rect:  # checking the knives in the circle with the recent thrown knife
        if objt.done and (i.rot == -360 + (2 * step)):
            # NOTE: for the knife to reach the circle area, it requires two steps.
            objt.crash = True


def circle():
    global circle_rot, circle_trans, r

    # circle_rot: rotation , circle_trans: translation on the Y-axis , r: radius of the circle
    glLoadIdentity()
    glClearColor(1, 1, 1, 1)
    glClear(GL_COLOR_BUFFER_BIT)
    background(1)  # background image, not the circle
    glBindTexture(GL_TEXTURE_2D, texture_names[2])

    glTranslate(0, circle_trans, 0)
    glRotate(circle_rot, 0, 0, 1)
    glBegin(GL_POLYGON)
    res = 0.1  # circle resolution
    for i in arange(0, 2 * pi, res):
        x = r * cos(i)
        y = r * sin(i)
        glTexCoord2f((x / r+1)/2, (y / r+1)/2)
        glVertex(x, y)

    glEnd()

    glBindTexture(GL_TEXTURE_2D, -1)  # komy
    s = hit_cntr  # in case of lose, so that the score doesn't increase
    if rect[hit_cntr - 1].crash:
        s -= 1
    string = "SCORE : " + str(s)  # score of the player

    drawText(string, -.9, .9, 1)
    if not knife_out:  # drawing the point of the knife postion on the cricle
        for i in range(0, N_knife):
            glLoadIdentity()
            glTranslate(0, circle_trans, 0)
            glRotate(rect[i].rot, 0, 0, 1)
            glTranslate(0, -circle_trans, 0)
            glPointSize(10)
            glColor(1, 1, 0)
            glBegin(GL_POINTS)
            glVertex(0, -rect[i].top + .4)
            glEnd()


def keyboard(key, x, y):
    global hit_cntr, rect, again, tryflg
    # hit_cntr: counting thrown knifes, rect: knife object
    if (key == b"a") | (key == b"A"):
        if hit_cntr < N_knife:  # handling 'index out of range' error
            hit_cntr += 1
            if hit_cntr <= N_knife:  # stating that the knife is thrown and testing if crashed with another knife.
                rect[hit_cntr - 1].done = True
                detctor(rect[hit_cntr - 1])
    if tryflg:
        if (key == b"r") | (key == b"R"):
            again = True


def moving():
    """the drawing function"""
    global rect, N_knife, hit_cntr, circle_rot, t_delay, step, tryflg
    # N_knife: number of knifes , hit_cntr: counter of throws, t_delay: time of win/lose image, tryflg: to restart the game

    circle()  # drawing the circle

    if not knife_out:  # if the knife didn't crash
        for i in range(0, N_knife):  # continue drawing knives
            glColor3d(1, 1, 1)
            draw_knife(rect[i])
        if hit_cntr == N_knife:
            t_delay += 1  # an arbitrary delay to show that all knifes are correctly in the circle.
            tryflg = True  # maintains the try_state so that the game continues properly.
            if t_delay > 7:
                glLoadIdentity()
                background(2)  # win image
                winner = " You win and get " + str(hit_cntr + hit_cntr) + "point"
                if step == 10:
                    winner = " You win and get to "
                    drawText(winner, -.9, .6, 2)
                    winner = " the next level"
                    drawText(winner, -.5, .45, 2)
                else:
                    drawText(winner, -.9, .6, 2)  # if step == 10:
                #     winner = " You win and get to the next level"
                if again:  # if 'r' is pressed
                    glLoadIdentity()
                    Try_again(15)  # restart the game


    # if the knife crashed
    else:
        tryflg = True
        glLoadIdentity()
        glClearColor(1, 1, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT)
        background(3)  # lose image

        if again:
            glLoadIdentity()
            Try_again()

    glutSwapBuffers()

    for n in range(0, hit_cntr):  # {animation..

        if rect[n].k_c_crash:  # if the knife didn't crashed
            rect[n].tran += 0.45  # translating on Y-axis till hitting the circle
        else:
            if rect[n].rot == -360 + step:  # rotating the knife,and..
                rect[n].rot = 0  # handling the overflow.
            else:
                rect[n].rot -= step
    # NOTE: the knife rotation must equal the circle rotation
    if circle_rot == -360 + step:
        circle_rot = 0
    else:
        circle_rot -= step


# .. control}

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(600, 600)
    glutInitWindowPosition(600, 30)
    glutCreateWindow(b"knife_hit")
    glutDisplayFunc(moving)
    glutKeyboardFunc(keyboard)
    glutTimerFunc(INTERVAL, game_timer, 1)
    init()  # establishing the texture
    glutMainLoop()


main()
