# ============================================================
# game_logic.py
# ------------------------------------------------------------
# This file contains the actual game rules.
#
# Part 2 includes:
# - legal movement
# - one action per turn
# - attack / defend / heal
# - special cell effects
# - queen-control update
# - demo AI turn selection
# - win/tie logic
# ============================================================

import copy
import math
import random

from settings import (
    GRID_SIZE,
    ATTACK_COST,
    DEFEND_COST,
    HEAL_COST,
    ATTACK_DAMAGE,
    HEAL_AMOUNT,
    ENERGY_BONUS,
    TRAP_DAMAGE,
    MAX_HP,
    MAX_ENERGY,
    MAX_TURNS,
    ENERGY_CELLS,
    TRAP_CELLS,
    SHIELD_CELLS,
    QUEEN_POS,
)


# ------------------------------------------------------------
# Basic helpers
# ------------------------------------------------------------
def in_bounds(pos):
    """
    Check whether a board position is inside the 7x7 grid.
    """
    x, y = pos
    return 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE


def manhattan(a, b):
    """
    Manhattan distance between two cells.
    This is useful for grid movement and adjacency checks.
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def get_neighbors(pos):
    """
    Return the 4-directional neighboring cells.
    """
    x, y = pos
    candidates = [
        (x + 1, y),
        (x - 1, y),
        (x, y + 1),
        (x, y - 1),
    ]
    return [p for p in candidates if in_bounds(p)]


# ------------------------------------------------------------
# Action generation
# ------------------------------------------------------------
def get_legal_actions(state):
    """
    Generate all legal actions for the current player.

    Action format:
        ("MOVE", target_pos)
        ("ATTACK", None)
        ("DEFEND", None)
        ("HEAL", None)
    """
    player = state.get_current_player()
    enemy = state.get_other_player()

    actions = []

    # ------------------------
    # MOVE actions
    # ------------------------
    for nxt in get_neighbors(player.pos):
        # cannot move onto the enemy cell
        if nxt != enemy.pos:
            actions.append(("MOVE", nxt))

    # ------------------------
    # ATTACK action
    # ------------------------
    # Attack only if adjacent and enough energy
    if manhattan(player.pos, enemy.pos) == 1 and player.energy >= ATTACK_COST:
        actions.append(("ATTACK", None))

    # ------------------------
    # DEFEND action
    # ------------------------
    if player.energy >= DEFEND_COST:
        actions.append(("DEFEND", None))

    # ------------------------
    # HEAL action
    # ------------------------
    if player.energy >= HEAL_COST and player.hp < MAX_HP:
        actions.append(("HEAL", None))

    return actions


# ------------------------------------------------------------
# Damage and cell effects
# ------------------------------------------------------------
def compute_attack_damage(enemy):
    """
    Compute final attack damage after defend/shield modifiers.
    """
    damage = ATTACK_DAMAGE

    # Defend reduces incoming damage by 50%
    if enemy.defend_active:
        damage *= 0.5

    # Shield reduces incoming damage by 25%
    if enemy.shield_active:
        damage *= 0.75

    return max(1, int(round(damage)))


def apply_cell_effect(player, state):
    """
    Apply the effect of the cell the player ends on.
    """
    # Energy cell
    if player.pos in ENERGY_CELLS:
        old_energy = player.energy
        player.energy = min(MAX_ENERGY, player.energy + ENERGY_BONUS)
        gained = player.energy - old_energy
        if gained > 0:
            state.action_log.append(f"{player.name} gained {gained} energy from E cell.")

    # Trap cell
    if player.pos in TRAP_CELLS:
        player.hp = max(0, player.hp - TRAP_DAMAGE)
        state.action_log.append(f"{player.name} took {TRAP_DAMAGE} trap damage.")

    # Shield cell
    if player.pos in SHIELD_CELLS:
        player.shield_active = True
        state.action_log.append(f"{player.name} activated shield.")


def update_queen_control(state):
    """
    Queen control rule:
    A player gains 1 queen-control point if they are adjacent
    to the queen and the opponent is not adjacent.
    """
    a_adj = manhattan(state.player_a.pos, QUEEN_POS) == 1
    b_adj = manhattan(state.player_b.pos, QUEEN_POS) == 1

    if a_adj and not b_adj:
        state.player_a.queen_control += 1
        state.action_log.append("A gained queen control.")
    elif b_adj and not a_adj:
        state.player_b.queen_control += 1
        state.action_log.append("B gained queen control.")


# ------------------------------------------------------------
# Turn action execution
# ------------------------------------------------------------
def apply_action(state, action):
    """
    Apply exactly one action to the current state.

    This function directly modifies the state.
    """
    player = state.get_current_player()
    enemy = state.get_other_player()

    # Defend only lasts until this player's next action.
    # So when this player starts a turn, we reset their old defend.
    player.defend_active = False

    action_type, payload = action

    if action_type == "MOVE":
        player.pos = payload
        state.action_log.append(f"{player.name} moved to {player.pos}.")
        apply_cell_effect(player, state)

    elif action_type == "ATTACK":
        player.energy -= ATTACK_COST

        damage = compute_attack_damage(enemy)
        enemy.hp = max(0, enemy.hp - damage)

        state.action_log.append(f"{player.name} attacked {enemy.name} for {damage} damage.")

        # After getting hit, defend and shield are consumed
        enemy.defend_active = False
        enemy.shield_active = False

    elif action_type == "DEFEND":
        player.energy -= DEFEND_COST
        player.defend_active = True
        state.action_log.append(f"{player.name} used defend.")

    elif action_type == "HEAL":
        player.energy -= HEAL_COST
        old_hp = player.hp
        player.hp = min(MAX_HP, player.hp + HEAL_AMOUNT)
        healed = player.hp - old_hp
        state.action_log.append(f"{player.name} healed for {healed} HP.")

    # Keep action log short
    if len(state.action_log) > 12:
        state.action_log = state.action_log[-12:]


# ------------------------------------------------------------
# Winner / tie-break logic
# ------------------------------------------------------------
def decide_winner_by_tiebreak(state):
    """
    If max turns are reached, decide winner by:
    1. queen control
    2. HP
    3. Energy
    else draw
    """
    a = state.player_a
    b = state.player_b

    if a.queen_control != b.queen_control:
        return "A" if a.queen_control > b.queen_control else "B", "Won by queen control"

    if a.hp != b.hp:
        return "A" if a.hp > b.hp else "B", "Won by higher HP"

    if a.energy != b.energy:
        return "A" if a.energy > b.energy else "B", "Won by higher energy"

    return "Draw", "Perfect draw after tie-break"


def check_game_over(state):
    """
    Check whether the game is over.
    """
    a = state.player_a
    b = state.player_b

    if a.hp <= 0 and b.hp <= 0:
        state.game_over = True
        state.winner = "Draw"
        state.winner_reason = "Both players were defeated"
        return

    if a.hp <= 0:
        state.game_over = True
        state.winner = "B"
        state.winner_reason = "A was defeated"
        return

    if b.hp <= 0:
        state.game_over = True
        state.winner = "A"
        state.winner_reason = "B was defeated"
        return

    if state.turn_count > MAX_TURNS:
        state.game_over = True
        state.winner, state.winner_reason = decide_winner_by_tiebreak(state)
        return


def end_turn(state):
    """
    Finish the current turn:
    - update queen control
    - check game over
    - switch active player
    - increment turn count after B -> A transition
    """
    update_queen_control(state)
    check_game_over(state)

    if state.game_over:
        return

    old_turn = state.current_turn

    # switch turn
    if state.current_turn == "A":
        state.current_turn = "B"
    else:
        state.current_turn = "A"
        state.turn_count += 1

    state.action_log.append(f"Turn passed from {old_turn} to {state.current_turn}.")



# ------------------------------------------------------------
# Full one-step AI turn
# ------------------------------------------------------------
def play_one_ai_turn(state):
    """
    Let the current temporary AI choose one action and apply it.
    """
    if state.game_over:
        return

    action = choose_demo_ai_action(state)
    if action is None:
        state.action_log.append(f"{state.current_turn} had no legal action.")
        end_turn(state)
        return

    apply_action(state, action)
    check_game_over(state)

    if not state.game_over:
        end_turn(state)