from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700

'''
To draw the health bar we have to do 3 steps:
1- We draw the white bar which represents full health.
2- We need to calculate the length of the green bar which represnts health.
3- We change the color of the health bar.
4- We draw the green bar.
'''


# 1- drawing the white bar on the top left of the screen relative to the car center.
def draw_white_bar(center):
    glColor3f(1, 1, 1)
    glBegin(GL_POLYGON)
    glVertex(center[0] - 60 - 230, center[1] - 7 + 165, 0)
    glVertex(center[0] + 60 - 230, center[1] - 7 + 165, 0)
    glVertex(center[0] + 60 - 230, center[1] + 7 + 165, 0)
    glVertex(center[0] - 60 - 230, center[1] + 7 + 165, 0)
    glEnd()

def draw_health_bar(health, center):
    # 2- as health decreases the green degree decreases and the red degree increases.
    glColor3f(1 - health / 100, health / 100, 0)
    # 3- drawing the bar depends mainly on health as (Green_Section / 116 = health / 100)
    Green_Section = (health * (116 / 100))
    glBegin(GL_POLYGON)
    # 4- fixing the left side of the health to decrease only from right.
    glVertex(center[0] - 58 - 230, center[1] - 5 + 165, 0)
    glVertex(center[0] - 58 + Green_Section - 230, center[1] - 5 + 165, 0)
    glVertex(center[0] - 58 + Green_Section - 230, center[1] + 5 + 165, 0)
    glVertex(center[0] - 58 - 230, center[1] + 5 + 165, 0)
    glEnd()


def draw_health(health, center):
    glPushMatrix()
    draw_health_bar(health, center)
    draw_white_bar(center)
    glPopMatrix()
