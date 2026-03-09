# ============================================================
# board.py
# ------------------------------------------------------------
# This file handles drawing:
# - the board
# - coordinate labels
# - special cells
# - players
# - side panel
# - hp/energy bars
#
# Very important idea:
# We separate "drawing" from "game logic".
# That makes the code easier to understand and maintain.
# ============================================================

import pygame

from settings import (
    GRID_SIZE,
    CELL_SIZE,
    BOARD_X,
    BOARD_Y,
    BOARD_WIDTH,
    BOARD_HEIGHT,
    SIDE_PANEL_X,
    SIDE_PANEL_Y,
    SIDE_PANEL_WIDTH,
    SIDE_PANEL_HEIGHT,
    CELL_LIGHT,
    CELL_DARK,
    BOARD_FRAME,
    BOARD_LINE,
    ENERGY_CELLS,
    TRAP_CELLS,
    SHIELD_CELLS,
    QUEEN_POS,
    ENERGY_COLOR,
    ENERGY_BORDER,
    TRAP_COLOR,
    TRAP_BORDER,
    SHIELD_COLOR,
    SHIELD_BORDER,
    QUEEN_COLOR,
    QUEEN_BORDER,
    A_COLOR,
    A_BORDER,
    B_COLOR,
    B_BORDER,
    PANEL_BG,
    PANEL_BORDER,
    TEXT_MAIN,
    TEXT_SOFT,
    TEXT_GOLD,
    HP_BG,
    HP_FILL,
    ENERGY_BG,
    ENERGY_FILL,
    TURN_BOX,
    LOG_BOX,
    HIGHLIGHT,
    WHITE
)


def game_to_screen(cell_x, cell_y):
    """
    Convert game coordinates to screen coordinates.

    Game coordinates:
        (0,0) is bottom-left

    But Pygame screen coordinates:
        (0,0) is top-left

    So we must flip the y-axis.

    Example:
        game (0,0) -> bottom-left board cell
        screen     -> lower visible cell on the screen
    """
    screen_x = BOARD_X + cell_x * CELL_SIZE
    screen_y = BOARD_Y + (GRID_SIZE - 1 - cell_y) * CELL_SIZE
    return screen_x, screen_y


def draw_text(surface, text, font, color, x, y, center=False):
    """
    Draw text on the screen.

    surface -> where to draw
    text    -> string to show
    font    -> pygame font object
    color   -> text color
    x, y    -> position
    center  -> if True, text is centered at (x,y)
               if False, top-left starts at (x,y)
    """
    image = font.render(text, True, color)
    rect = image.get_rect()

    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)

    surface.blit(image, rect)


def draw_special_cell(surface, pos, label, fill_color, border_color, font):
    """
    Draw a special board cell with:
    - rounded colored box
    - label inside like E, T, S, Q
    """
    x, y = game_to_screen(*pos)

    # Inner rectangle so the marker does not fully touch grid lines
    rect = pygame.Rect(x + 9, y + 9, CELL_SIZE - 18, CELL_SIZE - 18)

    pygame.draw.rect(surface, fill_color, rect, border_radius=16)
    pygame.draw.rect(surface, border_color, rect, width=3, border_radius=16)

    draw_text(surface, label, font, WHITE, rect.centerx, rect.centery, center=True)


def draw_base_board(surface):
    """
    Draw the outer board and checker-style grid cells.
    """
    # Outer frame behind the board
    frame_rect = pygame.Rect(BOARD_X - 10, BOARD_Y - 10, BOARD_WIDTH + 20, BOARD_HEIGHT + 20)
    pygame.draw.rect(surface, BOARD_FRAME, frame_rect, border_radius=18)

    # Draw all cells
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            x = BOARD_X + col * CELL_SIZE
            y = BOARD_Y + row * CELL_SIZE

            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)

            # Alternate light and dark cells for nicer appearance
            if (row + col) % 2 == 0:
                color = CELL_LIGHT
            else:
                color = CELL_DARK

            pygame.draw.rect(surface, color, rect)

    # Draw grid lines
    for i in range(GRID_SIZE + 1):
        # Vertical line
        x = BOARD_X + i * CELL_SIZE
        pygame.draw.line(surface, BOARD_LINE, (x, BOARD_Y), (x, BOARD_Y + BOARD_HEIGHT), 2)

        # Horizontal line
        y = BOARD_Y + i * CELL_SIZE
        pygame.draw.line(surface, BOARD_LINE, (BOARD_X, y), (BOARD_X + BOARD_WIDTH, y), 2)


