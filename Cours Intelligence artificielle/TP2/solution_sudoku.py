# -*- coding: utf-8 -*-

#####
# Abdel Néjib SOUMAILA 16 052 192
###

from pdb import set_trace as dbg  # Utiliser dbg() pour faire un break dans votre code.

import numpy as np


#####
# reviser: Fonction utilisée par AC3 afin de réduire le domaine de Xi en fonction des contraintes de Xj.
#
# Xi: Variable (tuple (Y,X)) dont ses domaines seront réduit, si possible.
#
# Xj: Variable (tuple (Y,X)) dont ses domaines seront réduit, si possible.
#
# csp: Objet de la classe CSP contenant tous les informations relative aux problème
#      de satisfaction de contraintes pour une grille de Sudoku.
#      Pour plus d'information, voir doc de la fonction 'backtracking_search'.
#
# retour: Un tuple contenant un booléen indiquant si il y a eu des changements et le csp.
###
def reviser(Xi, Xj, csp):
    # 1 changé=faux
    change = False
    # 2 pour chaque x dans DOMAINE(Xi, csp)
    for x in csp.domaines[Xi]:
        crit = False
        for y in csp.domaines[Xj]:
            if y != x:
                crit = True
                break
                #           4 enlever x de DOMAI NE(Xi, csp)
        if not crit:
            csp.domaines[Xi].remove(x)
                #           5 changé= vrai
            change = True
    # 6 retourner changé, csp
    return change, csp


#####
# AC3: Fonction s'occupant de réduire les domaines des variables selon l'algorithme AC3.
#
# csp: Objet de la classe CSP contenant tous les informations relative aux problème
#      de satisfaction de contraintes pour une grille de Sudoku.
#      Pour plus d'information, voir doc de la fonction 'backtracking_search'.
#
# retour: Un tuple contenant le csp optimisé et un booléen indiquant si aucune contrainte n'est violée.
###
def AC3(csp):
    # 1 file_arcs= ARCS-DI-CSP(csp)
    file_arcs = csp.arcs()
    # 2 tant que file_arcs n est pas vide
    while file_arcs:
        #   3 (Xi, Xj) = pop(file_arc)
        (Xi, Xj) = file_arcs.pop()
        #   4 change, csp = REVISER(Xi, Xj, csp)


        change, csp = reviser(Xi, Xj, csp)
        #   5 si changé
        if change:
            #       6 si DOMAINE(Xj, csp) est vide, retourner (void, faux)
            if not csp.domaines[Xi]:
                return None, False
            #       7 pour chaque Xk dans VOISINS (Xi,csp) ?????????????
            for Xk in csp.contraintes[Xi]:
                #           8 si Xk n'egale pas Xj, ajouter (Xk,Xi) dans file_arcs
                if Xk != Xj:
                    file_arcs.append((Xk, Xi))
    # 3 retourner (csp, vrai)
    return csp, True


#####
# est_compatible: Fonction vérifiant la légalité d'une affectation.
#
# X: Tuple contenant la position en y et en x de la case concernée par l'affectation.
#
# v: String représentant la valeur (entre [1-9]) concernée par l'affectation.
#
# assignations: dict mappant les cases (tuple (Y,X)) vides à une valeur.
#
# csp: Objet de la classe CSP contenant tous les informations relative aux problème
#      de satisfaction de contraintes pour une grille de Sudoku.
#      Pour plus d'information, voir doc de la fonction 'backtracking_search'.
#
# retour: Un booléean indiquant si l'affectation de la valeur v à la case X est légale.
###
def est_compatible(X, v, assignations, csp):
    # si l'assignation aucune contrainte n'Est violée
    for x in csp.contraintes[X]:
        if x in assignations:
            if assignations[x] == v:
                return False

    return True


#####
# backtrack : Fonction s'occupant de trouver les assignations manquantes de la grille de Sudoku
#             en utilisant l'algorithme de Backtracking Search.
#
# assignations: dict mappant les cases (tuple (Y,X)) vides à une valeur.
#
# csp: Objet de la classe CSP contenant tous les informations relative aux problème
#      de satisfaction de contraintes pour une grille de Sudoku.
#      Pour plus d'information, voir doc de la fonction 'backtracking_search'.
#
# retour: Le dictionnaire des assignations (case => valeur)
###
def backtrack(assignations, csp):
    # 1. si assignation est complete, retourner assignation
    if len(assignations) == (9 * 9):
        return assignations
    # 2 X= var-non-assignée(assignation, csp)
    X = var_non_assignée(assignations, csp)
    # 3 pour chaque v dans  valeurs-ordonnées(X, assignation, csp)
    for v in csp.domaines[X]:
        #     4 si compatible(x=v, assignation, csp)
        if est_compatible(X, v, assignations, csp):
            #           5 ajouter x=v a assignation
            assignations.update({X: v})
            #           6 csp_etoile= csp mais wayen DOMAINE(x, csp) est  {v}
            csp_etoile = csp.copy()
            csp_etoile.domaines[X] = [v]
            #           7 csp_etoile, ok = inference(csp_etoile)
            csp_etoile, ok = AC3(csp_etoile)
            #           8 si ok= vrai
            if ok:
                #               9  resultat= BACKTRACK(assignation, csp_etoile)
                resultat = backtrack(assignations, csp_etoile)
                #               10 si resultat n'est pas faux, retourner resultat
                if resultat is not False:
                    return resultat
            #           enlever x=v de assignation
            del assignations[X]
        # 12 retourner faux
    return False


#####
# backtracking_search : Fonction coquille pour la fonction 'backtrack'.
#
# csp: Objet de la classe CSP contenant tous les informations relative aux problème
#      de satisfaction de contraintes pour une grille de Sudoku. Les variables membres sont
#      'variables'   : list de cases (tuple (Y,X)) vides
#      'domaines'    : dict mappant une case à une liste des valeurs possibles
#      'contraintes' : dict mappant une case à une liste de cases dont leur valeur doivent être différentes
#
# retour: Le dictionnaire des assignations (case => valeur)
###
def backtracking_search(csp):
    return backtrack({}, csp)


def var_non_assignée(assignations, csp):
    for x in csp.variables:
        if x in assignations:
            continue
        else:
            return x

    return None
