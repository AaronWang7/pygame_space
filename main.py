import pygame
import random
import math
from pygame import mixer


# Initialize Pygame
pygame.init()

# set up background
background = pygame.image.load("recources\\background-1.jpg")
scaled_background = pygame.transform.scale(background, (800, 600))

game_over = False

# background sound
mixer.music.load("recources\\background.wav")
mixer.music.play(-1)

# Set up display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Game")

# Load images
alien_img = pygame.image.load("recources\\ufo-1.png")
# 32 x 32 image
pygame.display.set_icon(alien_img)

score_front = pygame.font.Font('freesansbold.ttf', 32)


game_over_front = pygame.font.Font('freesansbold.ttf', 64)
game_over_display = game_over_front.render("GAME OVER", True, (255, 0, 0))
screen.blit(game_over_display, (250, 25))

game_over = True


class Button:
    def __init__(self, x, y, img, scale):
        self.x = x
        self.y = y
        self.img = pygame.image.load(img)
        self.img = pygame.transform(
            self.img, (int(img.get_width()*scale, int(img.get_hight()*scale))))
        self.scale = scale
        self.rect = self.img.get_rect()

    def draw(self):
        pos = pygame.mouse.get_pos()
        print(pos)
        if self.rect.collidepoint(pos):
            print("Hover")
        screen.blit(self.img, (self.x, self.y))


class Bullet:
    def __init__(self, x=0, y=0):
        self.bullet_state = "ready"
        self.x = x
        self.y = y
        self.change = -1
        self.img = pygame.image.load("recources\\bullet.png")
        self.rotated = pygame.transform.rotate(self.img, 90)

    def shoot(self):
        self.bullet_state = "fire"
        screen.blit(self.rotated, (self.x, self.y))
        self.change = -1

    def move(self):
        self.y += self.change
        if self.y <= 0:
            self.bullet_state = "ready"
            self.y = player.y - 20
            self.change = -0.5


class Player:
    def __init__(self, x, y, change=0):
        self.img = pygame.image.load("recources\\spaceship.png")
        self.x = x
        self.y = 520
        self.change = change
        self.score = 0

    def player_set(self):
        screen.blit(self.img, (self.x, self.y))

    def move(self):
        self.x += self.change
        # boundary checking
        if self.x <= 0:
            self.x = 0
        elif self.x >= WIDTH - 64:  # assuming spaceship width is 64
            self.x = WIDTH - 64


class Enemy:
    def __init__(self, x, y):
        self.img = pygame.image.load("recources\\ufo-1.png")
        self.x = x
        self.y = y
        self.x_change = 50
        self.y_change = 70
        self.game_over = False

    def enemy_set(self):
        screen.blit(self.img, (self.x, self.y))

    def move(self):
        self.x += self.x_change
        # boundary checking
        if self.x <= 0:
            self.x_change = 0.1
            self.y += self.y_change
        elif self.x >= WIDTH - 64:  # assuming enemy width is 64
            self.x_change = -0.1
            self.y += self.y_change
        elif self.y >= HEIGHT - 64:
            self.y = 0

    def is_hit(self, bullet):
        distance = math.sqrt((self.x - bullet.x) ** 2 +
                             (self.y - bullet.y) ** 2)
        if distance < 27:
            return True
        return False

    def lose(self, player):
        distance = math.sqrt((self.x - player.x) ** 2 +
                             (self.y - player.y) ** 2)
        if distance < 48:
            game_over = True
        game_over = False


enemies = []
player = Player(368, 520)
x = random.randint(0, WIDTH - 64)
y = random.randint(0, 300 - 64)
enemy = Enemy(x, y)
bullet = Bullet()
for i in range(6):
    x = random.randint(0, WIDTH - 64)
    y = random.randint(0, 400 - 64)
    enemies.append(Enemy(x, y))


running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(scaled_background, (0, 0))

    score_display = score_front.render(
        f"Score: {player.score}", True, (255, 255, 255))
    screen.blit(score_display, (10, 10))

    enemy.move()
  # Clear screen with black

    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if keys[pygame.K_LEFT]:
                player.change = -0.3
            if keys[pygame.K_RIGHT]:
                player.change = 0.3
            if keys[pygame.K_SPACE]:
                if bullet.bullet_state == "ready":
                    bullet.x = player.x + 16
                    bullet.y = player.y + 10
                    bullet.bullet_state = "fire"
                    mixer.Sound("recources\\laser.wav").play(0)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player.change = 0

    player.move()
    for i, enemy in enumerate(enemies):
        if enemy.is_hit(bullet):
            bullet.bullet_state = "ready"
            x = random.randint(0, WIDTH - 64)
            y = random.randint(0, 300 - 64)
            mixer.Sound("recources\\explosion.wav").play(0)
            enemies.pop(i)
            bullet.y = player.y
            bullet.x = player.x
            bullet.change = 0
            player.score += 1
            if enemies == []:
                for i in range(6):
                    x = random.randint(0, WIDTH - 64)
                    y = random.randint(0, 300 - 64)
                    enemies.append(Enemy(x, y))

    for enemy in enemies:
        if game_over == True:
            screen.blit(game_over_display, (300, 300))
            enemies = []
            restart_front = score_front.render(
                "Click to restart", True, (255, 255, 255))
            # use img instead of text

            break

    bullet.move()
    for enemy in enemies:
        enemy.move()

    player.player_set()
    for enemy in enemies:
        enemy.enemy_set()
    if bullet.bullet_state == "fire":
        bullet.shoot()

    pygame.display.flip()
