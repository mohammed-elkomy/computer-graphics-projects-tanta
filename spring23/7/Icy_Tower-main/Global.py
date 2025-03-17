
# frastom 
frastom_top = 800
frastom_bottom = 0
frastom_y = 0
g = 9.8
start = False

#ball
squirrel=None
factor = 1
dtime = .1
ball_y_velocity = 0
ball_x_velocity = 0
ball_dir_y = -1
ball_dir_x = 1 #*
land = False #*
jumping = False
moving_up = 16
moving_down = 0
increaseF = True
#keyboard
keystates = [False, False, False, False]
gameover= False
gamestart= False
score = 0
hight_score = 0
# plates
plates = []
stair_step_x = 0
bstart_sound = None
Astart_sound = None
game_over_sound = None


man_fall=['images/fall_left.png','images/fall_right.png']

man_stand=['images/stand_left.png','images/stand_right.png']

man_jump=['images/jump_left.png','images/jump_right.png']

man_path_right=['images/run_right_1.png','images/run_right_2.png',
                'images/run_right_3.png','images/run_right_4.png']

man_path_left=['images/run_left_1.png','images/run_left_2.png',
                'images/run_left_3.png','images/run_left_4.png']

man_path = man_stand[0]


names=[0,1,2,3,4,5,6,7,8,9 ,10,11,12,13,14,15,16,17,18,19]

images=[]
textures=[]
paths=["images/Image AM.jpg","images/gameover.jpg",
        "images/plate.png",'images/startPlay.png',
        'images/hazelnut.png',"images/back ground.jpg",]
index=6
jump_texture=9
stand_left=True
INTERVAL=20