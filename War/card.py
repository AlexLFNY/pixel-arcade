import pyxel, random
from draw import draw_card #fonction (externe) qui dessine les cartes

#initialise la fenêtre Pyxel
pyxel.init(300, 250)
pyxel.load("cartes.pyxres")

debut = True #écran de début (affichage des règles)
fin = False #écran de la fin (affichage du gagnant)

deck = [] #paquet entier 
deck_a =[] #paquet divisé en deux (du joueur 1)
deck_b =[] #paquet divisé en deux (du joueur 2)
x = 1

score_a = 0 # score du joueur 1
score_b = 0 # score du joueur 2

end = 0 #indique si la partie est terminée

#création du paquet de cartes (avec 4 couleurs, et valeurs de 1 à 13)
for couleur in ["heart","diamond","club","spade"]:
    for i in range(1,14):
        deck.append({'couleur': couleur, 'valeur': i, 'retourne': False})

random.shuffle(deck) #melange le paquet
deck_a = deck[0:len(deck)//2] # séparation en 2
deck_b = deck[len(deck)//2:] # séparation en 2

#sélection au hasard d'une carte pour chaque joueur a chaque tour
carte_a = random.choice(deck_a)
carte_b = random.choice(deck_b)

print(deck_a, deck_b) #affichage pour debug

#fonction pour comparer les cartes, et donc mettre à jour le score de chacun
def compare_carte(a,b):
    global score_a, score_b
    
    
    if b['valeur'] == a['valeur']: # cas de l'egalite
        return score_a, score_b
    # Joueur 2 gagne
    elif b['valeur'] > a['valeur']: # cas si la carte b > carte a
        if a['valeur'] == 1: # cas special pour l'as
            score_a += 1
        else:
            score_b += 1
        return score_a, score_b
    # Joueur 1 gagne
    else: # si carte a > carte b
        if b['valeur'] == 1:
            score_b += 1
        else:
            score_a +=1
        return score_a, score_b
    
# Pour les tours
j1 = True # Joueur 1 peut jouer
j2 = False # Joueur 2 doit attendre


def update():
    global carte_a, carte_b, score_a, score_b, deck_a, deck_b, j1, j2, end, debut
    
    # Tour du Joueur 1
    if pyxel.btn(pyxel.KEY_Z) and j1 is True and j2 is False:
        #vérifie si la partie est finie
        if len(deck_a) == 0 and len(deck_b) == 0:
                end = 1
        if len(deck_a) > 0:
            carte_a = deck_a.pop() # Prend une carte puis l'enlève du paquet
            carte_a['retourne']=True # retourne la carte
            j1 = False # Joueur 1 doit attendre
            j2 = True # Joueur 2 peut jouer
    
    
    # Tour du Joueur 2
    if pyxel.btn(pyxel.KEY_M) and j2 is True and j1 is False:
        #vérifie si la partie est finie
        if len(deck_a) == 0 and len(deck_b) == 0:
                end = 1
        if len(deck_b) > 0:
            carte_b = deck_b.pop() # Prend une carte puis l'enlève du paquet
            carte_b['retourne']=True # retourne la carte
            compare_carte(carte_a,carte_b) #compare les cartes
            j2 = False # Joueur 2 attend
            j1 = False # Joueur 1 attend aussi

            
    # attendre entre 2 tours
    if pyxel.frame_count % 90 == 0:
        #vérifie si la partie est finie
        if len(deck_a) == 0 and len(deck_b) == 0:
                end = 1
        if j1 == False and j2 == False:
            carte_a['retourne'] = False # dos du paquet
            carte_b['retourne'] = False # dos du paquet
            
            # recommence un nouveau tour
            j1,j2 =True, False
    
    # pour quitter le jeu
    if pyxel.btnp(pyxel.KEY_Q):
        pyxel.quit()
    
    # quitter l'écran du début (commence la partie)
    if pyxel.btnp(pyxel.KEY_SPACE):
        debut = False


def draw():
    global carte, score_a, score_b, end, debut, fin
    pyxel.cls(3) #couleur de fond
    
    if debut:
        #consignes
        pyxel.rect(55, 95, 190, 65, 7)
        pyxel.text(60,100,"War is a two-player card game where the goal",5)
        pyxel.text(60,110,"is to win with the highest card rank against",5)
        pyxel.text(60,120,"your opponent and a point gets added to your",5)
        pyxel.text(60,130,"score. Each player takes a turn to flip the",5)
        pyxel.text(60,140,"card at the top of their deck. The highest",5)
        pyxel.text(60,150,"card wins! Good luck!",5)
        pyxel.text(95, 170, "---Press SPACE to start---", 1)
        
        #cotes du rectangle (decorations)
        pyxel.blt(55,95,1,1,1,1,65)
        pyxel.blt(245,95,1,1,1,1,65)
        pyxel.line(55,95,245,95, 1)
        pyxel.line(55,160,245,160,1)
        
    else:
        #affiche les cartes
        draw_card(carte_a, 25, 30)
        draw_card(carte_b, 175, 30)
        
        pyxel.blt(150,0,1,1,1,1,250)
        
        #les espaces de joueurs
        pyxel.text(60, 5, "Player 1", 1)
        pyxel.text(210, 5, "Player 2", 1)
        
        pyxel.text(20, 220, "Player 1 = Z Key", 1)
        pyxel.text(170, 220, "Player 2 = M Key", 1)
        
        #Affichage des scores
        pyxel.text(30, 20, f"Score: {score_a}", 1)
        pyxel.text(180, 20, f"Score: {score_b}", 1)
    
    if end == 1: #détermine si la partie est terminée
        if score_a > score_b:
            w = "1" #joueur 1 gagne
        elif score_b > score_a:
            w = "2" #joueur 2 gagne
        else:
            w = "1 & 2" # en cas d'egalite
        fin = True #permet l'affichage de l'écran de fin
        
    #affichage de l'écran de fin
    if fin:
        pyxel.cls(0)
        pyxel.text(110, 100, f"Player {w} wins!!!", 7)
        pyxel.text(100, 120, f"Thank you for playing.", 7)

#lancement de la boucle du jeu
pyxel.run(update, draw)
