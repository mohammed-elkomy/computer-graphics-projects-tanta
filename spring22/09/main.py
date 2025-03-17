from pathlib import Path

from pygame import mixer, image
from classes import *

cur_path = str(Path(__file__).parent.resolve())
PERIOD = 10
# ######## to control the game ######################################################################
GAME_STATES = ["welcome", "main", "over"]
STATE_SEQUENCE = cycle([1, 2, 0])   # sequence in which game states flow.
STATE_INDEX = 0   # pointer to the game state.
######################################################################
DISTANCE = SCREENWIDTH / 2
SCORE = 0
BP_SPEED = -3
# ######## bird's control ##########################################################################
ANGULAR_SPEED = 3
# control bird jump.
JUMP_VELOCITY = 5
GRAVITY = -0.22
########################################################################

pipes = []      # contains all displayed pipes on the screen
global bird, base

TEXTURES = {}   # at the start of game, all textures will be created once time and saved in it.

# ####################### Sounds ####################################################################
SOUNDS = {}
SOUNDEXT = ".ogg"
mixer.init()

SOUNDS["die"] = mixer.Sound(cur_path + "/assets/audio/die" + SOUNDEXT)
SOUNDS["jump"] = mixer.Sound(cur_path + "/assets/audio/jump" + SOUNDEXT)
SOUNDS["point"] = mixer.Sound(cur_path + "/assets/audio/point" + SOUNDEXT)

# ## list of images Addresses on my computer for the bird wings ####################################
PLAYERS_LIST = (
        cur_path + '/assets/sprites/up.png',
        cur_path + '/assets/sprites/mid.png',
        cur_path + '/assets/sprites/down.png')
####################################################################################################


