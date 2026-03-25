import pyxel
import random

# Taille de la fenêtre du jeu
WIDTH = 160
HEIGHT = 120


class Game:

    def __init__(self):
        # Crée la fenêtre du jeu
        pyxel.init(WIDTH, HEIGHT, title="Asteroid Game")

        # Position de départ du joueur
        self.player_x = WIDTH // 2
        self.player_y = HEIGHT - 10

        # Liste des astéroïdes
        self.asteroids = []

        # Variables du jeu
        self.score = 0
        self.lives = 3
        self.spawn = 0

        # Lance la boucle du jeu
        pyxel.run(self.update, self.draw)

    def update(self):

        # Quitte le jeu si on appuie sur Q
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        # Si le joueur n'a plus de vies, on arrête le jeu
        if self.lives <= 0:
            return

        # Déplace le joueur vers la gauche
        if pyxel.btn(pyxel.KEY_LEFT):
            self.player_x -= 2

        # Déplace le joueur vers la droite
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.player_x += 2

        # Empêche le joueur de sortir de l'écran à gauche
        if self.player_x < 0:
            self.player_x = 0

        # Empêche le joueur de sortir de l'écran à droite
        if self.player_x > WIDTH - 8:
            self.player_x = WIDTH - 8

        # Augmente le compteur pour faire apparaître les astéroïdes
        self.spawn += 1

        # Crée un nouvel astéroïde toutes les 20 images environ
        if self.spawn > 20:
            # Choisit une position x aléatoire
            x = random.randint(0, WIDTH - 6)

            # Choisit une vitesse aléatoire
            speed = random.randint(1, 4)

            # Ajoute un nouvel astéroïde en haut de l'écran
            self.asteroids.append([x, 0, speed])

            # Remet le compteur à 0
            self.spawn = 0

        # Fait descendre chaque astéroïde
        for a in self.asteroids:
            a[1] += a[2]

        # Vérifie si un astéroïde touche le joueur
        for a in self.asteroids:
            if self.player_x < a[0] + 6 and self.player_x + 8 > a[0] and self.player_y < a[1] + 6 and self.player_y + 8 > a[1]:
                # Enlève une vie si collision
                self.lives -= 1

                # Supprime tous les astéroïdes après collision
                self.asteroids = []

        # Augmente le score avec le temps
        self.score += 1

    def draw(self):

        # Efface l'écran avec la couleur noire
        pyxel.cls(0)

        # Dessine le joueur comme un carré bleu
        pyxel.rect(self.player_x, self.player_y, 8, 8, 11)

        # Dessine chaque astéroïde comme un cercle
        for a in self.asteroids:
            pyxel.circ(a[0] + 3, a[1] + 3, 3, 8)

        # Affiche le score en haut à gauche
        pyxel.text(5, 5, "Score: " + str(self.score), 7)

        # Affiche le nombre de vies en haut à gauche
        pyxel.text(5, 15, "Lives: " + str(self.lives), 7)

        # Affiche GAME OVER si le joueur n'a plus de vies
        if self.lives <= 0:
            pyxel.text(60, 60, "GAME OVER", 8)


# Démarre le jeu
Game()
