# ============================================================
# game_state.py
# ------------------------------------------------------------
# Stores all game data.
#
# In Part 2 this file now includes:
# - player stats
# - current turn
# - game result data
# - action log
# ============================================================

from dataclasses import dataclass, field
from settings import (
    PLAYER_A_START,
    PLAYER_B_START,
    MAX_HP,
    MAX_ENERGY,
    MAX_TURNS
)


@dataclass
class Player:
    """
    Represents one player on the board.
    """
    name: str
    pos: tuple
    hp: int = MAX_HP
    energy: int = MAX_ENERGY
    defend_active: bool = False
    shield_active: bool = False
    queen_control: int = 0


@dataclass
class GameState:
    """
    Full game state container.
    """
    player_a: Player = field(default_factory=lambda: Player("A", PLAYER_A_START))
    player_b: Player = field(default_factory=lambda: Player("B", PLAYER_B_START))

    # Whose turn is active right now
    current_turn: str = "A"

    # Turn number starts from 1
    turn_count: int = 1
    max_turns: int = MAX_TURNS

    # End state
    winner: str | None = None
    winner_reason: str = ""
    game_over: bool = False

    # Small text history
    action_log: list[str] = field(default_factory=lambda: [
        "Game started."
    ])

    def get_current_player(self):
        """
        Return the player whose turn is active.
        """
        return self.player_a if self.current_turn == "A" else self.player_b

    def get_other_player(self):
        """
        Return the opponent player.
        """
        return self.player_b if self.current_turn == "A" else self.player_a