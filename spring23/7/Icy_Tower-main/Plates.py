from Rectangle import *
from random import randint

def createPlate():
	""" create first plate"""
	if G.plates == []:
		left = randint(200, 400)
		right = (randint(300, 400)) + left
		top = 130
		bottom = 70
		rec = Rec(top,bottom,right,left)
		G.plates.append(rec)
	
	"""create other plates"""
	if G.plates[-1].top <= G.frastom_top - 100:
		left = randint(100, 600)
		right = (randint(170, 200)) + left
		top = G.plates[-1].top + 120
		bottom = G.plates[-1].bottom + 120
		rec = Rec(top,bottom,right,left)

		""" CREATE RANDOM NUTS"""
		if randint(0,1) == 1:
			l = randint(left + 50,right -50)
			hazelnut = Rec(top+25,top-15,l + 50,l)
			rec.hazelnut = hazelnut
		G.plates.append(rec)
		
def stairs():
	createPlate()
	""" check the plates """
	for plate in G.plates:
		""" move coins in x direction sycthronically with plates"""
		if plate.hazelnut:
			plate.hazelnut.drawrec(4)
			plate.hazelnut.right += G.stair_step_x * plate.direction
			plate.hazelnut.left += G.stair_step_x * plate.direction

		""" move plates in x direction"""
		plate.right += G.stair_step_x * plate.direction
		plate.left += G.stair_step_x * plate.direction
		if plate.right >= 800:
			plate.direction = -1
		elif plate.left <= 0:
			plate.direction = 1
		plate.drawrec(2)
	
	""" remove the plates out of the frastom"""
	G.plates = [it for it in G.plates if it.top > G.frastom_bottom]