def init():
    glClearColor(1, 1, 1, 0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    # creating textures and saving them as dictionary in TEXTURES{} variable.
    init_texture()
    
    init_objects()

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, SCREENWIDTH, 0, SCREENHEIGHT, -3, 3)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def init_texture():
    # ################### Pipe Textures ###########################################################
    img_pipe_load = image.load(cur_path + '/assets/sprites/pipe-green.png')
    width = img_pipe_load.get_width()
    height = img_pipe_load.get_height()
    img_pipe = [
        image.tostring(img_pipe_load, "RGBA", True),     # lower image
        image.tostring(img_pipe_load, "RGBA", False)]    # upper image "image is reflected".

    # creating 2 textures for pipes
    tex = glGenTextures(2)
    # adjust texture and uploading its image
    for i in [0, 1]:
        glBindTexture(GL_TEXTURE_2D, tex[i])
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        gluBuild2DMipmaps(GL_TEXTURE_2D, 4, width, height, GL_RGBA, GL_UNSIGNED_BYTE, img_pipe[i])

    TEXTURES["pipe"] = tex
    # ################### Bird Textures ############################################################
    img_bird_load = [image.load(Address) for Address in PLAYERS_LIST]
    width = [img.get_width() for img in img_bird_load]
    height = [img.get_height() for img in img_bird_load]
    img_bird = [image.tostring(img, "RGBA", True) for img in img_bird_load]

    # creating 3 textures for bird
    tex = glGenTextures(3)
    # adjust texture and uploading its image
    for i in [0, 1, 2]:
        glBindTexture(GL_TEXTURE_2D, tex[i])
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        gluBuild2DMipmaps(GL_TEXTURE_2D, 4, width[i], height[i], GL_RGBA, GL_UNSIGNED_BYTE, img_bird[i])

    TEXTURES["bird"] = tex
    # ################### Background Texture ############################################################
    img_backG_load = image.load(cur_path + '/assets/sprites/background-day.png')
    width = img_backG_load.get_width()
    height = img_backG_load.get_height()
    img_backG = image.tostring(img_backG_load, "RGBA", True)

    # creating 1 texture for BackG
    tex = glGenTextures(1)
    # adjust texture and uploading its image
    glBindTexture(GL_TEXTURE_2D, tex)
    glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
    glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    gluBuild2DMipmaps(GL_TEXTURE_2D, 4, width, height, GL_RGBA, GL_UNSIGNED_BYTE, img_backG)

    TEXTURES["BackG"] = tex
    # ################### numbers Textures ############################################################
    img_num_load = [image.load(cur_path + f'/assets/sprites/{i}.png') for i in range(10)]
    width = [img.get_width() for img in img_num_load]
    height = [img.get_height() for img in img_num_load]
    img_num = [image.tostring(img, "RGBA", True) for img in img_num_load]

    # creating 10 textures for numbers
    tex = glGenTextures(10)
    # adjust texture and uploading its image
    for i in range(10):
        glBindTexture(GL_TEXTURE_2D, tex[i])
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        gluBuild2DMipmaps(GL_TEXTURE_2D, 4, width[i], height[i], GL_RGBA, GL_UNSIGNED_BYTE, img_num[i])

    TEXTURES["numbers"] = {f'{i}': tex[i] for i in range(10)}
    # ################### base Texture ############################################################
    img_base_load = image.load(cur_path + '/assets/sprites/base.png')
    width = img_base_load.get_width()
    height = img_base_load.get_height()
    img_base = image.tostring(img_base_load, "RGBA", True)

    # creating 1 texture
    tex = glGenTextures(1)
    # adjust texture and uploading its image
    glBindTexture(GL_TEXTURE_2D, tex)
    glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
    glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    gluBuild2DMipmaps(GL_TEXTURE_2D, 4, width, height, GL_RGBA, GL_UNSIGNED_BYTE, img_base)

    TEXTURES["base"] = tex
    # ################### message Texture ############################################################
    img_msg_load = image.load(cur_path + '/assets/sprites/message.png')
    width = img_msg_load.get_width()
    height = img_msg_load.get_height()
    img_msg = image.tostring(img_msg_load, "RGBA", True)

    # creating 1 texture
    tex = glGenTextures(1)
    # adjust texture and uploading its image
    glBindTexture(GL_TEXTURE_2D, tex)
    glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    gluBuild2DMipmaps(GL_TEXTURE_2D, 4, width, height, GL_RGBA, GL_UNSIGNED_BYTE, img_msg)
    # glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_msg)

    TEXTURES["msg"] = tex
    # ################### game over Texture ############################################################
    img_gameO_load = image.load(cur_path + '/assets/sprites/gameover.png')
    width = img_gameO_load.get_width()
    height = img_gameO_load.get_height()
    img_gameO = image.tostring(img_gameO_load, "RGBA", True)

    # creating 1 texture
    tex = glGenTextures(1)
    # adjust texture and uploading its image
    glBindTexture(GL_TEXTURE_2D, tex)
    glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
    glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    gluBuild2DMipmaps(GL_TEXTURE_2D, 4, width, height, GL_RGBA, GL_UNSIGNED_BYTE, img_gameO)

    TEXTURES["game over"] = tex
    # ################### start Texture ############################################################
    img_msg_load = image.load(cur_path + '/assets/sprites/start.png')
    width = img_msg_load.get_width()
    height = img_msg_load.get_height()
    img_msg = image.tostring(img_msg_load, "RGBA", True)
    # creating 1 texture
    tex = glGenTextures(1)
    # adjust texture and uploading its image
    glBindTexture(GL_TEXTURE_2D, tex)
    glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    gluBuild2DMipmaps(GL_TEXTURE_2D, 4, width, height, GL_RGBA, GL_UNSIGNED_BYTE, img_msg)

    TEXTURES["start"] = tex
    # ################### restart Texture ############################################################
    img_msg_load = image.load(cur_path + '/assets/sprites/res.png')
    width = img_msg_load.get_width()
    height = img_msg_load.get_height()
    img_msg = image.tostring(img_msg_load, "RGBA", True)
    # creating 1 texture
    tex = glGenTextures(1)
    # adjust texture and uploading its image
    glBindTexture(GL_TEXTURE_2D, tex)
    glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    gluBuild2DMipmaps(GL_TEXTURE_2D, 4, width, height, GL_RGBA, GL_UNSIGNED_BYTE, img_msg)

    TEXTURES["restart"] = tex


def init_objects():
    global bird, base
    pipes.append(Pipe(TEXTURES["pipe"]))
    bird = Bird(TEXTURES["bird"], GRAVITY, ANGULAR_SPEED)
    base = Base(TEXTURES["base"], 0.1)


def timer(t):
    display()
    glutTimerFunc(PERIOD, timer, 1)


