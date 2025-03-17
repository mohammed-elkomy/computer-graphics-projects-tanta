from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import pygame
import numpy as np
from pygame import mixer, image
import sys
from FlagsEnum import *
from random import *
from Main import *
from Class import *

# region Initialization_Variable
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 800
time_interval = 10
AMMO = 10
ENEMY_KILLED = 0
HEALTH = 100  # write 0
mouse = Mouse(WINDOW_HEIGHT)

# Game state
current_Scenes = GameScenes.Main_Menu

# dress color
CurrentColor = ColorOfClothing.Yellow

# Game object
playerWidthFactor = .6
playerHeightFactor = .6
GhostWidth = 104.8
GhostHeight = 98.4
BulletRadius = 20
HealthLength = 120
HealthIconFactor = .15
AmmoIconFactor = .15


player: RECT = RECT(0, 0, 0, 0)
player.MakeRectFromCenter(700, 400, playerWidthFactor, playerHeightFactor)


GhostSpeed = 1.5
BulletSpeed = 5
PlayerSpeed = 2.5
GhostsAppearanceRate = 85
rateCreateHealthIcon = 900
rateCreateAmmoIcon = 500
Ghosts = []
Bullets = []
HealthIcon = []
AmmoIcon = []
CurrentPlayerState = PlayerState.Idel
CurrentPlayerLookTowards = PlayerLooksTowards.Right
wait = 10
wait1 = 0
wait2 = 0
wait3 = wait
# Photo object
texture = ()
img_num_load = [f'pic/Number/{i}.png' for i in range(10)]

PlayerDressYellow = [f'pic/character/left/y/Idel.png', f'pic/character/left/y/Run1.png',
                     f'pic/character/left/y/Run2.png', f'pic/character/left/y/Run3.png',
                     f'pic/character/right/y/Idel.png', f'pic/character/right/y/Run1.png',
                     f'pic/character/right/y/Run2.png', f'pic/character/right/y/Run3.png']
PlayerDressRed = [f'pic/character/left/r/Idel.png', f'pic/character/left/r/Run1.png',
                  f'pic/character/left/r/Run2.png', f'pic/character/left/r/Run3.png',
                  f'pic/character/right/r/Idel.png', f'pic/character/right/r/Run1.png',
                  f'pic/character/right/r/Run2.png', f'pic/character/right/r/Run3.png']
PlayerDressGreen = [f'pic/character/left/g/Idel.png', f'pic/character/left/g/Run1.png',
                    f'pic/character/left/g/Run2.png', f'pic/character/left/g/Run3.png',
                    f'pic/character/right/g/Idel.png', f'pic/character/right/g/Run1.png',
                    f'pic/character/right/g/Run2.png', f'pic/character/right/g/Run3.png']
PlayerDressBlue = [f'pic/character/left/b/Idel.png', f'pic/character/left/b/Run1.png',
                   f'pic/character/left/b/Run2.png', f'pic/character/left/b/Run3.png',
                   f'pic/character/right/b/Idel.png', f'pic/character/right/b/Run1.png',
                   f'pic/character/right/b/Run2.png', f'pic/character/right/b/Run3.png']
photos1 = ['pic\Main Menu.png', 'pic/About.jpg', 'pic/ShowYellowDress.jpg',
           'pic/ShowRedDress.jpg', 'pic/ShowGreenDress.jpg',
           'pic/ShowBlueDress.jpg', 'pic/GameOver.png', 'pic/background.jpg',
           'pic/AmmoWord.png', 'pic/EnemyKilledWord.png', 'pic/Ghost.png', 'pic/AmmoIcon.png',
           'pic/HealthIcon.png']  # 13->12

photos = img_num_load + photos1 + PlayerDressYellow + PlayerDressRed + PlayerDressGreen + PlayerDressBlue

YStart = 10 + len(photos1)
RStart = YStart + 8
GStart = RStart + 8
BStart = GStart + 8

p = len(photos)

# Sound object
CanPlayMenuSound = True
CanPlayGameSound = True
CanPlayGameOverSound = True

# endregion
