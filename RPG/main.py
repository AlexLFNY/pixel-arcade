#Final Project
# Usage:
#   python main.py                     → server  (Player 1, WASD)
#   python main.py client 192.168.x.x → client  (Player 2, arrow keys)

import sys
import pyxel
import random
from network import Network

# --- Determine role ---
if len(sys.argv) >= 2 and sys.argv[1] == "client":
    server_ip = sys.argv[2] if len(sys.argv) >= 3 else input("Server IP: ")
    net = Network("client", server_ip)
else:
    net = Network("server")

IS_SERVER = (net.role == "server")

# --- Game state ---
state = {
    "x": 0,   "y": 0,
    "x2": 485, "y2": 485,
    "apple_x": random.randint(1, 493),
    "apple_y": random.randint(1, 493),
    "lives": 1,
}

difficulty = 10   # easy=10  medium=5  hard=2
obstacle   = []

def obstacle_creation():
    for _ in range(difficulty):
        obstacle.append((
            random.randint(0, 100) * 5,
            random.randint(0, 100) * 5,
            random.randint(1, 3) * 15,
            random.randint(1, 3) * 15,
        ))

if IS_SERVER:
    obstacle_creation()
    net.set_obstacles(obstacle)   # share layout with client on connect

# --- Helpers ---
def collision(px, py):
    for ox, oy, ow, oh in obstacle:
        if px + 15 > ox and px < ox + ow and py + 15 > oy and py < oy + oh:
            return True
    return False

# --- Game loop ---
def update():
    if IS_SERVER:
        _update_server()
    else:
        _update_client()

def _update_server():
    s    = state
    keys = net.get_remote_keys()

    # Player 1 — WASD
    nx, ny = s["x"], s["y"]
    if pyxel.btn(pyxel.KEY_W) and s["y"] > 0:    ny -= 5
    if pyxel.btn(pyxel.KEY_S) and s["y"] < 485:  ny += 5
    if pyxel.btn(pyxel.KEY_A) and s["x"] > 0:    nx -= 5
    if pyxel.btn(pyxel.KEY_D) and s["x"] < 485:  nx += 5
    p2_block = (nx + 15 > s["x2"] and nx < s["x2"] + 15 and
                ny + 15 > s["y2"] and ny < s["y2"] + 15)
    if not collision(nx, ny) and not p2_block:
        s["x"], s["y"] = nx, ny

    # Player 2 — keys received over network
    nx2, ny2 = s["x2"], s["y2"]
    if keys["up"]    and s["y2"] > 0:    ny2 -= 5
    if keys["down"]  and s["y2"] < 485:  ny2 += 5
    if keys["left"]  and s["x2"] > 0:   nx2 -= 5
    if keys["right"] and s["x2"] < 485: nx2 += 5
    p1_block = (nx2 + 15 > s["x"] and nx2 < s["x"] + 15 and
                ny2 + 15 > s["y"] and ny2 < s["y"] + 15)
    if not collision(nx2, ny2) and not p1_block:
        s["x2"], s["y2"] = nx2, ny2

    # Apple
    ax, ay  = s["apple_x"], s["apple_y"]
    counter = pyxel.frame_count % 300
    if s["x"] < ax + 7 and s["x"] + 15 > ax and s["y"] < ay + 7 and s["y"] + 15 > ay:
        s["apple_x"], s["apple_y"] = random.randint(1, 493), random.randint(1, 493)
    elif s["x2"] < ax + 7 and s["x2"] + 15 > ax and s["y2"] < ay + 7 and s["y2"] + 15 > ay:
        s["apple_x"], s["apple_y"] = random.randint(1, 493), random.randint(1, 493)
        s["lives"] += 1
    elif counter == 299:
        s["apple_x"], s["apple_y"] = random.randint(1, 493), random.randint(1, 493)

    net.push_state(s)

def _update_client():
    # Populate obstacles once received from server
    if not obstacle:
        obs = net.get_obstacles()
        if obs:
            obstacle.extend(obs)

    # Send local key states to server
    net.push_keys({
        "up":    pyxel.btn(pyxel.KEY_UP),
        "down":  pyxel.btn(pyxel.KEY_DOWN),
        "left":  pyxel.btn(pyxel.KEY_LEFT),
        "right": pyxel.btn(pyxel.KEY_RIGHT),
    })

    # Mirror server state locally for draw()
    received = net.get_state()
    if received:
        state.update(received)

def draw():
    s = state
    if s["lives"] == 0:
        pyxel.cls(0)
        pyxel.text(240, 250, "GAME OVER", 8)
        return

    pyxel.cls(0)

    if not net.connected:
        msg = "Waiting for Player 2..." if IS_SERVER else "Connecting to server..."
        pyxel.text(160, 250, msg, 7)
        return

    # Apple
    pyxel.rect(s["apple_x"],     s["apple_y"],     7, 7, 8)
    pyxel.rect(s["apple_x"] + 2, s["apple_y"] - 2, 3, 3, 11)
    # Players
    pyxel.rect(s["x"],  s["y"],  15, 15, 3)   # P1 blue
    pyxel.rect(s["x2"], s["y2"], 15, 15, 4)   # P2 cyan
    # Obstacles
    for ox, oy, ow, oh in obstacle:
        pyxel.rect(ox, oy, ow, oh, 7)
    # HUD
    pyxel.text(5, 5,  "Lives: " + str(s["lives"]), 7)
    if IS_SERVER:
        pyxel.text(5, 15, "You: WASD  |  P2: Arrow keys", 7)
    else:
        pyxel.text(5, 15, "You: Arrow keys  |  P1: WASD", 7)

# --- Start ---
title = "RPG - Server (P1 WASD)" if IS_SERVER else "RPG - Client (P2 Arrows)"
pyxel.init(500, 500, title=title)
pyxel.mouse(True)
pyxel.run(update, draw)
