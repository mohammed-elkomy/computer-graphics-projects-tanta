import math, numpy as np
from Sounds import *

WINDOW_WIDTH, WINDOW_HEIGHT = 1200, 900


def obstacle_collision(ob, car_pos, car_vel, car_angle, CAR_LENGTH, CAR_WIDTH, game_over):

    ob_width = ob.right - ob.left
    ob_height = ob.top - ob.bottom
    ob_center = np.array([(ob.left + ob.right) / 2, (ob.top + ob.bottom) / 2])
    main_car_center1=np.array([car_pos[0]+CAR_WIDTH/4 * math.cos(math.radians(car_angle[0])),car_pos[1]+CAR_WIDTH/4 * math.sin(math.radians(car_angle[0]))])
    main_car_center2=np.array([car_pos[0]-CAR_WIDTH/4 * math.cos(math.radians(car_angle[0])),car_pos[1]-CAR_WIDTH/4 * math.sin(math.radians(car_angle[0]))])

    dist1 = math.sqrt((ob_center[0]-20 - main_car_center1[0])**2 + (ob_center[1] - main_car_center1[1])**2)
    dist2 = math.sqrt((ob_center[0]+20 - main_car_center2[0])**2 + (ob_center[1] - main_car_center2[1])**2)
    dist3 = math.sqrt((ob_center[0]+20 - main_car_center1[0])**2 + (ob_center[1] - main_car_center1[1])**2)
    dist4 = math.sqrt((ob_center[0]-20 - main_car_center1[0])**2 + (ob_center[1] - main_car_center1[1])**2)
    r=45
    if (dist1 < r or dist2<r or dist3<r or dist4<r ):
        car_pos[0], car_pos[1] = 100, 250
        car_angle[0] = 0
        car_vel[0], car_vel[1] = 0, 0
        game_over[0] += 1

    if game_over[0] == 3:
       game_over[0] = 0
       return True




def wall_collision(car_pos, car_vel, car_angle, CAR_LENGTH, CAR_WIDTH,game_over):
    # Front-side collision
    car_face = car_pos[0] + CAR_WIDTH / 2 * math.cos(math.radians(car_angle[0]))
    car_back = car_pos[0] - CAR_WIDTH / 2 * math.cos(math.radians(car_angle[0]))
    car_top = car_pos[1] + CAR_LENGTH / 2 * math.sin(math.radians(car_angle[0]))
    car_bottom = car_pos[1] - CAR_LENGTH / \
                 2 * math.sin(math.radians(car_angle[0]))

    if car_face >= WINDOW_WIDTH:
        car_vel[0] = -car_vel[0]
        print(car_pos[0])
        car_pos[0] = WINDOW_WIDTH - CAR_WIDTH / 2
    elif car_face <= 0:
        car_vel[0] = -car_vel[0]
        print(car_pos[0])
        car_pos[0] = 0 + CAR_WIDTH / 2
    elif car_top >= WINDOW_HEIGHT:
        car_vel[1] = -car_vel[1]
        car_pos[1] = WINDOW_HEIGHT - CAR_WIDTH / 2

    # face collision to layer 1:
    elif car_top <= 160:
        car_pos[0], car_pos[1] = 100, 250
        car_angle[0] = 0
        car_vel[0], car_vel[1] = 0, 0
        game_over[0] += 1



    # face collision to layer 2
    elif (340 <= car_top <= 360 + 150) and \
            ((car_face <= 650) or (car_face >= 650 + 250)):
        car_pos[0], car_pos[1] = 100, 250
        car_angle[0] = 0
        car_vel[0], car_vel[1] = 0, 0
        game_over[0] += 1


    # face collision to layer 3
    elif (340 + 250 + 100 <= car_top) and \
            ((car_face <= 150) or (400 <= car_face <= 300 + 500) or (1200 - 145 <= car_face)):
        car_pos[0], car_pos[1] = 100, 250
        car_angle[0] = 0
        car_vel[0], car_vel[1] = 0, 0
        game_over[0] += 1


    # Back-side collision
    elif car_back >= WINDOW_WIDTH:
        car_vel[0] = -car_vel[0]
        print(car_pos[0])
        car_pos[0] = WINDOW_WIDTH - CAR_WIDTH / 2
    elif car_back <= 0:
        car_vel[0] = -car_vel[0]
        print(car_pos[0])
        car_pos[0] = 0 + CAR_WIDTH / 2
    elif car_bottom >= WINDOW_HEIGHT:
        car_vel[1] = -car_vel[1]
        car_pos[1] = WINDOW_HEIGHT - CAR_WIDTH / 2

    # back collision to layer 1:
    elif car_bottom <= 160:
        car_pos[0], car_pos[1] = 100, 250
        car_angle[0] = 0
        car_vel[0], car_vel[1] = 0, 0
        game_over[0] += 1

    # back collision to layer 2
    elif (340 <= car_bottom <= 360 + 150) and \
            ((car_back <= 650) or (car_back >= 650 + 250)):
        car_pos[0], car_pos[1] = 100, 250
        car_angle[0] = 0
        car_vel[0], car_vel[1] = 0, 0
        game_over[0] += 1


    # back collision to layer 3
    elif (340 + 250 + 100 <= car_bottom) and \
            ((car_back <= 150) or (400 <= car_back <= 300 + 500) or (1200 - 145 <= car_back)):
        car_pos[0], car_pos[1] = 100, 250
        car_angle[0] = 0
        car_vel[0], car_vel[1] = 0, 0
        game_over[0] += 1

    if game_over[0] == 3:
             game_over[0] = 0
             return True


def arrival_line(car_pos, CAR_LENGTH):
    global WINDOW_HEIGHT
    car_top = car_pos[1] + CAR_LENGTH / 2
    car_bottom = car_pos[1] - CAR_LENGTH / 2

    if WINDOW_HEIGHT - 35 <= car_top:
        car_pos[1] = WINDOW_HEIGHT - 35 - CAR_LENGTH / 2
        win.play()
        return True

    elif WINDOW_HEIGHT - 35 <= car_bottom:
        car_pos[1] = WINDOW_HEIGHT - 35 - CAR_LENGTH / 2
        win.play()
        return True
