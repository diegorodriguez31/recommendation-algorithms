#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# Filtrage collabortatif
import numpy as np
from math import sqrt
from math import fabs
from math import acos
from CentreUser import lecture_csv

donnees = lecture_csv()

"""There have been several other similarity measures used in the literature, including Spearman rank
correlation, Kendall’s τ correlation, mean squared di erences, entropy, and adjusted cosine similarity (Herlocker,
Konstan, Borchers, & Riedl, 1999; Su & Khoshgo7aar,2009)."""

"""methode avec cosinus, les notes de deux users avec un vecteur dans un espace m-dimensionnel et calcule la similarite
basee sur le cosinus de l'angle"""
""". A good empirical comparison of variations
of item-based methods can be found in Sarwar et al.
(2001)."""

def cosinusSimilarite(user1, user2):
        sommeNum = 0
        sommeDenumUser1 = 0
        sommeDenumUser2 = 0
        for i in range(np.shape(donnees)[1]):
            if donnees[user1][i] != -1 and donnees[user2][i] != -1:
                sommeNum += donnees[user1][i] * donnees[user2][i]
                sommeDenumUser1 += donnees[user1][i] ** 2
                sommeDenumUser2 += donnees[user2][i] ** 2
        resultat = acos(sommeNum / sqrt(sommeDenumUser1 * sommeDenumUser2))
        return round(resultat,2)

def moyenneItems(user):
    somme = 0
    nombre = 0
    for i in range(np.shape(donnees)[1]):
        if donnees[user][i] != -1:
            somme += donnees[user][i]
            nombre += 1
    moyenne = somme/nombre
    return moyenne

def ponderationPremiere(user,item):
    num = 0
    den = 0
    for i in range(np.shape(donnees)[0]):
            if donnees[i][item] != -1:
                sim = cosinusSimilarite(user,i)
                num += sim * (donnees[i][item] - moyenneItems(i))
                den += fabs(sim)
    return round(moyenneItems(user) + num/den,2)
    
def ponderationSeconde(user, item):
    num = 0
    den = 0
    for i in range(np.shape(donnees)[0]):
        if donnees[i,item] != -1:       
            num += donnees[user][i] * cosinusSimilarite(user,i)
            den += fabs(cosinusSimilarite(user,i))
    return num/den

    
def donneesCompletes():
    donneesCompletes = donnees
    for i in range(np.shape(donneesCompletes)[0]):
        for j in range(np.shape(donneesCompletes)[1]):
            if donneesCompletes[i][j] == -1:
                donneesCompletes[i][j] = ponderationPremiere(i, j)     
                print donneesCompletes[i][j]
    return donneesCompletes

#donneesCompletes = donneesCompletes()                        

print donneesCompletes()