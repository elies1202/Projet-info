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
    name = _boardname if _boardname is not None else '2v2Map'
    #name = _boardname if _boardname is not None else 'demoMap'
    game = Game('Cartes/' + name + '.json', SpriteBuilder)
    game.O = Ontology(True, 'SpriteSheet-32x32/tiny_spritesheet_ontology.csv')
    game.populate_sprite_names(game.O)
    game.fps = 5  # frames per second
    game.mainiteration()
    player = game.player
    
def main():
    startTime = time.time()
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
    offset = int(nbPlayers/2)
    score = [0]*nbPlayers
    depth = 2

    tmp = [[],[]]
    tmp[0] = players[:offset]
    tmp[1] = players[offset:]
    players = tmp 
       
           
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
    posPlayers = [[],[]]
    posPlayers[0] = initStates[:offset]
    posPlayers[1] = initStates[offset:]

    objectifs = [[],[]]
    objectifs[1] = goalStates[:offset]
    objectifs[0] = goalStates[offset:]
    print("Objectif Team 0", objectifs[0])
    print("Objectif Team 1", objectifs[1])

    print(posPlayers,objectifs)

    
    
    grid =np.ones((nbLignes,nbCols),dtype=bool)  # par defaut la matrice comprend des True  
    for w in wallStates:            # putting False for walls
        grid[w]=False

    path = []
    for i in range(len(posPlayers[1])):
        p = ProblemeGrid2D(posPlayers[1][i],objectifs[1][i],grid,'manhattan')
        path.append(probleme.astar(p))

    mm = probleme.MiniMax(posPlayers,objectifs,grid,depth,0)
        
    #-------------------------------
    # Boucle principale de déplacements 
    #-------------------------------


    for i in range(iterations):
        
        # on fait bouger chaque joueur séquentiellement

        # Team 0: MiniMax 
        numT = 0
        sol = mm.solve(mm.posPlayers.copy()+[],mm.grid.copy(),mm.depth,numT,-np.Infinity,+np.Infinity) #evaluer ensemble
        for numJ in range(len(sol)): #faire bouger à chaque player
            mm.grid[mm.posPlayers[numT][numJ]] = True
            row,col = sol[numJ]
            mm.grid[(row,col)] = False
            mm.posPlayers[numT][numJ] = (row,col)
            players[numT][numJ].set_rowcol(row,col)

            print ("T",numT,"P",numJ,":", row,col)
            if (row,col) == objectifs[numT][numJ] and score[numT*offset+numJ]==0:
                #score[numT*offset+numJ]+=int(time.time()-startTime)
                score[numT*offset+numJ]+=i
                print("T",numT,"P",numJ," a atteint son but!")
                #break

        
        # Team 1: A* inde
        numT = 1
        for numJ in range(len(mm.posPlayers[numT])):

            if i<len(path[numJ]):

                if grid[path[numJ][i]] == False:
                    p = ProblemeGrid2D(mm.posPlayers[numT][numJ],objectifs[numT][numJ],grid,'manhattan')
                    path[numJ] = (path[numJ][:i-1]) + probleme.astar(p)

                grid[mm.posPlayers[numT][numJ]] = True
                row,col = path[numJ][i]
                grid[row,col] = False
                mm.posPlayers[numT][numJ]=(row,col)
                players[numT][numJ].set_rowcol(row,col)

                print("T",numT,"P",numJ,":", row,col)
                if (row,col) == objectifs[numT][numJ] and score[numT*offset+numJ]==0:
                    #score[numT*offset+numJ]+=int(time.time()-startTime)
                    score[numT*offset+numJ]+=i
                    print("T",numT,"P",numJ," a atteint son but!")
                    #break       
        
        if(min(score)>0): break

        # on passe a l'iteration suivante du jeu
        game.mainiteration()           

    print ("scores:", score)
    #pygame.quit()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    
    
    
    #-------------------------------
    
    
        
    
    
        
   

 
    
   

if __name__ == '__main__':
    main()
    


