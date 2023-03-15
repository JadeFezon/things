import pygame
import random
import sys
pygame.init()
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
screen = pygame.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])
# define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# set the dimensions of each block
BLOCK_WIDTH = 30
BLOCK_HEIGHT = 30
matrixImg = pygame.image.load('Screen Shot 2023-03-09 at 5.21.07 PM.png')
# set the dimensions of the game window
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# define the types of blocks and their colors
BLOCK_IMAGES = {
    YELLOW: pygame.image.load('Screen Shot 2023-03-09 at 5.18.39 PM.png').convert_alpha(),
    RED: pygame.image.load('Screen Shot 2023-03-09 at 5.18.54 PM.png').convert_alpha(),
    BLUE: pygame.image.load('Screen Shot 2023-03-09 at 5.19.21 PM.png').convert_alpha(),
    GREEN: pygame.image.load('Screen Shot 2023-03-09 at 5.19.33 PM.png').convert_alpha()
}
BLOCK_TYPES = {
    'yellow': YELLOW,
    'red': RED,
    'blue': BLUE,
    'green': GREEN
}
BLOCK_SIZE = 50

block_dict = {
    'yellow': YELLOW,
    'red': RED,
    'blue': BLUE,
    'green': GREEN,
}
clump_matrix = [
    ['*', '*'],
    ['*', '*']
]

# create the game window
pygame.init()

pygame.display.set_caption('Puyo Puyo Clone')

