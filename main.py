# ============================================================
# main.py
# ------------------------------------------------------------
# Entry point of Strategy Battle Arena
# Shows result clearly at the bottom when game ends
# ============================================================

import pygame

from settings import (
    TITLE,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    FPS,
    BG_COLOR,
    TEXT_MAIN,
    TEXT_GOLD,
)
from game_state import GameState
from board import draw_everything, draw_text
from game_logic import play_one_ai_turn


def load_fonts():
    fonts = {
        "title": pygame.font.SysFont("segoe ui", 30, bold=True),
        "heading": pygame.font.SysFont("segoe ui", 22, bold=True),
        "body": pygame.font.SysFont("segoe ui", 18),
        "small": pygame.font.SysFont("segoe ui", 14),
        "marker": pygame.font.SysFont("arial", 30, bold=True),
    }
    return fonts


def winner_label(winner):
    if winner == "A":
        return "AI A (Minimax)"
    elif winner == "B":
        return "AI B (MCTS)"
    return "Draw"


def main():
    pygame.init()

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(TITLE)

    clock = pygame.time.Clock()
    fonts = load_fonts()
    state = GameState()

    AI_STEP_DELAY_MS = 850
    last_ai_step_time = pygame.time.get_ticks()

    running = True

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        now = pygame.time.get_ticks()

        if not state.game_over and now - last_ai_step_time >= AI_STEP_DELAY_MS:
            play_one_ai_turn(state)
            last_ai_step_time = now

        screen.fill(BG_COLOR)
        draw_everything(screen, state, fonts)

        if state.game_over:
            draw_text(
                screen,
                f"Winner: {winner_label(state.winner)}",
                fonts["heading"],
                TEXT_GOLD,
                55,
                804
            )
            draw_text(
                screen,
                f"Reason: {state.winner_reason}",
                fonts["body"],
                TEXT_MAIN,
                55,
                832
            )

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()