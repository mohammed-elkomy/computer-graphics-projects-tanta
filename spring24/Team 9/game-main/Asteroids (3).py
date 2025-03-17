from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random, time
import math
import pygame


class Texture:
    def my_init(self):
        self.loadTextures(Texture)

    texture_names = [0,1,2,3]  # TODO IMPORTANT must be numbers

    def texture_setup(texture_image_binary, texture_name, width, height):
        glBindTexture(GL_TEXTURE_2D, texture_name)  
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)  # GL_MIRRORED_REPEAT , GL_CLAMP_TO_EDGE, GL_CLAMP_TO_BORDER
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexImage2D(GL_TEXTURE_2D,
                    0,  # mipmap
                    3,  # Bytes per pixel
                    width, height,
                    0,  # Texture border
                    GL_RGBA,  # RGBA Exactly as in  pygame.image.tostring(image, "RGBA", True)
                    GL_UNSIGNED_BYTE,
                    texture_image_binary)  # texture init step [7]

    def loadTextures(self):
        glEnable(GL_TEXTURE_2D) 
        images = []  
        images.append(pygame.image.load("background.jpeg"))  
        images.append(pygame.image.load("R.jpeg"))
        images.append(pygame.image.load("conner.jpeg")) 
        images.append(pygame.image.load("help.jpeg"))  
        textures = [pygame.image.tostring(image, "RGBA", True) # TODO change True to False
                    for image in images] 
        glGenTextures(len(images), self.texture_names)  
        for i in range(len(images)):
            self.texture_setup(textures[i],  # binary images
                        self.texture_names[i],  # identifiers
                        images[i].get_width(),
                        images[i].get_height())
    def draw(self):
        glBindTexture(GL_TEXTURE_2D, self.texture_names[0])  # repeat this if you want to bind another texture
        glBegin(GL_QUADS)
        glTexCoord2f(0, 1)  # TODO IMPORTANT: glTexCoord2f must come first before glVertex2d
        glVertex2d(-9, 5)

        glTexCoord2f(1, 1)
        glVertex2d(9, 5)

        glTexCoord2f(1.0, 0)
        glVertex2d(9, -5)

        glTexCoord2f(0, 0)
        glVertex2d(-9, -5)

        glEnd()
class gameState:
    currentState = 1
    playing = 0
    start = 1
    reset = 2
    gameover = 3
    clickedP = False

    def updateState():
        if gameState.currentState == gameState.start:
            Text.drawString(" SPACE   GAME", 1500, 1850, 0.6, 5)
            Text.drawString("  PRESS  => ( P )  TO  PLAY ", 3250, 1650, 0.2, 5)
            Text.drawString(" PRESS  => (E S C) TO  EXIT", 3150, 3450, 0.2, 4)
            Text.drawString("CREDITS", 400, 850, 0.1, 2, 2)
            Text.drawString("TEAM_9 ", 400, 650, 0.1, 2, 2)
            spawnHelpers.draw()
            Texture.draw(Texture)
            

            if gameState.clickedP:
                gameState.currentState = gameState.reset
                gameState.clickedP = False
                

        elif gameState.currentState == gameState.gameover:
            Texture.draw(Texture)
            Score.updateMax()
            Text.drawString(" GAME OVER", 1530, 1850, 0.4, 5)
            Text.drawString(" YOUR SCORE IS :  " + str(Score.currentScore), 1500, 1550, 0.4, 4)
            Text.drawString(" HIGHEST SCORE :  " + str(Score.maxScore), 1500, 1350, 0.4, 4)
            Text.drawString("   PRESS => ( P ) TO  PLAY  AGAIN ", 2750, 1650, 0.2, 4)
            Text.drawString("   PRESS =>( E S C ) TO  EXIT ", 3050, 1350, 0.2, 4)
            
            if gameState.clickedP == True:
                gameState.currentState = gameState.reset
                gameState.clickedP = False

        elif gameState.currentState == gameState.reset:
            spawnBlocks.reset()
            spawnHelpers.reset()
            Player.reset()
            Score.resetCurrent()
            Lives.reset()
            gameState.currentState = gameState.playing


        elif gameState.currentState == gameState.playing:
            Texture.draw(Texture)
            Player.draw()
            Player.shootBullets()
            spawnBlocks.draw()
            spawnHelpers.draw()
            Score.updateScore()
            Lives.updateLives()


