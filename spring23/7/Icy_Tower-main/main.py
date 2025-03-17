from Player import*
from Plates import*
from arrow import*
from text import *
from Rectangle import Rec
from pygame import mixer
from texture import *
import Global as G

wall=Rec(G.frastom_top,G.frastom_bottom,800,0)
startplay = Rec(450,300,500,250)

def game_speed():
	if 20 <= G.score <= 40:
		G.stair_step_x = 1
	elif 40 < G.score <= 60:
		G.stair_step_x = 2
	elif G.score > 60 :
		G.stair_step_x = 3
	
	if 3 < G.score <= 50:
		G.frastom_y = 1
	elif 50 < G.score <= 100:
		G.frastom_y = 1.5 
	elif G.score > 100:
		G.frastom_y = 2
	# load sound
mixer.init()   
G.bstart_sound=mixer.Sound('sound/before start the game.mp3')
G.Astart_sound=mixer.Sound('sound/when the game run.mp3')
G.game_over_sound=mixer.Sound('sound/after lose in background.mp3')

def init():
	
	glClearColor(0.0, 0.0, 0.0, 0.0)
	glClear(GL_COLOR_BUFFER_BIT)
	glMatrixMode(GL_PROJECTION)
	
	glLoadIdentity()	#important

	glOrtho(0, 800,G.frastom_bottom ,G.frastom_top, -1.0, 1.0) # left, right, bottom, top, near, far
	glMatrixMode(GL_MODELVIEW)
	if G.gamestart==False and G.gameover==False:
		G.bstart_sound.play()
	elif G.gamestart==True and G.gameover==False:
		G.bstart_sound.stop()
		G.game_over_sound.stop()
		G.Astart_sound.play()
	else:
		G.Astart_sound.stop()
		if G.gameover == True:
			G.game_over_sound.play()
	if G.frastom_top - G.squirrel.top<=300:		
		G.frastom_top += 2
		G.frastom_bottom += 2

	G.frastom_bottom += G.frastom_y 
	G.frastom_top += G.frastom_y
	game_speed()
	


def draw():
	init()
	global wall,startplay
	glLoadIdentity()

	if G.gamestart==False and G.gameover==False:
		# intro
		wall.drawrec(0)
		startplay.drawrec(3)

	if G.gamestart:
		
		wall.drawrec(5)
		# to refresh wall dimensions
		wall=Rec(G.frastom_top,G.frastom_bottom,800,0)
		
		stairs()
		player()
	 
		normal_score = "Score"
		Text(normal_score,20,G.frastom_top-160)
		scoreNum = str(G.score)
		Text(scoreNum,50,G.frastom_top-200)
		High_Score = "High Score"
		Text(High_Score,20,G.frastom_top-90)
		HighScoreNum = str(G.hight_score)
		Text(HighScoreNum,50,G.frastom_top-130)

	if G.gameover==True:
		wall=Rec(G.frastom_top,G.frastom_bottom,800,0)
		wall.drawrec(1)
	glutSwapBuffers()


def game_timer(v):
	draw()
	glutTimerFunc(G.INTERVAL, game_timer, 1)

def main():
	glutInit()
	glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
	glutInitWindowSize(800, 800)
	glutInitWindowPosition(0, 0)
	glutCreateWindow (b"OpenGL - First window demo")
	load_textures()
	glutTimerFunc(G.INTERVAL, game_timer, 1)
	glutKeyboardFunc(keypress)
	glutSpecialFunc(keypress)
	glutSpecialUpFunc(reset_keys)
	glutDisplayFunc(draw)
	glutMainLoop()

main()