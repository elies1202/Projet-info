# -*- coding: utf-8 -*-

# Nicolas, 2021-03-05
from __future__ import absolute_import, print_function, unicode_literals

import random 
import numpy as np
import sys
from itertools import chain

import time

import pygame

from pySpriteWorld.gameclass import Game,check_init_game_done
from pySpriteWorld.spritebuilder import SpriteBuilder
from pySpriteWorld.players import Player
from pySpriteWorld.sprite import MovingSprite
from pySpriteWorld.ontology import Ontology
import pySpriteWorld.glo

from search.grid2D import ProblemeGrid2D
from search import probleme




# ---- ---- ---- ---- ---- ----
# ---- Misc                ----
# ---- ---- ---- ---- ---- ----




# ---- ---- ---- ---- ---- ----
# ---- Main                ----
# ---- ---- ---- ---- ---- ----

game = Game()

def init(_boardname=None):
    global player,game
    name = _boardname if _boardname is not None else 'astarMap'
    #name = _boardname if _boardname is not None else 'demoMap'
    game = Game('Cartes/' + name + '.json', SpriteBuilder)
    game.O = Ontology(True, 'SpriteSheet-32x32/tiny_spritesheet_ontology.csv')
    game.populate_sprite_names(game.O)
    game.fps = 5  # frames per second
    game.mainiteration()
    player = game.player
    
def main():

    #for arg in sys.argv:
    iterations = 100 # default
    if len(sys.argv) == 2:
        iterations = int(sys.argv[1])
    print ("Iterations: ")
    print (iterations)

    init()
    

    
    #-------------------------------
    # Initialisation
    #-------------------------------
    
    nbLignes = game.spriteBuilder.rowsize
    nbCols = game.spriteBuilder.colsize
       
    print("lignes", nbLignes)
    print("colonnes", nbCols)
    
    
    players = [o for o in game.layers['joueur']]
    nbPlayers = len(players)
    score = [0]*nbPlayers
    
       
           
    # on localise tous les états initiaux (loc du joueur)
    # positions initiales des joueurs
    initStates = [o.get_rowcol() for o in game.layers['joueur']]
    print ("Init states:", initStates)
    
    # on localise tous les objets ramassables
    # sur le layer ramassable
    goalStates = [o.get_rowcol() for o in game.layers['ramassable']]
    print ("Goal states:", goalStates)
        
    # on localise tous les murs
    # sur le layer obstacle
    wallStates = [w.get_rowcol() for w in game.layers['obstacle']]
    print ("Wall states:", wallStates)
    
    def legal_position(row,col):
        # une position legale est dans la carte et pas sur un mur
        return ((row,col) not in wallStates) and row>=0 and row<nbLignes and col>=0 and col<nbCols
        
    #-------------------------------
    # Attributaion aleatoire des fioles 
    #-------------------------------
    
    objectifs = []
    objectifs.append(goalStates[1])
    objectifs.append(goalStates[0])
    #random.shuffle(objectifs)
    print("Objectif joueur 0", objectifs[0])
    print("Objectif joueur 1", objectifs[1])
    #-------------------------------
    # Carte demo 
    # 2 joueurs 
    # Joueur 0: A* indie
    # Joueur 1: A* indie
    #-------------------------------
    
    #-------------------------------
    # calcul A* pour le joueur 1
    #-------------------------------
    
    path = []
    
    g =np.ones((nbLignes,nbCols),dtype=bool)  # par defaut la matrice comprend des True  
    for w in wallStates:            # putting False for walls
        g[w]=False
    p = ProblemeGrid2D(initStates[0],objectifs[0],g,'manhattan')
    path.append(probleme.astar(p))

    p = ProblemeGrid2D(initStates[1],objectifs[1],g,'manhattan')
    path.append(probleme.astar(p))
        
    #-------------------------------
    # Boucle principale de déplacements 
    #-------------------------------
    
            
    posPlayers = initStates
    b = True
    for i in range(iterations):
        
        # on fait bouger chaque joueur séquentiellement
        
        # Joeur 0: A* inde
        numJ = 0
        
        if g[path[numJ][i]] == False: #quand le chemin est bloqué
            p = ProblemeGrid2D(posPlayers[numJ],objectifs[numJ],g,'manhattan') #re-creer un probleme
            path[numJ] = (path[numJ][:i-1]) + probleme.astar(p) #changer le chemin suivant

        g[posPlayers[numJ]] = True #liberer la case
        row,col = path[numJ][i]
        g[row,col] = False #occuper la case
        posPlayers[numJ]=(row,col)
        players[numJ].set_rowcol(row,col)

        print ("pos 0:", row,col)
        if (row,col) == objectifs[numJ]:
            score[numJ]+=1
            print("le joueur ",numJ," a atteint son but!")
            break
            

        # Joeur 1: A* inde
        numJ = 1

        if g[path[numJ][i]] == False:
            p = ProblemeGrid2D(posPlayers[numJ],objectifs[numJ],g,'manhattan')
            path[numJ] = (path[numJ][:i-1]) + probleme.astar(p)

        g[posPlayers[numJ]] = True
        row,col = path[numJ][i]
        g[row,col] = False
        posPlayers[numJ]=(row,col)
        players[numJ].set_rowcol(row,col)

        print ("pos 1:", row,col)
        if (row,col) == objectifs[numJ]:
            score[numJ]+=1
            print("le joueur ",numJ," a atteint son but!")
            break
         
        # on passe a l'iteration suivante du jeu
        game.mainiteration()

                
        
            
    
    print ("scores:", score)
    #time.sleep(100)
    #pygame.quit()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    
    
    
    #-------------------------------
    
    
        
    
    
        
   

 
    
   

if __name__ == '__main__':
    main()
    


