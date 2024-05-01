import sys
import copy
import pygame
import math
import os

# Constants
WIDTH, HEIGHT = 900, 950
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
FPS = 60
PI = math.pi

# Game state variables
color = 'blue'
player_x, player_y = 450, 660
score, lives, powerup = 0, 3, False
game_over, game_won = False, False
flicker = False
turns_allowed = [False, False, False, False]
direction = 0
player_speed = 2
eaten_ghost = [False, False, False, False]
moving = False
ghost_speeds = [2, 2, 2, 2]
startup_counter = 0
counter = 0  
direction_command = 0
blinky_speed = 1


# Player and ghost position handling
center_x = player_x + 23
center_y = player_y + 24

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
timer = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 20)

# Load player images
player_images_dir = os.path.join('C:\\Users\\User\\Desktop\\pacman\\assets\\player_images')
player_images = []
for i in range(1, 5):
    image_path = os.path.join(player_images_dir, f'{i}.png')
    player_images.append(pygame.transform.scale(pygame.image.load(image_path), (35, 35)))

# Load ghost images
ghost_images_dir = os.path.join('C:\\Users\\User\\Desktop\\pacman\\assets\\ghost_images')
blinky_img = pygame.transform.scale(pygame.image.load(os.path.join(ghost_images_dir, 'red.png')), (45, 45))
pinky_img = pygame.transform.scale(pygame.image.load(os.path.join(ghost_images_dir, 'pink.png')), (45, 45))
inky_img = pygame.transform.scale(pygame.image.load(os.path.join(ghost_images_dir, 'blue.png')), (45, 45))
clyde_img = pygame.transform.scale(pygame.image.load(os.path.join(ghost_images_dir, 'orange.png')), (45, 45))
# Ghost starting position and properties
blinky_x, blinky_y = 400, 300
blinky_direction = 0

# Ghost class
class Ghost:
    def __init__(self, x, y, img, speed):
        self.x = x
        self.y = y
        self.img = img
        self.speed = speed

    def move(self, direction):
        if direction == 0:  # Right
            self.x += self.speed
        elif direction == 1:  # Left
            self.x -= self.speed
        elif direction == 2:  # Up
            self.y -= self.speed
        elif direction == 3:  # Down
            self.y += self.speed

        # Boundary check
        if self.x > WIDTH:
            self.x = 0
        elif self.x < 0:
            self.x = WIDTH
        if self.y > HEIGHT:
            self.y = 0
        elif self.y < 0:
            self.y = HEIGHT

    def draw(self):
        screen.blit(self.img, (self.x, self.y))


    def is_collision(self, x, y, level):
        # Assuming 'level' is a grid or array of tiles where 1 represents walls
        tile_x = x // TILE_SIZE  # TILE_SIZE is the size of your tiles in the level
        tile_y = y // TILE_SIZE
        if level[tile_y][tile_x] == 1:
            return True
        return False

# Constants for the ghosts' starting positions inside the box
blinky_x, blinky_y = 405, 330
pinky_x, pinky_y = 450, 330
inky_x, inky_y = 495, 330
clyde_x, clyde_y = 540, 330

# Instantiate the ghosts using the ghost_speeds array
blinky = Ghost(blinky_x, blinky_y, blinky_img, ghost_speeds[0])
pinky = Ghost(pinky_x, pinky_y, pinky_img, ghost_speeds[1])
inky = Ghost(inky_x, inky_y, inky_img, ghost_speeds[2])
clyde = Ghost(clyde_x, clyde_y, clyde_img, ghost_speeds[3])

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
    
# Function to move the player and update the ghost's position
def move_player():
    global player_x, player_y
    dx, dy = 0, 0
    if direction == 0:
        dx = player_speed
    elif direction == 1:
        dx = -player_speed
    elif direction == 2:
        dy = -player_speed
    elif direction == 3:
        dy = player_speed

    new_x, new_y = player_x + dx, player_y + dy
    if check_position(new_x + 23, new_y + 24, level)[direction]:
        player_x, player_y = new_x, new_y
    
    # After player moves, update ghost positions
    blinky.move()

# Function to draw elements on the screen including the ghost
def draw_game():
    screen.fill(BLACK)  # Assuming the background color is set to black
    draw_board()
    draw_player()
    
    # Draw ghosts after the player
    blinky.draw()
    
    pygame.display.flip()  # Update the screen with what we've drawn
    
