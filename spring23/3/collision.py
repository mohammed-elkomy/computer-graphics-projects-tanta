from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from pygame import mixer
from camera import Camera
from coins import *
from monster import *
from player import *


coins_result = 0

def check_collisions(cam, coins, monsters,grenades):
    global coins_result
   
    #check collision with monster and grenades
    for grenad in grenades:
        check = grenad.draw(monsters, grenades)
        if check:
            coins_result -= 50
        if (coins_result <= 0):
            cam.flag = "lose"

    # check collision with coins
    for coin in coins:
        if coin.collission(cam):
            coins_result += 100
            coins.remove(coin)
            pygame.mixer.Channel(1). play(pygame.mixer.Sound('sounds/coin.ogg'))

    if (coins_result >= 500 and cam.camera_pos[0] >= 21 and cam.camera_pos[2] >= 15):
        cam.flag = "win"
        pygame.mixer.Channel(1).play(pygame.mixer.Sound('sounds/winvoice.ogg'))

    elif (coins_result < 500 and cam.camera_pos[0] >= 21 and cam.camera_pos[2] >= 15):
        cam.flag = "lose"
        pygame.mixer.Channel(1).play(pygame.mixer.Sound('sounds/gameovervoice.ogg'))

    for monster in monsters:
        # check collision with monster and player
        if monster.collission_1(cam):
            while (coins_result > 0):
                coins_result -= 100
                monsters.remove(monster)
                pygame.mixer.Channel(1).play(pygame.mixer.Sound('sounds/hit.ogg'))
                break
            if (coins_result <= 0):
                cam.flag = "lose"
                pygame.mixer.Channel(1).play(pygame.mixer.Sound('sounds/gameovervoice.ogg'))
    return coins_result

