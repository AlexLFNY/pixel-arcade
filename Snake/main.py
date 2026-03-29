import pyxel
import random
import time # je ne crois pas que j'utilise time mais je ne vais pas
pyxel.init(160,120)
pyxel.load("mygame.pyxres")

tile = 16
gw = 160//16
gh = 120//16

snake = [(5,5),(4,5),(3,5)]
dx = 1
dy = 0

lost = 0
won = 0
fruiteat = 0
#ai
apple = (random.randint(0, gw-1), random.randint(0, gh-1))
bapple = (random.randint(0, gw-1), random.randint(0, gh-1))
#stopai
def update():
    global dx,dy,apple,bapple , lost , won, speed, fruiteat
    if won == 1 or lost == 1:
        return #ecrans win/lose reste a l'infini
    # controls
    if pyxel.btnp(pyxel.KEY_RIGHT):
        dx,dy = 1,0
    if pyxel.btnp(pyxel.KEY_LEFT):
        dx,dy = -1,0
    if pyxel.btnp(pyxel.KEY_UP):
        dx,dy = 0,-1
    if pyxel.btnp(pyxel.KEY_DOWN):
        dx,dy = 0,1
    speedvar = 11 - len(snake) #le plus petit, le plus vite
    speed = speedvar

    # move snake
    if pyxel.frame_count % speed != 0:
        return

    hx,hy = snake[0]
    new = (hx+dx,hy+dy)
    if new[0] == -1 or new[1]== -1 or new[0] == 10 or new[1]== 8:
        lost = 1


    snake.insert(0,new)
    #les murs tuent

    # eat apple
    if new == apple:
        apple = (random.randint(0,gw-1), random.randint(0,gh-1)) #

        fruiteat = fruiteat +1
    else:
        snake.pop()


    # eat bapple
    if new == bapple:
        bapple = (random.randint(0,gw-1), random.randint(0,gh-1))
        fruiteat = fruiteat +1
        if len(snake) > 1:
            snake.pop()

    elif len(snake) == 1:
        lost = 1
    elif len(snake) == 12: #ce nombre dicte combien de cases snake a

        won = 1

    print(fruiteat)








def draw():

    pyxel.cls(1)
    if lost == 1 and won !=1 :
        pyxel.rect(0,0,160,120,8)
        pyxel.text(80, 60, "GAME OVER", 3)
    elif won == 1 and lost != 1:
        pyxel.rect(0,0,160,120,3)
        pyxel.text(80, 60, f"YOUR SCORE IS: {fruiteat}", 8)



    else:
        # background
        for x in range(gw):
            for y in range(gh):
                pyxel.blt(x*16,y*16,0,0,0,16,16)

        # apple
        ax, ay = apple
        pyxel.blt(ax*16, ay*16, 0, 16, 0, 16, 16, 0)

        # bad apple
        bx, by = bapple
        pyxel.blt(bx*16, by*16, 0, 16, 16, 16, 16, 0)

        # snake(ai)
        for i,(x,y) in enumerate(snake):
            if i==0:
                pyxel.blt(x*16,y*16,0,0,32,16,16,0)
            else:
                pyxel.blt(x*16,y*16,0,0,16,16,16,0)
        #plus ai







pyxel.run(update,draw)