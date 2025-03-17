from OpenGL.GL import *
from OpenGL.GLUT import *
import functions
import classes
import math


class Game:
    def __init__(self):
        self.textures = None
        self.current_scene = 'INTRO_SCENE'
        self.score = 0
        self.enemyScore = 0
        self.counter2 = 0
        self.counter1 = 0
        self.counter3 = 0
        self.interval = 10
        self.myBarrier = classes.barrier()
        self.myTank = classes.Tank()
        self.enemyTanks = classes.Tank(x=880, y=250, color=(0.8, 0.2, 0.2), cannon_angle=180.0)
        self.enemyTanks2 = classes.Tank(x=480, y=-50, color=(0.8, 0.2, 0.2), cannon_angle=-90.0)
        self.enemyTanks3 = classes.Tank(x=400, y=600, color=(0.8, 0.2, 0.2), cannon_angle=90.0)
        self.WINDOW_WIDTH = 800
        self.WINDOW_HEIGHT = 500
        self.check_flow = False
        self.level = 0
        self.function_called = True

    def init(self):
        glClearColor(1.0, 1.0, 1.0, 0.0)
        glMatrixMode(GL_PROJECTION)
        glOrtho(0, self.WINDOW_WIDTH, 0, self.WINDOW_HEIGHT, 0, 1)
        glMatrixMode(GL_MODELVIEW)
        self.load_textures()
        glEnable(GL_TEXTURE_2D)

    def load_textures(self):
        texture_name = [0, 1, 2, 3]
        self.textures = [
            functions.loadTexture("images/test_2.jpg", texture_name[0]),
            functions.loadTexture("images/about_test_2.jpg", texture_name[1]),
            functions.loadTexture("images/beige.jpg", texture_name[2]),
            functions.loadTexture("images/tryagain.jpg", texture_name[3])
        ]

    def adjust_background(self, texture_number):
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()
        glBindTexture(GL_TEXTURE_2D, self.textures[texture_number])

        glBegin(GL_QUADS)
        glTexCoord2f(0, 0)
        glVertex2f(0, 0)

        glTexCoord2f(1, 0)
        glVertex2f(self.WINDOW_WIDTH, 0)

        glTexCoord2f(1, 1)
        glVertex2f(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)

        glTexCoord2f(0, 1)
        glVertex2f(0, self.WINDOW_HEIGHT)
        glEnd()

    def Timer(self, value):
        self.draw()
        glutTimerFunc(self.interval, self.Timer, 0)

    def update_main_scene(self):

        self.enemyTanks.set_cannon_angle(
            180 - self.calculate_angle(self.myTank.x, self.myTank.y, self.enemyTanks.x, self.enemyTanks.y))
        self.enemyTanks2.set_cannon_angle(
            180 - self.calculate_angle(self.myTank.x, self.myTank.y, self.enemyTanks2.x, self.enemyTanks2.y))
        self.enemyTanks3.set_cannon_angle(
            180 - self.calculate_angle(self.myTank.x, self.myTank.y, self.enemyTanks3.x, self.enemyTanks3.y))

        if self.check_flow:
            self.enemy_move()
        self.check_tank_collisions(self.enemyTanks)
        self.check_tank_collisions(self.enemyTanks2)
        self.check_tank_collisions(self.enemyTanks3)

        self.update_Pj(self.myTank)
        self.update_Pj(self.enemyTanks)
        self.update_Pj(self.enemyTanks2)
        self.update_Pj(self.enemyTanks3)

    def update_Pj(self, tank):

        for projectile in tank.projectiles:
            projectile.draw()
            projectile.move()
            # Check if projectile hits any barrier
            if projectile.Pj_Barrier_collision(self.myBarrier.barrier_coordinates):
                projectile.active = False  # Deactivate the projectile
            self.outgoing_Pj_check(self.enemyTanks)
            self.outgoing_Pj_check(self.enemyTanks2)
            self.outgoing_Pj_check(self.enemyTanks3)
            self.incoming_Pj_check(self.enemyTanks)
            self.incoming_Pj_check(self.enemyTanks2)
            self.incoming_Pj_check(self.enemyTanks3)

            # Remove inactive projectiles
            if not projectile.active:
                tank.projectiles.remove(projectile)

    def outgoing_Pj_check(self, tank):
        for projectile in self.myTank.projectiles:
            if projectile.Pj_Tank_collision(tank):
                tank.health -= 10
                projectile.active = False
                if tank.health == 0:
                    # projectile.active = False
                    self.score += 1
                    tank.update_Tank(100, tank.og_x, tank.og_y)
                    if self.score == 1 or self.score == 5:
                        self.level += 1

    def incoming_Pj_check(self, tank):
        for projectile in tank.projectiles:
            if projectile.Pj_Tank_collision(self.myTank):
                self.myTank.health -= 5
                projectile.active = False
                if self.myTank.health == 0:
                    # projectile.active = False
                    self.enemyScore += 1
                    self.myTank.update_Tank(100, self.myTank.og_x, self.myTank.og_y)

    def check_tank_collisions(self, tank):
        if self.myTank.Tank_Tank_collision(tank):
            if self.myTank.x != 100 or self.myTank.y != 250:

                # Perform actions when collision happens, like stopping the tank
                self.enemyScore += 1
                if self.enemyScore == 5:

                    self.current_scene = 'DEAD_SCENE'
                    self.level = 0
                    self.score = 0
                    self.update_Loser()
                    self.check_flow = False

                self.myTank.update_Tank(100, 100, 250)
            else:
                self.myTank.update_Tank(100, 700, 250, 180)

    def update_Loser(self):
        self.enemyTanks.update_Tank(100, self.enemyTanks.og_x, self.enemyTanks.og_y)
        self.enemyTanks2.update_Tank(100, self.enemyTanks2.og_x, self.enemyTanks2.og_y)
        self.enemyTanks3.update_Tank(100, self.enemyTanks3.og_x, self.enemyTanks3.og_y)

    def enemy_move(self):

        if self.enemyTanks.x == 880 and self.enemyTanks.y == 250:
            self.counter1 = 0
            # !--------------------------------------
        if self.enemyTanks.x >= 680 and self.counter1 == 0:
            self.enemyTanks.x -= 1.5
        if self.enemyTanks.x <= 680 and self.enemyTanks.y <= 390 and self.counter1 == 0:
            self.enemyTanks.y += 1.5

        if self.enemyTanks.y >= 390 and self.enemyTanks.x >= 30 and self.counter1 == 0:
            self.enemyTanks.x -= 1.5
            if self.enemyTanks.x <= 30:
                self.counter1 = 1

        # !-----------------------------------------------------------------

        if self.counter1 == 1 and self.enemyTanks.y >= 130:
            self.enemyTanks.y -= 1.5
            if self.enemyTanks.y <= 130:
                self.counter1 = 2

        if self.counter2 == 2 and self.counter1 == 2 and self.enemyTanks.x <= 220:
            self.enemyTanks.x += 1.5
            if self.enemyTanks.x >= 220:
                self.counter1 = 3

        if self.counter1 == 3 and self.enemyTanks.y <= 380:
            self.enemyTanks.y += 1.5
            if self.enemyTanks.y >= 380:
                self.counter1 = 4

        if self.counter1 == 4 and self.enemyTanks.x >= 30:
            self.enemyTanks.x -= 1.5
            if self.enemyTanks.x <= 30:
                self.counter1 = 1

        # !------------------------------enemy_two----------------------------------
        if self.enemyTanks2.x == 480 and self.enemyTanks2.y == -50:
            self.counter2 = 0

            # !--------------------------------------
        if self.level > 0:
            if self.enemyTanks2.x == 480 and self.enemyTanks2.y <= 380 and self.counter2 == 0:
                self.enemyTanks2.y += 1.5

            if self.enemyTanks2.x >= 120 and self.enemyTanks2.y >= 380 and self.counter2 == 0:
                self.enemyTanks2.x -= 1.5

            if self.enemyTanks2.x <= 120 and self.enemyTanks2.y >= 380 and self.counter2 == 0:
                self.enemyTanks2.x += 1.5

                if self.enemyTanks2.x >= 120:
                    self.counter2 = 1

            #    !--------------------------------enemyTanks2more--------------------------------
            if self.counter2 == 1 and self.enemyTanks2.y >= 120:
                self.enemyTanks2.y -= 1.5
                if self.enemyTanks2.y <= 120:
                    self.counter2 = 2

            if self.counter2 == 2 and self.enemyTanks2.y <= 120 and self.enemyTanks2.x <= 700:
                self.enemyTanks2.x += 1.5
                if self.enemyTanks2.x >= 700:
                    self.counter2 = 3

            if self.counter2 == 3 and self.enemyTanks2.y <= 380:
                self.enemyTanks2.y += 1.5
                if self.enemyTanks2.y >= 380:
                    self.counter2 = 4

            if self.counter2 == 4 and self.enemyTanks2.x >= 120:
                self.enemyTanks2.x -= 1.5
                if self.enemyTanks2.x <= 120:
                    self.counter2 = 1

        # !---------------------------enemy_+tank3-----------------------------------
        if self.enemyTanks3.x == 400 and self.enemyTanks3.y == 600:
            self.counter3 = 0
        if self.level > 1:
            if self.enemyTanks3.x == 400 and self.enemyTanks3.y >= 120 and self.counter3 == 0:
                self.enemyTanks3.y -= 1.5

            if self.enemyTanks3.x >= 130 and self.enemyTanks3.y <= 120 and self.counter3 == 0:
                self.enemyTanks3.x -= 1.5

                if self.enemyTanks3.x <= 130:
                    self.counter3 = 1
            # !--------------------
            if self.counter3 == 1 and self.enemyTanks3.x <= 580:
                self.enemyTanks3.x += 1.5
                if self.enemyTanks3.x >= 580:
                    self.counter3 = 2

            if self.counter3 == 2 and self.enemyTanks3.y <= 380:
                self.enemyTanks3.y += 1.5
                if self.enemyTanks3.y >= 380:
                    self.counter3 = 3

            if self.counter3 == 3 and self.enemyTanks3.x >= 110:
                self.enemyTanks3.x -= 1.5
                if self.enemyTanks3.x <= 110:
                    self.counter3 = 4

            if self.counter3 == 4 and self.enemyTanks3.y >= 120:
                self.enemyTanks3.y -= 1.5
                if self.enemyTanks3.y <= 120:
                    self.counter3 = 1

    def draw(self):
        glLoadIdentity()
        glClear(GL_COLOR_BUFFER_BIT)

        if self.current_scene == 'MAIN_SCENE':
            self.draw_main_scene()
        elif self.current_scene == 'ABOUT_SCENE':
            self.draw_about_scene()
        elif self.current_scene == 'INTRO_SCENE':
            self.draw_intro_scene()
        elif self.current_scene == 'DEAD_SCENE':
            self.draw_dead_scene()

        glutSwapBuffers()

    def draw_intro_scene(self):
        self.adjust_background(0)
        functions.drawTextWithOutline("START(S)", 320, 420, 2)
        functions.drawTextWithOutline("ABOUT(A)", 315, 360, 2)
        functions.drawTextWithOutline("QUIT(Q)", 330, 300, 2)

    def draw_about_scene(self):
        self.adjust_background(1)
        glPushAttrib(GL_ALL_ATTRIB_BITS)

        string = "ABOUT TEAM 1"
        functions.drawTextWithOutline(string, 280, 400, 2)
        string = "MUHMD MATTAR - MUHMD ALAA - ZIAD GHORABA - HAMZA MAHROUS"
        functions.drawText(string, 20, 110, scale=0.13)
        string = "NOUR GAFAR - HASSAN ARAFAT - MAHMOUD RAMADAN"
        functions.drawText(string, 95, 70, scale=0.13)
        string = "MARIAM MAMDOUH - NADA REDA - SARA HESHAM"
        functions.drawText(string, 115, 30, scale=0.13)
        string = "MAIN MENU(B) - QUIT(Q)"
        functions.drawText(string, 140, 165)

        glPopAttrib()

    def draw_main_scene(self):

        self.adjust_background(2)
        glPushAttrib(GL_ALL_ATTRIB_BITS)
        string = "PLAYER : " + str(self.score)
        functions.drawText(string, 50, 470, 0.1)
        string = "PC : " + str(self.enemyScore)
        functions.drawText(string, 700, 470, 0.1)
        self.myTank.draw()
        self.enemyTanks.draw()
        self.enemyTanks2.draw()
        self.enemyTanks3.draw()
        self.myBarrier.draw()
        self.update_main_scene()
        self.call_function()
        glPopAttrib()

    def draw_dead_scene(self):
        self.adjust_background(3)

    def keyboard_control(self, key, x, y):
        if self.current_scene == 'INTRO_SCENE':
            if key == b's' or key == b'S':
                self.check_flow = True
                self.current_scene = 'MAIN_SCENE'
            elif key == b'a' or key == b'A':
                self.current_scene = 'ABOUT_SCENE'
            elif key == b'q' or key == b'Q':
                sys.exit(0)

        elif self.current_scene == 'ABOUT_SCENE':
            if key == b'b' or key == b'B':
                self.current_scene = 'INTRO_SCENE'
            elif key == b'q' or key == b'Q':
                sys.exit(0)

        elif self.current_scene == 'MAIN_SCENE':
            if key == b'q' or key == b'Q':
                sys.exit(0)
            elif (key == b'w' or key == b'W') and (self.myTank.y < self.WINDOW_HEIGHT - 30):
                self.myTank.move_up()
            elif (key == b's' or key == b'S') and (self.myTank.y > 30):
                self.myTank.move_down()
            elif (key == b'a' or key == b'A') and (self.myTank.x > 30):
                self.myTank.move_left()
            elif (key == b'd' or key == b'D') and (self.myTank.x < self.WINDOW_WIDTH - 70):
                self.myTank.move_right()

        elif self.current_scene == 'DEAD_SCENE':
            if key == b'q' or key == b'Q':
                sys.exit(0)
            elif key == b'p' or key == b'P':
                self.current_scene = 'MAIN_SCENE'
                self.enemyScore = 0
                self.check_flow = True

    def mouse_click(self, button, state, x, y):

        if self.current_scene == 'MAIN_SCENE' and button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
            self.myTank.fire()

    def mouse_motion(self, x, y):
        y = 500 - y
        # Calculate the angle between the tank's cannon and the mouse position
        angle = math.degrees(math.atan2(-y + self.myTank.y, x - self.myTank.x))

        self.myTank.set_cannon_angle(angle)

    def calculate_angle(self, x1, y1, x2, y2):
        # Calculate the difference in x and y coordinates
        dx = x2 - x1
        dy = y2 - y1

        # Calculate the angle using arctangent and convert it to degrees
        angle = math.degrees(math.atan2(dy, dx))
        return angle

    def call_function(self):

        if not self.function_called:
            self.enemyTanks.fire()
            if self.level > 0:
                self.enemyTanks2.fire()
            if self.level > 1:
                self.enemyTanks3.fire()
            self.function_called = True

    def reset_flag(self, value):

        self.function_called = False

        glutTimerFunc(2000, self.reset_flag, 0)


def main():
    game = Game()
    glutInit()
    glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE)
    glutInitWindowSize(game.WINDOW_WIDTH, game.WINDOW_HEIGHT)
    glutCreateWindow(b"Tank Wars")
    glutTimerFunc(game.interval, game.Timer, 0)
    glutTimerFunc(2000, game.reset_flag, 0)
    glutKeyboardFunc(game.keyboard_control)
    glutMouseFunc(game.mouse_click)  # Register mouse click callback
    glutPassiveMotionFunc(game.mouse_motion)
    glutDisplayFunc(game.draw)
    game.init()
    glutMainLoop()


main()
