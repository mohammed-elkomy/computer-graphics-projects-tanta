import pygame
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import math
import level2


pygame.init()
pygame.mixer.init()
little = pygame.mixer.Sound("sounds/quack.mp3")
passed = pygame.mixer.Sound("sounds/level complete.wav")
game_over = pygame.mixer.Sound("sounds/go.wav")
bg = pygame.mixer.Sound("sounds/levels.mp3")

texture_names = [0, 1, 2, 3, 4, 5, 6, 7, 8]  # must be numbers

# ###################------crocodile variables--------####################
crocodile_rotation = 0
movement_x_direction = 1
movement_y_translation = -4  # y_axis position, = croc_pos[1] initially

# ###################------super duck variables--------####################
duck_rotation = 0
duck_direction = 1

# ###################------little ducks variables--------####################
collided_children_indices = []  # list for the little duck to remove from it when collided by super duck
# steps of the 8 ducks
child_mov = [(0.1, -0.1),
             (-0.1, 0.1),
             (-0.1, -0.1),
             (0.1, 0.1),
             (0.1, -0.1),
             (-0.1, 0.1),
             (-0.1, -0.1),
             (0.1, 0.1)]

# ###################------Initial position for all--------####################
duck_pos = [0, 30]  # initial position for super duck
croc_pos = [10, -4]  # initial position for crocodile
children_pos = [[random.uniform(0, 50), random.uniform(0, 20)],  # matrix for 8 ducks
                [random.uniform(0, 50), random.uniform(0, 20)],
                [random.uniform(0, 50), random.uniform(0, 20)],
                [random.uniform(0, 50), random.uniform(0, 20)],
                [random.uniform(0, 50), random.uniform(0, 20)],
                [random.uniform(0, 50), random.uniform(0, 20)],
                [random.uniform(0, 50), random.uniform(0, 20)],
                [random.uniform(0, 50), random.uniform(0, 20)]]  # initial position for little ducks

# ###################------some needed variables--------####################
score = 0  # track score
switch = 0  # to switch scenes and go to level 2


def texture_setup(texture_image_binary, texture_name, width, height):
    glBindTexture(GL_TEXTURE_2D, texture_name)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_image_binary)


def loadTextures2():
    glEnable(GL_TEXTURE_2D)
    images = []
    images.append(pygame.image.load("textures/superside2.png"))  # 0
    images.append(pygame.image.load("textures/halfcroside.png"))  # 1
    images.append(pygame.image.load("textures/motherside.png"))  # 2
    images.append(pygame.image.load("textures/littleside.png"))  # 3
    images.append(pygame.image.load("textures/wallpaper2.png"))  # 4
    images.append(pygame.image.load("textures/worried mother.png"))  # 5
    images.append(pygame.image.load("textures/gameover.png"))  # 6
    images.append(pygame.image.load("textures/mission_completed.png")),  # 7
    images.append(pygame.image.load("textures/before_rabbits.png"))  # 8

    textures = [pygame.image.tostring(image, "RGBA", True) for image in images]
    glGenTextures(len(images), texture_names)
    for i in range(len(images)):
        texture_setup(textures[i], texture_names[i], images[i].get_width(), images[i].get_height())


def init():
    loadTextures2()
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glClearColor(1, 1, 1, 1)
    glMatrixMode(GL_PROJECTION)
    gluOrtho2D(-10.0, 50.0, -10.0, 50.0)  # lrbt
    glMatrixMode(GL_MODELVIEW)


# ###################------draw objects--------####################
def draw_bg():
    glPushMatrix()
    glBindTexture(GL_TEXTURE_2D, texture_names[4])
    glBegin(GL_QUADS)

    glTexCoord2f(0, 1)
    glVertex2d(-10, 50)

    glTexCoord2f(1, 1)
    glVertex2d(50, 50)

    glTexCoord2f(1, 0)
    glVertex2d(50, -10)

    glTexCoord2f(0, 0)
    glVertex2d(-10, -10)

    glEnd()
    glPopMatrix()


