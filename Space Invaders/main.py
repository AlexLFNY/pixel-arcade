import pyxel #OBLIGATOIRE
import random
import time
LARGEUR = 400
HAUTEUR = 300
pyxel.init(LARGEUR, HAUTEUR) #creation de la fenêtre

pyxel.sounds[0].set(
    "c3 e3 g3 b3 c4 r b3 g3", 
    "p",                     
    "6",    
    "v",                 
    20                      
)

pyxel.sounds[1].set(
    "g1 f#1 f1 e1 g1 f#1 f1 e1", 
    "s",                      
    "6", 
    "n", 
    20                   
)

pyxel.sounds[2].set(
    "c4 g4 e4 c4 r g4 c4 r",
    "p",               
    "4",                  
    "f",                
    20                        
)

pyxel.sounds[3].set(
    "c1 r r r c1 r r r",
    "n",      
    "4", 
    "s",                     
    15
)
pyxel.music(0).set([0, 2], [1], [3], [])


y= 290
x= 200
x_enemies = 100
y_enemies = 20
color=2
etat_cercle = False
dx =1
dy=-1
liste_balles = []
cooldown = 0
movement_enemy = 1.15
movement_shooter = 0.95
difference = 0
liste_enemies = []
liste_shooters = []
liste_bds = []
liste_asteroid = []
has_run = False
win = False
loss = False
score_enemy= 0
score_shooter=0
sc = 5
vies = 3
stars = []
asteroid_cooldown = 120 
color_asteroids = 4
immobilized = 0
spaceship_movement = 7
knockback = 0
probability_of_special_event_happening = "1/20"
radius_asteroids = 8
speed_asteroids = 3
timer=0
death_timer = 0
score_asteroid = 0
# Spaceship sprite
pyxel.images[0].set(0, 0, [
    "0000000000001000000000000",
    "0000000000012100000000000",
    "0000000000127210000000000",
    "0000000001277721000000000",
    "0000000001127211000000000",
    "0000000011221221100000000",
    "0000000011221221100000000",
    "0000000111111111110000000",
    "0000001111661661111000000",
    "0000001111661661111000000",
    "1000001111121211111000001",
    "1100011111121211111100011",
    "1111111111121211111111111",
    "1106111111121211111116011",
    "1106111111121211111116011",
    "0111111111111111111111110",
    "0011111655551555561111100",
    "0000111699961699961110000",
    "0000011699961699961100000",
    "0000001688881888861000000",
    "0000000688880888860000000",
    "0000000088880888800000000"
])
#Enemy Sprite
pyxel.images[0].set(30, 0, [
    "00ccccccccc00",
    "0ccccccccccc0",
    "ccccccccccccc",
    "cc7c7ccc7c7cc",
    "ccccccccccccc",
    "0ccc6ccc6ccc0",
    "00ccccccccc00",
    "0c600000006c0",
    "c00000000000c",
    "0000000000000"
])
#Shooter Sprite
pyxel.images[0].set(50, 0, [
    "900000000000009",
    "090000000000090",
    "099999999999990",
    "999797979797999",
    "999999999999999",
    "099a9aaaaa9a990",
    "009999999999900",
    "000999a9a999000",
    "009900000009900",
    "090000000000090",
    "000000000000000"
])
#Explosion Sprite
pyxel.images[0].set(70, 0, [
    "000804908000",
    "908989840800",
    "089494988000",
    "084999998800",
    "899449999480",
    "804999949980",
    "099949990880",
    "084999498800",
    "008494988000",
    "000888940800",
    "000040080040",
    "800000000000"
])

