# ============================================================
# game_logic.py
# ------------------------------------------------------------
# Part 4:
# - full game rules
# - Minimax (AI A)
# - Monte Carlo Tree Search (AI B)
# - winner reason support
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


# ============================================================
# Basic helpers
# ============================================================

def in_bounds(pos):
    x, y = pos
    return 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE


def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def get_neighbors(pos):
    x, y = pos
    candidates = [
        (x + 1, y),
        (x - 1, y),
        (x, y + 1),
        (x, y - 1),
    ]
    return [p for p in candidates if in_bounds(p)]


# ============================================================
# Action generation
# ============================================================

def get_legal_actions(state):
    player = state.get_current_player()
    enemy = state.get_other_player()

    actions = []

    for nxt in get_neighbors(player.pos):
        if nxt != enemy.pos:
            actions.append(("MOVE", nxt))

    if manhattan(player.pos, enemy.pos) == 1 and player.energy >= ATTACK_COST:
        actions.append(("ATTACK", None))

    if player.energy >= DEFEND_COST:
        actions.append(("DEFEND", None))

    if player.energy >= HEAL_COST and player.hp < MAX_HP:
        actions.append(("HEAL", None))

    return actions


# ============================================================
# Damage + cell effects
# ============================================================

def compute_attack_damage(enemy):
    damage = ATTACK_DAMAGE

    if enemy.defend_active:
        damage *= 0.5

    if enemy.shield_active:
        damage *= 0.75

    return max(1, int(round(damage)))


def apply_cell_effect(player):
    if player.pos in ENERGY_CELLS:
        player.energy = min(MAX_ENERGY, player.energy + ENERGY_BONUS)

    if player.pos in TRAP_CELLS:
        player.hp = max(0, player.hp - TRAP_DAMAGE)

    if player.pos in SHIELD_CELLS:
        player.shield_active = True


# ============================================================
# Queen control
# ============================================================

def update_queen_control(state):
    """
    A player gets 1 queen-control point if they are adjacent
    to the queen and the opponent is not adjacent.
    """
    a_adj = manhattan(state.player_a.pos, QUEEN_POS) == 1
    b_adj = manhattan(state.player_b.pos, QUEEN_POS) == 1

    if a_adj and not b_adj:
        state.player_a.queen_control += 1
    elif b_adj and not a_adj:
        state.player_b.queen_control += 1


# ============================================================
# Apply action
# ============================================================

def apply_action(state, action):
    player = state.get_current_player()
    enemy = state.get_other_player()

    player.defend_active = False

    action_type, payload = action

    if action_type == "MOVE":
        player.pos = payload
        apply_cell_effect(player)

    elif action_type == "ATTACK":
        player.energy -= ATTACK_COST
        damage = compute_attack_damage(enemy)
        enemy.hp = max(0, enemy.hp - damage)

        enemy.defend_active = False
        enemy.shield_active = False

    elif action_type == "DEFEND":
        player.energy -= DEFEND_COST
        player.defend_active = True

    elif action_type == "HEAL":
        player.energy -= HEAL_COST
        player.hp = min(MAX_HP, player.hp + HEAL_AMOUNT)


# ============================================================
# Winner decision
# ============================================================

def decide_winner_by_tiebreak(state):
    a = state.player_a
    b = state.player_b

    if a.queen_control > b.queen_control:
        return "A", "Higher Queen Control"
    elif b.queen_control > a.queen_control:
        return "B", "Higher Queen Control"

    if a.hp > b.hp:
        return "A", "Higher HP"
    elif b.hp > a.hp:
        return "B", "Higher HP"

    if a.energy > b.energy:
        return "A", "Higher Energy"
    elif b.energy > a.energy:
        return "B", "Higher Energy"

    return "Draw", "Perfect Draw"


def check_game_over(state):
    a = state.player_a
    b = state.player_b

    if a.hp <= 0 and b.hp <= 0:
        state.game_over = True
        state.winner = "Draw"
        state.winner_reason = "Both Players Defeated"
        return

    if a.hp <= 0:
        state.game_over = True
        state.winner = "B"
        state.winner_reason = "AI A Defeated"
        return

    if b.hp <= 0:
        state.game_over = True
        state.winner = "A"
        state.winner_reason = "AI B Defeated"
        return

    if state.turn_count > MAX_TURNS:
        state.game_over = True
        state.winner, state.winner_reason = decide_winner_by_tiebreak(state)
        return


def end_turn(state):
    update_queen_control(state)
    check_game_over(state)

    if state.game_over:
        return

    if state.current_turn == "A":
        state.current_turn = "B"
    else:
        state.current_turn = "A"
        state.turn_count += 1


# ============================================================
# Simulation helpers
# ============================================================

def clone_state(state):
    return copy.deepcopy(state)


def step_simulation(sim_state, action):
    apply_action(sim_state, action)

    # queen control must also update in simulation
    update_queen_control(sim_state)
    check_game_over(sim_state)

    if not sim_state.game_over:
        if sim_state.current_turn == "A":
            sim_state.current_turn = "B"
        else:
            sim_state.current_turn = "A"
            sim_state.turn_count += 1

    return sim_state


