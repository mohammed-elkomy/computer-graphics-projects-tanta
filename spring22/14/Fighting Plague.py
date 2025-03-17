from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import pygame
from numpy import random
x=30
fire=False
fire_x=x
moverx=1
movery=1
xstep=0
ystep=1
state=0
score=0
timer_detector=0
gamestate=False
global texture
objects=[]
life=3
#object comes from top
class object:
    def __init__(self,x):
        self.step=0
        self.ystep=0.2
        self.posx=x
        self.posy=100
        self.drow_state=1

    def drow(self,x,y,timer):#draw function of object
        if self.drow_state==1:
            glBindTexture(GL_TEXTURE_2D,texture[1])
            glBegin(GL_POLYGON)
            glTexCoord(0, 0)
            glVertex2f(self.posx,self.posy)
            glTexCoord(0, 1)
            glVertex2f(self.posx,self.posy+3)
            glTexCoord(1, 1)
            glVertex2f(self.posx+3,self.posy+3)
            glTexCoord(1, 0)
            glVertex2f(self.posx+3,self.posy)
            glEnd()
            self.detect(x,y)
            self.mover(timer)
            self.posx=self.posx+self.step
            if timer%1000==0:
                self.posy=self.posy-self.ystep
            return self.drow_state
        else:
            return self.drow_state
#ball obejct space detect function
    def detect(self,x,y):
        if x+3>=self.posx and x<=self.posx+3:
            if y+3>=self.posy and y<=self.posy+3:
                self.drow_state=2
    #object move control
    def mover(self,time):
        if self.posx+3>=7 and self.posx+3<20:
            if self.posy>=68 and self.posy<=70:
                self.step=-0.1
                self.ystep=0
        elif self.posx+3>=20 and self.posx<=30:
            if self.posy>=78 and self.posy<=80:
                self.step=0.1
                self.ystep=0
        elif self.posx+3>=40 and self.posx<=50:
            if self.posy>=44 and self.posy<=45:###############
                self.step=-0.1
                self.ystep=0
        elif self.posx+3>=50 and self.posx<=60:
            if self.posy>=44 and self.posy<=45:
                self.step=0.1
                self.ystep=0
        elif self.posx+3>=70 and self.posx+3<78:
            if self.posy>=50 and self.posy<=60:
                self.step=-0.1
                self.ystep=0
        elif self.posx+3>=78 and self.posx<95:
            if self.posy>=60 and self.posy<=70:
                self.step=0.05
                self.ystep=0
        elif self.posy<=2:
            self.drow_state=3
        elif self.posx<=0:
            self.step=1
        elif self.posx>=100:
            self.step=-0.5

        else:
            self.ystep=0.2
            self.step=0
            if self.posy<=40:
                if time%2000==0:
                    self.step=random.randint(-1,1)/100






#texture loading function .....
def loadtex():
    global texture
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_BLEND)
    texture = glGenTextures(3)  # Generate 5 textures
    # Create MipMapped Texture
    imgload = pygame.image.load("ANTI_PLAGUE.jpg")
    img = pygame.image.tostring(imgload, "RGBA", 1) # 0) # Serializing the image to a string
    width = imgload.get_width()
    height = imgload.get_height()
    glBindTexture(GL_TEXTURE_2D, texture[0])
    glTexParameter(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR)
    glTexParameter(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
    glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT) # GL_CLAMP)
    glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT) # GL_CLAMP)
    # gluBuild2DMipmaps( target, internalFormat,  width,  height,  format, type,  raw_image)
    gluBuild2DMipmaps(GL_TEXTURE_2D, 4, width, height, GL_RGBA, GL_UNSIGNED_BYTE, img)
    #glTexImage2D(GL_TEXTURE_2D, 0,  GL_RGBA, width, height,0, GL_RGBA,  GL_UNSIGNED_BYTE,img)
    imgload = pygame.image.load("PLAGUE.png")
    img = pygame.image.tostring(imgload, "RGBA", 1) # 0) # Serializing the image to a string
    width = imgload.get_width()
    height = imgload.get_height()
    glBindTexture(GL_TEXTURE_2D, texture[1])
    glTexParameter(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR)
    glTexParameter(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
    glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT) # GL_CLAMP)
    glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT) # GL_CLAMP)
    # gluBuild2DMipmaps( target, internalFormat,  width,  height,  format, type,  raw_image)
    gluBuild2DMipmaps(GL_TEXTURE_2D, 4, width, height, GL_RGBA, GL_UNSIGNED_BYTE, img)
    
    imgload = pygame.image.load("Plague_Mask.jpg")
    img = pygame.image.tostring(imgload, "RGBA", 1) # 0) # Serializing the image to a string
    width = imgload.get_width()
    height = imgload.get_height()
    glBindTexture(GL_TEXTURE_2D, texture[2])
    glTexParameter(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR)
    glTexParameter(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
    glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT) # GL_CLAMP)
    glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT) # GL_CLAMP)
    # gluBuild2DMipmaps( target, internalFormat,  width,  height,  format, type,  raw_image)
    gluBuild2DMipmaps(GL_TEXTURE_2D, 4, width, height, GL_RGBA, GL_UNSIGNED_BYTE, img)
    #glTexImage2D(GL_TEXTURE_2D, 0,  GL_RGBA, width, height,0, GL_RGBA,  GL_UNSIGNED_BYTE,img) 
    
