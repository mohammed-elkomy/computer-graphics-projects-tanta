from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from texture import *
LINE_WIDTH = 1


class line:
    def __init__(self, x1, y1, x2, y2):   # initialize line end points (x1,y1) & (x2,y2)
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.vertical = (x1 == x2)

    def get_vertices(self):
        return [[self.x1, self.y1], [self.x2, self.y2]]
    def draw_line(self):
        glColor3f(1, 0, 0)
        glLineWidth(1)
        glBegin(GL_LINES)
        glVertex(self.x1, self.y1, 0)
        glVertex(self.x2, self.y2, 0)
        glEnd()


class box:
    def __init__(self, left, bottom, right, top, Type = 0):
        # Type = 0 -->> coin , Type = 1 -->> bomb , Type = 2 -->> health kit
        self.left = left-5
        self.bottom = bottom-5
        self.right = right+5
        self.top = top+5
        self.type = Type
        self.collected = False  # if collected it will not be drawn ,else it will be drawn

    def draw(self):
        if self.collected == False:
            # choosing texture of box based on its type
            if self.type == 0:
                glBindTexture(GL_TEXTURE_2D, STAR)
            if self.type == 1:
                glBindTexture(GL_TEXTURE_2D, BOMB)
            if self.type == 2:
                glBindTexture(GL_TEXTURE_2D, HEALTH)
            if self.type == 3:
                glBindTexture(GL_TEXTURE_2D, FINISH_LINE)
            glBegin(GL_POLYGON)
            glTexCoord(0, 0)
            glVertex(self.left, self.bottom, 0)
            glTexCoord(1, 0)
            glVertex(self.right, self.bottom, 0)
            glTexCoord(1, 1)
            glVertex(self.right, self.top, 0)
            glTexCoord(0, 1)
            glVertex(self.left, self.top, 0)
            glEnd()
        glBindTexture(GL_TEXTURE_2D, -1)

    def get_vertices(self):
        vertices = [
            [self.left, self.top],
            [self.left, self.bottom],
            [self.right, self.bottom],
            [self.right, self.top],
        ]
        return vertices

# maze walls
maze1 = [
    line(0, 100, 300, 100), line(150, 200, 150, 600),
    line(0, 600, 150, 600), line(300, 200, 300, 600),
    line(300, 200, 900, 200), line(450, 300, 900, 300),
    line(600, 400, 900, 400), line(0, 700, 0, 0,),
    line(600, 500, 1200, 500), line(1050, 500, 1050, 200),
    line(600, 500, 600, 600), line(600, 600, 1050, 600),
    line(900, 400, 900, 300), line(450, 700, 450, 300),
    line(900, 200, 900, 100), line(450, 100, 1050, 100),
    line(450, 0, 450, 100), line(0, 0, 1200, 0),
    line(1200, 0, 1200, 700), line(1200, 700, 0, 700)
    ]

# car health will decrease by half after collision with a bomb
bombs1 =[box(180, 225, 210, 255, 1), box(330, 530, 360, 560, 1),
         box(480, 330, 510, 360, 1), box(990, 225, 1020, 255, 1),
         box(1140, 530, 1170, 560, 1), box(990, 10, 1020, 40, 1)]

# stars located on the map
coins1 = [box(400, 40, 420, 60), box(850, 140, 870, 160),
          box(50, 140, 70, 160), box(50, 630, 70, 650),
          box(225, 440, 245, 460), box(525, 40, 545, 60),
          box(1125, 440, 1145, 460), box(850, 340, 870, 360),
          box(500, 240, 520, 260)]

# health boasters to increase car health
health1 = [box(1125, 140, 1145, 160, 2), box(750, 440, 770, 460, 2),
           box(975, 640, 995, 660, 2), box(50, 540, 70, 560, 2),
           box(375, 440, 395, 460, 2)]

# finish line of maze
finish = [box(730, 507-0.5, 750, 593+0.5, 3)]

# reset every box in the given list of boxes to its initial state
def reset(lst_of_box : box):
    for i in lst_of_box:
        if i.collected:
            i.collected = False

# reset all boxes to the initial state to be able to play again
def reset_maze():
    reset(bombs1)
    reset(coins1)
    reset(health1)

# draw maze walls
def draw_map():
    for i in range(len(maze1)):
        maze1[i].draw_line()

# draw stars
def draw_coins():
    glColor3f(1, 1, 1)
    for i in coins1:
        i.draw()

def draw_healthkit():
    glColor3f(1, 1, 1)
    for i in health1:
        i.draw()

def draw_bombs():
    glColor3f(1, 1, 1)
    for i in bombs1:
        i.draw()

# draw finish line of the map
def draw_finish():
    glColor3f(1, 1, 1)
    for i in finish:
        i.draw()


# draw a grid 1200 * 700 ,every cell in this grid is 150 * 100 so we have a 8 * 7 grid to make it easy to allocate every thing in the world
def draw_grid():
    glLineWidth(1)
    glColor3f(1, 0, 0)
    glBegin(GL_LINES)
    for i in range(8):
        glVertex(-1500, i*100, 0)
        glVertex(1200, i*100, 0)
    for i in range(9):
        glVertex(i*150, -1500, 0)
        glVertex(i*150, 1500, 0)
    glEnd()
