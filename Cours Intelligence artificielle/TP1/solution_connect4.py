# -*- coding: utf-8 -*-

#####
# VotreNom (VotreMatricule) .~= À MODIFIER =~.
###

from pdb import set_trace as dbg  # Utiliser dbg() pour faire un break dans votre code.

import random
import numpy as np
import time


#
# joueur_connect4 : Fonction qui calcule le prochain coup optimal pour gagner la
#                    la partie de Connect4 à l'aide d'Alpha-Beta Prunning.
#
# etat: Objet de la classe Connect4Etat indiquant l'état actuel du jeu.
#
# fct_but: Fonction qui prend en entrée un objet de la classe Connect4Etat et
#          qui retourne le score actuel tu plateau. Si le score est positif, les 'X' ont l'avantage
#          si c'est négatif ce sont les 'O' qui ont l'avantage, si c'est 0 la partie est nulle.
#
# fct_transitions: Fonction qui prend en entrée un objet de la classe Connect4Etat et
#                   qui retourne une liste de tuples actions-états voisins pour l'état donné.
#
# str_joueur: String indiquant c'est à qui de jouer : les 'X' ou 'O'.
#
# int_tempsMaximal: Entier indiquant le temps, en secondes, alloué pour prendre une décision.
#
# retour: Cette fonction retourne l'action optimal à joeur pour le joueur actuel c.-à-d. 'str_joueur'.
#

def joueur_connect4(etat, fct_but, fct_transitions, str_joueur, int_tempsMaximal):

    # TODO: Implémenter un joueur alpha-beta

    # Retourne une action aléatoire (.~= À MODIFIER =~.)
    action = random.choice(list(fct_transitions(etat)))
    return action