def draw_duck():
    global duck_rotation
    glPushMatrix()
    glBindTexture(GL_TEXTURE_2D, texture_names[0])

    glTranslatef(duck_pos[0], duck_pos[1], 0.0)
    glScalef(0.6, 0.8, 1)
    glRotatef(duck_rotation, 0, 1, 0)

    glBegin(GL_QUADS)

    glTexCoord2f(0, 1)
    glVertex2d(-4, 4)

    glTexCoord2f(1, 1)
    glVertex2d(4, 4)

    glTexCoord2f(1.0, 0)
    glVertex2d(4, -4)

    glTexCoord2f(0, 0)
    glVertex2d(-4, -4)

    glEnd()
    glPopMatrix()


def draw_cro():
    global crocodile_rotation, movement_y_translation
    glPushMatrix()
    glBindTexture(GL_TEXTURE_2D, texture_names[1])

    glTranslatef(croc_pos[0], movement_y_translation, 0)
    glScalef(0.7, 0.4, 1)
    glRotatef(crocodile_rotation, 0, 1, 0)

    glBegin(GL_QUADS)

    glTexCoord2f(0, 1)
    glVertex2f(-8, 2)

    glTexCoord2f(1, 1)
    glVertex2f(8, 2)

    glTexCoord2f(1.0, 0)
    glVertex2f(8, -2)

    glTexCoord2f(0, 0)
    glVertex2f(-8, -2)

    glEnd()
    glPopMatrix()


def draw_worried_duck():  # static
    glPushMatrix()
    glBindTexture(GL_TEXTURE_2D, texture_names[5])

    glTranslatef(20, 30, 0)
    glScalef(2, 2, 1)

    glBegin(GL_QUADS)

    glTexCoord2f(0, 1)
    glVertex2d(-4, 4)

    glTexCoord2f(1, 1)
    glVertex2d(4, 4)

    glTexCoord2f(1.0, 0)
    glVertex2d(4, -4)

    glTexCoord2f(0, 0)
    glVertex2d(-4, -4)

    glEnd()
    glPopMatrix()


def draw_children(child_pos):
    glPushMatrix()
    glBindTexture(GL_TEXTURE_2D, texture_names[3])

    glTranslatef(child_pos[0], child_pos[1], 0.0)
    glScalef(3.5, 3.5, 1)

    glBegin(GL_QUADS)

    glTexCoord2f(0, 1)
    glVertex2d(-0.5, 0.5)

    glTexCoord2f(1, 1)
    glVertex2d(0.5, 0.5)

    glTexCoord2f(1, 0)
    glVertex2d(0.5, -0.5)

    glTexCoord2f(0, 0)
    glVertex2d(-0.5, -0.5)

    glEnd()
    glPopMatrix()


def draw_go():  # game over
    glPushMatrix()
    glBindTexture(GL_TEXTURE_2D, texture_names[6])
    glBegin(GL_QUADS)

    glTexCoord2f(0, 1)
    glVertex2d(-10, 50)

    glTexCoord2f(1, 1)
    glVertex2d(50, 50)

    glTexCoord2f(1, 0)
    glVertex2d(50, -10)

    glTexCoord2f(0, 0)
    glVertex2d(-10, -10)

    glEnd()
    glPopMatrix()


def draw_end():  # successful mission completed
    glPushMatrix()
    glBindTexture(GL_TEXTURE_2D, texture_names[7])
    glBegin(GL_QUADS)

    glTexCoord2f(0, 1)
    glVertex2d(-10, 50)

    glTexCoord2f(1, 1)
    glVertex2d(50, 50)

    glTexCoord2f(1, 0)
    glVertex2d(50, -10)

    glTexCoord2f(0, 0)
    glVertex2d(-10, -10)

    glEnd()
    glPopMatrix()


def draw_ready():  # into next level
    glPushMatrix()
    glBindTexture(GL_TEXTURE_2D, texture_names[8])
    glBegin(GL_QUADS)

    glTexCoord2f(0, 1)
    glVertex2d(-10, 50)

    glTexCoord2f(1, 1)
    glVertex2d(50, 50)

    glTexCoord2f(1, 0)
    glVertex2d(50, -10)

    glTexCoord2f(0, 0)
    glVertex2d(-10, -10)

    glEnd()
    glPopMatrix()


# ###################------move objects--------####################
def move_children():
    for i, child_pos in enumerate(children_pos):  # returns each item's index
        # Move the children
        child_pos[0] += child_mov[i][0]
        child_pos[1] += child_mov[i][1]

        # Check for collision with side walls to reverse direction if needed
        if child_pos[0] < -10 or child_pos[0] > 50:
            child_mov[i] = (-child_mov[i][0], child_mov[i][1])  # Reverse horizontal direction
        if child_pos[1] < -10 or child_pos[1] > 20:
            child_mov[i] = (child_mov[i][0], -child_mov[i][1])  # Reverse vertical direction


