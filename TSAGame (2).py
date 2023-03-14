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

# Set the dimensions of the grid
SCREEN_WIDTH = 12
SCREEN_HEIGHT = 18

# Set the size of each block in pixels
BLOCK_SIZE = 30

# Set the font for displaying the score and timer
FONT_NAME = pygame.font.match_font('arial')
SCORE_FONT = pygame.font.match_font('arial')
TIMER_FONT = pygame.font.match_font('arial')
GAME_OVER_FONT = pygame.font.match_font('arial')

NUM_ROWS = 8
NUM_COLS = 10
FPS = 60
MAX_TIMER = 5

clock = pygame.time.Clock()
clock.tick(FPS)
class Block:
    """A single block in the grid."""

    def __init__(self, color):
        self.color = color


class BlockGroup:
    """A group of four blocks that falls down the grid."""

    def __init__(self, blocks):
        self.blocks = blocks
    
    @classmethod
    def random(cls):
        blocks = []
        for i in range(4):
            block = (random.randint(0, 9), random.randint(0, 9))
            blocks.append(block)
        return cls(blocks)

    def __init__(self):
        self.blocks = [
            Block(random.choice([RED, GREEN, BLUE, YELLOW])),
            Block(random.choice([RED, GREEN, BLUE, YELLOW])),
            Block(random.choice([RED, GREEN, BLUE, YELLOW])),
            Block(random.choice([RED, GREEN, BLUE, YELLOW])),
        ]
        self.x = 5
        self.y = 0
        self.rotation = 0

    def rotate(self):
        """Rotate the block group."""
        self.rotation = (self.rotation + 1) % 4

    def move_left(self):
        """Move the block group to the left."""
        self.x -= 1

    def move_right(self):
        """Move the block group to the right."""
        self.x += 1

    def move_down(self):
        """Move the block group down."""
        self.y += 1


