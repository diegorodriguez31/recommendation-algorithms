#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import numpy as np
import csv
from math import sqrt
from math import fabs

# Lire le fichier csv et le mettre dans un tableau
def lecture_csv():
    n = 100
    m = 1000

    fichier = './toy_incomplet.csv'
    donnees = np.zeros((n, m))
    i = 0
    with open(fichier, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            for j in range(m):
                donnees[i, j] = row[j]
            i += 1
    return donnees

donnees = lecture_csv()

"""    Recuperer une selection d'informations sur laquelle va se baser le systeme de filtrage
    La première consiste a recueillir de l'information
    La seconde consiste a batir une matrice contenant l'information.
    La troisieme à extraire a partir de cette matrice une liste de suggestions"""

"""Pour un filtrage base sur l’utilisateur, il faut definir une mesure de la similarite entre utilisateurs, et une
facon d’agreger les notes attribuees par les utilisateurs similaires.
    Chercher des utilisateurs qui ont les memes comportements avec l'utilisateur a qui l'on souhaite faire des recommandations
    Utiliser les notes des utilisateurs similaires pour calculer une liste de recommandations pour cet utilisateur."""

def tauKendall(user1,user2):
    nbConcordant = 0
    nbDiscordant = 0
    for i in range(np.shape(donnees)[1]):
        for j in range(np.shape(donnees)[1]):
            if donnees[user1][i] != -1 and donnees[user2][i] != -1 and donnees[user1][j] != -1 and donnees[user2][j] != -1:
                if donnees[user1][i] > donnees[user2][i] and donnees[user1][j] > donnees[user2][j] or donnees[user1][i] < donnees[user2][i] and donnees[user1][j] < donnees[user2][j]:
                    nbConcordant += 1
                else:
                    if donnees[user1][i] > donnees[user2][i] and donnees[user1][j] < donnees[user2][j] or donnees[user1][i] < donnees[user2][i] and donnees[user1][j] > donnees[user2][j]:
                        nbDiscordant += 1
    print nbConcordant
    print nbDiscordant
    return 2/(1000*(1000-1))*(nbConcordant - nbDiscordant)

"""def ponderationPremiere(user,item):
    num = 0
    den = 0
    for i in range(np.shape(donnees)[0]):
        if donnees[i][item] != -1:
            num += tabSimilarite[user][i] * (donnees[i][item] - listeMoyennes[i])
            den += fabs(tabSimilarite[user][i])
    return round(listeMoyennes[user] + num/den,2)


def donneesCompletes():
    donneesCompletes = donnees
    for i in range(np.shape(donneesCompletes)[0]):
        for j in range(np.shape(donneesCompletes)[1]):
            if donneesCompletes[i][j] == -1:
                donneesCompletes[i][j] = tableauIntermediaire[i][j]
                print donneesCompletes[i][j]
    return donneesCompletes"""
    
print tauKendall(0,1)
