import math

import pygame
from pygame import mixer


import random


# initialize pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# Clock for frame rate control
clock = pygame.time.Clock()
FPS = 60

# Background
background = pygame.image.load('background.jpg')

# Initialize mixer with error handling for environments without audio
try:
    pygame.mixer.init()
    mixer_initialized = True
except:
    mixer_initialized = False
    pass

# Background sound (with error handling for environments without audio)
if mixer_initialized:
    try:
        mixer.music.load('background.wav')
        mixer.music.play(-1)
    except:
        pass  # Continue without background music if audio not available

# Caption and Icon
pygame.display.set_caption("space invader")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Preload sound effects (with error handling)
laser_sound = None
explosion_sound = None
if mixer_initialized:
    try:
        laser_sound = mixer.Sound('laser.wav')
        explosion_sound = mixer.Sound('explosion.wav')
    except:
        pass  # Continue without sound effects if audio not available

# Player
playerImg = pygame.image.load('player.png')
playerImg = pygame.transform.scale(playerImg, (64, 64))  # Optimize size
playerX = 370
playerY = 480
playerX_change = 0
player_speed = 5  # Increased speed

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6
enemy_speed = 3  # Increased enemy speed

for i in range(num_of_enemies):
    img = pygame.image.load('enemy.png')
    enemyImg.append(pygame.transform.scale(img, (64, 64)))  # Optimize size
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(enemy_speed)
    enemyY_change.append(40)

# Bullet

# Ready - Fou cannot se the bullet on the screen
# Fire - The bullet is currently moving
bulletImg = pygame.image.load('bullet.png')
bulletImg = pygame.transform.scale(bulletImg, (32, 32))  # Optimize size
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 7  # Increased bullet speed
bullet_state = "ready"

# score

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

# Game over Text
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("Score :" + str(score_value), True, (0, 255, 0))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = font.render("GAME OVER", True, (0, 255, 0))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isocollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2))
    if distance < 27:
        return True
    else:
        return False


# Game loop
running = True
while running:

    # RGB = RED, GREEN, BLUE
    screen.fill((255, 0, 0))
    # background image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.7
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.7
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    if laser_sound:
                        laser_sound.play()
                    # Get the current x coordinate of the spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # 5 = 5 + -0.1 -> 5 = 5 - 0.1
    # 5 = 5 + 0.1
    # checking for boundaries of spaceships
    playerX += playerX_change * player_speed

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    enemyX += enemyX_change

    # Enemy movement

    for i in range(num_of_enemies):

        # Game over
        if enemyY[i] > 400:
            for j in range(num_of_enemies):
                enemyY[j] = 20000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = enemy_speed
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -enemy_speed
            enemyY[i] += enemyY_change[i]

        # collision
        collision = isocollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            if explosion_sound:
                explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change



    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
    
    # Control frame rate
    clock.tick(FPS)
