# -*- coding: utf-8 -*-

#####
# Abdel Néjib SOUMAILA 16 052 192
###

from pdb import set_trace as dbg  # Utiliser dbg() pour faire un break dans votre code.

import numpy as np


#
# AEtoileTuple : Classe représentant un tuple de TaquinEtat, score f et d'un parent AEtoileTuple.
#
class AEtoileTuple:

    def __init__(self, etat, f, parent=None):
        self.etat = etat
        self.f = f
        self.parent = parent

    # Fonction de comparaison entre deux AEtoileTuple.
    def __lt__(self, autre):
        return self.f < autre.f

    # Fonctions d'équivalence entre deux AEtoileTuple.
    def __eq__(self, autre):
        return self.etat == autre.etat

    def __ne__(self, autre):
        return not (self == autre)


#
# joueur_taquin : Fonction qui calcule le chemin, suite d'états, optimal afin de complété
#                  le puzzle.
#
# etat_depart: Objet de la classe TaquinEtat indiquant l'état initial du jeu.
#
# fct_estEtatFinal: Fonction qui prend en entrée un objet de la classe TaquinEtat et
#                   qui vérifie si l'état passée en paramêtre est l'état final ou non.
#
# fct_transitions: Fonction qui prend en entrée un objet de la classe TaquinEtat et
#                   qui retourne la listes des états voisins pour l'état donné.
#
# fct_heuristique: Fonction qui prend en entrée un objet de la classe TaquinEtat et
#                   qui retourne le coût heuristique pour se rendre à l'état final.
#z
# retour: Cette fonction retourne la liste des états de la solution triés en ordre chronologique
#          c'est-à-dire de l'état initial jusqu'à l'état final inclusivement.
#
def joueur_taquin(etat_depart, fct_estEtatFinal, fct_transitions, fct_heuristique):

    # TODO: Implémenter une recherche A*
    #déclarer deux nœuds: n, n’
    f = fct_heuristique(etat_depart)
    n = AEtoileTuple(etat_depart, f, None)
    final = AEtoileTuple(etat_depart, f, None)
    listetat= []

    #2. déclarer deux listes (open, closed): toutes  les deux sont  vide au départ
    open = []
    closed = []
    #3. insérer noeud Initial dans open
    open.append(n)

    #4. tant que(1) // la condition de sortie (exit) est déterminée dans la boucle
    while True:
                #5.si open est vide, sor + r de la boucle avec échec
                if not open:
                    print("echec ")
                    break

               # 6.n = nœud au début de open;
                n = open.pop(0)

                #7.enlever n de open et l’ajouter dans closed
                closed.append(n)

               # 8.si n est le but(goal(n) est true), sor + r de la boucle  avec succès en retournant le chemin;
                if fct_estEtatFinal(n.etat):
                    final = AEtoileTuple(n.etat, n.f, n.parent)
                    open.insert(0 ,final)
                    break
               # 9. pour chaque successeur n’ de n (chaque n’ appartenant à transitions(n))
                for nprime in fct_transitions(n.etat):
                    #10. ini + aliser la valeur g(n’) à g(n) + c(n, n’)
                    # f-h=g
                    g_n = n.f - fct_heuristique(n.etat)
                    g_nPrime = g_n + 1
                    #11. meNre le parent de n’ à n
                    nPrime = AEtoileTuple(nprime, fct_heuristique(nprime) + g_nPrime, n)
                    #12. si closed ou open con + ent un nœud n’’ égal à n’ avec f(n’) ≤ f(n’’)
                    if nPrime in closed or nPrime in open:

                        if (nPrime in closed) and nPrime.f < closed[closed.index(nPrime)].f: #a inverser
                            # 13. enlever n’’ de closed ou open et insérer n’ dans open (ordre croissant selon f(n))
                            closed.pop(closed.index(nPrime))
                            if not open:
                                open.append(nPrime)
                            else:
                                for elem in open:
                                    if nPrime.f < elem.f:
                                        open.insert(open.index(elem), nPrime)
                                        break
                            if EstInserer == False:
                                open.append(nPrime)
                                EstInserer = True

                        elif (nPrime in open) and nPrime.f < open[open.index(nPrime)].f:
                            # 13. enlever n’’ de closed ou open et insérer n’ dans open (ordre croissant selon f(n))
                            open.pop(open.index(nPrime))
                            EstInserer = False
                            if not open:
                                open.append(nPrime)
                            elif EstInserer == False:
                                for elem in open:
                                    if nPrime.f < elem.f:
                                        open.insert(open.index(elem), nPrime)
                                        EstInserer = True
                                        break
                            if EstInserer == False:
                                open.append(nPrime)
                                EstInserer = True

                    #14. si  n’ est ni dans open ni dans closed
                    if (nPrime not in open) and (nPrime not in closed):
                        # 15. insérer n’ dans open (ordre croissant selon f(n))
                        EstInserer= False
                        if not open:
                            open.append(nPrime)
                            EstInserer = True
                        elif EstInserer == False:
                            for elem in open:
                                if nPrime.f < elem.f:
                                    open.insert(open.index(elem), nPrime)
                                    EstInserer = True
                                    break
                        if EstInserer == False:
                            open.append(nPrime)
                            EstInserer = True

    listetat.append(final.etat)

    while True:
        if final.parent is not None:
            listetat.append(final.parent.etat)
            final = final.parent
        else:
            break

    listetat.reverse()


    return listetat