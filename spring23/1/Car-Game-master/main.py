import os
# try:
#     del os.environ['DISPLAY']
# except:
#     pass
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from maze import *
from car import *
from collision import *
from Healthbar import *
from texture import *
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700
PERIOD = 10
First_Start_Flag = True
Go_Drive_Flag=False
Go_Back_Flag=False
Break_Flag =False
On_button = False
Song_Flag=False
mouse_x, mouse_y = 0, 0
start_game = 0
game_over = 0
credits_sc = 0
you_win = 0
carModel = car()


pygame.init()
sounds=[pygame.mixer.Sound("Sound/crash.wav"), 
        pygame.mixer.Sound("Sound/coin.wav"),
        pygame.mixer.Sound("Sound/revive.wav"),
        pygame.mixer.Sound("Sound/car_horn.wav"),
        pygame.mixer.Sound("Sound/starting_game.wav"),
        pygame.mixer.Sound("Sound/go_driving.wav"),
        pygame.mixer.Sound("Sound/car_reverse.wav"),
        pygame.mixer.Sound("Sound/car_break.wav"),
        pygame.mixer.Sound("Sound/song.wav"),
        pygame.mixer.Sound("Sound/lobby_music.wav"),
        pygame.mixer.Sound("Sound/mouse_point.wav"),
        pygame.mixer.Sound("Sound/car_reverse1.wav"),
        pygame.mixer.Sound("Sound/bomb.wav"),
        pygame.mixer.Sound("Sound/bravo.wav")
        ]
sounds[8].set_volume(0.3)
sounds[10].set_volume(0.5)
sounds[11].set_volume(0.08)

