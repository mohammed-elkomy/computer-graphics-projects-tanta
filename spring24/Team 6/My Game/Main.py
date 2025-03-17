from Initialization_Variable import *


# region This Region Main Interfaces


def drawMainMenu():
    global WINDOW_WIDTH, WINDOW_HEIGHT
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    startScreen = RECT(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
    startScreen.DrawRectangleWithPhoto(10)


def drawShowYellowDress():
    global WINDOW_WIDTH, WINDOW_HEIGHT, texture
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    startScreen = RECT(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
    startScreen.DrawRectangleWithPhoto(12)


def drawShowRedDress():
    global WINDOW_WIDTH, WINDOW_HEIGHT, texture
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    startScreen = RECT(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
    startScreen.DrawRectangleWithPhoto(13)


def drawShowGreenDress():
    global WINDOW_WIDTH, WINDOW_HEIGHT, texture
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    startScreen = RECT(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
    startScreen.DrawRectangleWithPhoto(14)


def drawShowBlueDress():
    global WINDOW_WIDTH, WINDOW_HEIGHT, texture
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    startScreen = RECT(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
    startScreen.DrawRectangleWithPhoto(15)


def drawAbout():
    global WINDOW_WIDTH, WINDOW_HEIGHT, texture
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    startScreen = RECT(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
    startScreen.DrawRectangleWithPhoto(11)


def drawGameOver():
    global WINDOW_WIDTH, WINDOW_HEIGHT, back
    global current_Scenes, AMMO, ENEMY_KILLED, \
        HEALTH, CurrentColor, Ghosts, mouse, player, fire, Bullets, CanPlayGameSound, CanPlayGameOverSound, \
        HealthIcon, AmmoIcon

    HEALTH = 100
    AMMO = 10
    Ghosts = []
    Bullets = []
    HealthIcon = []
    AmmoIcon = []

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    startScreen = RECT(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
    startScreen.DrawRectangleWithPhoto(16)
    if len(str(ENEMY_KILLED)) == 2:
        show_score(str(ENEMY_KILLED), 828, 524, 40, 60)
    if len(str(ENEMY_KILLED)) == 3:
        show_score(str(ENEMY_KILLED), 828, 524, 25, 60)
    if len(str(ENEMY_KILLED)) == 1:
        show_score(str(ENEMY_KILLED), 850, 524, 60, 60)
    GameOverSound()


# endregion


# region Region For Game


def drawGame():
    global WINDOW_WIDTH, WINDOW_HEIGHT
    global current_Scenes, CurrentColor, fire, Bullets, CurrentPlayerLookTowards, CurrentPlayerState
    global AMMO, ENEMY_KILLED, HEALTH
    BackgroundSoundAtTheGame()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    startScreen = RECT(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
    startScreen.DrawRectangleWithPhoto(17)

    show_AmmoWord(48, 755, 96, 25)
    show_score(str(AMMO), 150, 755)

    show_EnemyKilledWord(125, 720, 250, 25)
    show_score(str(ENEMY_KILLED), 300, 720)

    glColor(1, 1, 1)
    drawCharacter()
    if randrange(1, GhostsAppearanceRate) == 5:
        CreateRandomGhost()

    drawGhost()

    drawHealth()
    drawBullet()
    drawHealthIcon()
    drawAmmoIcon()
    if HEALTH <= .1:
        current_Scenes = GameScenes.Game_Over


def drawHealthIcon():
    global rateCreateHealthIcon, HEALTH, player, HealthIcon, WINDOW_WIDTH, HealthIconFactor
    if randrange(0, rateCreateHealthIcon) == 5:
        newHealthIcon = HealthIcon_Class(WINDOW_WIDTH, HealthIconFactor)
        HealthIcon.append(newHealthIcon)

    for icon in HealthIcon:
        if not CollisionDetection(icon.Rect, player):
            icon.draw()
        else:
            SoundWhenTakeHealthOrAmmo()
            IncreaseHealth()
            HealthIcon.remove(icon)


def drawAmmoIcon():
    global rateCreateAmmoIcon, HEALTH, player, AmmoIcon, WINDOW_WIDTH, AmmoIconFactor
    if randrange(0, rateCreateAmmoIcon) == 5:
        newAmmoIcon = AmmoIcon_Class(WINDOW_WIDTH, AmmoIconFactor)
        AmmoIcon.append(newAmmoIcon)

    for icon in AmmoIcon:
        if not CollisionDetection(icon.Rect, player):
            icon.draw()
        else:
            SoundWhenTakeHealthOrAmmo()
            IncreaseAmmo()
            AmmoIcon.remove(icon)


def IncreaseHealth():
    global HEALTH
    HEALTH += 25
    if HEALTH > 100:
        HEALTH = 100


def decreaseHealth():
    global HEALTH
    HEALTH -= 10
    if HEALTH < 0:
        HEALTH = 0


def IncreaseAmmo():
    global AMMO
    AMMO += 10


def decreaseAmmo():
    global AMMO
    AMMO -= 1
    if AMMO < 0:
        AMMO = 0


def drawHealth():
    global HEALTH, player
    length = HealthLength * (HEALTH / 100)
    tempRect = RECT(0, 0, 0, 0)
    tempRect.MakeRectFromCenter(player.XCenter(), player.YCenter() + 251 * playerHeightFactor / 2 + 10 + 5, length, 10)
    tempRect.DrawRectangle()


def MoveFromTo(centerXTarget, centerYTarget, centerX, centerY, speed):
    targetPosition = np.array([centerXTarget, centerYTarget])
    Position = np.array([centerX, centerY])
    directionToTarget = targetPosition - Position
    magnitude = np.linalg.norm(directionToTarget)
    if magnitude > 0:  # Avoid division by zero
        moveDirection = directionToTarget / magnitude
        velocity = moveDirection * speed
        # Assuming Time.deltaTime is the time elapsed since the last frame update
        deltaTime = 1  # Placeholder value for demonstration
        amountMovement = velocity * deltaTime
        newCenterX = centerX + amountMovement[0]
        newCenterY = centerY + amountMovement[1]
        return newCenterX, newCenterY
    else:
        # If magnitude is zero, no movement is needed
        return centerX, centerY


def MoveFromPlayerToCursor(centerXTarget, centerYTarget, centerX, centerY, speed):
    global CurrentPlayerState, CurrentPlayerLookTowards, player, wait2, wait, wait1, wait3
    if (not ((player.right > centerXTarget > player.left) and (player.top > centerYTarget > player.bottom))):
        if player.bottom > 548:
            return centerX - 1, centerY - 1

        targetPosition = np.array([centerXTarget, centerYTarget])
        Position = np.array([centerX, centerY])
        directionToTarget = targetPosition - Position
        magnitude = np.linalg.norm(directionToTarget)
        if magnitude > 0:
            moveDirection = directionToTarget / magnitude
            velocity = moveDirection * speed
            deltaTime = 1
            amountMovement = velocity * deltaTime
            newCenterX = centerX + amountMovement[0]
            newCenterY = centerY + amountMovement[1]

            if (((CurrentPlayerState == PlayerState.Idel or CurrentPlayerState == PlayerState.Run3) and wait3 == wait)
                    or (CurrentPlayerState == PlayerState.Run1 and wait1 < wait)):
                wait3 = 0
                wait1 += 1
                CurrentPlayerState = PlayerState.Run1
            elif (CurrentPlayerState == PlayerState.Run1 and wait1 == wait) \
                    or (CurrentPlayerState == PlayerState.Run2 and wait2 < wait):
                wait1 = 0
                wait2 += 1
                CurrentPlayerState = PlayerState.Run2
            elif (CurrentPlayerState == PlayerState.Run2 and wait2 == wait) \
                    or (CurrentPlayerState == PlayerState.Run3 and wait3 < wait):
                wait2 = 0
                wait3 += 1
                CurrentPlayerState = PlayerState.Run3

            if centerX < centerXTarget:
                CurrentPlayerLookTowards = PlayerLooksTowards.Right
            elif centerX > centerXTarget:
                CurrentPlayerLookTowards = PlayerLooksTowards.Left
            return newCenterX, newCenterY
    else:
        # If magnitude is zero, no movement is needed
        CurrentPlayerState = PlayerState.Idel
        wait3 = wait
        wait1 = 0
        wait2 = 0
        return centerX, centerY


def MoveFromToByCursor(centerXTarget, centerYTarget, centerX, centerY, speed, xCenterPlayer, yCenterPlayer):
    centerXTarget, centerYTarget = line(centerX, centerY, centerXTarget, centerYTarget, xCenterPlayer, yCenterPlayer)
    targetPosition = np.array([centerXTarget, centerYTarget])
    Position = np.array([centerX, centerY])
    directionToTarget = targetPosition - Position
    magnitude = np.linalg.norm(directionToTarget)
    if magnitude > 0:  # Avoid division by zero
        moveDirection = directionToTarget / magnitude
        velocity = moveDirection * speed
        # Assuming Time.deltaTime is the time elapsed since the last frame update
        deltaTime = 1  # Placeholder value for demonstration
        amountMovement = velocity * deltaTime
        newCenterX = centerX + amountMovement[0]
        newCenterY = centerY + amountMovement[1]
        return newCenterX, newCenterY
    else:
        # If magnitude is zero, no movement is needed
        return centerX, centerY


def CollisionDetection(Shocking, Shocked):
    if (Shocking.left < Shocked.right and Shocking.right > Shocked.left
            and Shocking.bottom < Shocked.top and Shocking.top > Shocked.bottom):
        return True
    return False


def CDGhostVsPlayer(Ghost, Player):
    if CollisionDetection(Ghost.Rect, Player):
        decreaseHealth()
        SoundWhenDamdge()
        return True
    return False


def CDBulletVsGhosts(Bullet, Ghosts):
    global ENEMY_KILLED
    for Ghost in Ghosts:
        if CollisionDetection(Bullet.Rect, Ghost.Rect):
            ENEMY_KILLED += 1
            Ghosts.remove(Ghost)
            return True
    return False


def drawGhost():
    global Ghosts, player, GhostSpeed
    if Ghosts != []:
        glLoadIdentity()
        centerXPlayer = player.XCenter()
        centerYPlayer = player.YCenter()
        for Ghost in Ghosts:
            if not CDGhostVsPlayer(Ghost, player):
                newCenterX, newCenterY = MoveFromTo(centerXPlayer, centerYPlayer, Ghost.Rect.XCenter(),
                                                    Ghost.Rect.YCenter(),
                                                    GhostSpeed)

                Ghost.changeCenter(newCenterX, newCenterY)
                Ghost.draw()
                # Ghost.DrawRectangle()
            else:
                Ghosts.remove(Ghost)


def CreateRandomGhost():
    global Ghosts
    list1 = [i for i in range(601)]
    list2 = [i for i in range(800, 1401)]

    merged_list = list1 + list2
    x = choice(merged_list)
    y = randrange(0, 800)

    list2 = [i for i in range(-700, 0, 1)]
    z = choice(list2) * .00001
    tempGhost = Ghost_Class(z, x, y, GhostWidth, GhostHeight)
    tempGhost.draw()
    Ghosts.append(tempGhost)


def drawCharacter():
    global player, mouse, PlayerSpeed, CurrentPlayerState, CurrentPlayerLookTowards
    glLoadIdentity()
    newCenterX, newCenterY = (MoveFromPlayerToCursor
                              (mouse.x, mouse.y, player.XCenter(),
                               player.YCenter(), PlayerSpeed))

    L = 0
    if CurrentPlayerLookTowards == PlayerLooksTowards.Left:
        L = 0
    else:
        L = 4
    S = 0

    if CurrentPlayerState == PlayerState.Idel:
        S = 0
        player.MakeRectFromCenter(newCenterX, newCenterY, playerWidthFactor * 157, playerHeightFactor * 244)
    elif CurrentPlayerState == PlayerState.Run1:
        S = 1
        player.MakeRectFromCenter(newCenterX, newCenterY, playerWidthFactor * 210, playerHeightFactor * 251)
    elif CurrentPlayerState == PlayerState.Run2:
        S = 2
        player.MakeRectFromCenter(newCenterX, newCenterY, playerWidthFactor * 200, playerHeightFactor * 244)
    else:
        S = 3
        player.MakeRectFromCenter(newCenterX, newCenterY, playerWidthFactor * 273, playerHeightFactor * 244)

    C = 0

    if CurrentColor == ColorOfClothing.Yellow:
        C = YStart
    elif CurrentColor == ColorOfClothing.Red:
        C = RStart
    elif CurrentColor == ColorOfClothing.Green:
        C = GStart
    elif CurrentColor == ColorOfClothing.Blue:
        C = BStart
    k = S + L + C
    player.DrawRectangleWithPhoto(k, -.1)


def CreateBullet(MouseX, MouseY, centerX, centerY):
    global Bullets, AMMO
    decreaseAmmo()
    if AMMO != 0:
        newBullet = Bullet(MouseX, MouseY, centerX, centerY)
        Bullets.append(newBullet)
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.Channel(1).play(pygame.mixer.Sound('Sound effect/FireSound.wav'))


def drawBullet():
    global Bullets, player, BulletSpeed, Ghosts
    if Bullets != []:
        glLoadIdentity()
        for bullet in Bullets:
            if (not CDBulletVsGhosts(bullet, Ghosts)):
                newCenterX, newCenterY = MoveFromToByCursor(bullet.xMouse, bullet.yMouse, bullet.xCenter,
                                                            bullet.yCenter, BulletSpeed, bullet.xCenterPlayer,
                                                            bullet.yCenterPlayer)
                if ((
                        (0 < bullet.Rect.XCenter() < WINDOW_WIDTH) and
                        (0 < bullet.Rect.YCenter() < WINDOW_HEIGHT))):
                    bullet.xCenter = newCenterX
                    bullet.yCenter = newCenterY
                    bullet.Rect.left = newCenterX - BulletRadius
                    bullet.Rect.right = newCenterX + BulletRadius
                    bullet.Rect.top = newCenterY + BulletRadius
                    bullet.Rect.bottom = newCenterY - BulletRadius
                    if (bullet.Rect.right <= player.left + 10 or bullet.Rect.left >= player.right - 10
                            or bullet.Rect.bottom >= player.top - 10 or bullet.Rect.top <= player.bottom + 10):
                        bullet.Rect.DrawCircle(BulletRadius)
                else:
                    Bullets.remove(bullet)
            else:
                Bullets.remove(bullet)


def line(x1, y1, x2, y2, Cx, Cy):
    if x2 > Cx:
        x3 = 180000
    elif x2 < Cx:
        x3 = -100000
    else:  # x2 == 400
        if y2 < Cy:
            y2 = -100000
        elif y2 > Cy:
            y2 = 150000
        else:  # y2 == 250
            y2 = -100000
        return Cx, y2

    y3 = ((y2 - y1) / (x2 - x1)) * (x3 - x2) + y2
    return x3, y3


# endregion


# region  Sound

def displaySound(Path, WorkingOnTopOfAnotherSound):
    # this function take a path and display it
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.Channel(WorkingOnTopOfAnotherSound).play(pygame.mixer.Sound(Path))


def BackgroundSoundAtMenu():
    global CanPlayMenuSound
    if BackgroundSoundAtMenu:
        displaySound('Sound effect/start menu.mp3', 0)
    CanPlayMenuSound = False


def BackgroundSoundAtTheGame():
    global CanPlayGameSound
    if CanPlayGameSound:
        displaySound("Sound effect/BackgroundSoundForGame.wav", 0)  # uncomment this
    CanPlayGameSound = False


def GameOverSound():
    global CanPlayGameOverSound
    if CanPlayGameOverSound:
        displaySound("Sound effect/gameover.wav", 0)
    CanPlayGameOverSound = False


def SoundWhenDamdge():
    displaySound("Sound effect/DamadgeSound.mp3", 1)


def SoundWhenTakeHealthOrAmmo():
    displaySound("Sound effect/SoundWhenTakeHealthOrAmmo.wav", 1)


# endregion


# region Texture And Image Region
def Texture_init():
    load_texture()
    glEnable(GL_BLEND)  # FOR BLENDING
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)  # FOR BLENDING


def load_texture():
    global photos, p
    texture_names = [i for i in range(p)]
    glEnable(GL_TEXTURE_2D)
    images = []
    for i in range(len(photos)):
        images.append(pygame.image.load(photos[i]))

    textures = [pygame.image.tostring(image, "RGBA", True)
                for image in images]

    glGenTextures(len(images), texture_names)

    for i in range(len(images)):
        texture_setup(textures[i],
                      texture_names[i],
                      images[i].get_width(),
                      images[i].get_height())


def texture_setup(texture_image_binary, texture_name, width, height):
    glBindTexture(GL_TEXTURE_2D, texture_name)  # texture init step [5]

    # texture init step [6]
    # affects the active selected texture which is identified by texture_name
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T,
                    GL_REPEAT)  # GL_MIRRORED_REPEAT , GL_CLAMP_TO_EDGE, GL_CLAMP_TO_BORDER
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    # END: texture init step [6]

    glTexImage2D(GL_TEXTURE_2D,
                 0,  # mipmap
                 GL_RGBA,  # FOR BLENDING
                 width, height,
                 0,  # Texture border
                 GL_RGBA,
                 GL_UNSIGNED_BYTE,
                 texture_image_binary)  # texture init step [7]
    glBindTexture(GL_TEXTURE_2D, -1)  # texture init step [5]


def show_score(score, x=300, y=406, width=24, height=24):
    """
    take score as a string and display it.
    """
    glLoadIdentity()
    f = 0
    for n in score:
        temp_rect = RECT(0, 0, 0, 0)
        temp_rect.MakeRectFromCenter(x + f * width, y, width, height)
        temp_rect.DrawRectangleWithPhoto(int(n), -.8)
        f += 1


def show_AmmoWord(x=160, y=406, width=24, height=24):
    temp_rect = RECT(0, 0, 0,
                     0)
    temp_rect.MakeRectFromCenter(x, y, width, height)
    temp_rect.DrawRectangleWithPhoto(18, -.8)


def show_EnemyKilledWord(x=160, y=406, width=24, height=24):
    temp_rect = RECT(0, 0, 0,
                     0)
    temp_rect.MakeRectFromCenter(x, y, width, height)
    temp_rect.DrawRectangleWithPhoto(19, -.8)


# endregion


# region regular implementation


def Display():
    global current_Scenes, s
    if current_Scenes == GameScenes.Main_Menu:
        drawMainMenu()
    elif current_Scenes == GameScenes.Game:
        drawGame()
    elif current_Scenes == GameScenes.ShowYellowDress:
        drawShowYellowDress()
    elif current_Scenes == GameScenes.ShowRedDress:
        drawShowRedDress()

    elif current_Scenes == GameScenes.ShowGreenDress:
        drawShowGreenDress()
    elif current_Scenes == GameScenes.ShowBlueDress:
        drawShowBlueDress()
    elif current_Scenes == GameScenes.About:
        drawAbout()
    elif current_Scenes == GameScenes.Game_Over:
        drawGameOver()

    glutSwapBuffers()


def keyboard(key, x, y):
    global current_Scenes, AMMO, ENEMY_KILLED, \
        HEALTH, CurrentColor, Ghosts, mouse, player, fire, Bullets, s, CanPlayGameSound, CanPlayGameOverSound

    if current_Scenes == GameScenes.Main_Menu:
        if key in [b"Q", b"q"]:
            sys.exit(0)

        if key in [b"P", b"p"]:
            CurrentColor = ColorOfClothing.Yellow
            current_Scenes = GameScenes.ShowYellowDress

        if key in [b"A", b"a"]:
            current_Scenes = GameScenes.About

    if current_Scenes == GameScenes.About:
        if key in [b"B", b"b"]:
            current_Scenes = GameScenes.Main_Menu

    if current_Scenes == GameScenes.Game_Over:
        if key in [b"Q", b"q"]:
            sys.exit(0)
        if key in [b"B", b"b"]:
            CanPlayMenuSound = True
            CanPlayGameSound = True
            CanPlayGameOverSound = True
            ENEMY_KILLED = 0
            BackgroundSoundAtMenu()

            current_Scenes = GameScenes.Main_Menu

    if current_Scenes == GameScenes.Game:
        if key == b"\r":
            CreateBullet(mouse.x, mouse.y, player.XCenter(), player.YCenter())
        if key == b" ":
            CreateBullet(mouse.x, mouse.y, player.XCenter(), player.YCenter())

    # region ShowDress
    if current_Scenes in [GameScenes.ShowYellowDress, GameScenes.ShowRedDress,
                          GameScenes.ShowGreenDress, GameScenes.ShowBlueDress]:
        if key in [b"R", b"r"]:
            CurrentColor = ColorOfClothing.Red
            current_Scenes = GameScenes.ShowRedDress
        if key in [b"G", b"g"]:
            CurrentColor = ColorOfClothing.Green
            current_Scenes = GameScenes.ShowGreenDress
        if key in [b"B", b"b"]:
            CurrentColor = ColorOfClothing.Blue
            current_Scenes = GameScenes.ShowBlueDress
        if key in [b"Y", b"y"]:
            CurrentColor = ColorOfClothing.Yellow
            current_Scenes = GameScenes.ShowYellowDress
        if key in [b"C", b"c"]:
            current_Scenes = GameScenes.Game
    # endregion


def init():
    glClearColor(0, 0.0, 0.0, 0.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT, -1, 1)

    glMatrixMode(GL_MODELVIEW)


def MouseMotion(x, y):
    global mouse
    mouse.x = x
    mouse.y = y


def Timer(v):
    Display()

    glutTimerFunc(time_interval, Timer, 1)


def mouseButton(key, state, xc, yc):
    global current_Scenes, AMMO, ENEMY_KILLED, TextureForDress, \
        HEALTH, CurrentColor, Ghosts, mouse, player, fire, Bullets, s, CanPlayGameSound, CanPlayGameOverSound
    if key == GLUT_LEFT_BUTTON and state == GLUT_DOWN and current_Scenes == GameScenes.Game:
        mouse.x = xc
        mouse.y = yc
        CreateBullet(mouse.x, mouse.y, player.XCenter(), player.YCenter())
        print(f"ym = {mouse.y} xm = {mouse.x}")
    if key == GLUT_LEFT_BUTTON and state == GLUT_DOWN and current_Scenes == GameScenes.Main_Menu:
        mouse.x = xc
        mouse.y = yc
        if 500 <= mouse.x <= 900 and 580 >= mouse.y >= 460:
            CurrentColor = ColorOfClothing.Yellow
            current_Scenes = GameScenes.ShowYellowDress
        elif 380 <= mouse.x <= 1024 and 421 >= mouse.y >= 280:
            current_Scenes = GameScenes.About
        elif 505 <= mouse.x <= 898 and 255 >= mouse.y >= 128:
            sys.exit(0)
    if key == GLUT_LEFT_BUTTON and state == GLUT_DOWN and current_Scenes == GameScenes.About:
        mouse.x = xc
        mouse.y = yc
        if 508 <= mouse.x <= 875 and 116 >= mouse.y >= 62:
            CurrentColor = ColorOfClothing.Yellow
            current_Scenes = GameScenes.Main_Menu
    if key == GLUT_LEFT_BUTTON and state == GLUT_DOWN and current_Scenes == GameScenes.Game_Over:
        mouse.x = xc
        mouse.y = yc
        if 378 <= mouse.x <= 1020 and 419 >= mouse.y >= 291:
            CanPlayMenuSound = True
            CanPlayGameSound = True
            CanPlayGameOverSound = True
            ENEMY_KILLED = 0
            current_Scenes = GameScenes.Main_Menu
            BackgroundSoundAtMenu()
        elif 505 <= mouse.x <= 898 and 255 >= mouse.y >= 124:
            sys.exit(0)

    # region ShowDress
    if current_Scenes in [GameScenes.ShowYellowDress, GameScenes.ShowRedDress,
                          GameScenes.ShowGreenDress,
                          GameScenes.ShowBlueDress] and key == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        if 229 <= mouse.x <= 478 and 241 >= mouse.y >= 203:
            CurrentColor = ColorOfClothing.Green
            current_Scenes = GameScenes.ShowGreenDress
        if 490 <= mouse.x <= 653 and 245 >= mouse.y >= 204:
            CurrentColor = ColorOfClothing.Red
            current_Scenes = GameScenes.ShowRedDress
        if 665 <= mouse.x <= 900 and 244 >= mouse.y >= 203:
            CurrentColor = ColorOfClothing.Yellow
            current_Scenes = GameScenes.ShowYellowDress
        if 913 <= mouse.x <= 1128 and 244 >= mouse.y >= 203:
            CurrentColor = ColorOfClothing.Blue
            current_Scenes = GameScenes.ShowBlueDress
        if 488 <= mouse.x <= 892 and 175 >= mouse.y >= 58:
            current_Scenes = GameScenes.Game
    # endregion


def main():
    glutInit()
    BackgroundSoundAtMenu()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)  # mouse coordinates inbetween [WINDOW_WIDTH=800,WINDOW_HEIGHT=500]
    glutInitWindowPosition(0, 0)
    glutCreateWindow(b"Ghost Killer")
    glEnable(GL_DEPTH_TEST)
    glutDisplayFunc(Display)
    glutTimerFunc(time_interval, Timer, 1)
    glutKeyboardFunc(keyboard)
    glutPassiveMotionFunc(MouseMotion)
    glutMouseFunc(mouseButton)
    init()
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)  # Blend
    glEnable(GL_BLEND)
    glutSetCursor(GLUT_CURSOR_DESTROY)
    Texture_init()
    glutMainLoop()


# endregion


if __name__ == '__main__':
    main()

