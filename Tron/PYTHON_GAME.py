import pyxel
import random

WIDTH = 160
HEIGHT = 120
FPS = 30
TRAIL_LIFE = FPS * 10

pyxel.init(WIDTH, HEIGHT, title="Tron 2 Player", fps=FPS)

x1 = WIDTH // 4
y1 = HEIGHT // 2
dx1 = 1
dy1 = 0

x2 = WIDTH * 3 // 4
y2 = HEIGHT // 2
dx2 = -1
dy2 = 0

trail1 = []
trail2 = []

game_over = False
winner = ""

particles = []


def make_explosion(x, y, colors):
    for _ in range(30):
        vx = random.uniform(-1.8, 1.8)
        vy = random.uniform(-1.8, 1.8)
        life = random.randint(12, 28)
        particles.append([x, y, vx, vy, life, random.choice(colors)])


def reset():
    global x1, y1, dx1, dy1
    global x2, y2, dx2, dy2
    global trail1, trail2, game_over, winner, particles

    x1 = WIDTH // 4
    y1 = HEIGHT // 2
    dx1 = 1
    dy1 = 0

    x2 = WIDTH * 3 // 4
    y2 = HEIGHT // 2
    dx2 = -1
    dy2 = 0

    trail1 = []
    trail2 = []
    particles = []

    game_over = False
    winner = ""


def current_trail_positions():
    cutoff = pyxel.frame_count - TRAIL_LIFE
    s1 = set()
    s2 = set()

    for tx, ty, t in trail1:
        if t > cutoff:
            s1.add((tx, ty))

    for tx, ty, t in trail2:
        if t > cutoff:
            s2.add((tx, ty))

    return s1, s2


def update_particles():
    global particles
    new_particles = []

    for p in particles:
        p[0] += p[2]
        p[1] += p[3]
        p[4] -= 1
        if p[4] > 0:
            new_particles.append(p)

    particles = new_particles


def update():
    global x1, y1, dx1, dy1
    global x2, y2, dx2, dy2
    global game_over, winner, trail1, trail2

    update_particles()

    cutoff = pyxel.frame_count - TRAIL_LIFE
    trail1 = [p for p in trail1 if p[2] > cutoff]
    trail2 = [p for p in trail2 if p[2] > cutoff]

    if game_over:
        if pyxel.btnp(pyxel.KEY_R):
            reset()
        return

    if pyxel.btnp(pyxel.KEY_W) and dy1 == 0:
        dx1 = 0
        dy1 = -1
    elif pyxel.btnp(pyxel.KEY_S) and dy1 == 0:
        dx1 = 0
        dy1 = 1
    elif pyxel.btnp(pyxel.KEY_A) and dx1 == 0:
        dx1 = -1
        dy1 = 0
    elif pyxel.btnp(pyxel.KEY_D) and dx1 == 0:
        dx1 = 1
        dy1 = 0

    if pyxel.btnp(pyxel.KEY_I) and dy2 == 0:
        dx2 = 0
        dy2 = -1
    elif pyxel.btnp(pyxel.KEY_K) and dy2 == 0:
        dx2 = 0
        dy2 = 1
    elif pyxel.btnp(pyxel.KEY_J) and dx2 == 0:
        dx2 = -1
        dy2 = 0
    elif pyxel.btnp(pyxel.KEY_L) and dx2 == 0:
        dx2 = 1
        dy2 = 0

    trail1.append((x1, y1, pyxel.frame_count))
    trail2.append((x2, y2, pyxel.frame_count))

    x1 += dx1
    y1 += dy1

    x2 += dx2
    y2 += dy2

    p1_crash = False
    p2_crash = False

    if x1 < 0 or x1 >= WIDTH or y1 < 0 or y1 >= HEIGHT:
        p1_crash = True
    if x2 < 0 or x2 >= WIDTH or y2 < 0 or y2 >= HEIGHT:
        p2_crash = True

    trail_positions1, trail_positions2 = current_trail_positions()

    if (x1, y1) in trail_positions1 or (x1, y1) in trail_positions2:
        p1_crash = True
    if (x2, y2) in trail_positions1 or (x2, y2) in trail_positions2:
        p2_crash = True

    if x1 == x2 and y1 == y2:
        p1_crash = True
        p2_crash = True

    if p1_crash and p2_crash:
        game_over = True
        winner = "DRAW"
        make_explosion(x1, y1, [7, 12, 5])
        make_explosion(x2, y2, [10, 8, 9])
    elif p1_crash:
        game_over = True
        winner = "PLAYER 2 WINS"
        make_explosion(x1, y1, [7, 12, 5])
    elif p2_crash:
        game_over = True
        winner = "PLAYER 1 WINS"
        make_explosion(x2, y2, [10, 8, 9])


def draw():
    pyxel.cls(0)

    for x, y, t in trail1:
        age = pyxel.frame_count - t
        if age < TRAIL_LIFE:
            core = 12 if age < TRAIL_LIFE * 0.5 else 5
            glow = 1
            pyxel.pset(x-1, y-1, glow)
            pyxel.pset(x+1, y+1, glow)
            pyxel.pset(x, y, core)

    for x, y, t in trail2:
        age = pyxel.frame_count - t
        if age < TRAIL_LIFE:
            core = 8 if age < TRAIL_LIFE * 0.5 else 9
            glow = 2
            pyxel.pset(x-1, y-1, glow)
            pyxel.pset(x+1, y+1, glow)
            pyxel.pset(x, y, core)

    if not game_over:
        pyxel.pset(x1, y1, 7)
        pyxel.pset(x2, y2, 10)

    for p in particles:
        pyxel.pset(int(p[0]), int(p[1]), p[5])

    pyxel.text(5, 5, "P1: WASD", 12)
    pyxel.text(WIDTH - 60, 5, "P2: IJKL", 8)

    if game_over:
        pyxel.text(WIDTH // 2 - 30, HEIGHT // 2, winner, 7)
        pyxel.text(WIDTH // 2 - 40, HEIGHT // 2 + 10, "Press R to restart", 7)


pyxel.run(update, draw)
