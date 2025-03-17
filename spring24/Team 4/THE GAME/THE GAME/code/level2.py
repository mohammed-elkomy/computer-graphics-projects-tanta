import math
import random
import pygame
import pygame.time
from OpenGL.GL import *
from OpenGL.GLUT import *

pygame.init()
pygame.mixer.init()
game_over2 = pygame.mixer.Sound("sounds/go2.wav")
bonus = pygame.mixer.Sound("sounds/gift.wav")
saving = pygame.mixer.Sound("sounds/rabbit.wav")
trees = pygame.mixer.Sound("sounds/tree.wav")
stones = pygame.mixer.Sound("sounds/rock.mp3")
enemy = pygame.mixer.Sound("sounds/roar.wav")


texture_names = [i for i in range(0, 88)]  # 9 + 54 + 24 = 87

# ###################------load frames--------####################
bird_images = [pygame.image.load(os.path.join('', f'bird/frame ({i}).png')) for i in range(1, 55)]  # 54 frame from 9:62
fox_images = [pygame.image.load(os.path.join('', f'fox/frame_{i}_delay-0.06s.png')) for i in range(0, 24)]  # 24 frame from 63:87


# ###################------Initial position for all--------####################
duck_pos = [25, 25]  # initial
trees_pos = [[0, 19], [40, 20], [30, 10], [22, 20], [0, 0], [15, 0]]  # fixed
gift_pos = [-20, -20]
child_pos = [0, 0]
rock_pos = [0, 0]
light_pos = [-20, -20]

# ###################------super duck variables--------####################
duck_rotation = 0
duck_direction = 1  # right
collided_children_indices = []

# ###################------bird variables--------####################
current_bird_frame = 9  # first bird frame
bird_x_position = -10

# ###################------fox variables--------####################
current_fox_frame = 63  # first fox frame
fox_x_position = -10
fox_y_pos = 0
fox_rotation = 0
movement_direction = 1

# ###################------some needed variables--------####################
rocks = []  # List to store rock positions
prev_bird_xpos = -10.0  # to track the x bird position for generating fallen stones
length = 3  # track health
is_drawn = False  # check if there is a child drawn on the screen
score = 0  # track score
gift = 1  # condition to draw added health as a gift


def init():
    loadTextures()
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glClearColor(1, 1, 1, 1)
    glMatrixMode(GL_MODELVIEW)


def texture_setup(texture_image_binary, texture_name, width, height):
    glBindTexture(GL_TEXTURE_2D, texture_name)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_image_binary)


def loadTextures():
    glEnable(GL_TEXTURE_2D)
    images = [pygame.image.load("textures/superside.png"), pygame.image.load("textures/rabbit.png"),
              pygame.image.load("textures/land.png"), pygame.image.load("textures/game_over.jpeg"),
              pygame.image.load("textures/health.png"), pygame.image.load("textures/tree.png"),
              pygame.image.load("textures/Squirrel.png"), pygame.image.load("textures/light shelter.png"),
              pygame.image.load("textures/rock.png")]

    images = images + bird_images + fox_images

    textures = [pygame.image.tostring(image, "RGBA", True) for image in images]

    for i in range(len(images)):
        texture_setup(textures[i], texture_names[i], images[i].get_width(), images[i].get_height())


# ###################------draw objects--------####################
def draw_bg():
    glPushMatrix()
    glBindTexture(GL_TEXTURE_2D, texture_names[2])
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
    glScalef(0.5, 0.7, 1)
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


def draw_gift():
    glPushMatrix()
    glBindTexture(GL_TEXTURE_2D, texture_names[4])

    glTranslatef(gift_pos[0], gift_pos[1], 0)
    glScalef(1.5, 1.5, 1)

    glBegin(GL_QUADS)

    glTexCoord2f(0, 1)
    glVertex2d(-1, 1)

    glTexCoord2f(1, 1)
    glVertex2d(1, 1)

    glTexCoord2f(1, 0)
    glVertex2d(1, -1)

    glTexCoord2f(0, 0)
    glVertex2d(-1, -1)

    glEnd()
    glPopMatrix()


def draw_light(pos):
    glPushMatrix()
    glBindTexture(GL_TEXTURE_2D, texture_names[7])

    glTranslatef(pos[0], pos[1], 0)
    glScalef(0.5, 3.1, 1)

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


def draw_health():
    global length  # 3
    x = 0
    for i in range(length):
        glPushMatrix()
        glBindTexture(GL_TEXTURE_2D, texture_names[4])
        glTranslatef(x + 40, 45, 0)
        glScalef(1.5, 1.5, 1)

        glBegin(GL_QUADS)

        glTexCoord2f(0, 1)
        glVertex2d(-1, 1)

        glTexCoord2f(1, 1)
        glVertex2d(1, 1)

        glTexCoord2f(1, 0)
        glVertex2d(1, -1)

        glTexCoord2f(0, 0)
        glVertex2d(-1, -1)

        glEnd()
        glPopMatrix()
        x += 3


