# -*- coding: utf-8 -*-

#####
# ABDEL NEJIB SOUMAILA 16 052 192
###

from pdb import set_trace as dbg  # Utiliser dbg() pour faire un break dans votre code.

import numpy as np


class Correcteur:
    def __init__(self, p_init, p_transition, p_observation, int2letters, letters2int):
        '''Correcteur de frappes dans un mot.

        Modèle de Markov caché (HMM) permettant de corriger les erreurs de frappes
        dans un mot. La correction est dictée par l'inférence de l'explication
        la plus pausible du modèle.

        Parameters
        ------------
        p_init : array-like shape (N,)
                 Probabilités initiales de l'état caché à la première position.

        p_transition : array-like shape (X,Y)
                       Modèle de transition.

        p_observation : array-like shape (X,Y)
                        Modèle d'observation.

        int2letters : list
                      Associe un entier (l'indice) à une lettre.

        letters2int : dict
                      Associe une lettre (clé) à un entier (valeur).
        '''
        self.p_init = p_init
        self.p_transition = p_transition
        self.p_observation = p_observation
        self.int2letters = int2letters
        self.letters2int = letters2int

        '''Corrige les frappes dans un mot.

        Retourne la correction du mot donné et la probabilité p(mot, mot corrigé).

        Parameters
        ------------
        mot : string
              Mot à corriger.

        Returns
        -----------
        mot_corrige : string
                      Le mot corrigé.

        prob : float
               Probabilité dans le HMM du mot observé et du mot corrigé.
               C'est-à-dire 'p(mot, mot_corrige)'.
        '''

    def corrige(self, mot):

        alphabet = 26
        a_etoile = np.zeros((alphabet, len(mot)))
        # on store l'index des maximums choisis
        table_max = np.zeros((alphabet, len(mot)))
        # init: a_etoile(i, 1) = P(S1=s1, H1=i)	= P(S1=s1 |	H1=i) P(H1=i)
        value = np.multiply(self.p_observation[self.letters2int[mot[0]]], self.p_init)
        a_etoile[:, 0] = value

        # loop  matrice 2D transposée a_etoile
        for (t, i), v in np.ndenumerate(a_etoile.T):
            if t == 0:
                continue
            else:
                # colonne-1 * ligne[i]
                list = np.multiply(a_etoile[:, t - 1], self.p_transition[i])
                max_index = np.argmax(list)
                table_max[i, t] = max_index
                # P(St+1=st+1 | Ht+1=i) maxjP(Ht+1=i | Ht=j) α*(j,t)
                a_etoile[i, t] = self.p_observation[self.letters2int[mot[t]], i] * list[max_index]

        index = np.argmax(a_etoile[:, len(mot) - 1])
        probabilite = a_etoile[index, (len(mot) - 1)]
        compteur = len(mot) - 1
        x = 0
        list_pair = [(index, len(mot) - 1)]
        while x <= (len(mot) - 2):
            value = table_max[index, compteur]
            pair = (value, compteur - 1)
            list_pair.append(pair)
            index = int(pair[0])
            compteur -= 1
            x += 1
        list_pair.reverse()
        mot_corrige = ""
        for each in list_pair:
            mot_corrige += str(self.int2letters[int(each[0])])

        return mot_corrige, probabilite
