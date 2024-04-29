import sys
import os
import pygame
import math
import random

# Constants
WIDTH, HEIGHT = 900, 950
TILE_SIZE = 30  # Adjusted for game grid
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GAME_COLOR = 'blue'  # General color for game elements

# Game settings
PI = math.pi
PLAYER_SPEED = 2
GHOST_SPEEDS = [2, 2, 2, 2]
STARTUP_COUNTER = 0
COUNTER = 0

# Game state
score, lives, powerup = 0, 3, False
game_over, game_won = False, False
flicker = False
moving = False

# Positioning
player_x, player_y = 450, 663
direction = 0
direction_command = 0
turns_allowed = [False, False, False, False]
targets = [(player_x, player_y)] * 4

# Ghost state
eaten_ghost = [False, False, False, False]
blinky_dead, inky_dead, clyde_dead, pinky_dead = False, False, False, False
blinky_box, inky_box, clyde_box, pinky_box = False, False, False, False

# Assets directories
assets_dir = 'assets'
player_images_dir = os.path.join(assets_dir, 'player_images')
ghost_images_dir = os.path.join(assets_dir, 'ghost_images')

# Load images
player_images = [pygame.transform.scale(pygame.image.load(os.path.join(player_images_dir, f'{i}.png')), (45, 45)) for i in range(1, 5)]
assets_dir = 'assets'
ghost_images_dir = os.path.join(assets_dir, 'ghost_images')
ghost_images = {
    'blinky': pygame.transform.scale(pygame.image.load(os.path.join(ghost_images_dir, 'red.png')), (45, 45)),
    'pinky': pygame.transform.scale(pygame.image.load(os.path.join(ghost_images_dir, 'pink.png')), (45, 45)),
    'inky': pygame.transform.scale(pygame.image.load(os.path.join(ghost_images_dir, 'blue.png')), (45, 45)),
    'clyde': pygame.transform.scale(pygame.image.load(os.path.join(ghost_images_dir, 'orange.png')), (45, 45)),
    'spooked': pygame.transform.scale(pygame.image.load(os.path.join(ghost_images_dir, 'powerup.png')), (45, 45)),
    'dead': pygame.transform.scale(pygame.image.load(os.path.join(ghost_images_dir, 'dead.png')), (45, 45))
}
# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
timer = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 20)


