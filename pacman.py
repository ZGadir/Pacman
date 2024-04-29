import sys
import os
import pygame
import math
import random

# Constants
WIDTH, HEIGHT = 900, 950
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
FPS = 60
TILE_SIZE = 32  # Adjust as needed for your grid system

# Paths for assets
PLAYER_IMAGES_DIR = os.path.join('C:\\Users\\User\\Desktop\\pacman\\assets\\player_images')
GHOST_IMAGES_DIR = os.path.join('C:\\Users\\User\\Desktop\\pacman\\assets\\ghost_images')

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 20)

# Load images
def load_images(directory, names):
    images = []
    for name in names:
        path = os.path.join(directory, name)
        image = pygame.image.load(path).convert_alpha()
        image = pygame.transform.scale(image, (45, 45))
        images.append(image)
    return images

player_images = load_images(PLAYER_IMAGES_DIR, [f'{i}.png' for i in range(1, 5)])
ghost_images = {
    'blinky': pygame.image.load(os.path.join(GHOST_IMAGES_DIR, 'blinky.png')),
    'pinky': pygame.image.load(os.path.join(GHOST_IMAGES_DIR, 'pinky.png')),
    'inky': pygame.image.load(os.path.join(GHOST_IMAGES_DIR, 'inky.png')),
    'clyde': pygame.image.load(os.path.join(GHOST_IMAGES_DIR, 'clyde.png'))
}

# Entity classes
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction = 0  # up=0, right=1, down=2, left=3
        self.images = player_images

    def move(self, direction, walls):
        dx, dy = 0, 0
        if direction == 0: dy = -TILE_SIZE
        elif direction == 1: dx = TILE_SIZE
        elif direction == 2: dy = TILE_SIZE
        elif direction == 3: dx = -TILE_SIZE

        new_x, new_y = self.x + dx, self.y + dy
        if (new_x, new_y) not in walls:
            self.x, self.y = new_x, new_y
        self.direction = direction

    def draw(self):
        image = self.images[self.direction]
        screen.blit(image, (self.x, self.y))

class Ghost:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.direction = random.randint(0, 3)

    def move(self, walls):
        directions = [(0, -TILE_SIZE), (1, TILE_SIZE), (2, TILE_SIZE), (3, -TILE_SIZE)]
        random.shuffle(directions)
        for direction, (dx, dy) in enumerate(directions):
            new_x, new_y = self.x + dx, self.y + dy
            if (new_x, new_y) not in walls:
                self.x, self.y = new_x, new_y
                break

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

# Game logic
def main():
    running = True
    player = Player(450, 663)
    ghosts = [Ghost(100, 100, ghost_images['blinky'])]
    walls = {}  # Define your walls based on the level data

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP: player.move(0, walls)
                elif event.key == pygame.K_RIGHT: player.move(1, walls)
                elif event.key == pygame.K_DOWN: player.move(2, walls)
                elif event.key == pygame.K_LEFT: player.move(3, walls)

        screen.fill(BLACK)
        for ghost in ghosts:
            ghost.move(walls)
            ghost.draw()
        player.draw()
        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