# ============================================================
# Evaluation for Minimax
# ============================================================

def evaluate_state_for_a(state):
    a = state.player_a
    b = state.player_b

    if state.game_over:
        if state.winner == "A":
            return 100000
        if state.winner == "B":
            return -100000
        return 0

    score = 0
    score += (a.hp - b.hp) * 10
    score += (a.energy - b.energy) * 2
    score += (a.queen_control - b.queen_control) * 15
    score += (manhattan(b.pos, QUEEN_POS) - manhattan(a.pos, QUEEN_POS)) * 2

    return score


# ============================================================
# Minimax (AI A)
# ============================================================

def minimax(state, depth, alpha, beta, maximizing):
    if depth == 0 or state.game_over:
        return evaluate_state_for_a(state), None

    actions = get_legal_actions(state)

    if maximizing:
        best_score = -math.inf
        best_action = None

        for action in actions:
            child = clone_state(state)
            step_simulation(child, action)

            score, _ = minimax(child, depth - 1, alpha, beta, False)

            if score > best_score:
                best_score = score
                best_action = action

            alpha = max(alpha, best_score)
            if beta <= alpha:
                break

        return best_score, best_action

    else:
        best_score = math.inf
        best_action = None

        for action in actions:
            child = clone_state(state)
            step_simulation(child, action)

            score, _ = minimax(child, depth - 1, alpha, beta, True)

            if score < best_score:
                best_score = score
                best_action = action

            beta = min(beta, best_score)
            if beta <= alpha:
                break

        return best_score, best_action


def choose_minimax_action_for_a(state):
    _, action = minimax(state, 3, -math.inf, math.inf, True)

    if action is None:
        actions = get_legal_actions(state)
        return random.choice(actions)

    return action


# ============================================================
# MCTS Node
# ============================================================

class MCTSNode:
    def __init__(self, state, parent=None, action=None):
        self.state = state
        self.parent = parent
        self.action = action
        self.children = []
        self.visits = 0
        self.wins = 0
        self.untried_actions = get_legal_actions(state)

    def is_fully_expanded(self):
        return len(self.untried_actions) == 0

    def best_child(self, c=1.4):
        best = None
        best_score = -math.inf

        for child in self.children:
            exploitation = child.wins / child.visits
            exploration = c * math.sqrt(math.log(self.visits) / child.visits)
            score = exploitation + exploration

            if score > best_score:
                best_score = score
                best = child

        return best


def rollout_reward_for_b(state):
    """
    Return rollout reward from AI B perspective.
    Uses terminal winner when available, otherwise a heuristic fallback
    so MCTS can still learn from non-terminal rollouts.
    """
    if state.game_over:
        if state.winner == "B":
            return 1.0
        if state.winner == "A":
            return 0.0
        return 0.5

    a = state.player_a
    b = state.player_b

    # Simple bounded heuristic mapped to [0, 1]
    score = 0.0
    score += (b.hp - a.hp) * 0.03
    score += (b.energy - a.energy) * 0.01
    score += (b.queen_control - a.queen_control) * 0.08
    score += (manhattan(a.pos, QUEEN_POS) - manhattan(b.pos, QUEEN_POS)) * 0.02

    return max(0.0, min(1.0, 0.5 + score))


# ============================================================
# MCTS (AI B)
# ============================================================

def mcts(root_state, iterations=120):
    root = MCTSNode(clone_state(root_state))

    if not root.untried_actions:
        return None

    for _ in range(iterations):
        node = root
        state = clone_state(root_state)

        # Selection
        while node.is_fully_expanded() and node.children:
            node = node.best_child()
            step_simulation(state, node.action)

        # Expansion
        if node.untried_actions:
            action = node.untried_actions.pop()
            step_simulation(state, action)

            child = MCTSNode(state, node, action)
            node.children.append(child)
            node = child

        # Simulation
        rollout_state = clone_state(state)

        depth = 0
        while not rollout_state.game_over and depth < 20:
            actions = get_legal_actions(rollout_state)
            if not actions:
                break

            action = random.choice(actions)
            step_simulation(rollout_state, action)
            depth += 1

        # Backpropagation
        reward = rollout_reward_for_b(rollout_state)

        while node is not None:
            node.visits += 1

            node.wins += reward

            node = node.parent

    if not root.children:
        return random.choice(root.untried_actions)

    max_visits = max(child.visits for child in root.children)
    candidates = [child for child in root.children if child.visits == max_visits]
    best_child = max(candidates, key=lambda c: c.wins / c.visits)
    return best_child.action


# ============================================================
# AI controller
# ============================================================

def play_one_ai_turn(state):
    if state.game_over:
        return

    if state.current_turn == "A":
        action = choose_minimax_action_for_a(state)
    else:
        action = mcts(state, iterations=120)

    if action is None:
        end_turn(state)
        return

    apply_action(state, action)
    check_game_over(state)

    if not state.game_over:
        end_turn(state)