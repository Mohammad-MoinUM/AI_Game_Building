# ============================================================
# game_state.py
# ------------------------------------------------------------
# This file stores the data of the game.
# In this first part, the data is simple:
# - player positions
# - player HP and energy
# - current turn
# - turn count
# - log messages
#
# Later, AI and full rules will use this state.
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
    This class stores all information about one player.

    name           -> "A" or "B"
    pos            -> board position (x, y)
    hp             -> current health points
    energy         -> current energy
    defend_active  -> whether defend effect is active
    shield_active  -> whether shield effect is active
    queen_control  -> how many queen-control points this player has
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
    This class stores the full game state.

    player_a      -> data for player A
    player_b      -> data for player B
    current_turn  -> whose turn now ("A" or "B")
    turn_count    -> current turn number
    max_turns     -> total allowed turns
    winner        -> winner name later ("A", "B", or None)
    game_over     -> whether the game has ended
    action_log    -> messages shown in side panel
    """
    player_a: Player = field(default_factory=lambda: Player("A", PLAYER_A_START))
    player_b: Player = field(default_factory=lambda: Player("B", PLAYER_B_START))
    current_turn: str = "A"
    turn_count: int = 1
    max_turns: int = MAX_TURNS
    winner: str | None = None
    game_over: bool = False

    # action_log is a list of text messages
    action_log: list[str] = field(default_factory=lambda: [
        "Game initialized.",
        "Board loaded successfully.",
        "Waiting for AI logic in next parts."
    ])

    def get_current_player(self):
        """
        Return the player whose turn is currently active.
        """
        if self.current_turn == "A":
            return self.player_a
        return self.player_b

    def get_other_player(self):
        """
        Return the other player.
        """
        if self.current_turn == "A":
            return self.player_b
        return self.player_a