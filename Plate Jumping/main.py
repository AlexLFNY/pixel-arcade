import pyxel
import random

#initialisation du jeu
pyxel.init(120,160)
#son de la fin qd on meurt
pyxel.load("my_resource.pyxres")
pyxel.cls(12)
#positionement de la première plateforme
platform_x=20
platform_y=110
x = 30
y = 50

#intensite de gravite
gravite=0.4
force_saut=-8
velocite_y = 0
au_sol = True
fin = False
#score
scr = 0
score =  ("SCORE =", scr)

#plateformes affichées 
platforms= [[50, 60], [random.randint(0,100), 40], [random.randint(0,100), 50],[random.randint(0,100), 70], [random.randint(0,100), -10], [random.randint(0,100), -75]]
coll =False
x = 50
#collision avec les plateformes et les limites de l'ecran
def collision(platform_x, platform_y):
    return (x < platform_x + 20 and
            x  > platform_x -5 and
            y+8 >= platform_y and 
            y<= platform_y)
#sens du sprite
sens = 1
#pour que le jeu se reinitialise quand on appuie sur "espace"
def reset_game():
    global player_pos, score, enemies
    player_pos = [100, 100]
    score = 0
    enemies = []
    print("Game restarted!")

reset_game()

def update():
    global y,x, velocite_y,coll, scr, fin
    if fin:
#reinitialisation du jeu
        if pyxel.btn(pyxel.KEY_SPACE)==True:
                fin=False
                y = 0
                x = 25
                scr = 0
                velocite_y = 0.05
#bouger le sprite
    else:
        if pyxel.btn(pyxel.KEY_LEFT):
            x=x-4
#changement de sens du sprite
            sens = -1
        if pyxel.btn(pyxel.KEY_RIGHT):
            x=x+4
            sens = 1
        
        if x < 0:
            x = 0
        if x>112:
            x=112
        
        velocite_y = velocite_y + gravite
        y = y + velocite_y
        if y > 150: #on touche le sol
            end()
            #velocite_y = force_saut
        for p in platforms:
            if collision(p[0], p[1]):
                coll = True
#on rajoute une plateforme a la liste de plateformes existantes
                platforms.append( [random.randint(0,100), -20])
                scr = scr + 1
                #on rajoute
                if velocite_y > 0:
                    velocite_y = force_saut
         
 # pour qu'il y ait un nombre infini de plateformes               
        if coll:
               for p in platforms:
                 p[1] += 20
                
        coll = False
        
  
     
def draw():
    #couleur du fond 
    pyxel.cls(0)
    if fin:
           pyxel.text(50,50,"Fin....",4)
           pyxel.text(20,70,"Appuyez sur espace....",4)
           
    else:
        #continuation du jeu
        pyxel.rect(x,y,8,8,13)
        pyxel.blt(x,y, 1, 5,3,sens*10,13)
        for p in platforms:
            pyxel.rect(p[0], p[1], 10,4, 14)
        pyxel.text(0,10,str(scr),1)   
    
def end():
    global fin
    fin = True
    pyxel.playm(0)

        
pyxel.run(update,draw)