def update():
    global loss, score_asteroid, speed_asteroids, radius_asteroids, spaceship_movement,y, x, centre_x, centre_y, cooldown, x_enemies, y_enemies, movement_enemy, win, score_enemy, movement_shooter, sc, vies, score_shooter, asteroid_cooldown, color_asteroids, immobilized, knockback,probability_of_special_event_happening, timer, death_timer
    timer-=1
    if loss:
        if death_timer > 0:
            death_timer -= 1
            return
        return
    if pyxel.btn(pyxel.KEY_Q):
        pyxel.stop()
        
    if win == True:
        y-=5
    #Code for the cooldowns of the asteroids, the bullets of the spaceship, and the bullets of the shooters
    cooldown -= 0.8
    sc -= 0.75
    asteroid_cooldown -= 1
    immobilized -= 3
    # Code that makes a visual knockback effect
    x += knockback
    if x < 0:
        x = 0
    if x + 25 > LARGEUR:
        x = LARGEUR - 25
    knockback *= 0.85
    if abs(knockback) < 0.5:
        knockback = 0
        
    if immobilized <= 0:
    # Code that makes the spaceship shoot when SPACE or UP_ARROW is pressed
        if score_asteroid >= 2:
            if (pyxel.btn(pyxel.KEY_SPACE) or pyxel.btn(pyxel.KEY_UP))and cooldown <= 0: 
                liste_balles.append([x+4,y-22])
                liste_balles.append([x+19,y-22])
                cooldown = 15
        else:
            if (pyxel.btn(pyxel.KEY_SPACE) or pyxel.btn(pyxel.KEY_UP)) and cooldown <= 0:
                liste_balles.append([x+10,y-22])
                cooldown = 15
    # Code that makes the spaceship move left and right with (A,D) or (LEFT,RIGHT)
        if pyxel.btn(pyxel.KEY_A):
            x-=spaceship_movement
            if x<0:
                x=0
        elif pyxel.btn(pyxel.KEY_D):
            x+= spaceship_movement
            if x + 25 > LARGEUR:
                x= LARGEUR -25
        elif pyxel.btn(pyxel.KEY_LEFT):
            x-=spaceship_movement
            if x<0:
                x=0
        elif pyxel.btn(pyxel.KEY_RIGHT):
            x+= spaceship_movement
            if x + 25 > LARGEUR:
                x= LARGEUR -25
    # Code that makes the the bullets go up and makes them disappear once they leave the screen
    for b in liste_balles:
        b[1] -=6
    for el in liste_balles:
        if el[1] < 0:
            liste_balles.remove(el)
    # Code that makes the enemies' bullets go down, makes them disapear upon leaving the screen, and makes random enemies shoot then
    for b in liste_bds:
        b[1] += 5
    for el in liste_bds:
        if el[1] > 300:
            liste_bds.remove(el)
    if sc < 0 and score_shooter < 10:
        liste_bds.append(random.choice(liste_shooters).copy())
        sc = 20
        
    # Code that makes enemies go left and right and move down once one has touched the edge
    for coord in liste_enemies:
        if coord[0] <= 0 or coord[0] + 13 >= LARGEUR:
            movement_enemy = movement_enemy * -1
            for coord in liste_enemies:
                coord[1] += 5.5
    for coord in liste_enemies:
        coord[0] += movement_enemy
    # Code that makes the shooters go left and right and move down once one has touched the edge
    for coordo in liste_shooters:
        if coordo[0] <= 0 or coordo[0] + 15 >= LARGEUR:
            movement_shooter = movement_shooter * -1
            for coordo in liste_shooters:
                coordo[1] += 5.5
    for coordo in liste_shooters:
        coordo[0] += movement_shooter
    # Code that ensures that spaceship bullets destroy the enemies
    for balle in liste_balles:
        for enemy in liste_enemies:
            if enemy[1] <= balle[1] <= enemy[1]+10 and enemy[0]+13>balle[0]>enemy[0]-13:
                liste_enemies.remove(enemy)
                liste_balles.remove(balle)
                score_enemy += 1
    # Code that ensures that spaceship bullets destroy the shooters
    for b in liste_balles:
        for shooter in liste_shooters:
            if shooter[1] <= b[1] <= shooter[1]+11 and shooter[0]+15>b[0]>shooter[0]-15:
                liste_shooters.remove(shooter)
                liste_balles.remove(b)
                score_shooter += 1
    # Code that makes it so if the spaceship gets hit with a bullet, it loses a life
    for b in liste_bds[:]:
        if y-22<b[1]<y and x<b[0]<x+25:
            liste_bds.remove(b)
            vies -= 1
        
    # Code that sends a win signal if all enemies are destroyed
    if score_shooter+score_enemy == 20:
        win = True
        
    # Code that checks if the enemies have reached the y coordinate of the spaceship. If this is the case, the game ends
    for enem in liste_enemies:
        if enem[1] >= y-22:
            death_timer = 20
            loss = True
    if vies == 0:
        death_timer = 20
        loss = True

    for shooter in liste_shooters:
        if shooter[1] >= y-22:
            death_timer = 20
            loss = True
    # Code that makes makes the stars move
    for star in stars:
        star[1] += 1
        if star[1] > HAUTEUR:
            star[1] = 0
    # Code that makes asteroids move and be destroyed once they get off the screen
    if (score_shooter+score_enemy) >= 8:
        if asteroid_cooldown < 0:
            liste_asteroid.append([random.randint(30,LARGEUR-30),0,2])
            radius_asteroids += 0.5
            speed_asteroids += 0.35
            asteroid_cooldown = 120
    # Code that deletes the asteroids once they exit the frame
    if len(liste_asteroid) > 0:
        for asteroid in liste_asteroid:
            asteroid[1] += speed_asteroids
            if asteroid[1] >= 400:
                liste_asteroid.remove(asteroid)
    # Code that makes the asteroids have 2 lives
    if len(liste_asteroid) > 0:
        for asteroid in liste_asteroid[:]:
            for balle in liste_balles[:]:
                if asteroid[0]-radius_asteroids<balle[0]<asteroid[0]+radius_asteroids and asteroid[1]-radius_asteroids<balle[1]<asteroid[1]+radius_asteroids:
                    asteroid[2] -= 1
                    liste_balles.remove(balle)
            if asteroid[2] <= 0:
                    liste_asteroid.remove(asteroid)
                    score_asteroid += 1
                    color_asteroids = 4
    # Code for the collisions in between the asteroids and the player: 1/20 of special event happening + knockback
    if len(liste_asteroid) > 0:
        for asteroid in liste_asteroid[:]:
            if x<asteroid[0]<x+27 and y-22<asteroid[1]<y:
                if random.randint(1,int(probability_of_special_event_happening.split("/")[1])) == 1:
                    spaceship_movement *= -1
                    vies -= 1
                    liste_asteroid.remove(asteroid)
                    immobilized = 180
                    if asteroid[0]<x+11:
                        knockback = 8
                    else:
                        knockback = -8
                else:
                    vies -= 1
                    liste_asteroid.remove(asteroid)
                    immobilized = 180
                    if asteroid[0]<x+12:
                        knockback = 8
                    else:
                        knockback = -8


