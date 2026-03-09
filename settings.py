# ============================================================
# settings.py
# ------------------------------------------------------------
# This file stores all constant values used in the game.
# Keeping these values in one file makes the project cleaner.
# If you want to change colors, board size, window size, etc.,
# you can do it here without touching the main logic.
# ============================================================

# ----------------------------
# Window information
# ----------------------------
TITLE = "Strategy Battle Arena"

# Total window size
WINDOW_WIDTH = 1220
WINDOW_HEIGHT = 820

# Frames per second
FPS = 60

# ----------------------------
# Board information
# ----------------------------
GRID_SIZE = 7          # 7x7 board
CELL_SIZE = 88         # width and height of one square cell

# Top-left corner of the board on the screen
BOARD_X = 55
BOARD_Y = 100

# Full board width and height
BOARD_WIDTH = GRID_SIZE * CELL_SIZE
BOARD_HEIGHT = GRID_SIZE * CELL_SIZE

# ----------------------------
# Right-side panel information
# ----------------------------
SIDE_PANEL_X = BOARD_X + BOARD_WIDTH + 40
SIDE_PANEL_Y = 100
SIDE_PANEL_WIDTH = 470
SIDE_PANEL_HEIGHT = 620

# ----------------------------
# Game values (used later)
# ----------------------------
MAX_HP = 100
MAX_ENERGY = 100
MAX_TURNS = 40

# Action costs and effects
ATTACK_COST = 10
DEFEND_COST = 5
HEAL_COST = 12

ATTACK_DAMAGE = 15
HEAL_AMOUNT = 12
ENERGY_BONUS = 10
TRAP_DAMAGE = 8

# ----------------------------
# Board setup
# IMPORTANT:
# These are game coordinates, not screen coordinates.
#
# In game logic:
# (0,0) means bottom-left of the board
# (6,6) means top-right of the board
# ----------------------------
PLAYER_A_START = (0, 0)
PLAYER_B_START = (0, 6)

# Main objective cell
QUEEN_POS = (6, 3)

# Special cells
ENERGY_CELLS = [(2, 4), (4, 3)]
TRAP_CELLS = [(1, 3), (3, 2)]
SHIELD_CELLS = [(2, 2)]

# ----------------------------
# Colors
# ----------------------------

# Background of whole window
BG_COLOR = (17, 22, 30)

# Side panel colors
PANEL_BG = (29, 36, 47)
PANEL_BORDER = (70, 82, 100)

# Board frame and grid line colors
BOARD_FRAME = (35, 42, 55)
BOARD_LINE = (70, 78, 95)

# Checkerboard cell colors
CELL_LIGHT = (232, 235, 242)
CELL_DARK = (214, 220, 229)

# Text colors
TEXT_MAIN = (245, 247, 250)
TEXT_SOFT = (182, 189, 202)
TEXT_GOLD = (255, 214, 102)

# Player A colors
A_COLOR = (42, 122, 220)
A_BORDER = (20, 78, 158)

# Player B colors
B_COLOR = (219, 58, 70)
B_BORDER = (150, 33, 45)

# Energy cell colors
ENERGY_COLOR = (84, 186, 102)
ENERGY_BORDER = (49, 132, 67)

# Trap cell colors
TRAP_COLOR = (225, 74, 74)
TRAP_BORDER = (168, 40, 40)

# Shield cell colors
SHIELD_COLOR = (137, 103, 219)
SHIELD_BORDER = (95, 67, 175)

# Queen cell colors
QUEEN_COLOR = (50, 64, 84)
QUEEN_BORDER = (255, 205, 95)

# HP bar colors
HP_BG = (70, 35, 45)
HP_FILL = (222, 74, 96)

# Energy bar colors
ENERGY_BG = (35, 54, 72)
ENERGY_FILL = (78, 164, 240)

# Misc UI colors
TURN_BOX = (38, 46, 60)
LOG_BOX = (23, 29, 38)
HIGHLIGHT = (255, 223, 120)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)