def keyboard(key, x, y):  # moving super duck
    global duck_pos, duck_rotation, duck_direction
    if key == b'q':
        sys.exit(0)
    elif key == b'a':  # move left
        duck_pos[0] -= 0.5  # movement step
        if duck_direction == 1:
            duck_rotation += 180
            duck_direction = -1

    elif key == b'd':  # move right
        duck_pos[0] += 0.5
        if duck_direction == -1:
            duck_rotation += 180
            duck_direction = 1

    elif key == b'w':  # move up
        duck_pos[1] += 0.5

    elif key == b's':  # move down
        duck_pos[1] -= 0.5


def timer_cro(value):
    global croc_pos, crocodile_rotation, movement_x_direction, movement_y_translation
    croc_pos[0] += 0.3 * movement_x_direction  # crocodile step

    if croc_pos[0] >= 50:
        crocodile_rotation += 180
        movement_x_direction = -1
        movement_y_translation += 4
        croc_pos[0] = 50

    if croc_pos[0] <= -10:
        crocodile_rotation -= 180  # back to angle = 0
        movement_x_direction = 1
        movement_y_translation += 4
        croc_pos[0] = -10

    if movement_y_translation > 20:  # end of lake
        movement_y_translation = -20  # below the screen

    glutTimerFunc(100, timer_cro, 0)  # 100 ms is the animation speed
    glutPostRedisplay()


# ###################------check collisions--------####################
def collision_detection(pos1, pos2):
    distance_threshold = 3.5  # Adjust as needed
    distance = math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)
    if distance < distance_threshold:
        return True  # detection happened
    return False


# ###################------draw score--------####################
def draw_score():
    glLoadIdentity()
    glColor3f(1, 1, 1)  # White
    glLineWidth(4)
    draw_text(-9, 44, f"Score:{score}")


def draw_text(x, y, text, GLUT_STROKE_ROMAN=None):
    glPushMatrix()
    glTranslatef(x, y, 0)
    glScalef(0.02, 0.02, 0)  # Scale down for better visibility
    for char in text:
        glutStrokeCharacter(GLUT_STROKE_ROMAN, ord(char))
    glPopMatrix()


def update_switch(val):
    global switch
    switch += 1
    return switch


def draw_scene():
    global score, switch
    glClear(GL_COLOR_BUFFER_BIT)

    draw_bg()
    draw_score()
    draw_duck()
    draw_cro()
    draw_worried_duck()

    for child_pos in children_pos:
        draw_children(child_pos)

    # Move children
    move_children()

    # super duck limits of motion
    screen_left = -8
    screen_right = 45
    screen_bottom = -10
    screen_top = 35

    if duck_pos[0] < screen_left:
        duck_pos[0] = screen_left
    elif duck_pos[0] > screen_right:
        duck_pos[0] = screen_right
    elif duck_pos[1] < screen_bottom:
        duck_pos[1] = screen_bottom
    elif duck_pos[1] > screen_top:
        duck_pos[1] = screen_top

    # Check for collisions and remove collided children
    for i, child_pos in enumerate(children_pos):
        if collision_detection(duck_pos, child_pos):
            score += 1
            little.play()
            collided_children_indices.append(i)
            children_pos.pop(i)

        elif collision_detection(croc_pos, child_pos):
            game_over.play()
            draw_go()
            glutTimerFunc(1000, exit, 1)

    if collision_detection(duck_pos, croc_pos):
        duck_pos[0] = 0
        duck_pos[1] = 30
        score -= 1

    if score >= 3 and switch == 0:
        glLoadIdentity()
        passed.play()
        draw_end()
        glutTimerFunc(1000, update_switch, 0)

    elif switch == 1:
        glLoadIdentity()
        draw_ready()
        glutTimerFunc(2000, update_switch, 0)

    elif switch == 2:
        update_switch(switch)
        level2.main()

    glutSwapBuffers()


def main():
    glutDisplayFunc(draw_scene)
    glutKeyboardFunc(keyboard)
    init()
    glutTimerFunc(100, timer_cro, 0)
    bg.play()
    glutMainLoop()
