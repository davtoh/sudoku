import pygame
import sys
import random

pygame.init()

# Screen setup
info = pygame.display.Info()
screen_width = info.current_w
screen_height = info.current_h
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Sudoku")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (100, 100, 255, 100)
RED = (255, 0, 0)
GREEN = (0, 200, 0)

# Fonts
font = pygame.font.SysFont(None, 48)
small_font = pygame.font.SysFont(None, 36)

# Grid setup
GRID_SIZE = 9

# Dynamic scaling
def calculate_board_geometry():
    board_size = min(screen_width, screen_height - 100)  # leave space for keypad
    cell_size = board_size // GRID_SIZE
    offset_x = (screen_width - board_size) // 2
    offset_y = (screen_height - 100 - board_size) // 2
    return board_size, cell_size, offset_x, offset_y

BOARD_SIZE, CELL_SIZE, OFFSET_X, OFFSET_Y = calculate_board_geometry()

# Keypad setup
keypad_buttons = []
keypad_origin_y = BOARD_SIZE + OFFSET_Y + 20
button_size = 60
padding = 10

def center_number(x, y):
    return (x-padding+CELL_SIZE//2, y-padding+CELL_SIZE//2)

for i in range(9):
    x = (i % 3) * (button_size + padding) + 100
    y = (i // 3) * (button_size + padding) + keypad_origin_y
    rect = pygame.Rect(x, y, button_size, button_size)
    keypad_buttons.append((rect, i+1))

# Erase button
erase_rect = pygame.Rect(3*(button_size+padding)+100, keypad_origin_y, button_size, button_size)
keypad_buttons.append((erase_rect, 0))

# Win overlay image
WIN_IMAGE_PATH = "victory.jpg"  # set path if desired
win_image = None
if WIN_IMAGE_PATH:
    try:
        win_image = pygame.image.load(WIN_IMAGE_PATH)
        win_image = pygame.transform.scale(win_image, (200, 200))
    except:
        win_image = None

# Functions to generate puzzle
def create_full_grid():
    base = 3
    side = base*base

    def pattern(r,c): return (base*(r%base)+r//base+c)%side
    def shuffle(s): return random.sample(s,len(s))

    rBase = range(base)
    rows  = [ g*base + r for g in shuffle(rBase) for r in shuffle(rBase) ]
    cols  = [ g*base + c for g in shuffle(rBase) for c in shuffle(rBase) ]
    nums  = shuffle(range(1,base*base+1))

    return [[nums[pattern(r,c)] for c in cols] for r in rows]

def remove_numbers(grid, empties=40):
    puzzle = [row[:] for row in grid]
    for _ in range(empties):
        row = random.randint(0,8)
        col = random.randint(0,8)
        puzzle[row][col] = 0
    return puzzle

# Start game
def new_game():
    solution = create_full_grid()
    puzzle = remove_numbers(solution, empties=40)
    user_grid = [[0]*9 for _ in range(9)]
    return puzzle, solution, user_grid

# Draw board
def draw_board(puzzle, solution, user_grid, selected):
    screen.fill(WHITE)

    # Grid lines
    for i in range(GRID_SIZE+1):
        line_width = 3 if i%3==0 else 1
        pygame.draw.line(screen, BLACK, (OFFSET_X, OFFSET_Y + i*CELL_SIZE), (OFFSET_X + BOARD_SIZE, OFFSET_Y + i*CELL_SIZE), line_width)
        pygame.draw.line(screen, BLACK, (OFFSET_X + i*CELL_SIZE, OFFSET_Y), (OFFSET_X + i*CELL_SIZE, OFFSET_Y + BOARD_SIZE), line_width)

    # Cells
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            x = OFFSET_X + col*CELL_SIZE
            y = OFFSET_Y + row*CELL_SIZE

            if selected == (row,col):
                highlight = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
                highlight.fill(BLUE)
                screen.blit(highlight, (x, y))

            if puzzle[row][col] != 0:
                # Pre-filled numbers always black
                text = font.render(str(puzzle[row][col]), True, BLACK)
                screen.blit(text, center_number(x, y))
            elif user_grid[row][col] != 0:
                # User-entered numbers green/red
                color = GREEN if user_grid[row][col] == solution[row][col] else RED
                text = font.render(str(user_grid[row][col]), True, color)
                screen.blit(text, center_number(x, y))

    # Keypad
    for rect, value in keypad_buttons:
        pygame.draw.rect(screen, GRAY, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)
        text = font.render("X" if value == 0 else str(value), True, BLACK)
        screen.blit(text, (rect.x+15, rect.y+10))

def check_win(puzzle, user_grid, solution):
    for r in range(9):
        for c in range(9):
            if puzzle[r][c] == 0:
                if user_grid[r][c] != solution[r][c]:
                    return False
    return True

# Difficulty menu
def draw_menu():
    screen.fill(WHITE)
    title = font.render("Select Difficulty", True, BLACK)
    screen.blit(title, (screen_width//2 - title.get_width()//2, 100))

    buttons = []
    difficulties = ["Easy", "Medium", "Hard"]
    for i, level in enumerate(difficulties):
        rect = pygame.Rect(screen_width//2 - 100, 200 + i*100, 200, 60)
        pygame.draw.rect(screen, GRAY, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)
        text = small_font.render(level, True, BLACK)
        screen.blit(text, (rect.x + rect.width//2 - text.get_width()//2, rect.y+15))
        buttons.append((rect, level))
    return buttons

# Win overlay
def draw_win_overlay():
    overlay = pygame.Surface((screen_width, screen_height))
    overlay.set_alpha(200)
    overlay.fill(WHITE)
    screen.blit(overlay, (0,0))

    if win_image:
        screen.blit(win_image, (screen_width//2 - win_image.get_width()//2, 150))
    text = font.render("YOU WIN!", True, GREEN)
    screen.blit(text, (screen_width//2 - text.get_width()//2, 400))

# Main loop
state = "menu"
menu_buttons = draw_menu()
puzzle, solution, user_grid = None, None, None
selected = None

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if state == "menu":
            if event.type == pygame.MOUSEBUTTONDOWN:
                for rect, level in menu_buttons:
                    if rect.collidepoint(event.pos):
                        puzzle, solution, user_grid = new_game()
                        state = "playing"

        elif state == "playing":
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if OFFSET_X <= pos[0] < OFFSET_X+BOARD_SIZE and OFFSET_Y <= pos[1] < OFFSET_Y+BOARD_SIZE:
                    col = (pos[0]-OFFSET_X)//CELL_SIZE
                    row = (pos[1]-OFFSET_Y)//CELL_SIZE
                    if puzzle[row][col] == 0:
                        selected = (row,col)
                for rect, value in keypad_buttons:
                    if rect.collidepoint(pos) and selected:
                        r, c = selected
                        user_grid[r][c] = value
                        if check_win(puzzle, user_grid, solution):
                            state = "win"

        elif state == "win":
            if event.type == pygame.MOUSEBUTTONDOWN:
                state = "menu"
                menu_buttons = draw_menu()

    if state == "menu":
        draw_menu()
    elif state == "playing":
        draw_board(puzzle, solution, user_grid, selected)
    elif state == "win":
        draw_board(puzzle, solution, user_grid, selected)
        draw_win_overlay()

    pygame.display.flip()
