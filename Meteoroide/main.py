import pyxel #OBLIGATOIRE
import random
import time
LARGEUR = 400
HAUTEUR = 300
pyxel.init(LARGEUR, HAUTEUR) #creation de la fenêtre
#chargement image
pyxel.images[0].load(0, 0, "SPACESHIP2.png")
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
movement_enemy = 1.5
movement_shooter = 1.25
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
vies = 5
stars = []
asteroid_cooldown = 120
color_asteroids = 3
immobilized = 0
spaceship_movement = 7
knockback = 0
probability_of_special_event_happening = "1/30"
radius_asteroids = 8
speed_asteroids = 3


def update():
    global loss, speed_asteroids, radius_asteroids, spaceship_movement,y, x, centre_x, centre_y, cooldown, x_enemies, y_enemies, movement_enemy, win, score_enemy, movement_shooter, sc, vies, score_shooter, asteroid_cooldown, color_asteroids, immobilized, knockback,probability_of_special_event_happening
    if win == True or loss == True:
        return None
    #Code for the cooldowns of the asteroids, the bullets of the spaceship, and the bullets of the shooters
    cooldown -= 0.8
    sc -= 0.75
    asteroid_cooldown -= 1
    immobilized -= 3
    # Code that makes a visual knockback effect
    x += knockback
    if x < 0:
        x = 0
    if x + 50 > LARGEUR:
        x = LARGEUR - 50
    knockback *= 0.85
    if abs(knockback) < 0.5:
        knockback = 0
       
    if immobilized <= 0:
    # Code that makes the spaceship shoot when SPACE is pressed
        if pyxel.btn(pyxel.KEY_SPACE) and cooldown <= 0:
            liste_balles.append([x+20,(y-25)])
            cooldown = 15
    # Code that makes the spaceship move left and right
        if pyxel.btn(pyxel.KEY_A):
            x-=spaceship_movement
            if x<0:
                x=0
        elif pyxel.btn(pyxel.KEY_D):
            x+= spaceship_movement
            if x + 50 > LARGEUR:
                x= LARGEUR -50
    # Code that makes the the bullets go up and makes them disappear once they leave the screen
    for b in liste_balles :
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
        if coord[0] <= 0 or coord[0] + 10 >= LARGEUR:
            movement_enemy = movement_enemy * -1
            for coord in liste_enemies:
                coord[1] += 5.5
    for coord in liste_enemies:
        coord[0] += movement_enemy
    # Code that makes the shooters go left and right and move down once one has touched the edge
    for coordo in liste_shooters:
        if coordo[0] <= 0 or coordo[0] + 10 >= LARGEUR:
            movement_shooter = movement_shooter * -1
            for coordo in liste_shooters:
                coordo[1] += 5.5
    for coordo in liste_shooters:
        coordo[0] += movement_shooter
    # Code that ensures that spaceship bullets destroy the enemies
    for balle in liste_balles:
        for enemy in liste_enemies:
            if enemy[1] <= balle[1] <= enemy[1]+10 and enemy[0]+10>balle[0]>enemy[0]-10:
                liste_enemies.remove(enemy)
                liste_balles.remove(balle)
                score_enemy += 1
    # Code that ensures that spaceship bullets destroy the shooters
    for b in liste_balles:
        for shooter in liste_shooters:
            if shooter[1] <= b[1] <= shooter[1]+10 and shooter[0]+10>b[0]>shooter[0]-10:
                liste_shooters.remove(shooter)
                liste_balles.remove(b)
                score_shooter += 1
    # Code that makes it so if the spaceship gets hit with a bullet, it loses a life
    for b in liste_bds[:]:
        if y-25<b[1]<y+13 and x<b[0]<x+50:
            liste_bds.remove(b)
            vies -= 1
       
    # Code that sends a win signal if all enemies are destroyed
    if score_shooter+score_enemy == 20:
        win = True
       
    # Code that checks if the enemies have reached the y coordinate of the spaceship. If this is the case, the game ends
    for enem in liste_enemies:
        if enem[1] >= y-25:
            loss = True
    if vies == 0:
        loss = True

    for shooter in liste_shooters:
        if shooter[1] >= y-25:
            pyxel.quit()
    # Code that makes makes the stars move
    for star in stars:
        star[1] += 1
        if star[1] > HAUTEUR:
            star[1] = 0
    # Code that makes asteroids move and be destroyed once they get off the screen
    if (score_shooter+score_enemy) >= 5:
        if asteroid_cooldown < 0:
            liste_asteroid.append([random.randint(30,LARGEUR-30),0,2])
            radius_asteroids += 0.2
            speed_asteroids += 0.2
            asteroid_cooldown = 120
           
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
                    color_asteroids = 3
    # Code that makes it so if the
    if len(liste_asteroid) > 0:
        for asteroid in liste_asteroid[:]:
            if x<asteroid[0]<x+50 and y-25<asteroid[1]<y-13:
                if random.randint(1,int(probability_of_special_event_happening.split("/")[1])) == 1:
                    spaceship_movement *= -1
                    vies -= 1
                    liste_asteroid.remove(asteroid)
                    immobilized = 180
                    if asteroid[0]<x+25:
                        knockback = 8
                    elif asteroid[0]<50:
                        knockback = -8
                else:
                    vies -= 1
                    liste_asteroid.remove(asteroid)
                    immobilized = 180
                    if asteroid[0]<x+25:
                        knockback = 8
                    elif asteroid[0]<50:
                        knockback = -8


