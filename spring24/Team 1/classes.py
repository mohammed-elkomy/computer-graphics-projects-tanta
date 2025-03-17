from OpenGL.GL import *
from OpenGL.GLUT import *
import math


class Tank:
    def __init__(self, x=100, y=250, color=(0.4, 0.5, 0.2), cannon_angle=0.0, health=100):
        self.x = x
        self.y = y
        self.og_x = x
        self.og_y = y
        self.color = color
        self.cannon_angle = cannon_angle
        self.cannon_length = 35
        self.projectiles = []
        self.myBarrier = barrier()
        self.health = health

    def Tank_Tank_collision(self, other_tank):
        tank_left = self.x - 30
        tank_right = self.x + 30
        tank_top = self.y + 25
        tank_bottom = self.y - 25

        other_left = other_tank.x - 30
        other_right = other_tank.x + 30
        other_top = other_tank.y + 25
        other_bottom = other_tank.y - 25

        if (tank_right >= other_left and tank_left <= other_right and
                tank_top >= other_bottom and tank_bottom <= other_top):
            return True
        return False

    def update_Tank(self, health, x, y, angle=0):
        # Update tank's position, health, or any other properties
        self.health = health
        self.x = x
        self.y = y
        self.cannon_angle = angle
        self.projectiles.clear()

    def draw_health_bar(self):
        health_bar_width = self.health * 0.5

        health_bar_offset_x = -25
        health_bar_offset_y = 35

        health_bar_x = self.x + health_bar_offset_x
        health_bar_y = self.y + health_bar_offset_y

        # Draw the black border
        glColor3f(0, 0, 0)
        glLineWidth(1)  # Adjust line width as needed
        glBegin(GL_LINE_LOOP)
        glVertex2f(health_bar_x - 1, health_bar_y - 1)
        glVertex2f(health_bar_x + health_bar_width + 1, health_bar_y - 1)
        glVertex2f(health_bar_x + health_bar_width + 1, health_bar_y + 6)  # Adjust height as needed
        glVertex2f(health_bar_x - 1, health_bar_y + 6)  # Adjust height as needed
        glEnd()

        # Draw the health bar
        glColor3f(*self.color)
        glBegin(GL_QUADS)
        glVertex2f(health_bar_x, health_bar_y)
        glVertex2f(health_bar_x + health_bar_width, health_bar_y)
        glVertex2f(health_bar_x + health_bar_width, health_bar_y + 5)  # Adjust height as needed
        glVertex2f(health_bar_x, health_bar_y + 5)  # Adjust height as needed
        glEnd()

    def draw(self):
        glLoadIdentity()
        self.draw_health_bar()
        glTranslate(self.x, self.y, 0)
        glColor(*self.color)  # Set tank color
        # Draw tank body
        self.draw_tank_body()
        # Draw cannon
        self.draw_cannon()

    def draw_tank_body(self):

        self.draw_quad(-35, 10, 35, 30)  # Top Body
        self.draw_quad(-35, -10, 35, -30)  # Bot Body
        self.draw_quad(-30, 25, 30, -25)  # Main Body

        glColor3d(0, 0, 0)
        glutSolidCylinder(18, 1, 100, 1)  # Circle

    def draw_cannon(self):

        glColor3d(0, 0, 0)
        glTranslate(2, 0, 0)  # Translate to the tip of the tank
        glRotatef(-self.cannon_angle, 0, 0, 1)

        self.draw_quad(0, -2.5, self.cannon_length, 2.5)  # Cannon

    def set_cannon_angle(self, angle):
        self.cannon_angle = angle
        
    def draw_quad(self, x1, y1, x2, y2):
        glBegin(GL_QUADS)
        glVertex2d(x1, y1)
        glVertex2d(x2, y1)
        glVertex2d(x2, y2)
        glVertex2d(x1, y2)
        glEnd()
     
    def fire(self):
        projectile = Projectile(self.x + 2, self.y, self.cannon_angle)
        self.projectiles.append(projectile)

    def Pj_Window_collision(self):

        for projectile in self.projectiles:

            if projectile.x < 0 or projectile.x > 800 or projectile.y < 0 or projectile.y > 500:
                self.projectiles.remove(projectile)

    def move_up(self):
        if self.myBarrier.Tank_Barrier_NoCollision(self.x, self.y + 5):
            self.y += 5

    def move_down(self):
        if self.myBarrier.Tank_Barrier_NoCollision(self.x, self.y - 5):
            self.y -= 5

    def move_left(self):
        if self.myBarrier.Tank_Barrier_NoCollision(self.x - 5, self.y):
            self.x -= 5

    def move_right(self):
        if self.myBarrier.Tank_Barrier_NoCollision(self.x + 5, self.y):
            self.x += 5


