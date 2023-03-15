import pygame
import random
import sys

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Set the width and height of each grid block
BLOCK_WIDTH = 32
BLOCK_HEIGHT = 32

# Set the width and height of the screen
SCREEN_WIDTH = 320
SCREEN_HEIGHT = 640

# Set the number of rows and columns in the grid
ROWS = SCREEN_HEIGHT // BLOCK_HEIGHT
COLS = SCREEN_WIDTH // BLOCK_WIDTH

# Set the font color
FONT_COLOR = (255, 255, 255)

# Load the matrix image
matrixImg = pygame.image.load('Screen Shot 2023-03-09 at 5.21.07 PM.png')

# Define the shapes of the different block clumps
BLOCK_SHAPES = [
    [(YELLOW, 0, 0), (YELLOW, 0, 1), (YELLOW, 1, 0), (YELLOW, 1, 1)],
    [(RED, 0, 0), (RED, 0, 1), (RED, 1, 0), (RED, 1, -1)],
    [(BLUE, 0, 0), (BLUE, 0, -1), (BLUE, 1, 0), (BLUE, 2, 0)],
    [(GREEN, 0, 0), (GREEN, 1, 0), (GREEN, 1, -1), (GREEN, 2, -1)]
]

# Define the different block clumps
BLOCKS = []
score = 0
for shape in BLOCK_SHAPES:
    blocks = []
    for color, row, col in shape:
        blocks.append((color, row + ROWS // 2, col + COLS // 2))
    BLOCKS.append(blocks)

# Initialize Pygame
pygame.init()

# Set the height and width of the screen
size = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode(size)

# Set the title of the window
pygame.display.set_caption("Tetris Clone")

# Set the font for the timer display
font = pygame.font.Font(None, 36)

# Create a matrix to represent the grid
matrix = [[None] * COLS for _ in range(ROWS)]

# Set the initial timer value
timer_value = 5

# Set the initial score value
score_value = 0

# Set the initial game over state
game_over = False

# Define a function to draw a block at the specified location
def draw_block(color, row, col):
    x = col * BLOCK_WIDTH
    y = row * BLOCK_HEIGHT
    image = pygame.image.load(f"{color}.png")
    screen.blit(image, (x, y))

# Define a function to draw the matrix
def draw_matrix():
    for row in range(ROWS):
        for col in range(COLS):
            block = matrix[row][col]
            if block is not None:
                color, _, _ = block
                draw_block(color, row, col)

# Define a function to generate a new block clump
def new_block():
    return random.choice(BLOCKS)

# Define a function to check if a row is full
def is_row_full(row):
    return all(matrix[row])

# Define a function to clear a row


# Game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Update game state

    # Move the current block down one row
    current_block_row += 1

    # Check if the current block has collided with another block or the bottom of the grid
    for color, row, col in current_block:
        if row >= ROWS or matrix[row][col] is not None:
            # Move the current block back up one row
            current_block_row -= 1

            # Add the current block to the matrix
            for color, row, col in current_block:
                matrix[row][col] = (color, row, col)

            # Check for full rows and clear them
            rows_to_clear = []
            for row in range(ROWS):
                if is_row_full(row):
                    clear_row(row)
                    rows_to_clear.append(row)
            score += len(rows_to_clear) ** 2

            # Generate a new block clump
            current_block = new_block()
            current_block_row = 0
            current_block_col = COLS // 2

            # Check if the game is over
            if any(matrix[0]):
                game_over = True

            break

    if game_over:
        # Draw the "Game Over" screen
        game_over_text = font.render("Game Over", True, FONT_COLOR)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT // 2 - 18))

    else:
        # Draw everything
        screen.fill((255, 255, 255))
        screen.blit(matrixImg, (250, 0))
        draw_matrix()
        draw_block_at_current_position()
        score_text = font.render("Score: " + str(score), True, FONT_COLOR)
        screen.blit(score_text, (50, 50))

    # Update the display
    pygame.display.flip()

    # Wait for a short amount of time to control the game speed
    pygame.time.wait(100)