def draw_coordinate_labels(surface, fonts):
    """
    Draw x and y coordinate labels around the board.

    This helps the board match your project concept.
    """
    small_font = fonts["small"]

    # x-axis labels
    for x in range(GRID_SIZE):
        sx, sy = game_to_screen(x, 0)
        draw_text(
            surface,
            str(x),
            small_font,
            TEXT_SOFT,
            sx + CELL_SIZE // 2,
            BOARD_Y + BOARD_HEIGHT + 18,
            center=True
        )

    # y-axis labels
    for y in range(GRID_SIZE):
        sx, sy = game_to_screen(0, y)
        draw_text(
            surface,
            str(y),
            small_font,
            TEXT_SOFT,
            BOARD_X - 25,
            sy + CELL_SIZE // 2,
            center=True
        )


def draw_special_cells(surface, fonts):
    """
    Draw all special cells:
    E = energy
    T = trap
    S = shield
    Q = queen
    """
    marker_font = fonts["marker"]

    for pos in ENERGY_CELLS:
        draw_special_cell(surface, pos, "E", ENERGY_COLOR, ENERGY_BORDER, marker_font)

    for pos in TRAP_CELLS:
        draw_special_cell(surface, pos, "T", TRAP_COLOR, TRAP_BORDER, marker_font)

    for pos in SHIELD_CELLS:
        draw_special_cell(surface, pos, "S", SHIELD_COLOR, SHIELD_BORDER, marker_font)

    draw_special_cell(surface, QUEEN_POS, "Q", QUEEN_COLOR, QUEEN_BORDER, marker_font)


def draw_player(surface, player, fonts, main_color, border_color):
    """
    Draw a player piece.

    We use ellipse shapes instead of plain rectangles
    so the game looks better.
    """
    marker_font = fonts["marker"]
    x, y = game_to_screen(*player.pos)

    outer = pygame.Rect(x + 10, y + 10, CELL_SIZE - 20, CELL_SIZE - 20)
    inner = pygame.Rect(x + 14, y + 14, CELL_SIZE - 28, CELL_SIZE - 28)

    pygame.draw.ellipse(surface, border_color, outer)
    pygame.draw.ellipse(surface, main_color, inner)

    draw_text(surface, player.name, marker_font, WHITE, inner.centerx, inner.centery, center=True)


def draw_bar(surface, x, y, width, height, value, max_value, bg_color, fill_color):
    """
    Draw a simple progress bar.
    This will be used for HP and energy bars.
    """
    # background
    pygame.draw.rect(surface, bg_color, (x, y, width, height), border_radius=8)

    # filled amount
    ratio = max(0, min(1, value / max_value))
    fill_width = int(width * ratio)

    pygame.draw.rect(surface, fill_color, (x, y, fill_width, height), border_radius=8)


def draw_player_block(surface, x, y, title, player, fonts):
    """
    Draw one player's info block inside the side panel.
    """
    heading_font = fonts["heading"]
    body_font = fonts["body"]
    small_font = fonts["small"]

    draw_text(surface, title, heading_font, TEXT_MAIN, x, y)
    draw_text(surface, f"Position: {player.pos}", body_font, TEXT_SOFT, x, y + 34)
    draw_text(surface, f"Queen Control: {player.queen_control}", body_font, TEXT_SOFT, x, y + 60)

    draw_text(surface, f"HP: {player.hp}", body_font, TEXT_MAIN, x, y + 96)
    draw_bar(surface, x + 58, y + 100, 260, 16, player.hp, 100, HP_BG, HP_FILL)

    draw_text(surface, f"EN: {player.energy}", body_font, TEXT_MAIN, x, y + 132)
    draw_bar(surface, x + 58, y + 136, 260, 16, player.energy, 100, ENERGY_BG, ENERGY_FILL)

    # Build status text
    statuses = []
    if player.defend_active:
        statuses.append("Defend")
    if player.shield_active:
        statuses.append("Shield")
    if not statuses:
        statuses.append("None")

    draw_text(surface, f"Status: {', '.join(statuses)}", small_font, TEXT_SOFT, x, y + 168)


