# ============================================================
# settings.py
# ------------------------------------------------------------
# Global settings for Strategy Battle Arena
# ============================================================

TITLE = "Strategy Battle Arena"

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 860
FPS = 60

# ----------------------------
# Board settings
# ----------------------------
GRID_SIZE = 7
CELL_SIZE = 88

BOARD_X = 55
BOARD_Y = 110

BOARD_WIDTH = GRID_SIZE * CELL_SIZE
BOARD_HEIGHT = GRID_SIZE * CELL_SIZE

# ----------------------------
# Side panel settings
# ----------------------------
SIDE_PANEL_X = BOARD_X + BOARD_WIDTH + 40
SIDE_PANEL_Y = 110
SIDE_PANEL_WIDTH = 520
SIDE_PANEL_HEIGHT = 650

# ----------------------------
# Game values
# ----------------------------
MAX_HP = 100
MAX_ENERGY = 100
MAX_TURNS = 40

ATTACK_COST = 10
DEFEND_COST = 5
HEAL_COST = 12

ATTACK_DAMAGE = 15
HEAL_AMOUNT = 12
ENERGY_BONUS = 10
TRAP_DAMAGE = 8

# ----------------------------
# Starting positions
# ----------------------------
PLAYER_A_START = (0, 0)
PLAYER_B_START = (0, 6)

# ----------------------------
# Objective
# ----------------------------
QUEEN_POS = (6, 3)

# ----------------------------
# Special cells
# ----------------------------
ENERGY_CELLS = [
    (2, 5),
    (3, 4),
    (4, 5),
    (5, 2),
    (4, 1)
]

TRAP_CELLS = [
    (2, 3),
    (4, 3),
    (5, 4),
    (3, 1)
]

SHIELD_CELLS = [
    (2, 2),
    (3, 3),
    (5, 5)
]

# ----------------------------
# Main colors
# ----------------------------
BG_COLOR = (8, 14, 26)

PANEL_BG = (20, 28, 42)
PANEL_BORDER = (78, 102, 140)

BOARD_FRAME = (16, 24, 40)
BOARD_LINE = (72, 92, 122)

CELL_LIGHT = (88, 110, 155)
CELL_DARK = (66, 84, 128)

TEXT_MAIN = (245, 247, 250)
TEXT_SOFT = (196, 205, 220)
TEXT_GOLD = (255, 220, 120)
TEXT_MUTED = (150, 165, 190)

WHITE = (255, 255, 255)

# ----------------------------
# Player colors
# ----------------------------
A_COLOR = (50, 145, 255)
A_BORDER = (20, 92, 190)

B_COLOR = (214, 62, 120)
B_BORDER = (145, 28, 82)

# ----------------------------
# Special cell colors
# ----------------------------
ENERGY_COLOR = (65, 215, 125)
ENERGY_BORDER = (28, 150, 80)

TRAP_COLOR = (245, 120, 82)
TRAP_BORDER = (185, 72, 38)

SHIELD_COLOR = (170, 118, 255)
SHIELD_BORDER = (112, 70, 200)

QUEEN_COLOR = (32, 46, 76)
QUEEN_BORDER = (255, 214, 90)

# ----------------------------
# Bars
# ----------------------------
HP_BG = (72, 28, 38)
HP_FILL = (240, 82, 104)

ENERGY_BG = (28, 56, 82)
ENERGY_FILL = (88, 182, 255)

# ----------------------------
# UI boxes
# ----------------------------
TURN_BOX = (28, 38, 58)
HIGHLIGHT = (255, 214, 102)
LOG_BOX = (14, 21, 34)
LEGEND_BOX = (18, 25, 38)
BADGE_BG = (36, 52, 78)