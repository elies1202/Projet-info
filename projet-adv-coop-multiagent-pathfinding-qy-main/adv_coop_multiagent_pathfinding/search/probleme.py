# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 09:32:05 2016

@author: nicolas
"""

import numpy as np
import copy
import heapq
from abc import ABCMeta, abstractmethod
import functools
import time
import math
import search.grid2D as gp


def distManhattan(p1,p2):
    """ calcule la distance de Manhattan entre le tuple 
        p1 et le tuple p2
        """
    (x1,y1)=p1
    (x2,y2)=p2
    return abs(x1-x2)+abs(y1-y2) 



    
###############################################################################

class Probleme(object):
    """ On definit un probleme comme étant: 
        - un état initial
        - un état but
        - une heuristique
        """
        
    def __init__(self,init,but,heuristique):
        self.init=init
        self.but=but
        self.heuristique=heuristique
        
    @abstractmethod
    def estBut(self,e):
        """ retourne vrai si l'état e est un état but
            """
        pass
        
    @abstractmethod    
    def cost(self,e1,e2):
        """ donne le cout d'une action entre e1 et e2, 
            """
        pass
        
    @abstractmethod
    def successeurs(self,etat):
        """ retourne une liste avec les successeurs possibles
            """
        pass
        
    @abstractmethod
    def immatriculation(self,etat):
        """ génère une chaine permettant d'identifier un état de manière unique
            """
        pass


###############################################################################

@functools.total_ordering # to provide comparison of nodes
class Noeud:
    def __init__(self, etat, g, pere=None):
        self.etat = etat
        self.g = g
        self.pere = pere
        
    def __str__(self):
        #return np.array_str(self.etat) + "valeur=" + str(self.g)
        return str(self.etat) + " valeur=" + str(self.g)
        
    def __eq__(self, other):
        return str(self) == str(other)
        
    def __lt__(self, other):
        return str(self) < str(other)
        
    def expand(self,p):
        """ étend un noeud avec ces fils
            pour un probleme de taquin p donné
            """
        nouveaux_fils = [Noeud(s,self.g+p.cost(self.etat,s),self) for s in p.successeurs(self.etat)]
        return nouveaux_fils
        
    def expandNext(self,p,k):
        """ étend un noeud unique, le k-ième fils du noeud n
            ou liste vide si plus de noeud à étendre
            """
        nouveaux_fils = self.expand(p)
        if len(nouveaux_fils)<k: 
            return []
        else: 
            return self.expand(p)[k-1]
            
    def trace(self,p):
        """ affiche tous les ancetres du noeud
            """
        n = self
        c=0    
        while n!=None :
            print (n)
            n = n.pere
            c+=1
        print ("Nombre d'étapes de la solution:", c-1)
        return            
        
        
###############################################################################
# A*
###############################################################################

def astar(p,verbose=False,stepwise=False):
    """
    application de l'algorithme a-star
    sur un probleme donné
        """
        
    startTime = time.time()

    nodeInit = Noeud(p.init,0,None)
    frontiere = [(nodeInit.g+p.h_value(nodeInit.etat,p.but),nodeInit)] 

    reserve = {}        
    bestNoeud = nodeInit
    
    while frontiere != [] and not p.estBut(bestNoeud.etat):              
        (min_f,bestNoeud) = heapq.heappop(frontiere)
           
    # VERSION 1 --- On suppose qu'un noeud en réserve n'est jamais ré-étendu
    # Hypothèse de consistence de l'heuristique        
        
        if p.immatriculation(bestNoeud.etat) not in reserve:            
            reserve[p.immatriculation(bestNoeud.etat)] = bestNoeud.g #maj de reserve
            nouveauxNoeuds = bestNoeud.expand(p)
            for n in nouveauxNoeuds:
                f = n.g+p.h_value(n.etat,p.but)
                heapq.heappush(frontiere, (f,n))

    # TODO: VERSION 2 --- Un noeud en réserve peut revenir dans la frontière        
        
        stop_stepwise=""
        if stepwise==True:
            stop_stepwise = input("Press Enter to continue (s to stop)...")
            print ("best", min_f, "\n", bestNoeud)
            print ("Frontière: \n", frontiere)
            print ("Réserve:", reserve)
            if stop_stepwise=="s":
                stepwise=False
    
            
    # Mode verbose            
    # Affichage des statistiques (approximatives) de recherche   
    # et les differents etats jusqu'au but
    if verbose:
        bestNoeud.trace(p)          
        print ("=------------------------------=")
        print ("Nombre de noeuds explorés", len(reserve))
        c=0
        for (f,n) in frontiere:
            if p.immatriculation(n.etat) not in reserve:
                c+=1
        print ("Nombre de noeuds de la frontière", c)
        print ("Nombre de noeuds en mémoire:", c + len(reserve))
        print ("temps de calcul:", time.time() - startTime)
        print ("=------------------------------=")
     
    n=bestNoeud
    path = []
    while n!=None :
        path.append(n.etat)
        n = n.pere
    if len(path[::-1])==0: return [p.init]
    return path[::-1] # extended slice notation to reverse list


###############################################################################
#greedy
###############################################################################
def greedy(but,x,y):
    droite = x + 1 , y
    gauche =  x - 1, y 
    haut = x, y - 1
    bas =  x, y + 1
    reste = x, y
    direction = ["droite", "gauche", "haut", "bas", "reste"]
    liste_direction = [droite, gauche, haut, bas, reste]
    listeDistance = [distManhattan(but, droite), distManhattan(but, gauche), distManhattan(but, haut), distManhattan(but, bas), distManhattan(but, reste)]
    LongueurMax = max(listeDistance) + 1 
    res = [0]*5
    tour = 0  
  
    while tour != len(liste_direction):
        LongueurMin = LongueurMax
        for i in range(0, len(listeDistance)):
            if listeDistance[i] < LongueurMin:
                LongueurMin = listeDistance[i]
                n =  i

        listeDistance[n] = LongueurMax         
        res[tour] = liste_direction[n]
        tour = tour +1
        print(direction[n])

    return res
###############################################################################
#MiniMax
###############################################################################

class MiniMax:
    def __init__(self, posPlayers, objectifs, grid, depth, numT):
        self.posPlayers = posPlayers
        self.objectifs = objectifs
        self.grid = grid
        self.numT = numT
        self.depth = depth

    #l'algo minimax, fonction recursive
    def solve(self, pos3, grid, depth, numT, alpha, beta):
        if depth==0: #si arriver au profondeur max
            #structure dict: {((pos de notre equipe) , (pos de enemie) , (pos de notre equipe en 1er profondeur)) : S calculé}
            return {(tuple(pos3[0]),tuple(pos3[1]),tuple(pos3[2])) : (self.eval(pos3,grid))}
        else:
            nodes = self.get_variations(0,pos3[numT],self.objectifs[numT],grid)
            if numT==self.numT:  out = {((),(),()) : -np.Infinity}
            else: out = {((),(),()) : +np.Infinity} #simuler la structure de retourne

            for n in nodes:
                #Collision update
                gridcopy = grid.copy() #copier le grid pour malipuler dans chaque variations
                for pos in pos3[0]+pos3[1]:
                    gridcopy[pos] = True

                tab = [[],[],[]] #preparer la strcture du argument pos3
                tab[numT] = n
                tab[(numT+1)%2] = pos3[(numT+1)%2]
                if depth==self.depth: #garder toujours pos de numT du premier profondeur (pour retourner)
                    tab[2] = n
                else: tab[2] = pos3[2]
                
                for pos in tab[0]+tab[1]:  #Collision update
                    gridcopy[pos] = False

                eval = self.solve(tab,gridcopy,depth-1,(numT+1)%2,alpha,beta) #fonction recursive

                #Max 
                if numT==self.numT: 
                    if(list(eval.values())[0]>list(out.values())[0]):
                        out = eval
                    if(list(eval.values())[0]>alpha):
                        alpha = list(eval.values())[0]
                    if beta <= alpha: break #pas besoins de calculer le reste
                #Min
                else:
                    if(list(eval.values())[0]<list(out.values())[0]):
                        out = eval
                    if(list(eval.values())[0]<beta):
                        beta = list(eval.values())[0]
                    if beta <= alpha: break

            #si premier profondeur, preparer a retourner le resultat
            if depth==self.depth: return list(out)[0][2]
            #sinon, sortir de ce profondeur
            return out 

    # S = (1000 x nombre d'objectifs de A 
    # + somme des chemins de B à leurs objectifs) 
    # - (1000 x nombre d'objectifs de B 
    # + somme des chemins de A*10 à leurs objectifs).

    #Calculer S
    def eval(self,posPlayers,grid):
        chemA = 0
        chemB = 0
        numT = self.numT
        numE = (1+numT)%2

        #myself
        for i in range(len(posPlayers[numT])):
            if posPlayers[numT][i] != self.objectifs[numT][i]:
                p = gp.ProblemeGrid2D(posPlayers[numT][i],self.objectifs[numT][i],grid,'manhattan')
                chem =  astar(p)
                if chem == [posPlayers[numT][i]]: chemA += 400
                chemA += len(astar(p))*10  #fois 10 pour que l'argent a moins d'intention de "defendre"
                
                #une autre version de chemin, avec distManhattan, pas precis
                #chemA += distManhattan(posPlayers[numT][i],self.objectifs[numT][i])

        #enemie
        for i in range(len(posPlayers[numE])):
            if posPlayers[numE][i] != self.objectifs[numE][i]:
                p = gp.ProblemeGrid2D(posPlayers[numE][i],self.objectifs[numE][i],grid,'manhattan')
                chem =  astar(p)
                if chem == [posPlayers[numT][i]]: chemB += 400
                chemB += len(astar(p))

                #chemB += distManhattan(posPlayers[numE][i],self.objectifs[numE][i])

        return (1000*len(posPlayers[0]) - 1000*len(posPlayers[1]) + chemB - chemA)

    #Generer toutes les variations possibles (fonction recursive)
    def get_variations(self, currentJ, posPlayers,objectifs, grid):
        #if non leaf
        if currentJ < len(posPlayers): #currentJ sers comme le profondeur
            out = []
            if posPlayers[currentJ]==objectifs[currentJ]: #si deja le but, continuer sans bouger
                successeurs = [posPlayers[currentJ]]
            else: #else, calculer successeurs a l'aide de probleme
                p = gp.ProblemeGrid2D(posPlayers[currentJ],objectifs[currentJ],grid,"manhattan")
                successeurs = p.successeurs(posPlayers[currentJ])

            for node in successeurs:
                gridcopy = grid.copy() #copier le grid pour avoir des variations
                gridcopy[posPlayers[currentJ]] = True #update collision
                tmp = posPlayers.copy() #copier le pos pour avoir des variations 
                tmp[currentJ] = node
                gridcopy[tmp[currentJ]] = False
                out += self.get_variations(currentJ+1, tmp,objectifs,gridcopy) #recursive
            return out

        #leaf, on arrive au dernier player
        else: return [posPlayers.copy()]