boards = [
    [6, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5],
    [3, 6, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 6, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 3],
    [3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3],
    [3, 3, 1, 6, 4, 4, 5, 1, 6, 4, 4, 4, 5, 1, 3, 3, 1, 6, 4, 4, 4, 5, 1, 6, 4, 4, 5, 1, 3, 3],
    [3, 3, 2, 3, 0, 0, 3, 1, 3, 0, 0, 0, 3, 1, 3, 3, 1, 3, 0, 0, 0, 3, 1, 3, 0, 0, 3, 2, 3, 3],
    [3, 3, 1, 7, 4, 4, 8, 1, 7, 4, 4, 4, 8, 1, 7, 8, 1, 7, 4, 4, 4, 8, 1, 7, 4, 4, 8, 1, 3, 3],
    [3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3],
    [3, 3, 1, 6, 4, 4, 5, 1, 6, 5, 1, 6, 4, 4, 4, 4, 4, 4, 5, 1, 6, 5, 1, 6, 4, 4, 5, 1, 3, 3],
    [3, 3, 1, 7, 4, 4, 8, 1, 3, 3, 1, 7, 4, 4, 5, 6, 4, 4, 8, 1, 3, 3, 1, 7, 4, 4, 8, 1, 3, 3],
    [3, 3, 1, 1, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 1, 1, 3, 3],
    [3, 7, 4, 4, 4, 4, 5, 1, 3, 7, 4, 4, 5, 0, 3, 3, 0, 6, 4, 4, 8, 3, 1, 6, 4, 4, 4, 4, 8, 3],
    [3, 0, 0, 0, 0, 0, 3, 1, 3, 6, 4, 4, 8, 0, 7, 8, 0, 7, 4, 4, 5, 3, 1, 3, 0, 0, 0, 0, 0, 3],
    [3, 0, 0, 0, 0, 0, 3, 1, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 1, 3, 0, 0, 0, 0, 0, 3],
    [8, 0, 0, 0, 0, 0, 3, 1, 3, 3, 0, 6, 4, 4, 9, 9, 4, 4, 5, 0, 3, 3, 1, 3, 0, 0, 0, 0, 0, 7],
    [4, 4, 4, 4, 4, 4, 8, 1, 7, 8, 0, 3, 0, 0, 0, 0, 0, 0, 3, 0, 7, 8, 1, 7, 4, 4, 4, 4, 4, 4],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    [4, 4, 4, 4, 4, 4, 5, 1, 6, 5, 0, 3, 0, 0, 0, 0, 0, 0, 3, 0, 6, 5, 1, 6, 4, 4, 4, 4, 4, 4],
    [5, 0, 0, 0, 0, 0, 3, 1, 3, 3, 0, 7, 4, 4, 4, 4, 4, 4, 8, 0, 3, 3, 1, 3, 0, 0, 0, 0, 0, 6],
    [3, 0, 0, 0, 0, 0, 3, 1, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 1, 3, 0, 0, 0, 0, 0, 3],
    [3, 0, 0, 0, 0, 0, 3, 1, 3, 3, 0, 6, 4, 4, 4, 4, 4, 4, 5, 0, 3, 3, 1, 3, 0, 0, 0, 0, 0, 3],
    [3, 6, 4, 4, 4, 4, 8, 1, 7, 8, 0, 7, 4, 4, 5, 6, 4, 4, 8, 0, 7, 8, 1, 7, 4, 4, 4, 4, 5, 3],
    [3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3],
    [3, 3, 1, 6, 4, 4, 5, 1, 6, 4, 4, 4, 5, 1, 3, 3, 1, 6, 4, 4, 4, 5, 1, 6, 4, 4, 5, 1, 3, 3],
    [3, 3, 1, 7, 4, 5, 3, 1, 7, 4, 4, 4, 8, 1, 7, 8, 1, 7, 4, 4, 4, 8, 1, 3, 6, 4, 8, 1, 3, 3],
    [3, 3, 2, 1, 1, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 1, 1, 2, 3, 3],
    [3, 7, 4, 5, 1, 3, 3, 1, 6, 5, 1, 6, 4, 4, 4, 4, 4, 4, 5, 1, 6, 5, 1, 3, 3, 1, 6, 4, 8, 3],
    [3, 6, 4, 8, 1, 7, 8, 1, 3, 3, 1, 7, 4, 4, 5, 6, 4, 4, 8, 1, 3, 3, 1, 7, 8, 1, 7, 4, 5, 3],
    [3, 3, 1, 1, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 1, 1, 3, 3],
    [3, 3, 1, 6, 4, 4, 4, 4, 8, 7, 4, 4, 5, 1, 3, 3, 1, 6, 4, 4, 8, 7, 4, 4, 4, 4, 5, 1, 3, 3],
    [3, 3, 1, 7, 4, 4, 4, 4, 4, 4, 4, 4, 8, 1, 7, 8, 1, 7, 4, 4, 4, 4, 4, 4, 4, 4, 8, 1, 3, 3],
    [3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3],
    [3, 7, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 8, 3],
    [7, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 8]
]

level = boards.copy()

