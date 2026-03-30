import pyxel
import random
import time

   
pyxel.init(160, 120)
pyxel.load("marioassets.pyxres")      
                    

#pyxel edit marioassets.pyxres 


# Position du carré
x = 10
y = 60
        
# Numéro de scène   
scene = 1    

dx = 1
dy = 1

# Food location 
food_x = random.randint(0,150)
food_y = random.randint(0,110)

score = 0
def update():
    global x, y, dx, dy, scene, food_x, food_y  , score


    # Exit game with x
    if pyxel.btnp(pyxel.KEY_X):
        pyxel.quit()

    x = x + dx    
    y = y + dy

    # Moving
    if scene == 1:
        if pyxel.btnp(pyxel.KEY_D):
            dx = 2
        if pyxel.btnp(pyxel.KEY_A):
            dx = -2
        if pyxel.btnp(pyxel.KEY_W):   
            dy -= 2
        if pyxel.btnp(pyxel.KEY_S):
            dy += 2

    # Eat food
    if x > food_x - 5 and x < food_x + 15 and y > food_y - 5 and y < food_y + 15:
        food_x = random.randint(0,150)
        food_y = random.randint(0,110)
        dx += 3   
        dy += 3
        score +=1

    if x > 160 or x < 0:
        scene = 2
    if y > 120 or y < 0:
        scene = 2

# Erase the screen
def score_board():
    pyxel.text(5,5,f"Score :{score}",18)
def draw():
    pyxel.cls(0)

    # Player    
    if scene == 1:
        #pyxel.rect(x, y, 10, 10, 3) Snake into -> IMAGE   
        pyxel.blt(x, y, 0, 32,48,16,16)

    # Food
    pyxel.blt(food_x, food_y, 0, 16, 32, 15, 15)

    if scene == 2:
        pyxel.text(60, 60, "SORRY YOU LOST", 7)         
        pyxel.text(50, 70, f"Your FINAL SCORE WAS   : {score}", 7)
    
    score_board()   

pyxel.playm(0, loop=True)

pyxel.run(update, draw)       
# FORMAT   
# 
# pyxel.init()
# 
# def update():
#     # game logic here
# 
# def draw():
#     # drawing here
# 
# pyxel.run(update, draw)   