class Block:
    playerPosition = []
    x = y = z = killZ = 0
    kill  = bulletCollided = split  = False
    leftCollided =  bottomCollided =False
    visible = True
    scaleFactor = 1
    rotation = 0
    blockSpeed = .03
    def __init__(self,playerX, playerY, x, y, z, scaleFactor):
        self.playerPosition = [playerX, playerY]
        self.x = x
        self.y = y
        self.z = z
        self.scaleFactor = scaleFactor
        
    def blockShape(self):
        glBindTexture(GL_TEXTURE_2D, Texture.texture_names[1])  
        glBegin(GL_TRIANGLE_FAN)
        for i in range(360):
                x = 0.5 * math.cos(i)
                y = 0.5 * math.sin(i)
                glTexCoord2f((x + 1) / 2, (y + 1) / 2) 
                glVertex2f(x, y)  # Vertex on the circle
        glEnd()

    def updateMovement(self):
        if self.scaleFactor <= 1 :
            self.blockSpeed = .01
        if self.x <= -4 :
            self.leftCollided =True
        elif self.x >= 4 :
            self.leftCollided =False
        elif self.y >= 2 or (self.scaleFactor >= 2 and self.y >= 0.5):
            self.bottomCollided =False
        elif self.y <= -2 :
            self.bottomCollided =True

        if self.bottomCollided :
            self.y += self.blockSpeed
        if not self.bottomCollided :
            self.y -= self.blockSpeed
        if self.leftCollided :
            self.x += self.blockSpeed
        if not self.leftCollided :
            self.x -= self.blockSpeed
            
    def draw(self):
        
        if self.visible:
            self.updateMovement()
            self.killAnimation()

            if Player.visible:
                if not self.bulletCollided:
                    self.detectBulletsCollision()
                    self.splitBlock()
                if Player.collided:
                    now = time.time()
                    if now - Player.collisionTime >= 2:
                        Player.collided = False
                else:
                    self.detectPlayerCollision()

            glPushMatrix()
            glLoadIdentity()
            glColor(1,1,1,1)
            glTranslate(0, 0, self.killZ)
            glTranslate(self.x, self.y, self.z)
            glScale(self.scaleFactor, self.scaleFactor, 0)
            glScale(0.1, 0.1, 0)
            self.blockShape()
            
            glPopMatrix()

    def detectBulletsCollision(self):
        for bullet in Player.renderedBullets:
            distance = math.sqrt((bullet.bulletPosition[0] - self.x)**2 + \
                                 (bullet.bulletPosition[1] - self.y)**2)
            if distance <= 0.15*self.scaleFactor:
                self.bulletCollided = True
                bullet.visible = False

                self.split = True
                Score.currentScore += 1
                

    
    def detectPlayerCollision(self):
        distance = math.sqrt((Player.xPos - self.x)**2 + (Player.yPos - self.y)**2)

        if distance <= 0.15*self.scaleFactor or \
          (distance <= 0.15 and self.scaleFactor < 1):

            Player.collisionTime = time.time()
            Player.collided = True
            Player.gradientUp = True
            Lives.totalLives -= 1
            if Lives.totalLives == 0:
                Player.kill = True
                gameState.currentState = gameState.gameover


    def killAnimation(self):
        if self.kill:
            self.scaleFactor -= 0.1
            if self.scaleFactor <= 0:
                self.visible = False
                self.kill = False
                

    def splitBlock(self):
        if self.split:
            if self.scaleFactor >=1:
                self.scaleFactor *= 0.5
                newBlock = Block(Player.xPos, Player.yPos,
                                 self.x + 0.2, self.y + 0.3,
                                 self.z, self.scaleFactor)
                
                spawnBlocks.spawned.append(newBlock)
                self.split = False
                self.bulletCollided = False
            else:
                self.split = False
                self.kill = True


