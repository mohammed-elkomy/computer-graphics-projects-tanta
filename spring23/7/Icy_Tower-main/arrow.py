from Rectangle import *
from texture import *

def keypress(key, x, y):
	global man_path,left_key,right_key

	""" moving ball to the left"""
	if G.squirrel.left > 0 and key == GLUT_KEY_LEFT:
		G.ball_dir_x = -1
		G.keystates[0] = True
		G.increaseF = True
		G.stand_left=True

	""" moving ball to the right"""
	if G.squirrel.right < 800 and key == GLUT_KEY_RIGHT:
		G.ball_dir_x = 1
		G.keystates[1] = True
		G.increaseF = True
		G.stand_left=False

	""" jumping """
	if key == GLUT_KEY_UP:
		G.keystates[2] = True
		G.jumping = True
		G.on_plate=False

	""" BEGIN"""
	if key == b' ' and G.gamestart is False:
		G.gamestart = True
		G.gameover = False

	glutPostRedisplay()

def reset_keys(key,x,y):
	if G.keystates[0]==True:
		G.index=6
		
	if G.keystates[1]==True:
		G.index=7

	G.keystates = [False, False, False, False]
	G.increaseF = False
	glutPostRedisplay() # to redraw the scene