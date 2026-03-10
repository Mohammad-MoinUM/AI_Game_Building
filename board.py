# ============================================================
# board.py
# ------------------------------------------------------------
# Final visual board layer
# - animated pulse / glow
# - active AI badge
# - thinking indicator
# - legend box
# - no action log
# - fixed lower-right overlap
# ============================================================

import math
import pygame
from settings import *


def game_to_screen(cell_x, cell_y):
    """
    Convert game coordinates to screen coordinates.

    Game coordinates:
    (0,0) = bottom-left

    Pygame coordinates:
    (0,0) = top-left
    """
    screen_x = BOARD_X + cell_x * CELL_SIZE
    screen_y = BOARD_Y + (GRID_SIZE - 1 - cell_y) * CELL_SIZE
    return screen_x, screen_y


def draw_text(surface, text, font, color, x, y, center=False):
    """
    General helper for drawing text.
    """
    img = font.render(text, True, color)
    rect = img.get_rect()

    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)

    surface.blit(img, rect)


def get_pulse_value(speed=0.004):
    """
    Smooth oscillating value between 0 and 1.
    Used for glow / pulse animation.
    """
    t = pygame.time.get_ticks()
    return (math.sin(t * speed) + 1.0) / 2.0


def draw_background_effect(surface):
    """
    Draw large soft background glows.
    """
    glow_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)

    pygame.draw.circle(glow_surface, (70, 90, 180, 22), (280, 360), 280)
    pygame.draw.circle(glow_surface, (110, 70, 180, 16), (560, 200), 220)
    pygame.draw.circle(glow_surface, (60, 170, 130, 14), (980, 560), 250)

    surface.blit(glow_surface, (0, 0))


def draw_board_title(surface, fonts):
    """
    Draw title and subtitle.
    """
    draw_text(surface, "STRATEGY BATTLE ARENA", fonts["title"], TEXT_MAIN, BOARD_X, 22)
    draw_text(surface, "Minimax vs MCTS • Tactical Grid Battle", fonts["small"], TEXT_GOLD, BOARD_X + 4, 64)


def draw_board_background(surface):
    """
    Draw layered board shadow and frame.
    """
    shadow1 = pygame.Rect(BOARD_X - 26, BOARD_Y - 26, BOARD_WIDTH + 52, BOARD_HEIGHT + 52)
    pygame.draw.rect(surface, (5, 8, 14), shadow1, border_radius=34)

    shadow2 = pygame.Rect(BOARD_X - 18, BOARD_Y - 18, BOARD_WIDTH + 36, BOARD_HEIGHT + 36)
    pygame.draw.rect(surface, (10, 18, 32), shadow2, border_radius=30)

    frame = pygame.Rect(BOARD_X - 8, BOARD_Y - 8, BOARD_WIDTH + 16, BOARD_HEIGHT + 16)
    pygame.draw.rect(surface, BOARD_FRAME, frame, border_radius=24)


def draw_cells(surface):
    """
    Draw board cells with subtle shine.
    """
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            x = BOARD_X + col * CELL_SIZE
            y = BOARD_Y + row * CELL_SIZE
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)

            color = CELL_LIGHT if (row + col) % 2 == 0 else CELL_DARK
            pygame.draw.rect(surface, color, rect)

            inner = pygame.Rect(x + 2, y + 2, CELL_SIZE - 4, CELL_SIZE - 4)
            overlay = pygame.Surface((inner.width, inner.height), pygame.SRCALPHA)
            pygame.draw.rect(
                overlay,
                (255, 255, 255, 10),
                (0, 0, inner.width, inner.height),
                border_radius=10
            )
            surface.blit(overlay, inner.topleft)


