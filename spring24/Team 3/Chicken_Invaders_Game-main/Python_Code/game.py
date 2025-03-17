#texture
#generate(chicken,egg,hearts)
# draw-game -->drawing
# update --> moving && collision
#controling -->level-end , game-over

from OpenGL.GL import*
from OpenGL.GLUT import*
import numpy as np
import sys
import random
import pygame

# Define global variables
window_width = 900
window_height = 700
player_x = window_width // 2
player_y = 50
player_speed = 20
chickens = []
chickens2=[]
missiles = []
eggs = []
count = 0
score = 0
level = 1
game_over = False
show_poster = True
game_started = False
heart_score = 2  # Initial heart score
hearts = []  # List to store heart positions
heart_speed = 3.5  # Speed at which hearts fall
heart_width = 20
heart_height = 20

# Chicken properties
chicken_width = 80
chicken_height = 80
chicken_speed = 3

# Missile properties
missile_width = 25
missile_height = 40
missile_speed = 10

# Egg properties
egg_width = 50
egg_height = 55
egg_speed = 2

#next level
level_end = False
rocket_up = -280


# collision
re_draw = False
a = 0
dead = False
start_level = True
theta = 0

# Initialize OpenGL
def init():
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    loadTextures()
    glClearColor(.5, .7, 0.8, 1)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, window_width, 0, window_height, -1, 1)
    glMatrixMode(GL_MODELVIEW)

texture_names = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
def texture_setup(texture_image_binary, texture_name, width, height):
    glBindTexture(GL_TEXTURE_2D, texture_name)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexImage2D(GL_TEXTURE_2D,
                 0,
                 GL_RGBA,
                 width, height,
                 0,
                 GL_RGBA,
                 GL_UNSIGNED_BYTE,
                 texture_image_binary)



def loadTextures():
    glEnable(GL_TEXTURE_2D)
    images = []
    images.append(pygame.image.load("rocket.png"))
    images.append(pygame.image.load("chicken1.png"))
    images.append(pygame.image.load("chicken invaders poster.png"))
    images.append(pygame.image.load("button_play.png"))
    images.append(pygame.image.load("fire3.png"))
    images.append(pygame.image.load("background-1.png"))
    images.append(pygame.image.load("egg.png"))
    images.append(pygame.image.load("game_over.png"))
    images.append(pygame.image.load("heart.png"))
    images.append(pygame.image.load("winner.png"))
    textures = [pygame.image.tostring(image, "RGBA", True)
                for image in images]
    glGenTextures(len(images), texture_names)
    for i in range(len(images)):
        texture_setup(textures[i],
                      texture_names[i],
                      images[i].get_width(),
                      images[i].get_height())

def keyboard(key, x, y):
    global show_poster, game_started, player_x, player_y, missiles, level_end

    if key == b"q":
        sys.exit(0)
    elif key == b"p":  # Press 'p' to toggle play/pause
        if not game_started:
            show_poster = False
            game_started = True
        else:
            show_poster = not show_poster
    elif game_started: # If the game is started
        print("keyboard")
        if key == b'a':  # Left arrow key
            player_x -= player_speed
        elif key == b'd':  # Right arrow key
            player_x += player_speed
        elif key == b'w':  # Up arrow key
            player_y += player_speed
        elif key == b's':  # Down arrow key
            player_y -= player_speed
        elif key == b' ':  # Spacebar to shoot
            missiles.append([player_x + 2.5, player_y + 45])

# Draw player spaceship
def draw_player(a):
    global player_x, player_y
    glColor3f(1, 1, 1)  # Set color to white
    glBindTexture(GL_TEXTURE_2D, texture_names[0])  # Bind player texture
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)
    glVertex2f(player_x - 20, player_y)
    glTexCoord2f(1, 0)
    glVertex2f(player_x + 80, player_y)
    glTexCoord2f(1, 1)
    glVertex2f(player_x + 80, player_y + 80)
    glTexCoord2f(0, 1)
    glVertex2f(player_x - 20, player_y + 80)
    glEnd()
    glBindTexture(GL_TEXTURE_2D, -1)