def draw_player():
    # 0-RIGHT, 1-LEFT, 2-UP, 3-DOWN
    if direction == 0:
        screen.blit(player_images[counter // 5], (player_x, player_y))
    elif direction == 1:
        screen.blit(pygame.transform.flip(player_images[counter // 5], True, False), (player_x, player_y))
    elif direction == 2:
        screen.blit(pygame.transform.rotate(player_images[counter // 5], 90), (player_x, player_y))
    elif direction == 3:
        screen.blit(pygame.transform.rotate(player_images[counter // 5], 270), (player_x, player_y))

def check_position(centerx, centery):
    turns = [False, False, False, False]
    num1 = (HEIGHT - 50) // 32
    num2 = (WIDTH // 30)
    num3 = 15
    # check collisions based on center x and center y of player +/- fudge number
    if centerx // 30 < 29:
        if direction == 0:
            if level[centery // num1][(centerx - num3) // num2] < 3:
                turns[1] = True
        if direction == 1:
            if level[centery // num1][(centerx + num3) // num2] < 3:
                turns[0] = True
        if direction == 2:
            if level[(centery + num3) // num1][centerx // num2] < 3:
                turns[3] = True
        if direction == 3:
            if level[(centery - num3) // num1][centerx // num2] < 3:
                turns[2] = True

        if direction == 2 or direction == 3:
            if 12 <= centerx % num2 <= 18:
                if level[(centery + num3) // num1][centerx // num2] < 3:
                    turns[3] = True
                if level[(centery - num3) // num1][centerx // num2] < 3:
                    turns[2] = True
            if 12 <= centery % num1 <= 18:
                if level[centery // num1][(centerx - num2) // num2] < 3:
                    turns[1] = True
                if level[centery // num1][(centerx + num2) // num2] < 3:
                    turns[0] = True
        if direction == 0 or direction == 1:
            if 12 <= centerx % num2 <= 18:
                if level[(centery + num1) // num1][centerx // num2] < 3:
                    turns[3] = True
                if level[(centery - num1) // num1][centerx // num2] < 3:
                    turns[2] = True
            if 12 <= centery % num1 <= 18:
                if level[centery // num1][(centerx - num3) // num2] < 3:
                    turns[1] = True
                if level[centery // num1][(centerx + num3) // num2] < 3:
                    turns[0] = True
    else:
        turns[0] = True
        turns[1] = True

    return turns

# Modify the movement code to include collision detection
if moving:
    new_player_x = player_x
    new_player_y = player_y
    
    if direction == 0:
        new_player_x += player_speed
    elif direction == 1:
        new_player_x -= player_speed
    elif direction == 2:
        new_player_y -= player_speed
    elif direction == 3:
        new_player_y += player_speed
        
    # Check if the new position is valid (no collision)
    if not is_collision(new_player_x, new_player_y):
        player_x = new_player_x
        player_y = new_player_y


def is_collision(new_player_x, new_player_y):
    center_x = new_player_x + 23
    center_y = new_player_y + 24
    turns = check_position(center_x, center_y)
    if direction == 0 and not turns[0]:
        return True
    elif direction == 1 and not turns[1]:
        return True
    elif direction == 2 and not turns[2]:
        return True
    elif direction == 3 and not turns[3]:
        return True
    return False

    if event.type == pygame.KEYUP:
        if event.key == pygame.K_RIGHT and direction_command == 0:
            direction_command = direction
        if event.key == pygame.K_LEFT and direction_command == 1:
            direction_command = direction
        if event.key == pygame.K_UP and direction_command == 2:
            direction_command = direction
        if event.key == pygame.K_DOWN and direction_command == 3:
                direction_command = direction

# Main game loop
run = True
while run:
    timer.tick(FPS)  # Maintain the game's framerate
    screen.fill(BLACK)  # Clear the screen each frame
    draw_board()  # Draw the game board or background

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                direction = 0
            elif event.key == pygame.K_LEFT:
                direction = 1
            elif event.key == pygame.K_UP:
                direction = 2
            elif event.key == pygame.K_DOWN:
                direction = 3

    # Player movement
    if moving:
        new_player_x = player_x
        new_player_y = player_y

        # Determine new position based on direction
        if direction == 0:  # Right
            new_player_x += player_speed
        elif direction == 1:  # Left
            new_player_x -= player_speed
        elif direction == 2:  # Up
            new_player_y -= player_speed
        elif direction == 3:  # Down
            new_player_y += player_speed

        # Collision detection for player
        if not is_collision(new_player_x, new_player_y):
            player_x = new_player_x
            player_y = new_player_y

    # Move and draw ghosts
    blinky.move(level)
    blinky.draw()
    pinky.move(level)
    pinky.draw()
    inky.move(level)
    inky.draw()
    clyde.move(level)
    clyde.draw()

    # Check collision with each ghost
    for ghost in [blinky, pinky, inky, clyde]:
        if abs(player_x - ghost.x) < 20 and abs(player_y - ghost.y) < 20:
            if powerup:
                print("Ghost eaten!")  # Logic for when a ghost is eaten
            else:
                lives -= 1
                print("Player loses a life!")  # Logic for when the player loses a life
                if lives == 0:
                    game_over = True
                    print("Game Over!")  # Handle the game over state

    # Draw the player
    draw_player()

    # Animation and power-up logic
    counter += 1
    if counter > 19:
        counter = 0
        flicker = not flicker

    if powerup:
        power_counter += 1
        if power_counter >= 600:
            power_counter = 0
            powerup = False

    # Startup logic to control initial player movement
    if startup_counter < 180 and not (game_over or game_won):
        moving = False
        startup_counter += 1
    else:
        moving = True

    # Refresh the display
    pygame.display.flip()

# Cleanup and exit
pygame.quit()
sys.exit()