def draw_board():
    num1 = ((HEIGHT - 50) // 32)
    num2 = (WIDTH // 30)
    for i in range(len(level)):
        for j in range(len(level[i])):
            if level[i][j] == 1:
                pygame.draw.circle(screen, 'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 4)
            if level[i][j] == 2 and not flicker:
                pygame.draw.circle(screen, 'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 10)
            if level[i][j] == 3:
                pygame.draw.line(screen, color, (j * num2 + (0.5 * num2), i * num1),
                                 (j * num2 + (0.5 * num2), i * num1 + num1), 3)
            if level[i][j] == 4:
                pygame.draw.line(screen, color, (j * num2, i * num1 + (0.5 * num1)),
                                 (j * num2 + num2, i * num1 + (0.5 * num1)), 3)
            if level[i][j] == 5:
                pygame.draw.arc(screen, color, [(j * num2 - (num2 * 0.4)) - 2, (i * num1 + (0.5 * num1)), num2, num1],
                                0, PI / 2, 3)
            if level[i][j] == 6:
                pygame.draw.arc(screen, color,
                                [(j * num2 + (num2 * 0.5)), (i * num1 + (0.5 * num1)), num2, num1], PI / 2, PI, 3)
            if level[i][j] == 7:
                pygame.draw.arc(screen, color, [(j * num2 + (num2 * 0.5)), (i * num1 - (0.4 * num1)), num2, num1], PI,
                                3 * PI / 2, 3)
            if level[i][j] == 8:
                pygame.draw.arc(screen, color,
                                [(j * num2 - (num2 * 0.4)) - 2, (i * num1 - (0.4 * num1)), num2, num1], 3 * PI / 2,
                                2 * PI, 3)
            if level[i][j] == 9:
                pygame.draw.line(screen, 'white', (j * num2, i * num1 + (0.5 * num1)),
                                 (j * num2 + num2, i * num1 + (0.5 * num1)), 3)
    
def draw_player():
    global player_x, player_y, direction
    player_image = player_images[COUNTER // 5 % len(player_images)]
    if direction == 1:  # Left
        player_image = pygame.transform.flip(player_image, True, False)
    elif direction == 2:  # Up
        player_image = pygame.transform.rotate(player_image, 90)
    elif direction == 3:  # Down
        player_image = pygame.transform.rotate(player_image, 270)
    screen.blit(player_image, (player_x, player_y))

# Define the Ghost class
class Ghost:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.direction = random.randint(0, 3)

    def move(self):
        directions = [0, 1, 2, 3]
        random.shuffle(directions)
        for dir in directions:
            # Assume TILE_SIZE and can_move_to are defined
            if dir == 0:
                next_x = self.x + TILE_SIZE
            elif dir == 1:
                next_x = self.x - TILE_SIZE
            elif dir == 2:
                next_y = self.y - TILE_SIZE
            elif dir == 3:
                next_y = self.y + TILE_SIZE

            if can_move_to(next_x, next_y):  # You need to define this function
                self.x, self.y = next_x, next_y
                break

    def draw(self):
        screen.blit(self.image, (self.x, self.y))



def can_move_to(x, y):
    grid_x, grid_y = x // TILE_SIZE, y // TILE_SIZE
    return 0 <= grid_x < WIDTH // TILE_SIZE and 0 <= grid_y < HEIGHT // TILE_SIZE and level[grid_y][grid_x] != 0


def move_player(play_x, play_y, direction):
    if can_move_to(play_x + PLAYER_SPEED * (direction == 0), play_y + PLAYER_SPEED * (direction == 3)):
        play_x += PLAYER_SPEED * (direction == 0) - PLAYER_SPEED * (direction == 1)
        play_y += PLAYER_SPEED * (direction == 3) - PLAYER_SPEED * (direction == 2)
    return play_x, play_y

class Ghost:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.direction = random.randint(0, 3)

    def move(self):
        directions = [0, 1, 2, 3]
        random.shuffle(directions)  # Shuffle directions to randomize movement order
        for dir in directions:
            next_x, next_y = self.x, self.y
            if dir == 0:
                next_x += TILE_SIZE
            elif dir == 1:
                next_x -= TILE_SIZE
            elif dir == 2:
                next_y -= TILE_SIZE
            elif dir == 3:
                next_y += TILE_SIZE

            if can_move_to(next_x, next_y):
                self.x, self.y = next_x, next_y
                break
            
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

# Starting positions based on a standard Pac-Man grid (example values)
starting_x_position_blinky = 13 * TILE_SIZE  
starting_y_position_blinky = 14 * TILE_SIZE

starting_x_position_pinky = 13 * TILE_SIZE   
starting_y_position_pinky = 17 * TILE_SIZE

starting_x_position_inky = 11 * TILE_SIZE    
starting_y_position_inky = 17 * TILE_SIZE

starting_x_position_clyde = 15 * TILE_SIZE   
starting_y_position_clyde = 17 * TILE_SIZE

# Initialize ghosts
ghosts = [
    Ghost(starting_x_position_blinky, starting_y_position_blinky, ghost_images['blinky']),
    Ghost(starting_x_position_pinky, starting_y_position_pinky, ghost_images['pinky']),
    Ghost(starting_x_position_inky, starting_y_position_inky, ghost_images['inky']),
    Ghost(starting_x_position_clyde, starting_y_position_clyde, ghost_images['clyde']),
]

player_x, player_y = move_player(player_x, player_y, direction)

for ghost in ghosts:
    ghost.move()

# Rendering
screen.fill(BLACK)
for ghost in ghosts:
    ghost.draw(screen)
pygame.display.flip()

# Then, in your main loop where you check for KEYDOWN events:
if event.type == pygame.KEYDOWN:
    if event.key == pygame.K_RIGHT and can_move_to(player_x + TILE_SIZE, player_y):
        player_x += TILE_SIZE
    # And so on for K_LEFT, K_UP, K_DOWN

# Main game loop
run = True
while run:
    timer.tick(FPS)  
    screen.fill(BLACK)  
    draw_board()
    draw_player()
    if counter < 19:
        counter += 1
        if counter > 3:
            flicker = False
    else:
        counter = 0
        flicker = True
    if powerup and power_counter < 600:
        power_counter += 1
    elif powerup and power_counter >= 600:
        power_counter = 0
        powerup = False
        eaten_ghost = [False, False, False, False]
    if startup_counter < 180 and not game_over and not game_won:
        moving = False
        startup_counter += 1
    else:
        moving = True

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                direction_command = 0
            if event.key == pygame.K_LEFT:
                direction_command = 1
            if event.key == pygame.K_UP:
                direction_command = 2
            if event.key == pygame.K_DOWN:
                direction_command = 3
            if event.key == pygame.K_SPACE and (game_over or game_won):
                powerup = False
                power_counter = 0
                lives -= 1
                startup_counter = 0
                player_x = 450
                player_y = 663
                direction = 0
                direction_command = 0
                blinky_x = 56
                blinky_y = 58
                blinky_direction = 0
                inky_x = 440
                inky_y = 388
                inky_direction = 2
                pinky_x = 440
                pinky_y = 438
                pinky_direction = 2
                clyde_x = 440
                clyde_y = 438
                clyde_direction = 2
                eaten_ghost = [False, False, False, False]
                blinky_dead = False
                inky_dead = False
                clyde_dead = False
                pinky_dead = False
                score = 0
                lives = 3
                level = copy.deepcopy(boards)
                game_over = False
                game_won = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT and direction_command == 0:
                direction_command = direction
            if event.key == pygame.K_LEFT and direction_command == 1:
                direction_command = direction
            if event.key == pygame.K_UP and direction_command == 2:
                direction_command = direction
            if event.key == pygame.K_DOWN and direction_command == 3:
                direction_command = direction

    if direction_command == 0 and turns_allowed[0]:
        direction = 0
    if direction_command == 1 and turns_allowed[1]:
        direction = 1
    if direction_command == 2 and turns_allowed[2]:
        direction = 2
    if direction_command == 3 and turns_allowed[3]:
        direction = 3

    if player_x > 900:
        player_x = -47
    elif player_x < -50:
        player_x = 897

    if blinky.in_box and blinky_dead:
        blinky_dead = False
    if inky.in_box and inky_dead:
        inky_dead = False
    if pinky.in_box and pinky_dead:
        pinky_dead = False
    if clyde.in_box and clyde_dead:
        clyde_dead = False

    pygame.display.flip()

pygame.quit()