# Strategy Battle Arena (AI vs AI)

Strategy Battle Arena is a turn-based tactical simulation built with Python and Pygame.
It showcases two different AI decision strategies competing on the same board under shared rules:

- AI A uses Minimax with Alpha-Beta pruning.
- AI B uses Monte Carlo Tree Search (MCTS).

The project is designed to make AI behavior visible in real time through a polished visual board, a live match status panel, and deterministic game rules.

## Table of Contents

1. Project Overview
2. Core Gameplay Rules
3. AI Decision Systems
4. Runtime Turn Flow
5. Project Structure
6. Installation and Setup
7. Configuration
8. How to Use
9. Technical Notes
10. Future Improvements

## 1. Project Overview

The game runs on a `7 x 7` grid where each AI controls one unit with health and energy.
Both agents move, attack, defend, heal, and interact with special board cells (energy, trap, shield) while contesting positional advantage around a queen objective tile.

The simulation ends when:

- one player is defeated (`HP <= 0`), or
- the match exceeds the maximum turn limit.

If the turn limit is reached, the winner is selected by tie-break rules based on strategic metrics (queen control, HP, then energy).

## 2. Core Gameplay Rules

### Board and Coordinates

- Grid size: `7 x 7`
- Board origin in game logic: `(0, 0)` is bottom-left
- Rendering origin in Pygame: `(0, 0)` is top-left
- A coordinate conversion layer maps game positions to screen positions.

### Player State

Each player tracks:

- Position (`pos`)
- Health (`hp`)
- Energy (`energy`)
- Defense flag (`defend_active`)
- Shield flag (`shield_active`)
- Queen control score (`queen_control`)

### Legal Actions

On each turn, the current player may select one of the legal actions:

- `MOVE`: move to one adjacent cell (up, down, left, right) inside bounds and not occupied by the opponent
- `ATTACK`: available only when adjacent to opponent and enough energy is available
- `DEFEND`: activates temporary damage reduction
- `HEAL`: restores HP if not already at max HP and enough energy is available

### Resource and Combat Rules

- `ATTACK_COST = 10`
- `DEFEND_COST = 5`
- `HEAL_COST = 12`
- `ATTACK_DAMAGE = 15` (modified by enemy defense/shield)
- `HEAL_AMOUNT = 12`
- `MAX_HP = 100`
- `MAX_ENERGY = 100`

Damage modifiers:

- If target has `defend_active`: damage is reduced by `50%`
- If target has `shield_active`: damage is further reduced by `25%`
- Minimum attack damage is clamped to `1`

### Special Cells

The board includes tactical cell types:

- `ENERGY_CELLS`: grant bonus energy (`+10`, clamped to max)
- `TRAP_CELLS`: apply trap damage (`-8 HP`)
- `SHIELD_CELLS`: activate shield status
- `QUEEN_POS`: central objective influencing tie-break scoring

### Win Conditions

Immediate endings:

- Both defeated: draw
- Only AI A defeated: AI B wins
- Only AI B defeated: AI A wins

Turn-limit ending (`MAX_TURNS = 40`):

1. Higher queen control
2. Higher HP
3. Higher energy
4. If all equal: draw

## 3. AI Decision Systems

### AI A: Minimax + Alpha-Beta

AI A runs a depth-limited minimax search (`depth = 3`) with alpha-beta pruning.

Evaluation function emphasizes:

- HP advantage
- energy advantage
- queen control advantage
- distance to queen objective

Terminal states are strongly weighted (`+100000` for AI A win, `-100000` for AI A loss).

### AI B: Monte Carlo Tree Search (MCTS)

AI B runs MCTS with:

- `120` iterations per move
- UCT child selection (`c = 1.4`)
- random rollout simulations (up to depth `20`)
- backpropagation using win outcomes for AI B

Final action is selected from the root child with the highest visit count.

## 4. Runtime Turn Flow

High-level flow for one game step:

1. Main loop waits for AI step delay.
2. Current AI selects action (`Minimax` for A, `MCTS` for B).
3. Selected action is applied to game state.
4. Cell effects, objective control, and game-over conditions are evaluated.
5. Turn is handed over or game is finalized.
6. UI is redrawn with updated board and side panel.

The visual loop runs at `60 FPS`, while AI turns are intentionally delayed (`850 ms`) to keep decisions observable.

## 5. Project Structure

```
AI_Game_Building/
|-- main.py         # Entry point, game loop, rendering cycle trigger
|-- settings.py     # Constants for board, rules, costs, colors, layout
|-- game_state.py   # Dataclasses for Player and GameState containers
|-- game_logic.py   # Rules engine, action handling, Minimax, MCTS
|-- board.py        # Rendering pipeline (board, tokens, panel, indicators)
|-- README.md       # Project documentation
```

Module responsibilities:

- `main.py`: initializes Pygame, fonts, clock, and controls the simulation loop
- `settings.py`: central source of configurable values
- `game_state.py`: immutable-style data model foundation for gameplay state
- `game_logic.py`: complete game mechanics and AI move selection
- `board.py`: all visual drawing utilities and UI composition

## 6. Installation and Setup

### Prerequisites

- Python 3.10 or newer
- `pip`

### Install Dependencies

```bash
pip install pygame
```

### Run the Project

```bash
python main.py
```

## 7. Configuration

All gameplay and UI constants are centralized in `settings.py`.

Typical adjustments:

- board size and layout (`GRID_SIZE`, `CELL_SIZE`, panel positions)
- match pacing (`FPS`, AI delay in `main.py`)
- combat balance (costs, damage, heal amount)
- match length (`MAX_TURNS`)
- special cell coordinates (`ENERGY_CELLS`, `TRAP_CELLS`, `SHIELD_CELLS`)
- visual design colors

## 8. How to Use

1. Start the game with `python main.py`.
2. Watch both AI agents play automatically.
3. Track key stats in the right panel:
	- turn number
	- active AI
	- HP and energy bars
	- status effects
	- queen control
4. At game end, review winner and reason shown near the bottom of the window.

## 9. Technical Notes

- Simulation cloning is performed with deep copy to isolate hypothetical states during search.
- Minimax and MCTS share the same legal action generator and state transition logic, ensuring fair rule parity.
- Rendering is separated from rules, making it easier to evolve AI logic independently from UI.
- The architecture supports future expansion such as additional cell types, new actions, and alternate AI policies.

## 10. Future Improvements

- Add reproducible seeding controls for deterministic AI comparisons.
- Add automated tests for rule validation and winner resolution paths.
- Add configurable difficulty profiles (search depth, iteration budget).
- Export match statistics to file for benchmarking.
- Add pause/step mode for debugging AI decisions turn by turn.