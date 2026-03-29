import pyxel
import random

# -------------------------------------------------------
# CONSTANTES
# -------------------------------------------------------
TAILLE  = 16
VIDE    = 0
MUR     = 1
DEPART  = 2
SORTIE  = 3
PORTE   = 4
OUVERTE = 5

# -------------------------------------------------------
# CARTE
# -------------------------------------------------------
CARTE = [
   [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
   [1,2,0,0,1,0,4,0,0,0,1,0,0,0,0,1],
   [1,1,1,0,1,0,1,1,1,0,1,0,1,1,0,1],
   [1,0,0,0,4,0,1,0,0,0,0,0,1,0,0,1],
   [1,0,1,1,1,1,1,0,1,1,4,0,1,0,1,1],
   [1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1],
   [1,1,1,0,1,1,1,1,1,0,1,1,1,1,0,1],
   [1,0,0,0,1,0,4,0,0,0,1,0,0,0,0,1],
   [1,1,1,0,4,0,1,0,1,1,1,0,1,1,0,1],
   [1,0,1,0,0,0,1,0,0,0,4,0,0,1,0,1],
   [1,0,1,0,1,1,4,0,1,1,1,1,0,1,0,1],
   [1,0,0,0,1,0,0,0,0,1,0,0,0,0,3,1],
   [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

# -------------------------------------------------------
# DEVINETTES
# -------------------------------------------------------
DEVINETTES_LIST = [
   {"question": ["J'ai des touches mais j'ouvre rien.", "Qui suis-je ?"], "choices": ["1. Piano", "2. Sac", "3. Livre"], "answer": 0},
   {"question": ["Plus j'enleve, plus je grandis", "Qui suis-je ?"], "choices": ["1. Ombre", "2. Trou", "3. Arbre"], "answer": 1},
   {"question": ["Je tombe sans me faire mal", "Qui suis-je ?"], "choices": ["1. Pluie", "2. Pierre", "3. Feuille"], "answer": 0},
   {"question": ["Je fais le tour de la maison mais je ne bouge pas.", "Qui suis-je ?"], "choices": ["1. Papa", "2. Mur", "3. Fauteuil"], "answer": 1},
   {"question": ["Plus j'ai de gardiens, moins je suis gardé.", "Qui suis-je ?"], "choices": ["1. Rihanna", "2. Lady Gaga", "3. Un secret"], "answer": 2},
   {"question": ["Je commence par e et finis par e.", "Qui suis-je ?"], "choices": ["1. Enveloppe", "2. ee", "3. emmenez"], "answer": 0},
   {"question": ["Je commence la nuit et termine le matin.", "Qui suis-je ?"], "choices": ["1. lune", "2. lettre n", "3. sommeil"], "answer": 1},
   {"question": ["13 carreaux mais pas de fenêtres ?", "Qui suis-je ?"], "choices": ["1. appartement", "2. jeu de cartes", "3. maison"], "answer": 1},
]

DEVINETTES_ORIG = DEVINETTES_LIST.copy()

# -------------------------------------------------------
# PYXEL
# -------------------------------------------------------
LARGEUR = len(CARTE[0]) * TAILLE
HAUTEUR = len(CARTE) * TAILLE
pyxel.init(LARGEUR, HAUTEUR, title="Maze Game", fps=60)

# -------------------------------------------------------
# JOUEUR
# -------------------------------------------------------
x = 1 * TAILLE + TAILLE // 2
y = 1 * TAILLE + TAILLE // 2
speed = 2

# -------------------------------------------------------
# ETAT
# -------------------------------------------------------
win = False
lose = False
devinette = None
current_question = None

message = ""
msg_timer = 0

temps = 60 * 60

etat = "menu"

# -------------------------------------------------------
# UTILS
# -------------------------------------------------------
def case_en(px, py):
   return px // TAILLE, py // TAILLE

def type_case(col, ligne):
   if 0 <= ligne < len(CARTE) and 0 <= col < len(CARTE[0]):
       return CARTE[ligne][col]
   return MUR

def popup(msg, duree=90):
   global message, msg_timer
   message = msg
   msg_timer = duree

# -------------------------------------------------------
# DEVINETTE
# -------------------------------------------------------
def lancer_devinette(col, ligne):
   global devinette, current_question, DEVINETTES_LIST

   devinette = (col, ligne)

   if not DEVINETTES_LIST:
       DEVINETTES_LIST = DEVINETTES_ORIG.copy()

   current_question = DEVINETTES_LIST.pop(random.randrange(len(DEVINETTES_LIST)))

def repondre(choix):
   global devinette

   if choix == current_question["answer"]:
       col, ligne = devinette
       CARTE[ligne][col] = OUVERTE
       popup("Correct !")
   else:
       popup("Faux !")

   devinette = None

# -------------------------------------------------------
# UPDATE
# -------------------------------------------------------
def update():
   global x, y, win, lose, msg_timer, message, temps, etat

   if etat == "menu":
       if pyxel.btnp(pyxel.KEY_SPACE):
           etat = "jeu"
       return

   if win or lose:
       return

   temps -= 1
   if temps <= 0:
       lose = True

   if msg_timer > 0:
       msg_timer -= 1
       if msg_timer == 0:
           message = ""

   if devinette:
       if pyxel.btnp(pyxel.KEY_1):
           repondre(0)
       elif pyxel.btnp(pyxel.KEY_2):
           repondre(1)
       elif pyxel.btnp(pyxel.KEY_3):
           repondre(2)
       return

   new_x, new_y = x, y

   if pyxel.btn(pyxel.KEY_LEFT):
       new_x -= speed
   if pyxel.btn(pyxel.KEY_RIGHT):
       new_x += speed
   if pyxel.btn(pyxel.KEY_UP):
       new_y -= speed
   if pyxel.btn(pyxel.KEY_DOWN):
       new_y += speed

   r = 5
   coins = [(new_x-r,new_y-r),(new_x+r,new_y-r),(new_x-r,new_y+r),(new_x+r,new_y+r)]

   bloque = False
   for cx, cy in coins:
       col, ligne = case_en(cx, cy)
       t = type_case(col, ligne)

       if t == MUR:
           bloque = True
           break

       if t == PORTE:
           lancer_devinette(col, ligne)
           bloque = True
           break

   if not bloque:
       x, y = new_x, new_y

   col, ligne = case_en(x, y)
   if type_case(col, ligne) == SORTIE:
       win = True

# -------------------------------------------------------
# DRAW
# -------------------------------------------------------
def draw():

   if etat == "menu":
       pyxel.cls(0)
       pyxel.text(70, 40, "ESCAPE THE MAZE", 10)
       pyxel.text(40, 70, "Utilise les fleches pour bouger", 7)
       pyxel.text(40, 85, "Reponds aux devinettes", 7)
       pyxel.text(40, 100, "Evite le temps !", 7)
       pyxel.text(80, 140, "ESPACE POUR JOUER", 11)
       return

   pyxel.cls(0)

   for ligne in range(len(CARTE)):
       for col in range(len(CARTE[0])):
           t = CARTE[ligne][col]
           px = col * TAILLE
           py = ligne * TAILLE

           if t == MUR:
               pyxel.rect(px, py, TAILLE, TAILLE, 5)
           elif t == DEPART:
               pyxel.rect(px, py, TAILLE, TAILLE, 0)
               pyxel.rect(px+4, py+4, TAILLE-8, TAILLE-8, 11)
           elif t == SORTIE:
               pyxel.rect(px, py, TAILLE, TAILLE, 11)
               pyxel.text(px+1, py+5, "OUT", 0)
           elif t == PORTE:
               pyxel.rect(px, py, TAILLE, TAILLE, 8)
               pyxel.text(px+4, py+5, "?", 7)
           elif t == OUVERTE:
               pyxel.rect(px, py, TAILLE, TAILLE, 3)
           else:
               pyxel.rect(px, py, TAILLE, TAILLE, 0)

   pyxel.circ(x, y, 5, 7)
   pyxel.text(5, 5, f"Temps: {temps//60}", 10)

   if message:
       pyxel.text(5, 15, message, 9)

   if devinette:
       d = current_question
       pyxel.rect(20, 40, LARGEUR-40, 100, 1)
       pyxel.rectb(20, 40, LARGEUR-40, 100, 7)
       pyxel.text(30, 50, d["question"][0], 7)
       pyxel.text(30, 60, d["question"][1], 7)
       pyxel.text(30, 80, d["choices"][0], 11)
       pyxel.text(30, 95, d["choices"][1], 11)
       pyxel.text(30, 110, d["choices"][2], 11)

   if win:
       pyxel.cls(0)
       pyxel.text(80, 90, "YOU WIN!", 10)

   if lose:
       pyxel.cls(0)
       pyxel.text(80, 90, "TIME UP!", 8)

pyxel.run(update, draw)