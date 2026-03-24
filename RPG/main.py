#Final Project
import pyxel
import random

#screen size definition
largeur = 500
hauteur = 500

#shooting initialization (from gemini)
# Bullets: [x, y, dx, dy] (dx/dy is the direction)
bullets1 = []
bullets2 = []

# Directions: [dx, dy]
dir1 = [0, -5] # Default up
dir2 = [0, -5] 

#enemy spawn rate, spawn point and speed definition
enemies = [] # [x, y, timer_to_shoot]
enemy_speed = 1.5
spawn_timer = 0
bulletsE = []

def spawn_enemy():
    # Spawns at a random edge of the screen
    side = random.randint(0, 3)
    if side == 0: return [0, random.randint(0, 500), 0] # Left
    if side == 1: return [500, random.randint(0, 500), 0] # Right
    if side == 2: return [random.randint(0, 500), 0, 0] # Top
    return [random.randint(0, 500), 500, 0] # Bottom

def update_enemies():
    global enemies, bulletsE, lives, x, y, x2, y2, spawn_timer
    
    # Spawn new enemy every 3 seconds (90 frames)
    spawn_timer += 1
    if spawn_timer > 90:
        enemies.append(spawn_enemy())
        spawn_timer = 0

    for e in enemies[:]:
        # Target the closest player
        dist1 = abs(e[0]-x) + abs(e[1]-y) #returns the absolute value in order to determine which is the closest player (abs() is a function that gives the absolute value)
        dist2 = abs(e[0]-x2) + abs(e[1]-y2)
        tx, ty = (x, y) if dist1 < dist2 else (x2, y2)

        # Movement towards target
        new_ex, new_ey = e[0], e[1]
        if e[0] < tx: new_ex += enemy_speed #complicated stuff that you just need to figure out
        elif e[0] > tx: new_ex -= enemy_speed
        if e[1] < ty: new_ey += enemy_speed
        elif e[1] > ty: new_ey -= enemy_speed
        
        # Move if no obstacle
        if not collision(new_ex, new_ey):
            e[0], e[1] = new_ex, new_ey

        # Shooting (every 2 seconds / 60 frames)
        e[2] += 1
        if e[2] > 60:
            # Calculate direction toward target
            dx = 4 if tx > e[0] else -4
            dy = 4 if ty > e[1] else -4
            bulletsE.append([e[0]+6, e[1]+6, dx, dy])
            e[2] = 0

#music definition
music = True


#player 1 spawn definition
x = 0
y = 0

#player 2 spawn definition
x2 = 485
y2 = 485

#initialization of the pyxel window
pyxel.init(largeur, hauteur)

#loading the music (helped by the teacher)
pyxel.load("jeu.pyxres")

#spawn status definition
lives = 1
status = None
kills = 0

easy = 10
medium = 5
hard = 2
#choose your difficulty (as in the amount of cover you get)
difficulty = easy


obstacle = []
map = []
def obstacle_creation(): #code creating random coordinates for obstacles 
        for i in range(1, difficulty + 1):
            x = random.randint(0, 100) * 5
            y = random.randint(0, 100) * 5
            l = random.randint(1, 3) * 15
            L = random.randint(1, 3) * 15
            obstacle.append((x, y, l, L))

obstacle_creation()



def collision(px, py): #tout pasted from chatgpt
    for obs in obstacle: #code from gpt for collisions
        ox, oy, ow, oh = obs
        
        if (px + 15 > ox and
            px < ox + ow and
            py + 15 > oy and
            py < oy + oh):
            return True
            
    return False


collision(x, y) #player 1 collisions
collision(x2, y2) #player 2 collisions



counter = pyxel.frame_count % 300 #counts every 10 seconds by counting the number of frames (30fps) / 300

apple_x = random.randint(1, 500)
apple_y = random.randint(1, 500)
def apple(): #code for an apple that adds a life to the players
    global x, y, apple_x, apple_y, lives, counter 
    pyxel.rect(apple_x, apple_y, 7, 7, 8)
    pyxel.rect(apple_x + 2, apple_y - 2, 3, 3, 11)
    counter = pyxel.frame_count % 300
    if (x < apple_x + 7 and #code to reset the apple's position after being eaten
        x + 15 > apple_x and 
        y < apple_y + 7 and 
        y + 15 > apple_y):
        apple_x = random.randint(1, 500)
        apple_y = random.randint(1, 500)
        pyxel.play(0, 0)
    elif (x2 < apple_x + 7 and #same code for player 2
        x2 + 15 > apple_x and 
        y2 < apple_y + 7 and 
        y2 + 15 > apple_y):
        apple_x = random.randint(1, 500)
        apple_y = random.randint(1, 500)
        lives += 1 
        if music == True:
            pyxel.play(0, 0)
    elif counter == 299: #code to reset the apples position after 10 seconds
        apple_x = random.randint(1, 500)
        apple_y = random.randint(1, 500)




def update():
    global x, y, x2, y2
    global dir1, dir2, bullets1, bullets2, bulletsE #help from chatgpt
    global music
