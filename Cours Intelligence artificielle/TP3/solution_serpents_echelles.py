# -*- coding: utf-8 -*-

#####
# ABDEL-NEJIB SOUMAILA 16 052 192
###

from pdb import set_trace as dbg  # Utiliser dbg() pour faire un break dans votre code.
from typing import Dict, Any

import numpy as np


#################################
# Solution serpents et échelles #
#################################

#####
# calcul_valeur: Fonction qui retourne le tableau de valeurs d'un plan (politique).
#
# mdp: Spécification du processus de décision markovien (objet de la classe SerpentsEchelles, héritant de MDP).
#
# plan: Un plan donnant l'action associée à chaque état possible (dictionnaire).
#
# retour: Un tableau Numpy 1D de float donnant la valeur de chaque état du mdp, selon leur ordre dans mdp.etats.
### 
def calcul_valeur(mdp, plan):
    A = -np.identity(len(mdp.etats))
    B = np.zeros(len(mdp.etats))

    for s in mdp.etats:
        B[s] = -mdp.recompenses[s]
        dictionnaire = mdp.modele_transition[(s, plan[s])]
        for etat_possible, Prob in dictionnaire:
            droit = Prob * mdp.escompte
            A[s][etat_possible] = A[s][etat_possible] + droit

    A_inv = np.linalg.inv(A)
    valeur = np.dot(A_inv, B)

    return valeur


#####
# calcul_plan: Fonction qui retourne un plan à partir d'un tableau de valeurs.
#
# mdp: Spécification du processus de décision markovien (objet de la classe SerpentsEchelles, héritant de MDP).
#
# valeur: Un tableau de valeurs pour chaque état (tableau Numpy 1D de float).
#
# retour: Un plan (dictionnaire) qui maximise la valeur future espérée, en fonction du tableau "valeur".
### 
def calcul_plan(mdp, valeur):
    plan = dict()
    for s in mdp.etats:
        val = 0
        for a in mdp.actions[s]:
            z = mdp.modele_transition[(s, a)]
            somme = 0
            for etat_possible, Prob in z:
                somme += (Prob * valeur[etat_possible])
            val2 = mdp.recompenses[s] + (mdp.escompte * (somme))
            if val2 > val:
                val = val2
                plan.update({s: str(a)})

    return plan


#####
# iteration_politiques: Algorithme d'itération par politiques, qui retourne le plan optimal et sa valeur.
#
# plan_initial: Le plan à utiliser pour initialiser l'algorithme d'itération par politiques.
#
# retour: Un tuple contenant le plan optimal et son tableau de valeurs.
### 
def iteration_politiques(mdp, plan_initial):
    pi_prime = plan_initial
    pi = None
    valeur = None
    while pi != pi_prime:
        pi = pi_prime
        valeur = calcul_valeur(mdp, pi_prime)

        pi_prime = calcul_plan(mdp, valeur)
        valeur_2 = calcul_valeur(mdp, pi_prime)
        for index, x in np.ndenumerate(valeur):
            if valeur_2[index] > valeur[index]:
                valeur[index] = valeur_2[index]

    return pi_prime, valeur
