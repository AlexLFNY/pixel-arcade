# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Two Pyxel-based Python games for a French high school (Seconde) computer science class:
- **Meteoroide/** — single-player space shooter with wave-based enemies and asteroids
- **RPG/** — cooperative 2-player maze/arena avoidance game

## Running the Games

```bash
# Install dependency
pip install pyxel

# Run Meteoroide (requires SPACESHIP2.png in the same directory)
cd Meteoroide && python main.py

# Run RPG
cd RPG && python main.py
```

No build step, no tests, no linter configured.

## Architecture

Both games follow the same Pyxel pattern: define `update()` and `draw()` functions, then call `pyxel.run(update, draw)`. All state is stored in global variables.

### Meteoroide (`Meteoroide/main.py`)

- **Entities**: player, 10 basic enemies, 10 shooter enemies, player bullets, enemy bullets, asteroids
- **Game loop**: `update()` handles input/physics/collisions; `draw()` renders everything
- **Progression**: two speed tiers based on kill count (0–9 kills = level 1, 10+ = level 2)
- **Special mechanic**: 1/30 chance asteroids trigger "mystery" effect (inverted controls + immobilization)
- Enemies bounce left/right and advance downward; lose condition triggers if they reach the player's Y

### RPG (`RPG/main.py`)

- **Players**: P1 (blue, WASD), P2 (cyan, arrow keys) in a 500×500 arena
- **Obstacles**: randomly generated rectangles; count controls difficulty (10=easy, 5=medium, 2=hard)
- **Apple power-up**: spawns randomly, respawns every 10 seconds, grants +1 life on pickup
- **Collision**: AABB detection in `collision()` used for both obstacles and player–player blocking
- `shoot()` is a stub — not yet implemented
