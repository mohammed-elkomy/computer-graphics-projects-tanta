from Rectangle import *
from texture import *

G.squirrel = Rec(80, 0 ,530, 470)

"""move player in x direction"""
def player_mover_x(player):
	global man_path
	G.ball_x_velocity = 0  # reset x velocity
	if G.increaseF == True:
		G.factor += 1
	else:
		G.factor=1
	if G.keystates[0] == True and  player.left > 0: # LEFT OR right 
			G.ball_x_velocity += G.factor * 0.25 * G.ball_dir_x
			G.index=14+(G.factor // 5)  % 4

	if G.keystates[1] == True and player.right < 790:
			G.index=10+(G.factor // 5)  % 4
			G.ball_x_velocity += G.factor * 0.25 * G.ball_dir_x
	
	player.left +=G.ball_x_velocity
	player.right += G.ball_x_velocity

def player_mover_y(player):
	"""jump in y direction"""
	if G.jumping == True:
		if G.moving_up <= 0:
			G.jumping = False
		else:
			if G.stand_left:
				G.index=8
			else:
				G.index=9
			G.jump_texture=G.index
			if G.ball_x_velocity < 0:
				G.ball_x_velocity *= -1
			G.ball_y_velocity = 0.5 * G.ball_x_velocity + G.moving_up
			G.moving_up -= 10 * G.dtime
		player.bottom += G.ball_y_velocity
		player.top = player.bottom + 80

	
	else:	
		"""fall"""
		for plate in G.plates:

			# collison detection
			if (player.left >= plate.left - 25 and player.right <= plate.right + 25 and 
				plate.top>= player.bottom+10  >= plate.bottom):
				player.bottom = plate.top - 35
				player.top = player.bottom + 80
				player.left += G.stair_step_x * plate.direction
				player.right += G.stair_step_x * plate.direction

				"""check score"""
				if plate.landed == False:
					G.score += 1
					plate.landed = True
				if G.hight_score < G.score:
					G.hight_score = G.score

				""" collison detection with plate hazelnuts"""
				if plate.hazelnut:
					if player.right > plate.hazelnut.left and player.left < plate.hazelnut.right :
						plate.hazelnut=None
						G.score += 5

				"""reset values"""
				G.moving_up = 16
				G.moving_down = 0
				G.ball_y_velocity = 0
				G.on_plate = True

				if G.keystates[0]== False and G.keystates[1] == False: 
					if G.stand_left:
						G.index=6
					else:
						G.index=7
				break
			else:
				G.on_plate = False ##used for movinf ball down

		if player.bottom > G.frastom_bottom and not G.on_plate:
			if G.stand_left:
				G.index=18
			else:
				G.index=19
			G.ball_y_velocity = G.moving_down
			G.moving_down += 10 * G.dtime
			player.bottom -= G.ball_y_velocity
			player.top = player.bottom + 80

	if player.bottom < G.frastom_bottom:
		
		player.bottom = 0
		player.top = player.bottom + 80
		G.moving_down = 0
		G.moving_up = 16
		G.ball_y_velocity = 0
		G.on_plate = False
		if G.stand_left:
			G.index=6
		else:
			G.index=7
		if  G.score>3:
			G.gamestart = False
			G.gameover = True
			G.score = 0
			G.frastom_y = 0
			G.frastom_bottom = 0
			G.frastom_top = 800
			G.plates = []
			G.stair_step_x = 0
			G.index=6

def player():
	player_mover_x(G.squirrel)
	player_mover_y(G.squirrel)
	G.squirrel.drawrec(G.index)