def draw_grid_lines(surface):
    """
    Draw board lines.
    """
    for i in range(GRID_SIZE + 1):
        x = BOARD_X + i * CELL_SIZE
        pygame.draw.line(surface, BOARD_LINE, (x, BOARD_Y), (x, BOARD_Y + BOARD_HEIGHT), 2)

        y = BOARD_Y + i * CELL_SIZE
        pygame.draw.line(surface, BOARD_LINE, (BOARD_X, y), (BOARD_X + BOARD_WIDTH, y), 2)


def draw_coordinate_labels(surface, fonts):
    """
    Draw x and y labels.
    """
    for x in range(GRID_SIZE):
        sx, _ = game_to_screen(x, 0)
        draw_text(surface, str(x), fonts["small"], TEXT_SOFT, sx + CELL_SIZE // 2, BOARD_Y + BOARD_HEIGHT + 20, center=True)

    for y in range(GRID_SIZE):
        _, sy = game_to_screen(0, y)
        draw_text(surface, str(y), fonts["small"], TEXT_SOFT, BOARD_X - 24, sy + CELL_SIZE // 2, center=True)


def draw_glow(surface, rect, glow_color, strength=1.0, layers=4):
    """
    Draw soft rounded glow around a rect.
    """
    for i in range(layers, 0, -1):
        grow = i * 10
        glow_rect = rect.inflate(grow, grow)

        temp = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
        alpha = int((8 + i * 6) * strength)

        pygame.draw.rect(
            temp,
            (*glow_color, alpha),
            (0, 0, glow_rect.width, glow_rect.height),
            border_radius=22
        )
        surface.blit(temp, glow_rect.topleft)


def draw_special_cell(surface, pos, label, fill_color, border_color, font, glow=False, pulse=False):
    """
    Draw one E/T/S/Q cell.
    """
    x, y = game_to_screen(*pos)

    outer = pygame.Rect(x + 9, y + 9, CELL_SIZE - 18, CELL_SIZE - 18)
    inner = pygame.Rect(x + 13, y + 13, CELL_SIZE - 26, CELL_SIZE - 26)

    glow_strength = 1.0
    if pulse:
        glow_strength = 0.7 + get_pulse_value(0.005) * 0.8

    if glow:
        draw_glow(surface, outer, border_color, strength=glow_strength, layers=4)

    pygame.draw.rect(surface, border_color, outer, border_radius=18)
    pygame.draw.rect(surface, fill_color, inner, border_radius=16)

    shine = pygame.Surface((inner.width, inner.height), pygame.SRCALPHA)
    pygame.draw.rect(
        shine,
        (255, 255, 255, 20),
        (0, 0, inner.width, inner.height // 2),
        border_radius=16
    )
    surface.blit(shine, inner.topleft)

    draw_text(surface, label, font, WHITE, inner.centerx, inner.centery, center=True)


def draw_special_cells(surface, fonts):
    """
    Draw all special cells.
    """
    marker_font = fonts["marker"]

    for cell in ENERGY_CELLS:
        draw_special_cell(surface, cell, "E", ENERGY_COLOR, ENERGY_BORDER, marker_font, glow=True, pulse=True)

    for cell in TRAP_CELLS:
        draw_special_cell(surface, cell, "T", TRAP_COLOR, TRAP_BORDER, marker_font, glow=False, pulse=False)

    for cell in SHIELD_CELLS:
        draw_special_cell(surface, cell, "S", SHIELD_COLOR, SHIELD_BORDER, marker_font, glow=True, pulse=True)

    draw_special_cell(surface, QUEEN_POS, "Q", QUEEN_COLOR, QUEEN_BORDER, marker_font, glow=True, pulse=True)


def draw_player(surface, player, fonts, main_color, border_color, is_active=False):
    """
    Draw player token with shadow, glow and active pulse.
    """
    x, y = game_to_screen(*player.pos)

    shadow = pygame.Rect(x + 10, y + 13, CELL_SIZE - 20, CELL_SIZE - 20)
    pygame.draw.ellipse(surface, (10, 14, 20), shadow)

    glow_rect = pygame.Rect(x + 6, y + 6, CELL_SIZE - 12, CELL_SIZE - 12)

    strength = 1.0
    if is_active:
        strength = 1.0 + get_pulse_value(0.006) * 0.8

    draw_glow(surface, glow_rect, border_color, strength=strength, layers=3)

    outer = pygame.Rect(x + 8, y + 8, CELL_SIZE - 16, CELL_SIZE - 16)
    mid = pygame.Rect(x + 12, y + 12, CELL_SIZE - 24, CELL_SIZE - 24)
    inner = pygame.Rect(x + 18, y + 18, CELL_SIZE - 36, CELL_SIZE - 36)

    pygame.draw.ellipse(surface, border_color, outer)
    pygame.draw.ellipse(surface, main_color, mid)

    lighter = tuple(min(255, c + 30) for c in main_color)
    pygame.draw.ellipse(surface, lighter, inner)

    draw_text(surface, player.name, fonts["marker"], WHITE, mid.centerx, mid.centery, center=True)


def draw_bar(surface, x, y, width, height, value, max_value, bg_color, fill_color):
    """
    Draw HP / Energy bar.
    """
    pygame.draw.rect(surface, bg_color, (x, y, width, height), border_radius=8)

    ratio = max(0, min(1, value / max_value))
    fill_w = int(width * ratio)

    pygame.draw.rect(surface, fill_color, (x, y, fill_w, height), border_radius=8)


def draw_divider(surface, x, y, width):
    """
    Draw subtle divider line.
    """
    pygame.draw.line(surface, (55, 72, 98), (x, y), (x + width, y), 1)


def draw_thinking_indicator(surface, x, y, fonts):
    """
    Draw animated thinking indicator.
    """
    phase = int((pygame.time.get_ticks() / 350) % 4)
    dots = "." * phase
    draw_text(surface, f"Evaluating{dots}", fonts["small"], TEXT_GOLD, x, y)


def draw_active_badge(surface, x, y, text, fonts):
    """
    Small badge for active AI.
    """
    badge_rect = pygame.Rect(x, y, 96, 30)
    pygame.draw.rect(surface, BADGE_BG, badge_rect, border_radius=12)
    pygame.draw.rect(surface, HIGHLIGHT, badge_rect, width=2, border_radius=12)
    draw_text(surface, text, fonts["small"], TEXT_MAIN, badge_rect.centerx, badge_rect.centery, center=True)


def draw_player_info(surface, player, title, fonts, x, y, active=False):
    """
    Draw one player's panel section.
    Compact spacing version.
    """
    draw_text(surface, title, fonts["heading"], TEXT_MAIN, x, y)

    if active:
        draw_active_badge(surface, x + 255, y - 2, "ACTIVE", fonts)

    draw_text(surface, f"Position: {player.pos}", fonts["body"], TEXT_SOFT, x, y + 32)
    draw_text(surface, f"Queen Control: {player.queen_control}", fonts["body"], TEXT_SOFT, x, y + 58)

    draw_text(surface, f"HP: {player.hp}", fonts["body"], TEXT_MAIN, x, y + 90)
    draw_bar(surface, x + 72, y + 96, 310, 16, player.hp, 100, HP_BG, HP_FILL)

    draw_text(surface, f"EN: {player.energy}", fonts["body"], TEXT_MAIN, x, y + 122)
    draw_bar(surface, x + 72, y + 128, 310, 16, player.energy, 100, ENERGY_BG, ENERGY_FILL)

    statuses = []
    if player.defend_active:
        statuses.append("Defend")
    if player.shield_active:
        statuses.append("Shield")
    if not statuses:
        statuses.append("None")

    draw_text(surface, f"Status: {', '.join(statuses)}", fonts["small"], TEXT_MUTED, x, y + 154)


def draw_legend(surface, fonts):
    """
    Draw legend box only.
    No action log below it.
    """
    rect = pygame.Rect(SIDE_PANEL_X + 28, SIDE_PANEL_Y + 520, SIDE_PANEL_WIDTH - 56, 82)
    pygame.draw.rect(surface, LEGEND_BOX, rect, border_radius=16)

    draw_text(surface, "Legend", fonts["heading"], TEXT_MAIN, rect.x + 14, rect.y + 8)

    items = [
        ("E = Energy", ENERGY_COLOR),
        ("T = Trap", TRAP_COLOR),
        ("S = Shield", SHIELD_COLOR),
        ("Q = Queen", QUEEN_BORDER),
    ]

    start_x = rect.x + 18
    y = rect.y + 48
    gap = 118

    for i, (label, color) in enumerate(items):
        cx = start_x + i * gap
        pygame.draw.circle(surface, color, (cx, y + 4), 6)
        draw_text(surface, label, fonts["small"], TEXT_SOFT, cx + 12, y - 6)


def draw_side_panel(surface, state, fonts):
    """
    Draw right-side information panel.
    Action log removed.
    """
    shadow = pygame.Rect(SIDE_PANEL_X + 4, SIDE_PANEL_Y + 4, SIDE_PANEL_WIDTH, SIDE_PANEL_HEIGHT)
    pygame.draw.rect(surface, (7, 10, 18), shadow, border_radius=22)

    panel = pygame.Rect(SIDE_PANEL_X, SIDE_PANEL_Y, SIDE_PANEL_WIDTH, SIDE_PANEL_HEIGHT)
    pygame.draw.rect(surface, PANEL_BG, panel, border_radius=22)
    pygame.draw.rect(surface, PANEL_BORDER, panel, width=3, border_radius=22)

    draw_text(surface, "MATCH STATUS", fonts["heading"], TEXT_MAIN, SIDE_PANEL_X + 26, SIDE_PANEL_Y + 20)

    turn_rect = pygame.Rect(SIDE_PANEL_X + 26, SIDE_PANEL_Y + 58, SIDE_PANEL_WIDTH - 52, 68)
    pygame.draw.rect(surface, TURN_BOX, turn_rect, border_radius=14)
    pygame.draw.rect(surface, HIGHLIGHT, turn_rect, width=2, border_radius=14)

    draw_text(surface, f"Turn: {state.turn_count} / {state.max_turns}", fonts["body"], TEXT_MAIN, turn_rect.x + 16, turn_rect.y + 10)
    draw_text(surface, f"Current AI: {state.current_turn}", fonts["body"], TEXT_GOLD, turn_rect.x + 16, turn_rect.y + 36)
    draw_thinking_indicator(surface, turn_rect.right - 130, turn_rect.y + 38, fonts)

    # Player A section
    draw_player_info(
        surface,
        state.player_a,
        "AI A  •  Minimax",
        fonts,
        SIDE_PANEL_X + 26,
        SIDE_PANEL_Y + 155,
        active=(state.current_turn == "A")
    )

    draw_divider(surface, SIDE_PANEL_X + 26, SIDE_PANEL_Y + 325, SIDE_PANEL_WIDTH - 52)

    # Player B section
    draw_player_info(
        surface,
        state.player_b,
        "AI B  •  MCTS",
        fonts,
        SIDE_PANEL_X + 26,
        SIDE_PANEL_Y + 345,
        active=(state.current_turn == "B")
    )

    draw_legend(surface, fonts)


def draw_everything(surface, state, fonts):
    """
    Main function for drawing the full scene.
    """
    draw_background_effect(surface)
    draw_board_title(surface, fonts)
    draw_board_background(surface)
    draw_cells(surface)
    draw_grid_lines(surface)
    draw_coordinate_labels(surface, fonts)
    draw_special_cells(surface, fonts)

    draw_player(surface, state.player_a, fonts, A_COLOR, A_BORDER, is_active=(state.current_turn == "A"))
    draw_player(surface, state.player_b, fonts, B_COLOR, B_BORDER, is_active=(state.current_turn == "B"))

    draw_side_panel(surface, state, fonts)