#movement player 1 (WASD)
    new_x = x
    new_y = y

    if pyxel.btn(pyxel.KEY_M):
        music = False

    if pyxel.btn(pyxel.KEY_W) and y >= 1:
        new_y -= 5
        dir1 = [0, -5]
    if pyxel.btn(pyxel.KEY_S) and y <= 500 - 15:
        new_y += 5
        dir1 = [0, 5]
    if pyxel.btn(pyxel.KEY_A) and x >= 1:
        new_x -= 5
        dir1 = [-5, 0]
    if pyxel.btn(pyxel.KEY_D) and x <= 500 - 15:
        new_x += 5
        dir1 = [5, 0]
    # Check if Player 1 hits obstacles OR hits Player 2 (gemini)
    p2_hit = (new_x + 15 > x2 and new_x < x2 + 15 and 
              new_y + 15 > y2 and new_y < y2 + 15)
    if not collision(new_x, new_y) and not p2_hit:
        x = new_x
        y = new_y
    if pyxel.btnp(pyxel.KEY_E): #append the coordinates and direction to the bullet list from gemini for player 1 when E is hit
        bullets1.append([x + 6, y + 6, dir1[0] * 2, dir1[1] * 2])
        if music == True:
            pyxel.play(0, 1)
#movement player 2 (arrow keys)
    new_x2 = x2
    new_y2 = y2
    if pyxel.btn(pyxel.KEY_UP) and y2 >= 1:
        new_y2 -= 5
        dir2 = [0, -5]
    if pyxel.btn(pyxel.KEY_DOWN) and y2 <= 500 - 15:
        new_y2 += 5
        dir2 = [0, 5]
    if pyxel.btn(pyxel.KEY_LEFT) and x2 >= 1:
        new_x2 -= 5
        dir2 = [-5, 0]
    if pyxel.btn(pyxel.KEY_RIGHT) and x2 <= 500 - 15:
        new_x2 += 5
        dir2 = [5, 0]
    # Check if Player 2 hits obstacles OR hits Player 1 (gemini)
    p1_hit = (new_x2 + 15 > x and new_x2 < x + 15 and 
              new_y2 + 15 > y and new_y2 < y + 15) 
    if not collision(new_x2, new_y2) and not p1_hit:
        x2 = new_x2
        y2 = new_y2
    if pyxel.btnp(pyxel.KEY_RETURN): #append the coordinates and direction to the bullet list from gemini for player 1 when RETURN is hit
        bullets2.append([x2 + 6, y2 + 6, dir2[0] * 2, dir2[1] * 2])
        if music == True:
            pyxel.play(0, 2)


    # --- Bullet Physics --- (from gemini)
    for b_list in [bullets1, bullets2, bulletsE]:
        for b in b_list[:]:
            b[0] += b[2] # Move X
            b[1] += b[3] # Move Y
            # Remove if off-screen or hitting obstacle
            if b[0] < 0 or b[0] > 500 or b[1] < 0 or b[1] > 500 or collision(b[0], b[1]):
                b_list.remove(b)
    
    #AI Movement and AI Intelligent Shooting
    global lives, kills
    update_enemies() # Call the new enemy logic

    # --- Bullet Collision with Players ---
    for b in bulletsE[:]:
        # Check if enemy bullet hits Player 1
        if (b[0] < x + 15 and b[0] + 3 > x and b[1] < y + 15 and b[1] + 3 > y):
            lives -= 1
            bulletsE.remove(b)
        # Check if enemy bullet hits Player 2
        elif (b[0] < x2 + 15 and b[0] + 3 > x2 and b[1] < y2 + 15 and b[1] + 3 > y2):
            lives -= 1
            bulletsE.remove(b)

    # --- Players shooting Enemies ---
    for b_list in [bullets1, bullets2]:
        for b in b_list[:]:
            for e in enemies[:]:
                if (b[0] < e[0] + 15 and b[0] + 3 > e[0] and b[1] < e[1] + 15 and b[1] + 3 > e[1]):
                    enemies.remove(e)
                    kills += 1
                    if b in b_list: b_list.remove(b)

    


def draw():
    global status, largeur, hauteur
    if lives == 0:
        pyxel.cls(0)
        largeur = 100
        hauteur = 100
        pyxel.text(240, 250, "GAME OVER", 8)
    else:
        pyxel.cls(0)
        apple()
        pyxel.rect(x, y, 15, 15, 3)
        pyxel.rect(x2, y2, 15, 15, 4)

        for obs in obstacle:
            pyxel.rect(obs[0], obs[1], obs[2], obs[3], 7)

        #this section was helped form gemini
        for b in bullets1:
            pyxel.rect(b[0], b[1], 3, 3, 10) #yellow bullets for player 1
        for b in bullets2:
            pyxel.rect(b[0], b[1], 3, 3, 14) # pink bullets for player 2 
        
        for e in enemies:
            pyxel.rect(e[0], e[1], 15, 15, 2) # Purple enemies

        for b in bulletsE:
            pyxel.rect(b[0], b[1], 3, 3, 8) # Red enemy bullets
            

        pyxel.text(5,5, "Lives: " + str(lives), 7 )
        pyxel.text(5,15, "Power Ups: " + str(status), 7)
        pyxel.text(5,25, "Enemies Killed: " + str(kills), 7)


pyxel.mouse(True)
pyxel.run(update, draw)