def init_proj():
    glClearColor(0, 0, 0, 0)
    glMatrixMode(GL_PROJECTION)
    glOrtho(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT, 0, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    load_texture()


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    global start_game, game_over,you_win
    # Check if the health become <= 0 , to close play screen and open GameOver
    if carModel.health <= 0:
        start_game = 2 
        game_over = 1
    # If User open credits button , Load credits SCREEN with back button
    if credits_sc == 1:
        # BACk Button
        if mouse_x >= 260 and mouse_x <= 460 and mouse_y >= 700-100 and mouse_y <= 700-20:
            draw_texture(260,20,460,100,BACK_RED)
        else:
            draw_texture(260,20,460,100,BACK_YELLOW)
        draw_texture(0,0,WINDOW_WIDTH,WINDOW_HEIGHT,CREDIT_SCREEN)
    # if We Are in Start screen , load background with 3 buttons
    elif start_game == 0:
        glLoadIdentity()
        # ON START Button
        if mouse_x >= 280 and mouse_x <= 520 and mouse_y >= 280 and mouse_y <= 360:
            draw_texture(280,340,520,420,START_RED)
        else:
            draw_texture(280,340,520,420,START_YELLOW)
        # On CREDITS button
        if mouse_x >= 280 and mouse_x <= 520 and mouse_y >= 380 and mouse_y <= 460:
            draw_texture(280,240,520,320,CREDIT_RED)
        else:
            draw_texture(280,240,520,320,CREDIT_YELLOW)

        # On EXIT button
        if mouse_x >= 280 and mouse_x <= 520 and mouse_y >= 480 and mouse_y <= 560:
            draw_texture(280,140,520,220,EXIT_RED)
        else:
            draw_texture(280,140,520,220,EXIT_YELLOW)
        draw_texture(0,0,WINDOW_WIDTH,WINDOW_HEIGHT,START_SCREEN)
    # If We are is the game play , then run the game 
    elif start_game == 1:
        # First We need to only project a small part from the map , so we use otho projection to do that
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        cen = carModel.center()
        # projection is related to center of car , we need the center of the car to be the center of the screen
        glOrtho(cen[0] - 300, cen[0] + 300, cen[1] - 175, cen[1] + 175, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glClearColor(0.2,0.2,0.2,0)
        # Test if there's a collision between car & Walls
        if test_car_walls(carModel, maze1):
            carModel.collosion = True
            sounds[0].set_volume(0.2)
            sounds[0].play(0)
            sounds[5].stop()
            sounds[6].stop()
        # Test if there's a collision between car & bomb
        if test_car_bomb(carModel, bombs1):
            sounds[12].set_volume(0.5)
            sounds[12].play(0)
            carModel.health -= 50
        # Test if there's a collision between car & coin
        if test_car_coin(carModel, coins1):
            carModel.coins += 1
            sounds[1].play(0)
        # Test if there's a collision between car & health
        if test_car_health(carModel,health1):
            carModel.health = carModel.health + 20 if carModel.health + 20 < 100 else 100
            sounds[2].set_volume(0.2)
            sounds[2].play(0)
        # Test if there's a collision between car & Walls , if true , then load you win screen
        if test_car_finish(carModel,finish):
            sounds[13].set_volume(0.5)
            sounds[13].play(0)
            you_win = 1
            start_game = 4
        # Draw Health Bar & Coins counter
        draw_health(carModel.health, cen)
        glPushMatrix()
        s = "stars : " + str(carModel.coins)
        print_text(s,cen[0]-285,cen[1] + 140)
        glPopMatrix()
        
        # Draw Map & Items that are on the map 
        draw_map()
        draw_coins()
        draw_healthkit()
        draw_bombs()
        draw_finish()

        # Draw Car and perform the animation of the car based on car attributes 
        glPushMatrix()
        carModel.animation()
        carModel.draw()
        glPopMatrix()
    # if game over , then load game over scree 
    elif game_over == 1:
        sounds[8].stop()
        glClearColor(0,0,0,0)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT, 0, 1)
        glMatrixMode(GL_MODELVIEW)
        if mouse_x >= 480 and mouse_x <= 720 and mouse_y >= 700-250 and mouse_y <= 700-150:
            draw_texture(480,150,720,250,TRY_AGAIN_RED)
        else:
            draw_texture(480,150,720,250,TRY_AGAIN_YEL)
        if mouse_x >= 480 and mouse_x <= 720 and mouse_y >= 700-130 and mouse_y <= 700-30:
            draw_texture(480,30,720,130,EXIT2_RED)
        else:
            draw_texture(480,30,720,130,EXIT2_YEL)
        draw_texture(0,0,WINDOW_WIDTH,WINDOW_HEIGHT,PLAY_AGAIN)
    # if you win , then load you win screen
    elif you_win == 1:
        sounds[8].stop()
        glClearColor(0,0,0,0)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT, 0, 1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        if mouse_x >= 480 and mouse_x <= 720 and mouse_y >= 700-130 and mouse_y <= 700-30:
            draw_texture(480,30,720,130,HOME_RED)
        else:
            draw_texture(480,30,720,130,HOME_YEL)
        draw_texture(0,0,WINDOW_WIDTH,WINDOW_HEIGHT,YOU_WIN)


    glutSwapBuffers()

def draw_texture(left,bottom, right,top,tex_iden):
    """
    this function Draw a texture on a rectangle
    """
    glBindTexture(GL_TEXTURE_2D, tex_iden)
    glColor3f(1,1,1)
    glBegin(GL_POLYGON)
    glTexCoord(0,0)
    glVertex2d(left,bottom)
    glTexCoord(1,0)
    glVertex2d(right,bottom)
    glTexCoord(1,1)
    glVertex2d(right,top)
    glTexCoord(0,1)
    glVertex2d(left,top)
    glEnd()
    glBindTexture(GL_TEXTURE_2D, -1)

def Timer(v):
    display()
    glutTimerFunc(PERIOD, Timer, 1)


def print_text(s, x, y):
    """
    this function draw text on the screen
    """
    glLineWidth(2)
    glColor3f(1, 1, 0)
    glTranslate(x, y, 0)
    glScale(0.08, 0.08, 1)
    s = s.encode()
    for char in s:
        glutStrokeCharacter(GLUT_STROKE_MONO_ROMAN, char)


def keyboard(key, x, y):
    global carModel,Go_Drive_Flag,Go_Back_Flag,Break_Flag,Song_Flag
    # if user hit 'w', then we need to make speed to be reaced = 2.5 and dir of car is postive
    if key == b"w":
        carModel.speed = 2.5   # <ws----------------------- This is the edit of speed
        if Go_Drive_Flag == False and start_game == 1:
            sounds[5].set_volume(0.1)
            sounds[5].play(-1)
            Go_Drive_Flag = True
    # if user hit 's', then we need to make speed to be reaced = -2 and 
    if key == b"s":
        carModel.speed = -2
        if Go_Back_Flag==False and start_game == 1:
            sounds[6].set_volume(0.5)
            sounds[6].play(-1)
            sounds[11].play(-1)
            Go_Back_Flag=True
    # Rot is clockwise
    if key == b"d":
        carModel.rot = -1.5  # to make it smooths
    # Rot is anti-clockwise
    if key == b"a":
        carModel.rot = 1.5  # to make it smooth
    # Break key 
    if key == b" ":
        sounds[11].stop()
        sounds[6].stop()
        if carModel.currSpeed==carModel.speed!=0 and Break_Flag==False and start_game == 1:
            sounds[7].play(0)
            Break_Flag==True
        carModel.currSpeed = carModel.currSpeed / 2 
        carModel.speed = 0
        sounds[6].stop()
        sounds[5].stop()
    # Klaxon sound
    if key == b"e" and start_game == 1:
        sounds[3].set_volume(0.2)
        sounds[3].play(0)
    if key ==b'p'and start_game == 1:
        if Song_Flag:
            sounds[8].stop()
            Song_Flag=False
        else:
            Song_Flag=True
            sounds[8].play(0)
    # Exit the game
    if key == b'q':
        os._exit(0)


def keyboardup(key, x, y):
    """
    This function is trace if we left the button or not , if we left it then do some action
    """
    global carModel,Go_Drive_Flag,Go_Back_Flag,Break_Flag
    if key == b"w" or key == b"s":
        carModel.speed = 0
        carModel.dir = 0
        Go_Drive_Flag=False
        Go_Back_Flag=False
        sounds[5].stop()
        sounds[6].stop()
        sounds[11].stop()
    if key == b"d" or key == b"a":
        carModel.rot = 0
    if key == b" ":
        Break_Flag=False

def mousePass(x,y):
    """
    this function Trace the mouse postision on the screen in order to play sound when user hit the button
    """
    global mouse_x,mouse_y, On_button
    mouse_x = x
    mouse_y = y
    # Start
    
    if start_game == 0 and credits_sc == 0 and x >= 280 and x <= 520 and y >= 280 and y <= 360:
        if On_button == False:
            sounds[10].play(0)
            On_button = True
    elif start_game == 0 and credits_sc == 0 and x >= 280 and x <= 520 and y >= 380 and y <= 460 and start_game == 0:
        if On_button == False:
            sounds[10].play(0)
            On_button = True
    elif start_game == 0 and credits_sc == 0 and x >= 280 and x <= 520 and y >= 480 and y <= 560 and start_game == 0:
        if On_button == False:
            sounds[10].play(0)
            On_button = True
    elif credits_sc == 1 and x >= 260 and x <= 460 and y >= 600 and y <= 680:
        if On_button == False:
            sounds[10].play(0)
            On_button = True
    elif game_over == 1 and x >= 480 and x <= 720 and y >= 700-250 and y <= 700-150:
        if On_button == False:
            sounds[10].play(0)
            On_button = True
    elif game_over == 1 and x >= 480 and x <= 720 and y >= 700-130 and y <= 700-30:
        if On_button == False:
            sounds[10].play(0)
            On_button = True
    elif you_win == 1 and x >= 480 and x <= 720 and y >= 700-130 and y <= 700-30:
        if On_button == False:
            sounds[10].play(0)
            On_button = True
    else:
        On_button = False


def mouse(state,key,x,y):
    """
    mouse function is check it user is on a button and click on it or not
    """
    global start_game, credits_sc, carModel,game_over,you_win
    if x >= 280 and x <= 520 and y >= 280 and y <= 360 and key == GLUT_LEFT_BUTTON  and start_game == 0 and credits_sc == 0:
        start_game = 1
        sounds[9].stop()
        sounds[4].set_volume(0.2)
        sounds[4].play(0)
    if x >= 280 and x <= 520 and y >= 380 and y <= 460 and key == GLUT_LEFT_BUTTON  and start_game == 0 and credits_sc == 0:
        credits_sc = 1
    if x >= 280 and x <= 520 and y >= 480 and y <= 560 and  key == GLUT_LEFT_BUTTON and start_game == 0 and credits_sc == 0:
        os._exit(0) 
    if x >= 260 and x <= 460 and y >= 600 and y <= 680 and key ==GLUT_LEFT_BUTTON and credits_sc == 1:
        credits_sc = 0
    # try Again
    if game_over == 1 and x >= 480 and x <= 720 and y >= 700-250 and y <= 700-150 and key ==GLUT_LEFT_BUTTON:
        carModel = car() # Make a new car or reset all param , we choose to create a new car
        # we need to reset all item's in maze
        reset_maze()
        start_game = 1
        game_over = 0
    # exit
    if you_win == 1 and x >= 480 and x <= 720 and y >= 700-130 and y <= 700-30 and key ==GLUT_LEFT_BUTTON:
        carModel = car()
        reset_maze()
        you_win = 0
        start_game = 0
    if game_over == 1 and x >= 480 and x <= 720 and y >= 700-130 and y <= 700-30 and key ==GLUT_LEFT_BUTTON:
        os._exit(0)
        





if __name__ == "__main__":
    sounds[9].set_volume(0.1)
    sounds[9].play(-1)
    glutInit()
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutInitWindowPosition(50, 50)
    glutCreateWindow(b"Maze Adventure")
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA|GLUT_DEPTH)
    glutDisplayFunc(display)
    glutTimerFunc(PERIOD, Timer, 1)
    glutKeyboardFunc(keyboard)
    glutKeyboardUpFunc(keyboardup)
    glutPassiveMotionFunc(mousePass)
    glutMouseFunc(mouse)
    init_proj()
    glutMainLoop()
