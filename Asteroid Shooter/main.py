import pyxel
import random
import math
W, H = 160, 120
pyxel.init(W, H, title="Moving Ship")


pyxel.load("/Users/pierrepeuze/Desktop/computer science/Projet_final_v0.0.001.pyxres")


pyxel.play(0, 0, loop=True)


#P1vars
p1_x = W // 2
p1_y = H // 2
p1_lives = 5
p1_explosion = 0
p1_score = 0
p2_score = 0
#P2vars
p2_x = W // 2
p2_y = H // 2
p2_lives = 5
p2_explosion = 0
#randomvars
ship_speed = 2
roches = []
etoiles = []


def spawn_roche(idx):
   r_type = random.choice([0, 0, 1, 2])
   if r_type == 0: rad, speed = 5, 2
   elif r_type == 1: rad, speed = 3, 3.5
   else: rad, speed = 12, 1


   for _ in range(50):
       x = random.randint(10, W - 10)
       y = random.randint(-100, -10)
       overlap = False
       for i, r in enumerate(roches):
           if i != idx:
               other_rad = 5 if r[3] == 0 else (3 if r[3] == 1 else 12)
               if math.sqrt((x - r[0])**2 + (y - r[1])**2) < (rad + other_rad + 10):
                   overlap = True
                   break
       if not overlap:
           return [x, y, speed, r_type]
   return [random.randint(0, W), -10, speed, r_type]


for i in range(9):
   roches.append(spawn_roche(i))
   roches[-1][1] = random.randint(0, H)


for i in range(50):
   etoiles.append([
       random.randint(0, 159),
       random.randint(0, 119),
       random.randint(3, 3)
   ])




p1_bullets = []
p2_bullets = []
scene = "START" 
num_players = 1
menu_index = 0 


def draw_heart(x, y):
   """Draws a single heart pixel by pixel"""
   pyxel.pset(x, y, 8)
   pyxel.pset(x+2, y, 8)
   pyxel.rect(x-1, y+1, 5, 2, 8)
   pyxel.rect(x, y+3, 3, 1, 8)
   pyxel.pset(x+1, y+4, 8)


def update():
   global p1_x, p1_y, p1_lives, p1_explosion
   global p2_x, p2_y, p2_lives, p2_explosion
   global p1_bullets, p2_bullets, scene, num_players, menu_index
   global roches, etoiles
   global p1_score, p2_score
   # --- 1. COMMON ENVIRONMENT (Always runs) ---
   for i in etoiles:
       i[1] += i[2]
       if i[1] > H:
           i[0] = random.randint(0, W - 1)
           i[1] = 0


   for i, f in enumerate(roches):
       f[1] += f[2]
       if f[1] > H:
           new_pos = spawn_roche(i)
           f[0] = new_pos[0]
           f[1] = new_pos[1]


   # --- 2. SCENE CONTROLLERS ---
   if scene == "START":
       # Menu Navigation
       if pyxel.btnp(pyxel.KEY_W) or pyxel.btnp(pyxel.KEY_UP):
           menu_index = 0
       if pyxel.btnp(pyxel.KEY_S) or pyxel.btnp(pyxel.KEY_DOWN):
           menu_index = 1


       if menu_index == 0:
           if pyxel.btnp(pyxel.KEY_A) or pyxel.btnp(pyxel.KEY_LEFT):
               num_players = 1
           if pyxel.btnp(pyxel.KEY_D) or pyxel.btnp(pyxel.KEY_RIGHT):
               num_players = 2
      
       if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.KEY_RETURN):
           if menu_index == 1:
               scene = "GAME"
               p1_lives = 5
               p1_explosion = 0
               p1_score = 0
               p2_lives = 5
               p2_explosion = 0
               p2_score = 0
              
               # Starting positions
               if num_players == 1:
                   p1_x, p1_y = W // 2, H // 2
               else:
                   p1_x, p1_y = W // 3, H // 2
                   p2_x, p2_y = 2 * W // 3, H // 2
              
               p1_bullets = []
               p2_bullets = []
       return
   if scene == "GAME":
       # --- 3. PLAYER 1 UPDATES (WASD + Space) ---
       if pyxel.btn(pyxel.KEY_D): p1_x += ship_speed
       if pyxel.btn(pyxel.KEY_A): p1_x -= ship_speed
       if pyxel.btn(pyxel.KEY_S): p1_y += ship_speed
       if pyxel.btn(pyxel.KEY_W): p1_y -= ship_speed


       p1_x = max(8, min(W - 8, p1_x))
       p1_y = max(8, min(H - 16, p1_y))


       if p1_explosion > 0: p1_explosion -= 1


       if pyxel.btnp(pyxel.KEY_SPACE):
           p1_bullets.append([p1_x, p1_y - 8])


       # --- 4. PLAYER 2 UPDATES (Arrows + Enter) ---
       if num_players == 2:
           if pyxel.btn(pyxel.KEY_RIGHT): p2_x += ship_speed
           if pyxel.btn(pyxel.KEY_LEFT):  p2_x -= ship_speed
           if pyxel.btn(pyxel.KEY_DOWN):  p2_y += ship_speed
           if pyxel.btn(pyxel.KEY_UP):    p2_y -= ship_speed


           p2_x = max(8, min(W - 8, p2_x))
           p2_y = max(8, min(H - 16, p2_y))


           if p2_explosion > 0: p2_explosion -= 1


           if pyxel.btnp(pyxel.KEY_RETURN):
               p2_bullets.append([p2_x, p2_y - 8])


       # --- 5. COMMON GAMEPLAY SYSTEMS ---
          
       # Player 1 Bullet Movement
       for b in p1_bullets[:]:
           b[1] -= 4
           if b[1] < 0: p1_bullets.remove(b)


       # Player 2 Bullet Movement
       for b in p2_bullets[:]:
           b[1] -= 4
           if b[1] < 0: p2_bullets.remove(b)


       # --- 5. COLLISIONS & PHYSICS ---
      
       # Player 1 Bullets vs Asteroids
       for b in p1_bullets[:]:
           for i, f in enumerate(roches):
               rad = 5 if f[3] == 0 else (3 if f[3] == 1 else 12)
               if math.sqrt((b[0] - f[0])**2 + (b[1] - f[1])**2) < rad:
                   if b in p1_bullets: p1_bullets.remove(b)
                   new_pos = spawn_roche(i)
                   f[0], f[1], f[2], f[3] = new_pos[0], new_pos[1], new_pos[2], new_pos[3]
                   p1_score += 1
                   break


       # Player 2 Bullets vs Asteroids
       for b in p2_bullets[:]:
           for i, f in enumerate(roches):
               rad = 5 if f[3] == 0 else (3 if f[3] == 1 else 12)
               if math.sqrt((b[0] - f[0])**2 + (b[1] - f[1])**2) < rad:
                   if b in p2_bullets: p2_bullets.remove(b)
                   new_pos = spawn_roche(i)
                   f[0], f[1], f[2], f[3] = new_pos[0], new_pos[1], new_pos[2], new_pos[3]
                   p2_score += 1
                   break


       # Player 1 vs Asteroids
       for i, f in enumerate(roches):
           rad = 5 if f[3] == 0 else (3 if f[3] == 1 else 12)
           if math.sqrt((p1_x - f[0])**2 + (p1_y - f[1])**2) < (rad + 6):
               p1_lives -= 2
               p1_explosion = 15
               res = spawn_roche(i)
               f[0], f[1], f[2], f[3] = res[0], res[1], res[2], res[3]
      
       # Player 2 vs Asteroids
       if num_players == 2:
           for i, f in enumerate(roches):
               rad = 5 if f[3] == 0 else (3 if f[3] == 1 else 12)
               if math.sqrt((p2_x - f[0])**2 + (p2_y - f[1])**2) < (rad + 6):
                   p2_lives -= 2
                   p2_explosion = 15
                   res = spawn_roche(i)
                   f[0], f[1], f[2], f[3] = res[0], res[1], res[2], res[3]


       # Check Game Over
       if num_players == 1:
           if p1_lives <= 0: scene = "START"
       else:
           if p1_lives <= 0 and p2_lives <= 0:  # Both players dead
               scene = "START"
      