def draw():
    
    global difference, has_run, win, score_shooter, score_enemy, color_asteroids, radius_asteroids, loss, timer, death_timer
    pyxel.cls(0)
    # Code that draws the stars
    for star in stars:
        pyxel.pset(star[0], star[1], 7)
    # Code that does the explosion if the player has lost
    if loss and death_timer > 0:
        pyxel.blt(x + 6, y - 18, 0, 70, 0, 11, 11, 0)
    elif not loss:
        pyxel.blt(x, y - 22, 0, 0, 0, 25, 25, 0)
    # Code that draws the player bullets
    for b in liste_balles:
        pyxel.rect(b[0],b[1],5,5,10)
    # Code that draws the shooter bullets
    for b in liste_bds:
        pyxel.rect(b[0],b[1],5,5,15)
    # Code that makes the 10 shooters and 10 enemies when the game has started
    while has_run == False:
        for i in range(10):
            liste_enemies.append([10+difference,30])
            liste_shooters.append([10+difference,10])
            difference += 40
        for i in range(50):
            stars.append([random.randint(0, LARGEUR), random.randint(0, HAUTEUR)])
        has_run = True
    for enem in liste_enemies:
        pyxel.blt(enem[0], enem[1], 0, 30, 0, 13, 10, 0)
    for shooter in liste_shooters:
        pyxel.blt(shooter[0], shooter[1], 0, 50, 0, 15, 11, 0)
    # Text for when the player has won
    if win == True:
        pyxel.text(180,150, "YOU WON!", 7)
    # text for when the player has lost
    if loss == True:
        pyxel.text(180,120, "YOU LOST.. :(",7)
    # Code that draws the asteroids. Makes them different colors according to the amount of lives they have
    for asteroid in liste_asteroid:
        if asteroid[2] == 1:
            color_asteroids = 8
        else:
            color_asteroids = 4
        pyxel.circ(asteroid[0],asteroid[1],radius_asteroids,color_asteroids)
    pyxel.text(2,2,f"Score: {score_shooter+score_enemy}",7)
        
    if score_shooter+score_enemy >= 8:
        pyxel.text(180,2,"Level 2",7)
    else:
        pyxel.text(180,2,"Level 1",7)
        
    if score_shooter+score_enemy == 8:
        timer=100
    if timer>0:
            pyxel.text(160,140,"WATCH OUT FOR ASTEROIDS!",7)
    
    pyxel.text(2,10,f"Lives: {vies}",7)
    if spaceship_movement < 0 and immobilized > 0:
        pyxel.text(40,150, "UH OH! YOU HAVE BEEN HIT WITH THE MYSTERY ASTEROID... YOUR MOVEMENT HAS BEEN AFFECTED",7)
    elif immobilized > 0:
        pyxel.text(90,150, "YOU HAVE BEEN IMMOBILIZED DUE TO CRITICAL DAMAGES TO YOUR SPACECRAFT!",7)

pyxel.playm(0, loop=True)

pyxel.run(update,draw)
