import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Colors
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)

# Map settings
TILE_SIZE = 25
MAP_WIDTH, MAP_HEIGHT = SCREEN_WIDTH // TILE_SIZE, SCREEN_HEIGHT // TILE_SIZE