# Draw a chicken
def draw_circle(x, y, radius):
    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(x, y)
    for i in range(361):
        angle = 2 * 3.14159 * i / 360
        glVertex2f(x + radius * np.cos(angle), y + radius * np.sin(angle))
    glEnd()
def draw_chicken(x, y):
    glColor3f(1.0, 1.0, 1.0)  # Set color to white
    glBindTexture(GL_TEXTURE_2D, texture_names[1])  # Bind chicken texture
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)
    glVertex2f(x - chicken_width / 2, y - chicken_height / 2)
    glTexCoord2f(1, 0)
    glVertex2f(x + chicken_width / 2, y - chicken_height / 2)
    glTexCoord2f(1, 1)
    glVertex2f(x + chicken_width / 2, y + chicken_height / 2)
    glTexCoord2f(0, 1)
    glVertex2f(x - chicken_width / 2, y + chicken_height / 2)
    glEnd()
    glBindTexture(GL_TEXTURE_2D, -1)

# Draw a missile
def draw_missile(x, y):
    glColor3f(1.0, 1.0, 1.0)  # Set color to white
    glBindTexture(GL_TEXTURE_2D, texture_names[4])  # Bind missile texture

    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)
    glVertex2f(x, y)
    glTexCoord2f(1, 0)
    glVertex2f(x + missile_width, y)
    glTexCoord2f(1, 1)
    glVertex2f(x + missile_width, y + missile_height)
    glTexCoord2f(0, 1)
    glVertex2f(x, y + missile_height)
    glEnd()
    glBindTexture(GL_TEXTURE_2D, -1)

def draw_egg(x, y):
    glColor3d(1, 1, 1)
    glBindTexture(GL_TEXTURE_2D, texture_names[6])  # Use egg texture
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)
    glVertex2f(x - egg_width / 2, y - egg_height / 2)
    glTexCoord2f(1, 0)
    glVertex2f(x + egg_width / 2, y - egg_height / 2)
    glTexCoord2f(1, 1)
    glVertex2f(x + egg_width / 2, y + egg_height / 2)
    glTexCoord2f(0, 1)
    glVertex2f(x - egg_width / 2, y + egg_height / 2)
    glEnd()
    glBindTexture(GL_TEXTURE_2D, -1)

def draw_heart(x, y):
    glColor3d(1, 1, 1)
    glBindTexture(GL_TEXTURE_2D, texture_names[8])  # Use heart texture
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)
    glVertex2f(x - heart_width / 2, y - heart_height / 2)
    glTexCoord2f(1, 0)
    glVertex2f(x + heart_width / 2, y - heart_height / 2)
    glTexCoord2f(1, 1)
    glVertex2f(x + heart_width / 2, y + heart_height / 2)
    glTexCoord2f(0, 1)
    glVertex2f(x - heart_width / 2, y + heart_height / 2)
    glEnd()
    glBindTexture(GL_TEXTURE_2D, -1)
def draw_game_background():
    glColor3f(1, 1, 1)
    glBindTexture(GL_TEXTURE_2D, texture_names[5])  # Use the texture for the background
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)
    glVertex2f(0, 0)
    glTexCoord2f(1, 0)
    glVertex2f(window_width, 0)
    glTexCoord2f(1, 1)
    glVertex2f(window_width, window_height)
    glTexCoord2f(0, 1)
    glVertex2f(0, window_height)
    glEnd()
    glBindTexture(GL_TEXTURE_2D, -1)
# Draw game over screen
def draw_Gameover():
    glColor3d(1, 1, 1)
    glBindTexture(GL_TEXTURE_2D, texture_names[7])  # Assuming index 7 corresponds to the "Game Over" texture
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)
    glVertex2f(0, 0)
    glTexCoord2f(1, 0)
    glVertex2f(window_width, 0)
    glTexCoord2f(1, 1)
    glVertex2f(window_width, window_height)
    glTexCoord2f(0, 1)
    glVertex2f(0, window_height)
    glEnd()
    glBindTexture(GL_TEXTURE_2D, -1)

