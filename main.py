# ============================================================
# main.py
# ------------------------------------------------------------
# This is the entry point of the game.
# When you run "python main.py", this file starts everything.
#
# In Part 1, this file does these jobs:
# 1. initialize pygame
# 2. create the screen
# 3. create fonts
# 4. create game state
# 5. run the main loop
# 6. call drawing functions every frame
# ============================================================

import pygame

from settings import (
    TITLE,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    FPS,
    BG_COLOR,
    TEXT_MAIN
)
from game_state import GameState
from board import draw_everything, draw_text


def load_fonts():
    """
    Create and return all fonts used in the game.

    We keep fonts in one dictionary so that other files
    can access them by name.
    """
    fonts = {
        "title": pygame.font.SysFont("arial", 32, bold=True),
        "heading": pygame.font.SysFont("arial", 24, bold=True),
        "body": pygame.font.SysFont("arial", 20),
        "small": pygame.font.SysFont("arial", 16),
        "marker": pygame.font.SysFont("arial", 34, bold=True),
    }
    return fonts


def main():
    """
    Main game function.
    """
    # Start pygame
    pygame.init()

    # Create game window
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(TITLE)

    # Clock controls FPS
    clock = pygame.time.Clock()

    # Fonts used in the game
    fonts = load_fonts()

    # Create initial game state
    state = GameState()

    # This variable keeps the loop running
    running = True

    while running:
        # Keep loop at fixed FPS
        clock.tick(FPS)

        # -----------------------------
        # Handle events
        # -----------------------------
        for event in pygame.event.get():
            # If user clicks the close button, end the game
            if event.type == pygame.QUIT:
                running = False

        # -----------------------------
        # Drawing
        # -----------------------------
        # Fill background
        screen.fill(BG_COLOR)

        # Draw all visual game elements
        draw_everything(screen, state, fonts)

        # Small helper text at bottom
        draw_text(
            screen,
            "Part 1 loaded: Board and UI foundation complete",
            fonts["small"],
            TEXT_MAIN,
            55,
            760
        )

        # Update screen
        pygame.display.flip()

    # Close pygame safely
    pygame.quit()


# This line means:
# run main() only when this file is executed directly
if __name__ == "__main__":
    main()