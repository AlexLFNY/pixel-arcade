import pyxel

pyxel.init(160,120)

x = 80
y = 100
vitesse_x = 2
vitesse_y = 2

game_state = "play"
score = 0

liste_rectangle = [[10,10,8],[35,10,9],[60,10,10],[85,10,11],[110,10,12],[135,10,13],
                   [10,20,9],[35,20,10],[60,20,11],[85,20,12],[110,20,13],[135,20,8],
                   [10,30,10],[35,30,11],[60,30,12],[85,30,13],[110,30,8],[135,30,9],
                   [10,40,11],[35,40,12],[60,40,13],[85,40,8],[110,40,9],[135,40,10]
                   ]

paddle_x = 70
paddle_y = 110
paddle_w = 20
paddle_h = 5

def update():
    global x, y, vitesse_x, vitesse_y, liste_rectangle, game_state, score

    if game_state == "play":

        x += vitesse_x
        y += vitesse_y

        # Wall collisions
        if x >= 160 or x <= 0:
            vitesse_x = -vitesse_x
        if y <= 0:
            vitesse_y = -vitesse_y

        # Game over
        if y > 120:
            game_state = "game_over"

        # Paddle movement
        if pyxel.btn(pyxel.KEY_LEFT):
            paddle_move(-2)
        if pyxel.btn(pyxel.KEY_RIGHT):
            paddle_move(2)

        # Paddle collision
        if (paddle_x <= x <= paddle_x + paddle_w and
            paddle_y <= y <= paddle_y + paddle_h):
            vitesse_y = -vitesse_y

        # Rectangle collisions + SCORE
        for r in liste_rectangle[:]:
            rx, ry = r[0],r[1]
            if (rx <= x <= rx + 20 and
                ry <= y <= ry + 5):
                vitesse_y = -vitesse_y
                liste_rectangle.remove(r)
                score += 1

    elif game_state == "game_over":
        if pyxel.btnp(pyxel.KEY_R):
            reset_game()

def paddle_move(dx):
    global paddle_x
    paddle_x += dx
    paddle_x = max(5, min(200 - paddle_w, paddle_x))

def reset_game():
    global x, y, vitesse_x, vitesse_y, liste_rectangle, game_state, score

    x = 80
    y = 60
    vitesse_x = 2
    vitesse_y = 2
    score = 0

    liste_rectangle = [[10,10,8],[35,10,9],[60,10,10],[85,10,11],[110,10,12],[135,10,13],
                       [10,20,9],[35,20,10],[60,20,11],[85,20,12],[110,20,13],[135,20,8],
                       [10,30,10],[35,30,11],[60,30,12],[85,30,13],[110,30,8],[135,30,9],
                       [10,40,11],[35,40,12],[60,40,13],[85,40,8],[110,40,9],[135,40,10]]
    game_state = "play"

def draw():
    pyxel.cls(0)

    if game_state == "play":
        # Ball
        pyxel.circ(x, y, 2, 19)

        # Paddle
        pyxel.rect(paddle_x, paddle_y, paddle_w, paddle_h, 7)

        # Bricks
        for r in liste_rectangle:
            pyxel.rect(r[0], r[1], 15, 5, r[2])

        pyxel.text(5, 5, f"Score: {score}", 7)

    elif game_state == "game_over":
        pyxel.text(50, 50, "GAME OVER", 8)
        pyxel.text(30, 65, f"Score: {score}", 7)
        pyxel.text(30, 80, "Press R to restart", 7)

    pyxel.mouse(True)

pyxel.run(update, draw)