def draw():
   pyxel.cls(0)


   # --- Draw Background (Stars and Rocks) ---
   for i in etoiles:
       pyxel.circ(i[0], i[1],0, 7)


   for f in roches:
       col = 13 if f[3] == 0 else (2 if f[3] == 1 else 1)
       rad = 5 if f[3] == 0 else (3 if f[3] == 1 else 12)
       pyxel.circ(f[0], f[1], rad, col)
       pyxel.circb(f[0], f[1], rad, 7 if f[3] == 1 else 0)


   if scene == "START":
       # Title
       pyxel.text(50, 30, "ASTEROID DESTROYER", pyxel.frame_count % 16)
      
       # Player Selector
       col1 = 7 if menu_index == 0 else 5
       pyxel.text(55, 60, f"PLAYERS: < {num_players} >", col1)
      
       # Play Button
       col2 = 7 if menu_index == 1 else 5
       pyxel.text(70, 80, "[ PLAY ]", col2)
      
       pyxel.text(35, 110, "USE WASD TO NAVIGATE & SPACE", 6)
       return


  




   # --- Draw Game Elements ---
   # Draw Player 1 bullets
   for b in p1_bullets:
       pyxel.pset(b[0], b[1], 8)


   # Draw Player 2 bullets
   for b in p2_bullets:
       pyxel.pset(b[0], b[1], 12)


   # --- Draw Ships and UI ---
  
   # Draw Player 1
   if p1_lives > 0:
       pyxel.blt(p1_x - 8, p1_y - 8, 0, 0, 0, 16, 24, 0)
   elif p1_lives == 0:
       pyxel.text(25, 40, "DEAD", 3)
   if p1_explosion > 0:
       pyxel.circ(p1_x, p1_y, (15 - p1_explosion) * 2, 10)
       pyxel.circ(p1_x, p1_y, (15 - p1_explosion) * 3, 7)
  
   # P1 Hearts (top left)
   if p1_lives > 0:
       for h in range(max(0, p1_lives)):
           draw_heart(10 + h*8, 5)
       pyxel.text(10, 15, f"P1 SCORE: {p1_score}", 7)
   elif p1_lives == 0:
       pyxel.text(10, 15, "UR DEAD", 7)


   # Draw Player 2
   if num_players == 2:
       if p2_lives > 0:
           pyxel.blt(p2_x - 8, p2_y - 8, 0, 16, 0, 16, 24, 0) # Changed sprite coordinates for Player 2
       elif p2_lives == 0:
           pyxel.text(W - 25, 40, "DEAD", 3)
       if p2_explosion > 0:
           pyxel.circ(p2_x, p2_y, (15 - p2_explosion) * 2, 10)
           pyxel.circ(p2_x, p2_y, (15 - p2_explosion) * 3, 7)
      
       # P2 Hearts (top right)
       for h in range(max(0, p2_lives)):
           draw_heart(W - 45 + h*8, 5)
           pyxel.text(W - 45, 15, f"P2 SCORE: {p2_score}", 7)
pyxel.run(update, draw)