#postion of player control function
def mouse_player(posx, poxy):
    global x
    x = posx/8
    #print(posx)
def init():
    glMatrixMode(GL_PROJECTION)  # ortho or perspective NO BRAINER
    glLoadIdentity()
    glOrtho(0,100, 0, 100, -1, 1)  # l,r,b,t,n,f
    glMatrixMode(GL_MODELVIEW)
#text display function
def draw_text(string, x, y):
    glLineWidth(2)
    glColor(0, 0, 0)  # WHITE COLOR
    glPushMatrix()  # remove the previous transformations
    # glScale(0.13,0.13,1)  # TODO: Try this line
    glTranslate(x, y, 0)
    glScale(0.03, 0.03, 1) # when writing text and see nothing downscale it to a very small value .001 and draw at center
    string = string.encode()  # conversion from Unicode string to byte string
    for c in string:
        glutStrokeCharacter(GLUT_STROKE_ROMAN, c)
    glPopMatrix()
    glColor(1, 1, 1)
#fired Ball displaying function
def fire_ball():
    global movery
    global moverx
    wall_state()
    if fire:
        glBindTexture(GL_TEXTURE_2D,texture[0])
        glBegin(GL_POLYGON)
        glTexCoord(0, 0)
        glVertex2f(fire_x+moverx,movery)
        glTexCoord(0, 1)
        glVertex2f(fire_x+moverx,movery+3)
        glTexCoord(1, 1)
        glVertex2f(fire_x+moverx+3,movery+3)
        glTexCoord(1, 0)
        glVertex2f(fire_x+moverx+3,movery)
        glEnd()
        movery=movery+ystep
        moverx=moverx+xstep
#fired Ball postion control
def wall_state():
    global movery
    global moverx
    global ystep
    global xstep
    global fire

    if fire_x+moverx>=100 :
        xstep=-1
    elif  fire_x+moverx<=0:
        xstep=1
    elif movery>=100:
        ystep=-1
    elif movery+3<=0:
        fire=False
        movery=1
        moverx=1
        ystep=1
        if state==0:
            xstep=0
        elif state==1:
            xstep=1
        else:
            xstep=-1
    elif fire_x+moverx+3>=7 and fire_x+moverx<=30:
        if movery+3>=60 and movery+3<=61:
            ystep=-1
        elif movery<=70 and movery>=69:
            if fire_x+moverx>=28:
                pass
            else:
                ystep=1
    elif fire_x+moverx<=4 and fire_x+moverx>=3:
        if movery+4>60 and movery<=70:
            xstep=-1
    if fire_x+moverx<=30 and fire_x+moverx>=29:
        if movery+3>=60 and movery+3<=80:
            xstep=1
    if fire_x+moverx<=30 and fire_x+moverx+3>=20:
        if movery<=80 and movery>=79:
            ystep=1
    if fire_x+moverx+3>=20 and fire_x+moverx+3<=21:
        if movery>=60 and movery<=80:
            xstep=-1
    if fire_x+moverx+3>=40 and fire_x+moverx<=60:
        if movery<=45 and movery>=44:
            ystep=1
        elif movery+3>=35 and movery+3<=36:
            ystep=-1
    if fire_x+moverx+3>=40 and fire_x+moverx+3<=41:
        if movery+3>=35 and movery<=45:
            xstep=-1
    if fire_x+moverx<=60 and fire_x+moverx>=59:
        if movery+3>=40 and movery<=50:
            xstep=1
    if fire_x+moverx+3>=70 and fire_x+moverx<=95:
        if movery+3>=50 and movery+3<=51:
            ystep=-1
        elif movery<=60 and movery>=59:
            ystep=1
    if fire_x+moverx+3<=71 and fire_x+moverx+3>=70:
        if movery+3>50 and movery<=60:
            xstep=-1
    if fire_x+moverx<=96 and fire_x+moverx>=95:
        if movery+3>=50 and movery<=70:
            xstep=1
    if fire_x+moverx+3>=77 and fire_x+moverx+3<=78:
        if movery>=60 and movery<=70:
            xstep=-1
    if fire_x+moverx+3>=78 and fire_x+moverx<=95:
        if movery>=69 and movery<=70:
            ystep=1