# define the game grid
GRID_WIDTH = 6
GRID_HEIGHT = 12
GRID_OFFSET_X = 200
GRID_OFFSET_Y = 50
GRID = [[None for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

# define the current and next clumps
CURRENT_CLUMP = None
NEXT_CLUMP = None

# define the game loop
clock = pygame.time.Clock()
running = True
GRID_ROWS = 10
GRID_COLS = 20
def generate_clump(clump_matrix, block_dict):
    clump = []
    for row_index, row in enumerate(clump_matrix):
        for col_index, block in enumerate(row):
            if block:
                block_image = block_dict[block]
                x = col_index * BLOCK_SIZE
                y = row_index * BLOCK_SIZE
                clump.append(Block(block_image, x, y, block))
    return clump

def add_clump_to_grid(clump, grid):
    for row, col in clump:
        grid[row][col] = clump.color

def can_move_down(clump, grid):
    for block in clump:
        row = block.row + 1
        if row == GRID_ROWS or grid[row][block.col]:
            return False
    return True


def move_down(clump):
    for block in clump:
        block.move(0, BLOCK_SIZE)


def clear_rows(grid):
    rows_cleared = 0
    for row_index in range(GRID_ROWS):
        if all(grid[row_index]):
            for above_row_index in range(row_index, 0, -1):
                grid[above_row_index] = grid[above_row_index - 1][:]
            grid[0] = [None] * GRID_COLS
            rows_cleared += 1
    return rows_cleared


def clear_columns(grid):
    columns_cleared = 0
    for col_index in range(GRID_COLS):
        if all(grid[row_index][col_index] for row_index in range(GRID_ROWS)):
            for row_index in range(GRID_ROWS):
                for above_col_index in range(col_index, 0, -1):
                    grid[row_index][above_col_index] = grid[row_index][above_col_index - 1]
                grid[row_index][0] = None
            columns_cleared += 1
    return columns_cleared

while running:
    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # generate the next clump if necessary
    if not CURRENT_CLUMP:
        CURRENT_CLUMP = NEXT_CLUMP
        NEXT_CLUMP = generate_clump(clump_matrix, block_dict)

    # move the current clump down
    if can_move_down(CURRENT_CLUMP, GRID):
        move_down(CURRENT_CLUMP)
    else:
        add_clump_to_grid(CURRENT_CLUMP, GRID)
        CURRENT_CLUMP = None

    # clear any rows or columns if necessary
    rows_cleared = clear_rows(GRID)
    columns_cleared = clear_columns(GRID)
    if rows_cleared or columns_cleared:
        pygame.time.wait(500)

    # draw the game grid
    screen.fill(BLACK)
    for i in range(GRID_HEIGHT):
        for j in range(GRID_WIDTH):
            if GRID[i][j]:
                block_type = GRID[i][j]['type']
                block_color = BLOCK_TYPES[block_type]
                block_image = BLOCK_IMAGES[block_type]
                x = GRID_OFFSET_X + j * BLOCK_WIDTH
                y = GRID_OFFSET_Y + i * BLOCK_HEIGHT
                # draw the block image
                screen.blit(block_image, (x, y))

    # draw the current and next clumps
    if CURRENT_CLUMP:
        for block in CURRENT_CLUMP:
            block_type = block['type']
            block_color = BLOCK_TYPES[block_type]
            block_image = BLOCK_IMAGES[block_type]
            x = GRID_OFFSET_X + block['x'] * BLOCK_WIDTH
            y = GRID_OFFSET_Y + block['y'] * BLOCK_HEIGHT
            # draw the block image
            screen.blit(block_image, (x, y))
    if NEXT_CLUMP:
        for block in NEXT_CLUMP:
            block_type = block['type']
            block_color = BLOCK_TYPES[block_type]

class Board:
    def __init__(self, width, height, block_size, images):
        self.width = width
        self.height = height
        self.block_size = block_size
        self.images = images
        self.grid = [[None for _ in range(width)] for _ in range(height)]

    def draw_board(self, screen):
        screen.fill((0, 0, 0))
        for row in range(self.height):
            for col in range(self.width):
                block = self.grid[row][col]
                if block is not None:
                    x = col * self.block_size
                    y = row * self.block_size
                    screen.blit(self.images[block.color], (x, y))

    def add_block(self, block):
        for row, col in block.get_block_positions():
            self.grid[row][col] = block

    def is_valid_position(self, block):
        for row, col in block.get_block_positions():
            if row < 0 or row >= self.height or col < 0 or col >= self.width or self.grid[row][col] is not None:
                return False
        return True

    def clear_full_rows(self):
        full_rows = []
        for row in range(self.height):
            if all(self.grid[row]):
                full_rows.append(row)

        for row in full_rows:
            for col in range(self.width):
                self.grid[row][col] = None

        for row in range(max(full_rows) - 1, -1, -1):
            for col in range(self.width):
                block = self.grid[row][col]
                if block is not None:
                    block.move(1, 0)
                    self.grid[row][col] = None
                    self.grid[row+1][col] = block

        return len(full_rows)

class Block:
    def __init__(self, color, positions):
        self.color = color
        self.positions = positions

    def get_block_positions(self):
        return [(row, col) for row, col in self.positions]

    def move(self, d_row, d_col):
        self.positions = [(row+d_row, col+d_col) for row, col in self.positions]

    def rotate(self):
        center_row = sum(row for row, col in self.positions) / len(self.positions)
        center_col = sum(col for row, col in self.positions) / len(self.positions)

        new_positions = []
        for row, col in self.positions:
            d_row, d_col = row - center_row, col - center_col
            new_positions.append((center_row - d_col, center_col + d_row))

        self.positions = new_positions
def generate_clump(clump_matrix, block_dict):
    clump = []
    for row_index, row in enumerate(clump_matrix):
        for col_index, block in enumerate(row):
            if block:
                block_image = block_dict[block]
                x = col_index * BLOCK_SIZE
                y = row_index * BLOCK_SIZE
                clump.append(Block(block_image, x, y, block))
    return clump


def can_move_down(clump, grid):
    for block in clump:
        row = block.row + 1
        if row == GRID_ROWS or grid[row][block.col]:
            return False
    return True


def move_down(clump):
    for block in clump:
        block.move(0, BLOCK_SIZE)


def clear_rows(grid):
    rows_cleared = 0
    for row_index in range(GRID_ROWS):
        if all(grid[row_index]):
            for above_row_index in range(row_index, 0, -1):
                grid[above_row_index] = grid[above_row_index - 1][:]
            grid[0] = [None] * GRID_COLS
            rows_cleared += 1
    return rows_cleared
def draw_grid():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            screen.blit(matrixImg, (x * BLOCK_SIZE, y * BLOCK_SIZE))

def draw_block(x, y, color):
    screen.blit(block_dict[color], (x * BLOCK_SIZE, y * BLOCK_SIZE))

def can_move_sideways(delta_x):
    for block in CURRENT_CLUMP:
        x, y = block
        if x + delta_x < 0 or x + delta_x >= GRID_COLS:
            return False
        if GRID_ROWS - 1 >= y >= 0:
            if GRID[y][x + delta_x]:
                return False
    return True

def game_loop():
    global CURRENT_CLUMP, NEXT_CLUMP
    while True:
        draw_grid()
        draw_block(CURRENT_CLUMP, block_dict)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and can_move_sideways(-1):
                    CURRENT_CLUMP.move_sideways(-1)
                elif event.key == pygame.K_RIGHT and can_move_sideways(1):
                    CURRENT_CLUMP.move_sideways(1)
                elif event.key == pygame.K_DOWN and can_move_down():
                    CURRENT_CLUMP.move_down()
                elif event.key == pygame.K_SPACE:
                    CURRENT_CLUMP.rotate()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        if can_move_down():
            CURRENT_CLUMP.move_down()
        else:
            add_clump_to_grid(CURRENT_CLUMP, GRID_ROWS, GRID_COLS)
            clear_rows(GRID_ROWS, GRID_COLS, BLOCK_SIZE)
            clear_columns(GRID_ROWS, GRID_COLS, BLOCK_SIZE)
            CURRENT_CLUMP = NEXT_CLUMP
            NEXT_CLUMP = generate_clump(clump_matrix, block_dict)
while True:
    game_loop()