def draw():
   
    global difference, has_run, win, score_shooter, score_enemy, color_asteroids, radius_asteroids, loss
    pyxel.cls(0)
    for star in stars:
        pyxel.pset(star[0], star[1], 7)
    
    #joueur 
    #pyxel.rect(x,y-25,50,12, color) code initiale
    pyxel.blt(x,y-25, 0, 0,0,50,42)
    

    for b in liste_balles:
        pyxel.rect(b[0],b[1],5,5,10)
    for b in liste_bds:
        pyxel.rect(b[0],b[1],5,5,15)
    while has_run == False:
        for i in range(10):
            liste_enemies.append([10+difference,30])
            liste_shooters.append([10+difference,10])
            difference += 40
        for i in range(50):
            stars.append([random.randint(0, LARGEUR), random.randint(0, HAUTEUR)])
        has_run = True
    for enem in liste_enemies:
        pyxel.rect(enem[0],enem[1],10,10,9)
    for shooter in liste_shooters:
        pyxel.rect(shooter[0],shooter[1],10,10,10)
       
    if win == True:
        pyxel.text(180,150, "YOU WON!", 7)
    if loss == True:
        pyxel.text(180,150, "YOU LOST.. :(",7)
       
    for asteroid in liste_asteroid:
        if asteroid[2] == 1:
            color_asteroids = 8
        else:
            color_asteroids = 3
        pyxel.circ(asteroid[0],asteroid[1],radius_asteroids,color_asteroids)
    pyxel.text(2,2,f"Score: {score_shooter+score_enemy}",7)
    if score_shooter+score_enemy >= 10:
        pyxel.text(180,2,"Level 2",7)
    else:
        pyxel.text(180,2,"Level 1",7)
    pyxel.text(2,10,f"Lives: {vies}",7)
    pyxel.text(2,50,f"{len(liste_balles)}",7)
    if spaceship_movement < 0 and immobilized > 0:
        pyxel.text(40,150, "UH OH! YOU HAVE BEEN HIT WITH THE MYSTERY ASTEROID... YOUR MOVEMENT HAS BEEN AFFECTED",7)
    elif immobilized > 0:
        pyxel.text(90,150, "YOU HAVE BEEN IMMOBILIZED DUE TO CRITICAL DAMAGES TO YOUR SPACECRAFT!",7)
pyxel.run(update,draw)