class Projectile:
    def __init__(self, x, y, angle, speed=5):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = speed
        self.active = True

    def move(self):

        self.x += self.speed * math.cos(math.radians(self.angle))
        self.y += self.speed * -math.sin(math.radians(self.angle))

    def draw(self):

        glLoadIdentity()
        glTranslate(self.x, self.y, 0)
        glColor(0, 0, 0)
        glBegin(GL_QUADS)
        glVertex2d(-2.5, -2.5)
        glVertex2d(2.5, -2.5)
        glVertex2d(2.5, 2.5)
        glVertex2d(-2.5, 2.5)
        glEnd()

    def Pj_Barrier_collision(self, barrier_coordinates):

        for Barrier in barrier_coordinates:
            barrier_left = min(Barrier[0], Barrier[2])
            barrier_right = max(Barrier[0], Barrier[2])
            barrier_top = max(Barrier[1], Barrier[3])
            barrier_bottom = min(Barrier[1], Barrier[3])

            if (barrier_left <= self.x <= barrier_right and
                    barrier_bottom <= self.y <= barrier_top):
                return True
        return False

    def Pj_Tank_collision(self, tank):

        tank_left = tank.x - 30
        tank_right = tank.x + 30
        tank_top = tank.y + 25
        tank_bottom = tank.y - 25

        if (tank_left <= self.x <= tank_right and
                tank_bottom <= self.y <= tank_top):
            return True
        return False


class barrier:
    def __init__(self):
        self.barrier_coordinates = [
            (645, 350, 625, 170),  # Right

            (155, 350, 175, 170),  # Left

            (555, 90, 575, 40),  # Right_down
            (525, 60, 575, 40),

            (525, 470, 575, 450),  # Right up
            (555, 470, 575, 420),

            (245, 90, 225, 40),  # Left down
            (225, 60, 275, 40),

            (225, 470, 275, 450),  # Left up
            (245, 470, 225, 420)
        ]

    def draw_quad(self, x1, y1, x2, y2):
        glBegin(GL_QUADS)
        glVertex2d(x1, y1)
        glVertex2d(x2, y1)
        glVertex2d(x2, y2)
        glVertex2d(x1, y2)
        glEnd()

    def draw(self):
        # RIGHT

        glLoadIdentity()

        glColor3f(0, 0, 0)
        self.draw_quad(645, 350, 625, 170)

        # LEFT
        self.draw_quad(155, 350, 175, 170)

        # RIGHT_DOWN
        self.draw_quad(555, 90, 575, 40)
        self.draw_quad(525, 60, 575, 40)

        # RIGHT_UP
        self.draw_quad(525, 470, 575, 450)
        self.draw_quad(555, 470, 575, 420)

        # LEFT_DOWN
        self.draw_quad(245, 90, 225, 40)
        self.draw_quad(225, 60, 275, 40)

        # LEFT_UP
        self.draw_quad(225, 470, 275, 450)
        self.draw_quad(245, 470, 225, 420)

    def Tank_Barrier_NoCollision(self, new_x, new_y):
        tank_left = new_x - 30
        tank_right = new_x + 30
        tank_top = new_y + 25
        tank_bottom = new_y - 25

        for BARRIER in self.barrier_coordinates:
            barrier_left = min(BARRIER[0], BARRIER[2])
            barrier_right = max(BARRIER[0], BARRIER[2])
            barrier_top = max(BARRIER[1], BARRIER[3])
            barrier_bottom = min(BARRIER[1], BARRIER[3])

            if tank_right >= barrier_left and tank_left <= barrier_right and \
                    tank_top >= barrier_bottom and tank_bottom <= barrier_top:
                return False
        return True
