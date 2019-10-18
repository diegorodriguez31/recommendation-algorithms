#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# Filtrage collabortatif
# Coefficient de corrélation de rang de Spearman
import numpy as np
import csv
from math import sqrt
from math import fabs
from CentreUser import lecture_csv

"""Principe du coefficient de correlation de rang de Spearman : comparer deux viariables apres transformation de leurs realisations
en liste de rangs et dans une liste ordonnee selon une certaine relation d'ordre.
Ce coefficient de correlation est base sur la difference des rangs obtenus par les realisations sur les deux variables
On suppose que la relation entre les variables n'est pas lineaire
Le coefficient entre 2 variables est de 1 lorsque les 2 variables comparees ont une relation parfaitement monotone
C'est une alternative interessante au coefficient de Pearson
Il faut ordonner les rangs"""

#On recree le tableau du code centre user
donnees = lecture_csv()

#Calcul du coefficient de correlation de rang de Spearman
#Nous allons trier les rangs par un ordre de preference de film croissant

def coefficientCorrelationSpearman(user1, user2):
    L1 = []
    L2 = []
    for i in range(np.shape(donnees)[1]):
        if donnees[user1][i] != -1:
            L1.append(donnees[user1][i])
        if donnees[user2][i] != -1:
            L2.append(donnees[user2][i])
    for i in L1:
    return 1