def draw_tree(tree_pos):
    glPushMatrix()
    glBindTexture(GL_TEXTURE_2D, texture_names[5])

    glTranslatef(tree_pos[0], tree_pos[1], 0)
    glScalef(0.5, 0.5, 1)

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


def draw_children(child_pos, id):
    glPushMatrix()
    glBindTexture(GL_TEXTURE_2D, texture_names[id])
    glTranslatef(child_pos[0], child_pos[1], 0)
    glScalef(2.5, 4, 1)
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


def generate_fallen_rock():
    glPushMatrix()
    glBindTexture(GL_TEXTURE_2D, texture_names[8])
    glTranslatef(rock_pos[0], rock_pos[1], 1)
    glScalef(0.5, 0.5, 1)

    glBegin(GL_QUADS)

    glTexCoord2f(0, 1)
    glVertex2d(-1, 1)

    glTexCoord2f(1, 1)
    glVertex2d(1, 1)

    glTexCoord2f(1, 0)
    glVertex2d(1, -1)

    glTexCoord2f(0, 0)
    glVertex2d(-1, -1)

    glEnd()
    glPopMatrix()


def draw_go():
    glClearColor(1, 1, 1, 1)
    glClear(GL_COLOR_BUFFER_BIT)

    glPushMatrix()
    glBindTexture(GL_TEXTURE_2D, texture_names[3])
    glScalef(0.99, 0.99, 1)

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


# ###################------draw and move flying bird --------####################
def draw_bird():
    glBindTexture(GL_TEXTURE_2D, texture_names[current_bird_frame])
    glPushMatrix()
    glTranslatef(bird_x_position, 45, 0)
    glScalef(4, 5.5, 1)

    glBegin(GL_QUADS)
    glTexCoord2f(0, 1)
    glVertex2d(-1, 1)
    glTexCoord2f(1, 1)
    glVertex2d(1, 1)
    glTexCoord2f(1, 0)
    glVertex2d(1, -1)
    glTexCoord2f(0, 0)
    glVertex2d(-1, -1)
    glEnd()

    glPopMatrix()


def timer_bird(value):
    glutPostRedisplay()  # Trigger a redraw
    glutTimerFunc(50, timer_bird, 0)  # Schedule the next redraw in 50 milliseconds

    # Update the current frame and bird position
    global current_bird_frame, bird_x_position
    if current_bird_frame + 1 < 63:  # 62: last frame of bird
        current_bird_frame += 1
    else:
        current_bird_frame = 9  # restart

    if bird_x_position > 50:
        glutTimerFunc(3000, update_x_bird, 0)

    bird_x_position += 0.3


def update_x_bird(val):
    global bird_x_position
    bird_x_position = -15


# ###################------draw and move walking fox --------####################
def draw_fox():
    glBindTexture(GL_TEXTURE_2D, texture_names[current_fox_frame])
    glPushMatrix()
    glTranslatef(fox_x_position, fox_y_pos, 0)
    glScalef(4, 5.5, 1)
    glRotatef(fox_rotation, 0, 1, 0)

    glBegin(GL_QUADS)
    glTexCoord2f(0, 1)
    glVertex2d(-1, 1)
    glTexCoord2f(1, 1)
    glVertex2d(1, 1)
    glTexCoord2f(1, 0)
    glVertex2d(1, -1)
    glTexCoord2f(0, 0)
    glVertex2d(-1, -1)
    glEnd()

    glPopMatrix()


def timer_fox(value):
    glutPostRedisplay()  # redraw
    glutTimerFunc(50, timer_fox, 0)  # next redraw after 50 ms

    # Update the current frame and fox position if needed
    global current_fox_frame, fox_x_position, fox_rotation, movement_direction, fox_y_pos
    if current_fox_frame + 1 < 87:
        current_fox_frame += 1
    else:
        current_fox_frame = 63  # restart

    # Update fox position based on movement direction
    fox_x_position += 0.3 * movement_direction

    # Check if fox_x_position reaches boundaries
    if fox_x_position >= 80:
        fox_rotation += 180
        movement_direction = -1
        fox_x_position = 50
        fox_y_pos += 4

    elif fox_x_position <= -30:
        fox_rotation -= 180  # back to angle = 0
        movement_direction = 1
        fox_x_position = -10
        fox_y_pos += 4

    if fox_y_pos > 25:
        fox_y_pos = -20


# ###################------check collisions--------####################
def collision_detection(pos1, pos2):
    distance_threshold = 3
    distance = math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)
    if distance < distance_threshold:
        return True
    return False


# ###################------draw score--------####################
def draw_score():
    glLoadIdentity()
    glColor3f(1, 1, 1)
    glLineWidth(5)
    draw_text(-8, 45, f"Score: {score}")


