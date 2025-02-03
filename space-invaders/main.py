import pygame
import math
import random

# Initializing pygame 
pygame.init()

# screen (x , y)
screen = pygame.display.set_mode((800,600))

pygame.display.set_caption('Space Invadors')
# icon
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# background image
backgroundImg = pygame.image.load('background.png')
# background music
pygame.mixer.music.load('background.wav')
pygame.mixer.music.play(-1)
# spaceship 
SpaceShip = pygame.image.load('spaceship.png')
SpaceShipX = 370
SpaceShipY = 480
SpaceShipXChange = 0 

# Enemy 
Enemy = []
EnemyX = []
EnemyY = []
EnemyXChange = []
EnemyYChange = []
NumberofEnemies = 30
for i in range (NumberofEnemies):
    Enemy.append(pygame.image.load('scary-alien.png'))
    EnemyX.append(random.randint(0,735))
    EnemyY.append(random.randint(50,150))
    EnemyXChange.append(2.5)
    EnemyYChange.append(35)

# Bullet
Bullet = pygame.image.load('bullet.png')
BulletX = 0
BulletY = 480
BulletXchange = 0
BulletYchange = 9
BulletState = 'ready'
# scores
scoreValue = 0
scoreValueX = 10
scoreValueY = 10
font = pygame.font.Font('freesansbold.ttf',30)

# Game Over 
GameOverfont = pygame.font.Font('freesansbold.ttf',64) 
def GameOver():
    GOver = GameOverfont.render(f'GAME OVER',True ,(255,255,255))
    screen.blit(GOver,(200,250))

def ShowScore(x , y):
    score = font.render(f'Score : {str(scoreValue)}',True ,(255,255,255))
    screen.blit(score , (x,y))

# draw spaceship
def spacePlayer(SpaceShipX,SpaceShipY):
    screen.blit(SpaceShip , (SpaceShipX , SpaceShipY))

# draw enemy
def AlienEnemy(EnemyX,EnemyY , i):
    screen.blit(Enemy[i] , (EnemyX , EnemyY))

# draw bulltet
def firebullet(x, y):
    global BulletState
    BulletState = "fire"
    screen.blit(Bullet, (x + 16, y + 10))

# colission

def colideDistance(EnemyX , EnemyY , BulletX , BulletY):
    distance = math.sqrt(math.pow(EnemyX - BulletX , 2) + math.pow(EnemyY - BulletY,2))
    if distance < 27:
        return True
    else:
        return False
# Game loop
running = True
while running: 
    # background color
    screen.fill((0,0,0))
    # background image
    screen.blit(backgroundImg , (0,0))
    # Quit window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # Left / Right key
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                SpaceShipXChange=-3.2
            if event.key == pygame.K_RIGHT:
                SpaceShipXChange=3.2
            # for firing loading the bullet
            if event.key == pygame.K_SPACE:
                if BulletState == 'ready':
                    firingMixer = pygame.mixer.Sound('laser.wav')
                    firingMixer.play()
                    BulletX = SpaceShipX
                    firebullet(BulletX , BulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                SpaceShipXChange= 0

    SpaceShipX = SpaceShipX+SpaceShipXChange
    # setting boundries
    if SpaceShipX <= 0:
        SpaceShipX = 0
    elif SpaceShipX >=736:
        SpaceShipX = 736
    
    # enemy boundries
    for i in range(NumberofEnemies): 
        # Game Over
        if EnemyY[i] > 440:
            for j in range(NumberofEnemies):
                EnemyY[j] = 2000
            GameOver()
            break
 
        EnemyX[i] = EnemyX[i]+EnemyXChange[i]
        if EnemyX[i] <= 0 :
            EnemyXChange[i] = 2.5
            EnemyY[i]+=EnemyYChange[i]
        elif EnemyX[i] >=736:
            EnemyXChange[i] = -2.5
            EnemyY[i]+=EnemyYChange[i]
           # alien enemy
        AlienEnemy(EnemyX[i],EnemyY[i],i)
  
    # bullet / enemy collision
        colid = colideDistance(EnemyX[i] , EnemyY[i] , BulletX , BulletY)
        if colid:
            ExplosionMixer = pygame.mixer.Sound('explosion.wav')
            ExplosionMixer.play()
            BulletY = 480
            BulletState = 'ready'
            scoreValue+=1

            # file handling the score  to a text file 
            f = open('new.txt' , 'w')
            f.write(str(scoreValue))
            f.close()

            EnemyX[i] = random.randint(0,735)
            EnemyY[i] = random.randint(50,150)

      # For reloading bullets
    if BulletY <=-1:
        BulletY = 480
        BulletState = 'ready'
    # Bullet state
    if BulletState == 'fire':
        firebullet(BulletX , BulletY)
        BulletY-=BulletYchange

    # space ship
    spacePlayer(SpaceShipX , SpaceShipY)      
    # Score  
    ShowScore(scoreValueX,scoreValueY)
    # using update function  to update the screen while game runs
    pygame.display.update()
    
    