class BlockGrid:
    """The grid that contains the blocks."""

    def __init__(self, rows, cols):
        """Initialize the grid with the specified number of rows and columns."""
        self.rows = rows
        self.cols = cols
        self.grid = [[None for _ in range(cols)] for _ in range(rows)]
        self.current_block = None
        self.score = 0
        self.timer = clock.tick(FPS)
        self.game_over = False

    def create_falling_block(self):
        """Create a new falling block."""
        self.current_block = BlockGroup.random()
        self.current_block.move(self.cols // 2 - 1, 0)

    def update(self):
        """Update the game state."""
        if self.current_block is None:
            self.create_falling_block()

        # Check if the current block can move down
        if self.current_block.can_move(0, 1):
            self.current_block.move(0, 1)
        else:
            # The block can't move down, so add it to the grid and create a new falling block
            self.current_block.add_to_grid(self.grid)
            cleared = self.clear_groups()
            self.score += 30 + 10 * (len(cleared) - 1)
            self.current_block = None

        # Check if any blocks are above the red line
        for col in range(self.cols):
            if self.grid[0][col] is not None:
                self.timer.count_down()
                self.game_over = True
                return

        # Update the timer
        self.timer.update()

    def clear_groups(self):
        """Clear all groups of three or more blocks and return the list of cleared blocks."""
        groups = self.get_groups()
        for group in groups:
            for block in group:
                block.remove_from_grid(self.grid)
        return [block for group in groups for block in group]

    def get_groups(self):
        """Return a list of all groups of three or more adjacent blocks of the same color."""
        groups = []
        visited = set()

        for row in range(self.rows):
            for col in range(self.cols):
                block = self.grid[row][col]
                if block is not None and block not in visited:
                    group = self.get_group(block)
                    if len(group) >= 3:
                        groups.append(group)
                    visited.update(group)

        return groups

    def get_group(self, block):
        """Return the group of adjacent blocks of the same color as the specified block."""
        color = block.color
        visited = {block}
        queue = [block]

        while queue:
            block = queue.pop(0)
            for neighbor in block.get_neighbors(self.grid):
                if neighbor not in visited and neighbor.color == color:
                    visited.add(neighbor)
                    queue.append(neighbor)

        return visited

    def handle_input(self, key):
        """Handle user input."""
        if key == "left" and self.current_block.can_move(-1, 0):
            self.current_block.move(-1, 0)
        elif key == "right" and self.current_block.can_move(1, 0):
            self.current_block.move(1, 0)
        elif key == "down" and self.current_block.can_move(0, 1):
            self.current_block.move(0, 1)
        elif key == "rotate":
            self.current_block.rotate()

    def draw(self, screen):
        """Draw the grid on the specified screen."""
        screen.fill((255, 255, 255))

        # Draw the blocks in the grid
        for row in range(self.rows):
            for col in range(self.cols):
                block = self.grid[row][col]
                if block is not None:
                    rect = pygame.Rect(col * BLOCK_SIZE, row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                    pygame.draw.rect(screen, block.color, rect)

        # Draw the falling block
        if self.current_block is not None:
            for block in self.current_block.blocks:
                row, col = block.row + self.current_block.row, block.col + self.current_block.col
                rect = pygame.Rect(col * BLOCK_SIZE, row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                pygame.draw.rect(screen, block.color, rect)

        # Draw the cursor
        if self.cursor is not None:
            rect = pygame.Rect(self.cursor.col * BLOCK_SIZE, self.cursor.row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(screen, (255, 0, 0), rect, 2)

        # Draw the score
        score_text = SCORE_FONT.render(f"Score: {self.score}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))

        # Draw the timer
        timer_text = TIMER_FONT.render(f"Time left: {self.timer // FPS}", True, (0, 0, 0))
        screen.blit(timer_text, (10, 50))

        # Draw the game over screen
        if self.game_over:
            game_over_text = GAME_OVER_FONT.render("Game Over", True, (255, 0, 0))
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))

        pygame.display.flip()

    def handle_input(self):
        """Handle user input."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.cursor.col -= 1
                elif event.key == pygame.K_RIGHT:
                    self.cursor.col += 1
                elif event.key == pygame.K_UP:
                    self.rotate_cursor()
                elif event.key == pygame.K_DOWN:
                    self.drop_falling_block()

    def rotate_cursor(self):
        """Rotate the block that the cursor is pointing to."""
        row, col = self.cursor.row, self.cursor.col
        if self.grid[row][col] is not None:
            self.grid[row][col].rotate()

    def drop_falling_block(self):
        """Drop the falling block into the grid."""
        if self.falling_block is None:
            return

        # Add the falling block to the grid
        for block in self.falling_block.blocks:
            row, col = block.row + self.falling_block.row, block.col + self.falling_block.col
            if row < 0:
                self.game_over = True
                return
            self.grid[row][col] = block

        # Check for completed groups
        self.check_groups()

        # Reset the falling block and generate a new one
        self.falling_block = None
        self.generate_falling_block()

    def check_groups(self):
        """Check for completed groups and remove them."""
        for row in range(self.rows):
            for col in range(self.cols):
                block = self.grid[row][col]
                if block is not None:
                    # Check for a group of 3 blocks with the same color
                    if self.get_block(row - 1, col) == block and self.get_block(row - 2, col) == block:
                        # Remove the group of 3 blocks
                        self.remove_block(row, col)
                        self.remove_block(row - 1, col)
                        self.remove_block(row - 2, col)
                        self.score += 30
                        # Check for additional blocks that can be removed as a result of this removal
                        self.check_groups()
                    elif self.get_block(row, col - 1) == block and self.get_block(row, col - 2) == block:
                        # Remove the group of 3 blocks
                        self.remove_block(row, col)
                        self.remove_block(row, col - 1)
                        self.remove_block(row, col - 2)
                        self.score += 30
                        # Check for additional blocks that can be removed as a result of this removal
                        self.check_groups()
                    elif self.get_block(row - 1, col - 1) == block and self.get_block(row - 2, col - 2) == block:
                        # Remove the group of 3 blocks
                        self.remove_block(row, col)
                        self.remove_block(row - 1, col - 1)
                        self.remove_block(row - 2, col - 2)
                        self.score += 30
                        # Check for additional blocks that can be removed as a result of this removal
                        self.check_groups()
                    elif self.get_block(row - 1, col + 1) == block and self.get_block(row - 2, col + 2) == block:
                        # Remove the group of 3 blocks
                        self.remove_block(row, col)
                        self.remove_block(row - 1, col + 1)
                        self.remove_block(row - 2, col + 2)
                        self.score += 30
                        # Check for additional blocks that can be removed as a result of this removal
                        self.check_groups()

        # Update the display
        self.draw(self.screen)
        pygame.display.flip()

def run_game():
    # Initialize the game
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Block Game")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 30)

    # Create the block grid
    block_grid = BlockGrid(NUM_ROWS, NUM_COLS, BLOCK_SIZE)

    # Initialize game variables
    score = 0
    timer = MAX_TIMER
    game_over = False

    # Game loop
    while not game_over:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    block_grid.move_left()
                elif event.key == pygame.K_RIGHT:
                    block_grid.move_right()
                elif event.key == pygame.K_UP:
                    block_grid.rotate_clockwise()
                elif event.key == pygame.K_DOWN:
                    block_grid.rotate_counter_clockwise()

        # Update the game state
        block_grid.update()
        block_grid.check_groups()

        # Update the score
        num_cleared_blocks = block_grid.num_cleared_blocks
        if num_cleared_blocks > 0:
            score += 30 + 10 * (num_cleared_blocks - 1)

        # Update the timer
        if block_grid.has_block_over_red_line():
            timer -= 1
        else:
            timer = MAX_TIMER

        # Check if the game is over
        if timer <= 0:
            game_over = True

        # Draw the game
        block_grid.draw(screen)
        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))
        timer_text = font.render(f"Timer: {timer}", True, (0, 0, 0))
        screen.blit(timer_text, (SCREEN_WIDTH - timer_text.get_width() - 10, 10))
        pygame.display.flip()

        # Wait for the next frame
        clock.tick(FPS)

    # Game over
    game_over_text = font.render("Game Over", True, (255, 0, 0))
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(2000)

    pygame.quit()

if __name__ == "__main__":
    run_game()
