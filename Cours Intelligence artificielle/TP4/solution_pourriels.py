# -*- coding: utf-8 -*-

#####
# ABDEL-NEJIB SOUMAILA 16 052 192
###

from pdb import set_trace as dbg  # Utiliser dbg() pour faire un break dans votre code.

from collections import defaultdict

import numpy as np
import re
import math


# Probabilite: Classe permettant de modéliser les distributions P(C) et P(W|C).
#              Pour ce faire, les dictionnaires 'nbMotsParClasse', 'nbDocsParClasse',
#              'freqWC' doivent être remplis lors de la phase d'entraînement. La variable
#              membre vocabulaire sera automatique affectée après l'appel de la fonction
#              creerVocabulaire, vous n'avez donc pas à la modifiée.
#
#              Au final, lors de la prédiction, P, un objet de la classe 'Probabilite',
#              peut être appelé directement de cette façon : P(C=0) ou bien
#              P(W='allo',C=0,delta=1).
#
class Probabilite():

    def __init__(self):
        # Nb. de mots total dans les documents de la catégorie c.
        self.nbMotsParClasse = defaultdict(lambda: 0.)

        # Nb. de documents de la catégorie c.
        self.nbDocsParClasse = defaultdict(lambda: 0.)

        # Nb. de fois que le mot w apparaît dans les documents de la catégorie c.
        self.freqWC = defaultdict(lambda: 0.)

        # Vocabulaire des mots contenus dans tous les documents.
        self.vocabulaire = []

    def probClasse(self, C):
        return self.nbDocsParClasse[C]/(self.nbDocsParClasse[0]+self.nbDocsParClasse[1])

    def probMotEtantDonneClasse(self, C, W, delta):
        return (delta+self.freqWC[(W, C)])/((delta*(len(self.vocabulaire)+1))+self.nbMotsParClasse[C])

    def __call__(self, C, W=None, delta=None):
        if W is None:
            return self.probClasse(C)

        return self.probMotEtantDonneClasse(C, W, delta)


# creerVocabulaire: Fonction qui s'occupe de créer une liste (i.e. un vocabulaire)
#                   des mots fréquents dans le corpus. Un mot est fréquent s'il
#                   apparaît au moins 'seuil' fois.
#
# documents: Liste de string représentant chacune le contenu d'un courriel.
#
# seuil: Fréquence minimale d'un mot pour qu'il puisse faire parti du vocabulaire.
#
# retour: Un 'set' contenant l'ensemble des mots ('str') du vocabulaire.
#
def creerVocabulaire(documents, seuil):
    # creation du dictionnaire
    dico = defaultdict(int)
    # creation du set vocabulaire de retour
    vocabulaire = set()

    for doc in documents:
        for mot in doc.split():
            dico[mot] += 1

    for key, value in dico.items():
        if value >= seuil:
            vocabulaire.add(key)

    return vocabulaire


# pretraiter: Fonction qui remplace les mots qui ne font pas parti du vocabulaire
#             par le token 'OOV'.
#
# doc: Un document représenté sous la forme d'une string.
#
# V: Vocabulaire représenté par un 'set' de mots ('str').
#
# retour: Une 'list' des mots contenu dans le document et présent dans le vocabulaire.
#
def pretraiter(doc, V):
    # cretation liste
    liste = doc.split()

    for mot in liste:
        if mot not in V:
            for i, j in enumerate(liste):
                if j == mot:
                    liste[i] = 'OOV'

    return liste


# entrainer: Fonction permettant d'entraîner les distributions P(C) et P(W|C)
#            à partir d'un ensemble de courriels.
#
# corpus: Liste de tuples, où chaque tuple est composé d'une liste de
#         mots (i.e. document prétraité) et un entier indiquant la
#         classe (0:SPAM,1:HAM). Par exemple,
#         corpus == [..., (["Mon", "courriel", "..."], 1), ...]
#
# P: Objet de la classe Probabilite qui doit être modifié directement (Référence!)
#
# retour: Rien! L'objet P doit être modifié via ses dictionnaires.
#
def entrainer(corpus, P):
    for current_tuple in corpus:
        mots, c = current_tuple

        P.nbMotsParClasse[c] += len(mots)
        P.nbDocsParClasse[c] += 1

        # incrementation frequence apparition mot
        for mot in mots:
            P.freqWC[(mot, c)] += 1


# predire: Fonction utilisée pour trouver la classe la plus probable à quelle
#          appartient le document d à partir des distribution P(C) et P(W|C).
#
# doc: Un document représenté sous la forme d'une 'list' de mots ('str').
#
# P: Objet de la classe Probabilite.
#
# C: Liste des classes possibles (0:SPAM,1:HAM)
#
# delta: Paramètre utilisé pour le lissage.
#
# retour: Un tuple (int,float) où l'entier désigne la classe la plus probable
#         du document et le nombre à virgule est la log-probabilité conjointe
#         d'un document D=[w_1,...,w_d] et de catégorie c, i.e. P(C=c,D=[w_1,...,w_d]). *N'oubliez pas vos logarithmes!
#
def predire(doc, P, C, delta):
    prob_log = float("-inf")
    classe = None

    for current_c in C:
        # init (float)
        valeur = 0.0
        for mot in doc:
            # calcul de la valeur
            valeur += math.log(P.probMotEtantDonneClasse(current_c, mot, delta))

        # calcul candidat
        candidat = math.log(P.probClasse(current_c)) + valeur
        if candidat > prob_log:
            # on mets la classe a lavaleur du P(C) courant
            classe = current_c
            prob_log = candidat

    return classe, prob_log