def draw_winner():
    glColor3d(1, 1, 1)
    glBindTexture(GL_TEXTURE_2D, texture_names[9])  # Assuming index 7 corresponds to the "Game Over" texture
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)
    glVertex2f(0, 0)
    glTexCoord2f(1, 0)
    glVertex2f(window_width, 0)
    glTexCoord2f(1, 1)
    glVertex2f(window_width, window_height)
    glTexCoord2f(0, 1)
    glVertex2f(0, window_height)
    glEnd()
    glBindTexture(GL_TEXTURE_2D, -1)

# Draw text on the screen
def drawText(string, x, y ) :
    glColor3f(1.0, 1.0, 1.0)
    glPushMatrix()
    glTranslate(x, y, 0)
    glScale(0.1, 0.1, 1)
    string = string.encode()
    for c in string:
        glutStrokeCharacter(GLUT_STROKE_ROMAN, c)
    glPopMatrix()

# draw poster
def draw_button():
    global show_poster
    glColor3f(1, 1, 1) # Button color
    if show_poster:
        glBindTexture(GL_TEXTURE_2D, texture_names[3])
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0)
        glVertex2f(200, 270)
        glTexCoord2f(1, 0)
        glVertex2f(290, 270)
        glTexCoord2f(1, 1)
        glVertex2f(290, 320)
        glTexCoord2f(0, 1)
        glVertex2f(200, 320)
        glEnd()
        glBindTexture(GL_TEXTURE_2D, -1)

def generate_hearts():
    global hearts
    hearts = [[random.randint(20, window_width - 20), window_height] for _ in range(1)]
def generate_chickens():
    global chickens, chickens2
    if level == 1:
        chickens = [[random.randint(50, 500), random.randint(250, 550)] for _ in range(10)]
    if level == 2:
        chickens = [[x, x + 300] for x in range(-300, 120, 60)]
        chickens2 = [[x, -x + 1100] for x in range(1100, 680, -60)]
    if level == 3:
        chickens = [[250*np.cos(x*3.14/180)+400, 250*np.sin(x*3.14/180)+400] for x in range(0, 360, 20)]

def generate_eggs():
    global eggs, chickens
    k = random.randint(1, 4)
    for i in range(k):
        if len(chickens) != 0:
            chicken = random.choice(chickens)
            eggs.append([chicken[0], chicken[1]])

def next_level():
    global rocket_up, level_end, level, player_x, player_y, dead, start_level, winner_sound


    if level_end and level != 4:
        glClear(GL_COLOR_BUFFER_BIT)
        #for increasing speed
        rocket_up += 10
        glBindTexture(GL_TEXTURE_2D, texture_names[0])  # Assuming index 9 corresponds to the rocket up texture
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0)
        glVertex2f(350, -100 + rocket_up)
        glTexCoord2f(1, 0)
        glVertex2f(450, -100 + rocket_up)
        glTexCoord2f(1, 1)
        glVertex2f(450, 100 + rocket_up)
        glTexCoord2f(0, 1)
        glVertex2f(350, 100 + rocket_up)
        glEnd()
        glBindTexture(GL_TEXTURE_2D, -1)
        print(rocket_up)
        winner_sound.play()
    if rocket_up >= window_height+100:
        level += 1
        start_level = True
        rocket_up = -280
        level_end = False
def end_game():
    global game_over
    if game_over:
        glClear(GL_COLOR_BUFFER_BIT)
        draw_Gameover()

def winner():
    if level == 4:
        draw_winner()
