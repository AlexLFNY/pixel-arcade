import random
import pyxel

# 3/4 ratio
floor_height = 144 #floor boundary(kill on impact)
ceiling_height = 0 #ceiling boundary

pyxel.init(192, 144) #initializes the window
pyxel.load("ufoassets.pyxres") #loads the assets(UFO + pillars) 

# Variables globales
y = 64 #ufo y coordinate at the start
velocite_y = 0 #speed at which it is falling
death = False #checks death sets at false
gravite = 0.8 #how fast it falls down
force_saut = -3.6 #how high it jumps
velocite_y = gravite 

# list of pillars includin a scoring-used flag: [x, y, whether it gives a point]
pillars = [
    [192, 120, False],
    [264, 90, False],
    [336, 130, False]
]

score = 0 #score at the start

# Start delay variables
start_delay = 90   # 90 frames = 1.5 seconds delay
game_started = False # so that the game is frozen

# collision box checker
def collide(ax, ay, aw, ah, bx, by, bw, bh):
    return (
        ax < bx + bw and
        ax + aw > bx and
        ay < by + bh and
        ay + ah > by
    )

def update():
    global x, y, velocite_y, death, score, start_delay, game_started

    # Wait before starting
    if not game_started:
        start_delay -= 1
        if start_delay <= 0:
            game_started = True
        return  # skip the rest of update until delay is over

    # jump
    if pyxel.btn(pyxel.KEY_W) or pyxel.btn(pyxel.KEY_SPACE):
        velocite_y = force_saut

    # gravity
    y = y + velocite_y
    velocite_y += gravite

    # kill if touching roof/floor
    if y <= ceiling_height or y >= floor_height:
        death = True

    # UFO hitbox
    ufo_x = 32
    ufo_y = y
    ufo_w = 16
    ufo_h = 16

    for p in pillars:
        # move pillar
        p[0] -= 2

        # score when pillar fully passes UFO
        if p[0] + 16 < ufo_x and not p[2]:
            score += 1
            p[2] = True

        # respawn pillar
        if p[0] <= -16:
            p[0] = 192
            p[1] = random.randint(64, 138)
            p[2] = False  # reset scoring flag

        # bottom pillar hitbox
        bot_x = p[0]
        bot_y = p[1]
        bot_w = 16
        bot_h = 144

        # top pillar hitbox
        top_x = p[0]
        top_y = p[1] - 192
        top_w = 16
        top_h = 144

        # collision check
        if (
            collide(ufo_x, ufo_y, ufo_w, ufo_h, bot_x, bot_y, bot_w, bot_h)
            or
            collide(ufo_x, ufo_y, ufo_w, ufo_h, top_x, top_y, top_w, top_h)
        ):
            death = True

    if death:
        quit() #ends code on death
        

def draw():
    pyxel.cls(1) #clears the background

    # draw ufo
    pyxel.blt(32, y, 0, 0,   0, 16, 16)

    # draw pillars (bottom + top)
    for p in pillars:
        pyxel.blt(p[0], p[1], 0, 16, 0, 16, 144)
        pyxel.blt(p[0], p[1] - 192, 0, 32, 0, 16, 144)

    # draw score
    pyxel.text(5, 5, f"Score: {score}", 7)
 
    # draw start message
    if not game_started:
        pyxel.text(60, 70, "GET READY!", 7)

pyxel.run(update, draw) #run the code
