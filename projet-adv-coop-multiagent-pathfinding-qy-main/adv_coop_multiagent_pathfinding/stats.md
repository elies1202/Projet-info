Projet Path-Finding
3970770 Qingyuan YAO
Elies ZERROUKI

# Greedy best first
Les deux argents font greedy, mais un est coincé grace à la positionnement de la carte

# A* independant
## astarMap testé avec astarIndie.py
L'agent astarIndie a évité l'autre argent, il montre que astarIndie a réussi à recalculer le chemin 

# MiniMax avec AlphaBeta 
## MiniMax comparé avec AlphaBeta
3v3 & depth=3 & Manhattan dans exAdvCoopMap:
MiniMax pure: 31.5s
MiniMax avec AB: 6.16s

## AlphaBeta vs astarIndie 
### 2v2 & depth=2 & astar dans 2v2Map
AlphaBeta: 54.5 iterations
A* indie: 71.5 iterations

### 2v2 & depth=3 & astar dans 2v2Map
AlphaBeta: 49.5 iterations
A* indie: 60.5 iterations

### 2v2 & depth=2 & astar dans 2v2Map eval chemA*10
AlphaBeta: 35 iterations
A* indie: 41.5 iterations

Remarque: l'argent a plus d'intention de bloquer l'enemie  que celle d'avancer quand chemA et chemB sont calculé le même