# Display function
def draw_game():
    glClear(GL_COLOR_BUFFER_BIT)
    global level_end, count, eggs, chickens2, a, game_over, start_level
    draw_game_background()
    # Draw hearts
    for heart in hearts:
        draw_heart(heart[0], heart[1])

    if show_poster:
        glColor3f(1, 1, 1)
        glBindTexture(GL_TEXTURE_2D, texture_names[2])
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0)
        glVertex2f(0, 0)
        glTexCoord2f(1, 0)
        glVertex2f(window_width, 0)
        glTexCoord2f(1, 1)
        glVertex2f(window_width, window_height)
        glTexCoord2f(0, 1)
        glVertex2f(0, window_height)
        glEnd()
        glBindTexture(GL_TEXTURE_2D, -1)
        draw_button()
    print(a)
    if not level_end and not show_poster and level != 4:
        draw_player(a)
        if start_level:
            generate_chickens()
            generate_hearts()
            start_level = False
        for chicken in chickens:
            draw_chicken(chicken[0], chicken[1])
        if level == 2:
            for chicken in chickens2:
                draw_chicken(chicken[0], chicken[1])

        for missile in missiles:
            draw_missile(missile[0], missile[1])
        # delay
        if count >= 350:
            eggs = []
            generate_eggs()
            count = 0

        for egg in eggs:
            draw_egg(egg[0], egg[1])

        count += 1

        drawText("Score: " + str(score), 10, window_height - 30)
        drawText("Level: " + str(level), window_width - 150, window_height - 30)
        drawText("Score heart: " + str(heart_score), 10, window_height - 50)

        if game_over:
            end_game()

    if len(chickens) == 0 and len(chickens2) == 0 and not show_poster:
        print("ok")
        level_end = True
        next_level()

    if level == 4:
        winner()
    glutSwapBuffers()