def draw_text(x, y, text, GLUT_STROKE_ROMAN=None):
    glPushMatrix()
    glTranslatef(x, y, 0)
    glScalef(0.02, 0.02, 0)  # Scale down for better visibility
    for char in text:
        glutStrokeCharacter(GLUT_STROKE_ROMAN, ord(char))
    glPopMatrix()


# ###################------needed functions--------####################
def check_duckHealth():
    global length
    length -= 1
    if length < 1:
        game_over2.play()
        draw_go()
        glutTimerFunc(1000, exit, 1)
    else:
        duck_pos[0] = 5
        duck_pos[1] = 20


def random_gift_pos(val):
    global gift_pos
    gift_pos = [random.uniform(0, 40), random.uniform(-5, 25)]


def stop_light(val):
    global light_pos
    light_pos = [-20, -20]  # outside screen


def random_child(id):
    global is_drawn
    if not is_drawn:
        child_pos[0] = random.uniform(0, 50)
        child_pos[1] = random.uniform(0, 25)
        is_drawn = True
    draw_children(child_pos, id)


def spawn_rock():
    rock_pos = [bird_x_position, 45 - 2]  # Spawn rock slightly below bird
    rocks.append(rock_pos)


# ###################------main scene--------####################
def draw_scene():
    global length, rock_pos, is_drawn, score, gift, light_pos, prev_bird_xpos, gift_pos
    glClear(GL_COLOR_BUFFER_BIT)

    draw_bg()
    draw_score()
    draw_duck()
    draw_health()
    draw_bird()
    draw_fox()
    draw_light(light_pos)
    random_child(1)

    if abs(bird_x_position - prev_bird_xpos) > 5:  # random.uniform(5,10):
        spawn_rock()
        prev_bird_xpos = bird_x_position

    for rock_pos in rocks:
        generate_fallen_rock()
        rock_pos[1] -= 0.5 + random.random()

        if collision_detection(rock_pos, light_pos):
            rocks.remove(rock_pos)  # Remove the rock from the list
            break

    for tree_pos in trees_pos:
        draw_tree(tree_pos)

    # duck limits of motion
    screen_left = -8
    screen_right = 49
    screen_bottom = -10
    screen_top = 27

    if duck_pos[0] < screen_left:
        duck_pos[0] = screen_left
    elif duck_pos[0] > screen_right:
        duck_pos[0] = screen_right
    elif duck_pos[1] < screen_bottom:
        duck_pos[1] = screen_bottom
    elif duck_pos[1] > screen_top:
        duck_pos[1] = screen_top

    if collision_detection(duck_pos, child_pos):
        saving.play()
        score += 1
        is_drawn = False
    random_child(1)

    if collision_detection(child_pos, [fox_x_position, fox_y_pos]):
        enemy.play()
        score -= 1
        is_drawn = False
    random_child(1)

    for i, rock in enumerate(rocks):
        if collision_detection(child_pos, rock):
            stones.play()
            score -= 1
            is_drawn = False
    random_child(1)

    for i, rock in enumerate(rocks):
        if collision_detection(duck_pos, rock):
            stones.play()
            check_duckHealth()
    draw_health()

    for i, tree in enumerate(trees_pos):
        if collision_detection(duck_pos, tree):
            trees.play()
            check_duckHealth()
    draw_health()

    if collision_detection(duck_pos, [fox_x_position, fox_y_pos]):
        enemy.play()
        check_duckHealth()
    draw_health()

    if score > 1 and length < 3 and gift == 1:
        glutTimerFunc(6000, random_gift_pos, 0)
        draw_gift()
        gift = 0  # stop drawing now

    if collision_detection(duck_pos, gift_pos):
        bonus.play()
        gift_pos = [-20, -20]  # outside screen
        gift = 1  # now you can create new gifts if the other two conditions are true
        length += 1
    draw_gift()
    draw_health()

    glutSwapBuffers()


def keyboard(key, x, y):
    global duck_pos, duck_rotation, duck_direction, light_pos, gift_pos

    if key == b'q':
        sys.exit(0)
    elif key == b'a':
        duck_pos[0] -= 0.5
        if duck_direction == 1:
            duck_rotation += 180
            duck_direction = -1
    elif key == b'd':
        duck_pos[0] += 0.5
        if duck_direction == -1:
            duck_rotation += 180
            duck_direction = 1
    elif key == b'w':
        duck_pos[1] += 0.5
    elif key == b's':
        duck_pos[1] -= 0.5

    elif key == b'l':
        light_pos = duck_pos
        glutTimerFunc(7000, stop_light, 0)


def main():
    init()
    glutDisplayFunc(draw_scene)
    glutKeyboardFunc(keyboard)
    glutTimerFunc(50, timer_bird, 0)
    glutTimerFunc(50, timer_fox, 0)
    glutMainLoop()
