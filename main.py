import pygame
import random


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


class Alien:
    def __init__(self, x, y, change_x=4, change_y=40):
        self.img = pygame.image.load("recources\\ufo-1.png")
        self.x = x
        self.y = y
        self.change_x = change_x
        self.change_y = change_y

    def alien_set(self):
        screen.blit(self.img, (self.x, self.y))

    def move(self):
        self.x += self.change_x
        if self.x <= 0 or self.x >= WIDTH - 32:  # assuming alien width is 32
            self.change_x *= -1
            self.y += self.change_y


player = Player(368, 536)

# show items
player.move()

player.player_set()


running = True
while running:
    screen.fill((0, 0, 0))  # Clear screen with black
    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if keys[pygame.K_LEFT]:
                player.change = -5
            if keys[pygame.K_RIGHT]:
                player.change = 5
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player.change = 0

    pygame.display.flip()