def draw_action_log(surface, state, fonts):
    """
    Draw the recent action log.
    In this part, it only shows initial messages.
    Later this will display real moves and actions.
    """
    heading_font = fonts["heading"]
    small_font = fonts["small"]

    log_x = SIDE_PANEL_X + 25
    log_y = SIDE_PANEL_Y + 465
    log_w = SIDE_PANEL_WIDTH - 50
    log_h = 125

    rect = pygame.Rect(log_x, log_y, log_w, log_h)
    pygame.draw.rect(surface, LOG_BOX, rect, border_radius=14)

    draw_text(surface, "Action Log", heading_font, TEXT_MAIN, log_x + 14, log_y + 10)

    # show last 4 messages
    recent_lines = state.action_log[-4:]

    for i, line in enumerate(recent_lines):
        draw_text(surface, f"- {line}", small_font, TEXT_SOFT, log_x + 16, log_y + 42 + i * 20)


def draw_side_panel(surface, state, fonts):
    """
    Draw the full right-side panel.
    """
    heading_font = fonts["heading"]
    body_font = fonts["body"]

    panel_rect = pygame.Rect(
        SIDE_PANEL_X,
        SIDE_PANEL_Y,
        SIDE_PANEL_WIDTH,
        SIDE_PANEL_HEIGHT
    )

    pygame.draw.rect(surface, PANEL_BG, panel_rect, border_radius=18)
    pygame.draw.rect(surface, PANEL_BORDER, panel_rect, width=3, border_radius=18)

    # Panel title
    draw_text(surface, "MATCH STATUS", heading_font, TEXT_MAIN, SIDE_PANEL_X + 24, SIDE_PANEL_Y + 20)

    # Current turn box
    turn_rect = pygame.Rect(SIDE_PANEL_X + 24, SIDE_PANEL_Y + 60, SIDE_PANEL_WIDTH - 48, 60)
    pygame.draw.rect(surface, TURN_BOX, turn_rect, border_radius=14)
    pygame.draw.rect(surface, HIGHLIGHT, turn_rect, width=2, border_radius=14)

    draw_text(surface, f"Turn: {state.turn_count} / {state.max_turns}", body_font, TEXT_MAIN, turn_rect.x + 16, turn_rect.y + 8)
    draw_text(surface, f"Current AI: {state.current_turn}", body_font, TEXT_GOLD, turn_rect.x + 16, turn_rect.y + 32)

    # Player A block
    draw_player_block(surface, SIDE_PANEL_X + 24, SIDE_PANEL_Y + 145, "AI A  •  Minimax", state.player_a, fonts)

    # Player B block
    draw_player_block(surface, SIDE_PANEL_X + 24, SIDE_PANEL_Y + 320, "AI B  •  MCTS", state.player_b, fonts)

    # Action log
    draw_action_log(surface, state, fonts)


def draw_everything(surface, state, fonts):
    """
    Main drawing function.
    This function is called from main.py every frame.

    It draws:
    - board
    - labels
    - special cells
    - players
    - side panel
    """
    draw_base_board(surface)
    draw_coordinate_labels(surface, fonts)
    draw_special_cells(surface, fonts)

    draw_player(surface, state.player_a, fonts, A_COLOR, A_BORDER)
    draw_player(surface, state.player_b, fonts, B_COLOR, B_BORDER)

    draw_side_panel(surface, state, fonts)