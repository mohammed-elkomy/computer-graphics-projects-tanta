from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from cube import Cube
from image_to_array import*
from texture import Texture
from pygame import mixer
from camera import Camera
from coins import *
from monster import *
from player import *
from collision import *

cam = Camera()
# Size of cubes used to create wall segments.
cubesize = 2
map = []
MILLISECONDS = 5

def initGL(Width, Height):
    glClearColor(0.0, 0.1, 0.26, 0.0)
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(90, float(Width) / float(Height), 0.1, 100)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


monsters = [Monster(9, 2, 90),Monster(2, 5, 0),Monster(14, 3, -180),Monster(16, 2, 90),Monster( 18, 16, 5),       
            Monster(20, 18, 90),Monster(15, 18, -90),Monster(12, 18, -90),Monster(6, 16, 5)]

coins = [Coin(1, -.1, 2),Coin(4, -0.1, 6),Coin(4, -0.1, 2),Coin(10, -0.1, 5),Coin(14, -0.1, 5),
        Coin(12, -0.1, 6),Coin(18, -0.1, 5),Coin(18, -0.1, 8),Coin(18, -0.1, 10),Coin(18, - 0.1, 12),
        Coin(18, -0.1, 18),Coin(14, -0.1, 18),Coin(10, -0.1, 16),Coin(10, -0.1, 14),Coin(8, -0.1, 14), 
        Coin(2, -0.1, 18),Coin(2, -0.1, 16),Coin(2, -0.1, 14),Coin(2, -0.1, 12)]


def drawScene():
    global  cam, coins_result
    locations = []
    cam.setup_camera()
    cube = Cube()
    
    coins_result = check_collisions(cam, coins, monsters, cam.grenades)
    # Draw monsters
    for monster in monsters:
        monster.set_monster()
    # Draw Coins
    for coin in coins:
        coin.set_coin()
        draw_text_3d_wrapper("Collected coins : " + str(coins_result), -0.9, .8)
    # Draw Player
    player(cam)
# ============================================================================

    # Build the maze like a printer; back to front, left to right.
    row_count = 0
    column_count = 0

    wall_x = 0.0
    wall_z = 0.0

    for i in map:
        wall_z = (row_count * (cubesize * 1))
        for j in i:
            # 1 = wall, 0 = floor.
            if (j == 1):
                glPushMatrix()
                cube.drawcube(2, 1.0)
                wall_x = (column_count * (cubesize * 1))
                locations.append([wall_x, wall_z])
                glPopMatrix()
            else:
                glPushMatrix()
                glTranslate(0, -1, 0)
                glScale(1, 0.1, 1)
                # this number controls the direction of the texture --> -1
                cube.drawcube(1, -1.0)
                glPopMatrix()
            # Move from left to right one cube size.
            glTranslatef(cubesize, 0.0, 0.0)
            column_count += 1

        # Reset position before starting next row, while moving
        # one cube size towards the camera.
        glTranslatef(((cubesize * column_count) * -1), 0.0, cubesize)

        row_count += 1
        # Reset the column count; this is a new row.
        column_count = 0
        cam.locations = locations

    glutSwapBuffers()
# ============================================================================


def draw_win_or_lose():

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    if cam.flag == "play":
        drawScene()

    elif cam.flag == "lose":

        glTranslate(0, 0, -2)
        glBindTexture(GL_TEXTURE_2D, 20)
        glBegin(GL_POLYGON)
        glTexCoord2f(0, 0)
        glVertex2d(-2, -2)
        glTexCoord2f(1, 0)
        glVertex2d(2, -2)
        glTexCoord2f(1, 1)
        glVertex2d(2, 2)
        glTexCoord2f(0, 1)
        glVertex2d(-2, 2)
        glEnd()
        glutSwapBuffers()

    elif cam.flag == "win":

        glTranslate(0, 0, -2)
        glBindTexture(GL_TEXTURE_2D, 19)
        glBegin(GL_POLYGON)
        glTexCoord2f(0, 0)
        glVertex2d(-2, -2)
        glTexCoord2f(1, 0)
        glVertex2d(2, -2)
        glTexCoord2f(1, 1)
        glVertex2d(2, 2)
        glTexCoord2f(0, 1)
        glVertex2d(-2, 2)
        glEnd()
        glutSwapBuffers()

    elif cam.flag == "start":

        glTranslate(0, 0, -2)
        glBindTexture(GL_TEXTURE_2D, 21)
        glBegin(GL_POLYGON)
        glTexCoord2f(0, 0)
        glVertex2d(-2, -2)
        glTexCoord2f(1, 0)
        glVertex2d(2, -2)
        glTexCoord2f(1, 1)
        glVertex2d(2, 2)
        glTexCoord2f(0, 1)
        glVertex2d(-2, 2)
        glEnd()

        glutSwapBuffers()
#################################################################################
def anim_timer(v):
    draw_win_or_lose()
    glutTimerFunc(MILLISECONDS,anim_timer,1)
    
def main():

    global map, cam
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(1000, 1000)
    glutInitWindowPosition(0, 0)
    glutCreateWindow(b'Experimental Maze')
    # Generate map.
    generator = image_to_array()
    map = generator.generateMap("textures/maze_12.png")
    
    glutDisplayFunc(draw_win_or_lose)
    glutTimerFunc(MILLISECONDS, anim_timer,1)
    Texture().load_textures()
    initGL(15, 15)

    glutPassiveMotionFunc(cam.mouse_look_clb)
    glutKeyboardFunc(cam.keyboard)
    glutKeyboardUpFunc(cam.throw)

    glutSetCursor(GLUT_CURSOR_NONE)  # the pointer disappears
    glutMouseFunc(cam.activeMouse)

    mixer.init()
    mixer.music.set_volume(0.4)
    mixer.music.load('sounds/background2.ogg')
    mixer.music.play(-1)
    glutMainLoop()

if __name__ == "__main__":

    main()