def keyboard(key, a, b):
    global bird, pipes, STATE_INDEX, SCORE
    if key == b" ":
        if STATE_INDEX == 1:    # state is MAIN GAME, hence make the bird jump.
            SOUNDS["jump"].play()
            bird.velocity = JUMP_VELOCITY   # make bird go up

        elif STATE_INDEX == 0:  # state is WELCOME.
            SOUNDS["jump"].play()
            bird.reset()
            bird.velocity = JUMP_VELOCITY   # make bird go up
            STATE_INDEX = next(STATE_SEQUENCE)

        elif STATE_INDEX == 2:  # state is GAME OVER.
            pipes = [Pipe(TEXTURES["pipe"])]
            bird.reset()
            SCORE = 0
            STATE_INDEX = next(STATE_SEQUENCE)

    if key == b"q":
        glutDestroyWindow(window)


# ############################### game states ########################################################
def welcome():
    show_welcome()
    bird.fly()


def main_game():
    global STATE_INDEX, SCORE

    base.move(BP_SPEED)
    for pipe in pipes:
        pipe.move(BP_SPEED)
        pipe.draw()
    update_pipes()

    update_score()
    show_score(str(SCORE))

    bird.move()
    if check_crash():
        STATE_INDEX = next(STATE_SEQUENCE)


def game_over():
    for pipe in pipes:
        pipe.draw()
    bird.die()
    show_score(str(SCORE))
    show_game_over()


# #################### assistant functions ##################################
def check_crash():
    pipe = pipes[0]
    # crash with the pipe
    if bird.right > pipe.left and bird.left < pipe.right:
        if bird.bottom < pipe.lower_y or bird.top > pipe.upper_y:
            SOUNDS["die"].play()
            return True

    # crash with the ground
    if bird.bottom <= BASEY:
        SOUNDS["die"].play()
        return True

    return False


def update_pipes():
    if pipes[0].right < 0:
        pipes.pop(0)
    if pipes[-1].left <= DISTANCE:
        pipes.append(Pipe(TEXTURES["pipe"]))


def update_score():
    global SCORE
    pipe = pipes[0]
    # increase score if bird crossed the pipe's centre
    if not pipe.count and pipe.right - (pipe.width / 2) <= bird.right:
        SCORE += 1
        SOUNDS["point"].play()
        pipe.count = True


def show_score(score):
    """
    take score as a string and display it.
    """
    width = 40
    height = width * 1.5

    glPushMatrix()
    glTranslate(-(len(score) / 2 + 1) * width, 0, 0)    # centre the text.
    for n in score:
        glTranslate(width, 0, 0)    # to show numbers beside each other one, not over.
        draw_rectangle_with_tex(0.5 * SCREENWIDTH, 0.5 * SCREENWIDTH + width,
                                0.85 * SCREENHEIGHT, 0.85 * SCREENHEIGHT + height,
                                TEXTURES["numbers"][n], 0.5)
    glPopMatrix()


def set_background():
    draw_rectangle_with_tex(0, SCREENWIDTH, 0, SCREENHEIGHT + 5, TEXTURES["BackG"], -1)


def show_game_over():
    draw_rectangle_with_tex(100, 500, 400, 600, TEXTURES["game over"], 0.5)
    draw_rectangle_with_tex(0, SCREENWIDTH, 0, BASEY + 200, TEXTURES["restart"], 0.9)


def show_welcome():
    draw_rectangle_with_tex(50, 550, 420, 720, TEXTURES["msg"], 0.5)
    draw_rectangle_with_tex(0, SCREENWIDTH, 0, BASEY + 200, TEXTURES["start"], 0.2)

######################################################################################################


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    set_background()
    base.draw()

    if GAME_STATES[STATE_INDEX] == "welcome":
        welcome()
    elif GAME_STATES[STATE_INDEX] == "main":
        main_game()
    elif GAME_STATES[STATE_INDEX] == "over":
        game_over()

    glutSwapBuffers()


def main():
    global window
    glutInit()
    glutInitWindowPosition(10, 10)
    glutInitWindowSize(SCREENWIDTH, SCREENHEIGHT)
    glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
    window = glutCreateWindow(b"Flappy Bird")

    glutDisplayFunc(display)
    glutTimerFunc(PERIOD, timer, 1)
    glutKeyboardFunc(keyboard)
    glutSetKeyRepeat(GLUT_KEY_REPEAT_OFF)
    init()
    glutMainLoop()


if __name__ == "__main__":
    main()
