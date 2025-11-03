import pygame
import random
import math


# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Game")

# Load images
alien_img = pygame.image.load("recources\\ufo-1.png")
# 32 x 32 image
pygame.display.set_icon(alien_img)


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

    def move(self):
        self.y += self.change
        if self.y <= 0:
            self.bullet_state = "ready"
            self.y = 520
            self.change = -0.5


class Player:
    def __init__(self, x, y, change=0):
        self.img = pygame.image.load("recources\\spaceship.png")
        self.x = x
        self.y = 520
        self.change = change

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
        self.x_change = 100
        self.y_change = 7

    def enemy_set(self):
        screen.blit(self.img, (self.x, self.y))

    def move(self):
        self.x += self.x_change
        # boundary checking
        if self.x <= 0:
            self.x_change = 0.3
            self.y += self.y_change
        elif self.x >= WIDTH - 64:  # assuming enemy width is 64
            self.x_change = -0.3
            self.y += self.y_change
        elif self.y >= HEIGHT - 64:
            self.y = 0

    def is_hit(self, bullet):
        distance = math.sqrt((self.x - bullet.x) ** 2 +
                             (self.y - bullet.y) ** 2)
        if distance < 27:
            return True
        return False


player = Player(368, 520)
x = random.randint(0, WIDTH - 64)
y = random.randint(0, 300 - 64)
enemy = Enemy(x, y)
bullet = Bullet()

running = True
while running:
    screen.fill((0, 0, 0))
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
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player.change = 0

    player.move()
    bullet.move()
    player.player_set()
    enemy.enemy_set()
    if bullet.bullet_state == "fire":
        bullet.shoot()

    pygame.display.flip()

# why isn't the spaceship showing up? because we didn't call the player_set method, where to call it? inside the game loop
