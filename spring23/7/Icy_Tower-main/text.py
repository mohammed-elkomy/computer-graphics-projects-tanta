from Rectangle import *
from OpenGL.GLUT import GLUT_STROKE_ROMAN
def Text(score,x,y):
    glBindTexture(GL_TEXTURE_2D,-1)

    glLineWidth(3)
    glColor(1,1,1)
    glLoadIdentity()
    glTranslate(x,y,0)
    glScale(0.19,0.19,1)
    string = score.encode()
    for c in string:
        glutStrokeCharacter(GLUT_STROKE_ROMAN,c)