# Update function
def update(value):
    global player_x, chickens, missiles, eggs, score, level, game_over, chicken_speed,level_end,chickens2,re_draw,a,show_poster,heart_score,hearts,heart_speed,theta,player_y
    # Move hearts
    for heart in hearts:
        heart[1] -= heart_speed

    # Check for heart collection
    for heart in hearts:
        if player_x + 30 >= heart[0] - heart_width / 2 and player_x - 30 <= heart[0] + heart_width / 2 and \
                player_y + 80 >= heart[1] - heart_height / 2 and player_y <= heart[1] + heart_height / 2:
            hearts.remove(heart)
            heart_score += 1


    # Move chickens
    if level == 1:
        for chicken in chickens:
            chicken[0] += chicken_speed
            # chicken and wall
            if chicken[0] >= window_width - chicken_width / 2 or chicken[0] <= chicken_width / 2:
                chicken_speed = -chicken_speed
            # chicken && player collision
            if chicken[0] - 20 - chicken_width // 2 <= player_x <= chicken[
                0] + 80 + chicken_width // 2 and player_y + 80 >= chicken[1] - chicken_height // 2 and player_y <= \
                    chicken[1] + chicken_height // 2:
                for i in range(100):
                    player_x -= 1
                    player_y -= 1
                heart_score -= 1
                if heart_score <= 0:
                    game_over = True

    if level == 2:
        for chicken in chickens:
            if chickens[0][0] >= 200:
                chicken_speed = 0
            else:
                chicken_speed = 5
            if chicken[1] <= 500:
                chicken[0] += chicken_speed
                chicken[1] += chicken_speed
            else:
                chicken[0] += chicken_speed

            if chicken[0] - 20 - chicken_width // 2 <= player_x <= chicken[
                0] + 80 + chicken_width // 2 and player_y + 80 >= chicken[1] - chicken_height // 2 and player_y <= \
                    chicken[1] + chicken_height // 2:
                for i in range(100):
                    player_x -= 1
                    player_y -= 1
                heart_score -= 1
                if heart_score <= 0:
                    game_over = True

        for chicken in chickens2:
            if chickens2[0][0] <= 540:
                chicken_speed = 0
            else:
                chicken_speed = 5
            if chicken[1] <= 400:
                chicken[0] -= chicken_speed
                chicken[1] += chicken_speed
            else:
                chicken[0] -= chicken_speed
            if chicken[0] - 20 - chicken_width // 2 <= player_x <= chicken[
                0] + 80 + chicken_width // 2 and player_y + 80 >= chicken[1] - chicken_height // 2 and player_y <= \
                    chicken[1] + chicken_height // 2:
                for i in range(100):
                    player_x -= 1
                    player_y -= 1
                heart_score -= 1
                if heart_score <= 0:
                    game_over = True
    if level == 3:
        # moving
        for chicken in chickens:
            if (chicken[0] - 400) > 0 and (chicken[1] - 400) > 0:
                theta = np.arctan((chicken[1] - 400) / (chicken[0] - 400)) * (180 / 3.14)
                print(1)
            elif (chicken[0] - 400) < 0 and (chicken[1] -400) > 0:
                theta = 180 - (np.arctan((chicken[1] - 400) / -(chicken[0] - 400)) * (180 / 3.14))
                print(2)
            elif (chicken[0] - 400) < 0 and (chicken[1] - 400) < 0:
                theta = 180 + (np.arctan(-(chicken[1] - 400) / -(chicken[0] - 400)) * (180 / 3.14))
                print(3)
            elif (chicken[0] - 400) > 0 and (chicken[1] - 400) < 0:
                theta = 360 - (np.arctan(-(chicken[1] - 400) / (chicken[0] - 400)) * (180 / 3.14))
                print(4)
            theta += 1
            chicken[0] = 250 * np.cos(theta * (3.14 / 180)) + 400
            chicken[1] = 250 * np.sin(theta * (3.14 / 180)) + 400
            if chicken[0] - 20 - chicken_width // 2 <= player_x <= chicken[
                0] + 80 + chicken_width // 2 and player_y + 80 >= chicken[1] - chicken_height // 2 and player_y <= \
                    chicken[1] + chicken_height // 2:
                for i in range(100):
                    player_x -= 1
                    player_y -= 1
                heart_score -= 1
                if heart_score <= 0:
                    game_over = True
    # Move missiles
    for missile in missiles:
        missile[1] += missile_speed

    # Move eggs
    for egg in eggs:
        egg[1] -= egg_speed
        # collision egg &&player
        if player_y <= egg[1] + egg_height // 2 and \
                player_y + 80 >= egg[1] - egg_height // 2 and \
                player_x + 30 >= egg[0] - egg_width // 2 and \
                player_x - 20 <= egg[0] + egg_width // 2:
            eggs.remove(egg)
            heart_score -= 1
            if heart_score <= 0:
                game_over = True

    # Check for missile-chicken collisions
    for missile in missiles:
        for chicken in chickens:  # edit
            if missile[0] < chicken[0] + chicken_width // 2 and \
                    missile[0] + missile_width > chicken[0] - chicken_width and \
                    chicken[1] + chicken_height // 2 >= missile[1] + missile_height >= chicken[1] - chicken_height // 2:
                chickens.remove(chicken)
                score += 10
        for chicken in chickens2:
            if missile[0] < chicken[0] + chicken_width // 2 and \
                    missile[0] + missile_width > chicken[0] - chicken_width and \
                    chicken[1] + chicken_height // 2 >= missile[1] + missile_height >= chicken[1] - chicken_height // 2:
                chickens2.remove(chicken)
                score += 10

    if game_over:
        game_over_sound.play()

    glutPostRedisplay()
    glutTimerFunc(20, update, 0)

# Main function
def main():
    global chickens, eggs,  background_sound,  winner_sound, game_over_sound, game_over
    import pygame.mixer

    # Initialize pygame mixer
    pygame.mixer.init()

    # Load sound files
    background_sound = pygame.mixer.Sound("Backgroundsound.mp3")
    winner_sound = pygame.mixer.Sound("Chicken Invaders 4 OST Mission Complete.mp3")
    game_over_sound = pygame.mixer.Sound("Chicken Invaders 4 OST Game Over.mp3")

    # Set volume for each sound
    background_sound.set_volume(0.1)
    winner_sound.set_volume(0.6)
    game_over_sound.set_volume(1)
    # In your main function, start playing the background sound
    background_sound.play(-1)  # -1 plays the sound indefinitely

    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(window_width, window_height)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Chicken Invaders")
    glutDisplayFunc(draw_game)
    glutTimerFunc(1, update, 0)
    glutKeyboardFunc(keyboard)
    init()
    glutMainLoop()

if __name__ == "__main__":
    main()

#finally ....what should we do ?
#motion with keyboard done
# some editing in texture >>
# collision chicken with rocket done
# add sound done
