# -*- coding: utf-8 -*-

#####
# ABDEL-NEJIB SOUMAILA 16 052 192
###

from pdb import set_trace as dbg  # Utiliser dbg() pour faire un break dans votre code.

import numpy as np


def logistic(x):
    return 1. / (1. + np.exp(-x))


class ReseauDeNeurones:

    def __init__(self, alpha, T):
        self.alpha = alpha
        self.T = T

    def initialisation(self, W, w):
        self.W = W
        self.w = w

    def parametres(self):
        return (self.W, self.w)

    def prediction(self, x):
        # pour noued i dans L:
        ai = x
        # pour noeud j dans L:
        aj = np.zeros(self.W.shape[0])

        for j in range(self.W.shape[0]):
            # inj = sumi(Wij*ai)
            inj = sum(self.W[j] * ai)
            lo = logistic(inj)
            aj[j] = lo

        inf = sum(self.w * aj)
        # aj = g(inj)
        assort = logistic(inf)

        if round(assort, 1) >= 0.49999:
            return 1
        else:
            return 0

    def mise_a_jour(self, x, y):
        # pour noued i dans L:
        ai = x
        # pour noeud j dans L:
        aj = np.zeros(self.W.shape[0])

        for j in range(self.W.shape[0]):
            # inj = sumi(Wij*ai)
            inj = sum(self.W[j] * ai)
            lo = logistic(inj)
            aj[j] = lo

        inf = sum(self.w * aj)
        # aj = g(inj)
        assort = logistic(inf)

        # noeud j:
        deltaSortie = y - assort
        # noued I:
        deltaj = np.zeros(aj.shape)
        for index, gini in enumerate(aj):
            deltaj[index] = gini * (1 - gini) * self.w[index] * deltaSortie
        # pour chque poids dans le reseau:
        for index, Wij in np.ndenumerate(self.W):
            self.W[index[0], index[1]] = Wij + self.alpha * ai[index[1]] * deltaj[index[0]]
        for index, wij in enumerate(self.w):
            self.w[index] = wij + self.alpha * aj[index] * deltaSortie
        pass

    def entrainement(self, X, Y):
        boucle = 0
        while boucle != self.T:
            # chaque x,y dans example
            for i in range(X.shape[0]):
                x = X[i]
                y = Y[i]
                self.mise_a_jour(x, y)
            boucle += 1

        pass
        pass
