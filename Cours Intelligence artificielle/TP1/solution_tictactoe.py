# -*- coding: utf-8 -*-

#####
# Abdel Néjib SOUMAILA 16 052 192
###

from pdb import set_trace as dbg  # Utiliser dbg() pour faire un break dans votre code.

import random
import numpy as np

########################
# Solution tic-tac-toe #
########################

#####
# joueur_tictactoe : Fonction qui calcule le prochain coup optimal pour gagner la
#                     la partie de Tic-tac-toe à l'aide d'Alpha-Beta Prunning.
#
# etat: Objet de la classe TicTacToeEtat indiquant l'état actuel du jeu.
#
# fct_but: Fonction qui prend en entrée un objet de la classe TicTacToeEtat et
#          qui retourne le score actuel tu plateau. Si le score est positif, les 'X' ont l'avantage
#          si c'est négatif ce sont les 'O' qui ont l'avantage, si c'est 0 la partie est nulle.
#
# fct_transitions: Fonction qui prend en entrée un objet de la classe TicTacToeEtat et
#                   qui retourne une liste de tuples actions-états voisins pour l'état donné.
#
# str_joueur: String indiquant c'est à qui de jouer : les 'X' ou 'O'.
#
# retour: Cette fonction retourne l'action optimal à joeur pour le joueur actuel c.-à-d. 'str_joueur'.
###
def joueur_tictactoe(etat,fct_but,fct_transitions,str_joueur):

    def elegage_alpha_beta(noeudInitial):
        if str_joueur == 'X':
            util, action = tour_max(noeudInitial, -np.inf, np.inf)
        elif str_joueur == 'O':
            util, action = tour_min(noeudInitial, -np.inf, np.inf)
        return action

    def tour_max(n, alpha, beta):
        # 1. si n correspond a une fin de partie, alors retourner utilité(n)
        if fct_but(n) is not None:
            return fct_but(n), None

        # 2. u=-infinie, a= void
        u = -np.inf
        a = None

        # 3. pour chaque paire(a_prime, n_prime) donnée par transition(n)
        for action, nouvel_etat in fct_transitions(n).items():
            # 4. si l'utilité de tour_min(n_prime, alpha, beta) > u alors affecter a = a_prime, u = utilité de tour_min(n_prime, alpha, beta)
            util, act = tour_min(nouvel_etat, alpha, beta)
            if util > u:
                a = action
                u = util

            # 5. si u >= beta alors retourne l'utilité u l'action a
            if u >= beta:
                return u, a
            # 6. alpha= max(alpha, u )
            alpha = max(alpha, u)
        # 4. retourne l'utilité u et l'action alpha
        return u, a

    def tour_min(n, alpha, beta):
        # 1. si n correspond a une fin de partie, alors retourner utilité(n)
        if fct_but(n) is not None:
            return fct_but(n), None
        # 2. u= infinie, a= void
        u = np.inf
        a = None
        # 3. pour chaque paire(a_prime, n_prime) donnee par transition(n)
        for action, nouvel_etat in fct_transitions(n).items():
            # 4. si l'utilité de tour_max(n_prime, alpha, beta) < u alors affecter a= a_prime, u= utilité de tour_max(n_prime, alpha, beta)
            util, act = tour_max(nouvel_etat, alpha, beta)
            if util < u:
                a = action
                u = util
            # 5. si u<= alpha alors retourne l'utilité u et l'action a
            if u <= alpha:
                return u, a
            # 6. beta= min(beta, u)
            beta = min(beta, u)
        # 4. retourne l'utilité u et l'action a
        return u, a

    action = elegage_alpha_beta(etat)
    return action