#display fun
def display():
    global gamestate
    global life
    global score
    global objects
    #loading object control
    if len(objects)==0 or objects.count(None)<=5:
        if len(objects)==0:
            for i in range(0,10,1):
                v=random.randint(100)
                print(v)
                objects.append(object(v))
        else:
            for i in range(0,10,1):
                if objects[i]==None:
                    objects[i]=object(random.randint(100))
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(1, 1, 1, 1)
    glLoadIdentity()
    glBindTexture(GL_TEXTURE_2D, texture[2])
    #shape one start drawing
    glBegin(GL_POLYGON)
    glTexCoord(0, 0)
    glVertex2f(7, 60)
    glTexCoord(0, 1)
    glVertex2f(7, 70)
    glTexCoord(1, 1)
    glVertex2f(30, 70)
    glTexCoord(1, 0)
    glVertex2f(30, 60)
    glEnd()
    glBegin(GL_POLYGON)
    glTexCoord(0, 0)
    glVertex2f(20, 70)
    glTexCoord(0, 1)
    glVertex2f(20, 80)
    glTexCoord(1, 1)
    glVertex2f(30, 80)
    glTexCoord(1, 0)
    glVertex2f(30, 70)
    glEnd()
    #shape one end drawing
    #shape two start drawing
    glBegin(GL_POLYGON)
    glTexCoord(0, 0)
    glVertex2f(40, 35)
    glTexCoord(0, 1)
    glVertex2f(40, 45)
    glTexCoord(1, 1)
    glVertex2f(60, 45)
    glTexCoord(1, 0)
    glVertex2f(60, 35)
    glEnd()
    #shape two end drawing
    #shape three start drawing
    glBegin(GL_POLYGON)
    glTexCoord(0, 0)
    glVertex2f(70, 50)
    glTexCoord(0, 1)
    glVertex2f(70, 60)
    glTexCoord(1, 1)
    glVertex2f(95, 60)
    glTexCoord(1, 0)
    glVertex2f(95, 50)
    glEnd()
    glBegin(GL_POLYGON)
    glTexCoord(0, 0)
    glVertex2f(78, 60)
    glTexCoord(0, 1)
    glVertex2f(78, 70)
    glTexCoord(1, 1)
    glVertex2f(95, 70)
    glTexCoord(1, 0)
    glVertex2f(95, 60)
    glEnd()
    #shape three end drawing
    #shape player start drawing
    glBindTexture(GL_TEXTURE_2D, texture[0])
    glBegin(GL_POLYGON)
    glTexCoord(0, 0)
    glVertex2f(x, 0)
    glTexCoord(0, 1)
    glVertex2f(x, 5)
    glTexCoord(1, 1)
    glVertex2f(x + 5, 5)
    glTexCoord(1, 0)
    glVertex2f(x + 5, 0)
    glEnd()
    #shape player end drawing
    fire_ball()
    #detect if object was killed by ball
    for i in range(0,10,1):
        o=objects[i]
        if o!=None:
            if o.drow(fire_x+moverx,movery,timer_detector)==2:
                score=score+1
                objects[i]=None
            elif o.drow(fire_x+moverx,movery,timer_detector)==3:
                life=life-1
                objects[i]=None
    draw_text("Score: "+str(score),3,90)
    draw_text("Life: "+str(life),85,90)
    if life<=0:
        draw_text("The Earth has been ", 30, 30)
        draw_text("  COMPROMISED!", 30, 25)
        gamestate=True
    glFlush()
    glutSwapBuffers()
#timer function
def timer(v):
    global timer_detector
    display()
    timer_detector=v
    if gamestate==True:
        glutTimerFunc(5000,glutDestroyWindow)

    else:
        glutTimerFunc(10, timer, v+100)
#key ball control direction
def key(k,posx,posy):
    global fire
    global fire_x
    global state
    global xstep
    '''
    if k == b"f":
        if fire == False:
            fire = True
            fire_x = x
    '''

    if k==b"s":
        if fire==False:
            fire = True
            fire_x = x
            xstep=0
        state=0
    if k==b"d":
        if fire==False:
            fire = True
            fire_x = x
            xstep=1
        state=1
    if k==b"a":
        if fire==False:
            fire = True
            fire_x = x
            xstep=-1
        state=2
if __name__ == "__main__":
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(800, 700)
    glutInitWindowPosition(0, 0)
    glutCreateWindow(b"Simple Ball Bat OpenGL game")
    loadtex()
    glutDisplayFunc(display)
    glutTimerFunc(0, timer, 0)
    #glutIdleFunc(display)
    glutKeyboardFunc(key)
    glutPassiveMotionFunc(mouse_player)
    init()
    glutMainLoop()