class spawnBlocks:
    blocksNumber = 15
    spawned = []
    spawnTime = time.time()
    def init():
        for i in range(spawnBlocks.blocksNumber):
            block = Block(Player.xPos, Player.yPos,random.randrange(-4, 4),2,Player.zPos, random.randrange(1, 2,1))
            spawnBlocks.spawned.append(block)

        for i in range(spawnBlocks.blocksNumber//3):
            block = Block(Player.xPos, Player.yPos,random.randrange(-7, 4),random.randrange(1, 2,1) ,Player.zPos, random.randrange(1, 3,1) )
            spawnBlocks.spawned.append(block)
            
        for i in range(spawnBlocks.blocksNumber//3):
            block = Block(Player.xPos, Player.yPos,random.randrange(-4, 4),random.randrange(1, 2,1) ,Player.zPos, random.randrange(1, 5,1) )
            spawnBlocks.spawned.append(block)

    def draw():
        for block in spawnBlocks.spawned:
            block.draw()

        newTime = time.time()
        if newTime - spawnBlocks.spawnTime >= random.randint(15,60):
            Block.blockSpeed += .00088
            spawnBlocks.spawnTime = newTime
            spawnBlocks.init()
        
    def reset():
        spawnBlocks.spawned.clear()
        spawnBlocks.spawnTime = time.time()
        spawnBlocks.init()

class Helper:
    playerPosition = []
    x = y = z = killZ = kill = 0
    visible = True
    scaleFactor = 1
    def __init__(self,playerX, playerY, x, y, z, scaleFactor=1):
        self.playerPosition = [playerX, playerY]
        self.x = x
        self.y = y
        self.z = z
        self.scaleFactor = scaleFactor
        
    def helperShape(self):
    #   glColor(1,0,1)
      glBindTexture(GL_TEXTURE_2D, Texture.texture_names[3])
      glBegin(GL_TRIANGLE_FAN)
      num_segments = 30
      radius = 0.5
      for i in range(num_segments):
        angle = i * (2 * math.pi) / num_segments
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        glTexCoord2f((x + 1) / 2, (y + 1) / 2)  # Map circle coordinates to texture coordinates
        glVertex2f(x, y)  # Vertex on the circle
      glEnd()

      # Draw cross
      glColor(1, 1, 1, 1)  # White color
      glBegin(GL_LINES)
      glVertex2f(0, -radius)
      glVertex2f(0, radius)
      glVertex2f(-radius, 0)
      glVertex2f(radius, 0)
      glEnd()

    def updateMovement(self):
        self.y -= 0.02
        
    def draw(self):
        
        if self.visible:
            self.updateMovement()
            self.killAnimation()

            if Player.visible:
                if Player.collided:
                    
                    now = time.time()
                    if now - Player.collisionTime >= 1:
                        Player.collided = False
                else:
                    self.detectPlayerCollision()

            glPushMatrix()
            glLoadIdentity()
            glColor(1,1,1,1)
            glTranslate(0, 0, self.killZ)
            glTranslate(self.x, self.y, self.z)
            glScale(self.scaleFactor, self.scaleFactor, 0)
            glScale(0.2, 0.2, 0)
            self.helperShape()
            glPopMatrix()

    def detectPlayerCollision(self):
        distance = math.sqrt((Player.xPos - self.x)**2 + (Player.yPos - self.y)**2)
        if distance <= 0.15*self.scaleFactor or \
            (distance <= 0.15 and self.scaleFactor < 1):
            Player.collisionTime = time.time()
            Player.collided = True
            self.visible = False
            
            if Lives.totalLives < 3:
                Lives.totalLives += 1
            elif Bullet.bulletNumber < 4 :
                Bullet.bulletNumber += 1

    def killAnimation(self):
        if self.kill:
            self.scaleFactor -= 0.1
            if self.scaleFactor <= 0:
                self.visible = False
                self.kill = False
                

class spawnHelpers:
    helpersNumber = 2
    spawned = []
    spawnTime = time.time()
    def init():
        for _ in range(spawnHelpers.helpersNumber):
            helper = Helper(Player.xPos, Player.yPos,random.randrange(-4, 4,1),random.randrange(0, 2,1),Player.zPos, 1)
            spawnHelpers.spawned.append(helper)

    def draw():
        newTime = time.time()
        for helper in spawnHelpers.spawned:
                helper.draw()
        if newTime - spawnHelpers.spawnTime >= random.randint(30,60):
            spawnHelpers.spawnTime = newTime
            spawnHelpers.init()
            
        
    def reset():
        spawnHelpers.spawned.clear()
        spawnHelpers.spawnTime = time.time()
        spawnHelpers.init()

class Bullet:
    firePosition = bulletPosition = [0, 0]
    speed = 0.05
    visible = False
    bulletNumber =1
    def __init__(self, x, y, z):
        self.firePosition = [x, y]
        self.z = z
        self.visible = True
    def updateMovement(self, step = 0.05):
        self.firePosition[0] += 0 
        self.firePosition[1] += step 
        self.bulletPosition = self.firePosition

        distance = math.sqrt((self.bulletPosition[0] - Player.xPos)**2 + 
                             (self.bulletPosition[1] - Player.yPos)**2 )
        if distance >= 9: #longest path
            self.visible = False

    def draw(self,pos=0):
        if self.visible:
            self.updateMovement(self.speed)

            glPushMatrix()
            glLoadIdentity()

            glColor(1,1-Player.redColor,1-Player.redColor,1)
            
            glTranslate(self.bulletPosition[0]+pos, self.bulletPosition[1] ,self.z-0.1)
            glutSolidCube(0.03)

            glPopMatrix()
        else:
            # throws bullets away
            self.firePosition[0] = 100
            self.firePosition[1] = 100

class Display:
   
    width = 1280
    height = 720
    title = b"SPACE GAME "
    FPS = 200
    fullScreen = False
    def init():
        glutInit()
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
        glutInitWindowSize(Display.width, Display.height)
        glutCreateWindow(Display.title)

        glutSetCursor(GLUT_CURSOR_CROSSHAIR)
        
        glutDisplayFunc(render)
        
        glutPassiveMotionFunc(handleMouse)
        glutMouseFunc(mouseButtonCallback)
        glutKeyboardFunc(handleKeyboard)

        Display.perspectiveProjection()
        Display.setCamera()

    def perspectiveProjection():
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(50,Display.width/Display.height, 1, 100)
        glMatrixMode(GL_MODELVIEW)

    def orthographicProjection():
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, Display.width, 0, Display.height)
        glMatrixMode(GL_MODELVIEW)
    
    def setCamera():
        glLoadIdentity()
        gluLookAt(0, 0, 10,
                  0, 0, -5,
                  0, 1, 0 )

class Score:
    currentScore = maxScore = 0

    def updateScore():
        Text.drawString("Score : ", 300, 3200, 0.3)
        Text.drawString(str(Score.currentScore), 900, 3200, 0.3)
        Text.drawString("HIGH SCORE : ",610,6100,0.15)
        Text.drawString(str(Score.maxScore),1700,6100,0.15)

    def updateMax():
        Score.maxScore = max(Score.maxScore,Score.currentScore)
    
    def resetCurrent():
        Score.currentScore = 0

class Text:
    def drawString(text, xPos, yPos, scaleFactor, lineWidth = 2, fontID = 1):
        
        scaleFactor *= Display.width/1920
        text_encoded = text.encode()
        glLineWidth(lineWidth)

        glColor(1, 1, 1, 1)  # Set text color to whitep
        Display.orthographicProjection()
        glPushMatrix()
        glLoadIdentity()
        # glDisable(GL_TEXTURE_2D)
        glScale(scaleFactor,scaleFactor,1)
        glTranslate(xPos, yPos, 1) 
        
        if fontID == 1:
            glutStrokeString(GLUT_STROKE_ROMAN, text_encoded)
        else:
            glutStrokeString(GLUT_STROKE_MONO_ROMAN, text_encoded)

        Display.perspectiveProjection()
        glPopMatrix()

class Lives:
    totalLives = 3

    def updateLives():
        Text.drawString("Lives : ", 575, 5400, 0.16)

    def reset():
        Lives.totalLives = 3 

def handleMouse(x, y):
    mouseX = x
    mouseX -= Display.width/2
    mouseX *= (8/(Display.width))
    Player.xPos = mouseX
    if Player.xPos >= 4.5:
        Player.xPos -=  9

def mouseButtonCallback(button, state, x, y):
    now = time.time()
    if button == GLUT_LEFT_BUTTON and state != GLUT_UP and now - Player.lastShotTime >= Player.fireRate:
        Player.newBullet()
        Player.lastShotTime = now
        if Player.spaceNotification:
            Player.spaceNotification = False

def handleKeyboard(key, x, y):
    now = time.time()

    if key == b' ' and now - Player.lastShotTime >= Player.fireRate:
        Player.newBullet()
        
        Player.lastShotTime = now
        if Player.spaceNotification:
            Player.spaceNotification = False

    elif key == b"p" or key == b"P":
        if gameState.currentState != gameState.playing:
            gameState.clickedP = True

    elif key == b"\x1b": #escape button
        sys.exit(0)

class Player:
    firedBullets = []
    renderedBullets = []
    zPos = -5
    xPos = 0
    yPos = -4.5
    nextPositionX = 0
    fireRate = 0.1 #in seconds
    lastShotTime = 0
    kill = gradientUp = gradientDown = collided = False           
    visible = False
    scaleFactor = 1
    redColor = 0
    collisionTime = 0
    spaceNotification = True
    def init():
        glBindTexture(GL_TEXTURE_2D, Texture.texture_names[2]) 
        # Barrel
        glColor3f(0.3, 0.3, 0.3)  # Gray color for the barrel
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0)
        glVertex3f(-0.1, -0.1, 0)
        glTexCoord2f(1, 0)
        glVertex3f(0.1, -0.1, 0)
        glTexCoord2f(1, 1)
        glVertex3f(0.1, .6, 0)
        glTexCoord2f(0, 1)
        glVertex3f(-0.1, 0.6, 0)
        glEnd()
        glBindTexture(GL_TEXTURE_2D, Texture.texture_names[2]) 
        # Base
        glColor3f(0.5, 0.5, 0.5)  # Gray color for the base
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0)
        glVertex3f(-0.3, -0.2, 0)
        glTexCoord2f(1, 0)
        glVertex3f(0.3, -0.2, 0)
        glTexCoord2f(1, 1)
        glVertex3f(0.3, 0.0, 0)
        glTexCoord2f(0, 1)
        glVertex3f(-0.3, 0.0, 0)
        glEnd()
        glBindTexture(GL_TEXTURE_2D, Texture.texture_names[2]) 
        # Wheels
        glColor3f(0.2, 0.2, 0.2)  # Dark gray color for the wheels
        glBegin(GL_QUADS)
        glVertex3f(-0.25, -0.3, 0)
        glVertex3f(-0.15, -0.3, 0)
        glVertex3f(-0.15, -0.2, 0)
        glVertex3f(-0.25, -0.2, 0)

        glVertex3f(0.15, -0.3, 0)
        glVertex3f(0.25, -0.3, 0)
        glVertex3f(0.25, -0.2, 0)
        glVertex3f(0.15, -0.2, 0)
        glEnd()

    def draw():
        if Player.visible:
            Player.drawLives()
            Player.notifyPlayer()
            Player.killPlayer()
            Player.gradientAnimation()
            glPushMatrix()
            glLoadIdentity()
            glTranslate(Player.xPos, Player.yPos, Player.zPos)
            glRotate(Player.rot_angle, 0, 0, 1)
            glScale(0.4, 0.4, 0.4)
            glScale(Player.scaleFactor, Player.scaleFactor, 0)
            Player.init()
            glPopMatrix()

    def newBullet():
        newBullet = Bullet(Player.xPos, Player.yPos+0.02, Player.zPos)
        Player.firedBullets.append(newBullet)
        Player.renderedBullets = [bullet for bullet in Player.firedBullets \
                                                            if bullet.visible]
        Player.firedBullets = Player.renderedBullets

    def shootBullets():
        for bullet in Player.renderedBullets:
            if Bullet.bulletNumber == 1 :
                bullet.draw(0)
            if Bullet.bulletNumber == 2 :
                bullet.draw(-.02)
                bullet.draw(.02)
            if Bullet.bulletNumber == 3 :
                bullet.draw(-.03)
                bullet.draw(0)
                bullet.draw(.03)
            if Bullet.bulletNumber == 4:
                bullet.draw(-.05)
                bullet.draw(0.02)
                bullet.draw(-0.02)
                bullet.draw(.05)
    
    def killPlayer():
        if Player.kill:
            Player.scaleFactor -= 0.1
            if Player.scaleFactor <= 0:
                Player.kill = False
                Player.visible = False
                gameState.currentState = gameState.gameover

    def notifyPlayer():
        if Player.spaceNotification:
            Text.drawString("PRESS SPACE TO SHOOT ", 7500, 200, 0.2)

    def gradientAnimation():
        if Player.gradientUp:
            Player.redColor += 0.025
            if Player.redColor >= 0.8:
                Player.gradientDown = True
                Player.gradientUp = False
        if Player.gradientDown:
            Player.redColor -= 0.025
            if Player.redColor <= 0 :
                Player.gradientDown = False
                Player.gradientUp = False

    def drawLives():
        for i in range(Lives.totalLives):
            glPushMatrix()
            glLoadIdentity()
            glTranslate(-3.3+(i*0.2),1.4, Player.zPos)
            glScale(0.10, 0.10, 0.10)
            Player.init()
            glPopMatrix()

    def reset():
        Player.firedBullets = []
        Player.renderedBullets = []
        Player.rot_angle = 0
        Player.zPos = -5
        Player.xPos = 0
        Player.yPos = -2.1
        Player.kill = Player.gradientUp = False
        Player.gradientDown = Player.collided = False           
        Player.visible = True
        Player.scaleFactor = 1
        Player.redColor = 0
        Player.spaceNotification = True


def timer(v):
    render()
    
    glutTimerFunc(1000//Display.FPS,timer,0)

def render():
    glClearColor(0, 0, 0, 1)
    glBindTexture(GL_TEXTURE_2D, Texture.texture_names[0])  # repeat this if you want to bind another texture
    glBegin(GL_QUADS)
    glTexCoord2f(0, 1)  # TODO IMPORTANT: glTexCoord2f must come first before glVertex2d
    glVertex2d(-1, 1)

    glTexCoord2f(1, 1)
    glVertex2d(1, 1)

    glTexCoord2f(1.0, 0)
    glVertex2d(1, -1)

    glTexCoord2f(0, 0)
    glVertex2d(-1, -1)

    glEnd()
    glEnable(GL_DEPTH_TEST)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    Display.width = glutGet(GLUT_WINDOW_WIDTH)
    Display.height = glutGet(GLUT_WINDOW_HEIGHT)

    gameState.updateState()
    glutSwapBuffers()

def main():
    Display.init()   
    spawnBlocks.init()
    spawnHelpers.init()
    Texture.my_init(Texture)
    glutTimerFunc(0, timer, 0)
    glutMainLoop()

main()


