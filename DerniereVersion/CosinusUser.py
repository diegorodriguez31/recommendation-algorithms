#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# Filtrage collabortatif
# Coefficient de corrélation de Pearson
import numpy as np
import csv
import pickle
from math import sqrt
from math import fabs
from math import log
from math import acos

# Lire le fichier csv incomplet et le mettre dans un tableau
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

# tableau qui contient la moitie des notes seulement
donnees = lecture_csv()
# tableau intermediaire pour accelerer l'algorithme
tableauIntermediaire = np.zeros((100, 1000))
listeMoyennes = []
tabSimilarite = np.zeros((100, 100))

def similariteCosinus(user1, user2):
    sommeNum = 0
    sommeDenumUser1 = 0
    sommeDenumUser2 = 0
    for i in range(np.shape(donnees)[1]):
        if donnees[user1][i] != -1 and donnees[user2][i] != -1:
            sommeNum += donnees[user1][i] * donnees[user2][i]
            sommeDenumUser1 += donnees[user1][i] ** 2
            sommeDenumUser2 += donnees[user2][i] ** 2
    resultat = acos(sommeNum / sqrt(sommeDenumUser1 * sommeDenumUser2))
    return resultat

def remplirTabSimilarite():
    for i in range(np.shape(tabSimilarite)[0]):
        for j in range(np.shape(tabSimilarite)[0]):
            tabSimilarite[i][j] = similariteCosinus(i, j)
            print tabSimilarite[i][j]
    return tabSimilarite

def moyenneItems(user):
    somme = 0
    nombre = 0
    for i in range(np.shape(donnees)[1]):
        if donnees[user][i] != -1:
            somme += donnees[user][i]
            nombre += 1
    moyenne = somme / nombre
    return moyenne

def remplirListeMoyennes():
    for i in range(np.shape(donnees)[0]):
        listeMoyennes.append(moyenneItems(i))
    return listeMoyennes

def ponderationPremiere(user, item):
    num = 0
    den = 0
    for i in range(np.shape(donnees)[0]):
        if donnees[i][item] != -1:
            num += tabSimilarite[user][i] * (donnees[i][item] - listeMoyennes[i])
            den += fabs(tabSimilarite[user][i])
    return round(listeMoyennes[user] + num / den, 2)

#ponderation avec la moyenne
def moyenneUser(item):
    somme = 0
    nombre = 0
    for i in range(np.shape(donnees)[0]):
        if donnees[i][item] != -1:
            somme += donnees[i][item]
            nombre += 1
    moyenne = somme/nombre
    return moyenne

def remplirTabInter():
    for i in range(np.shape(donnees)[0]):
        for j in range(np.shape(donnees)[1]):
            if donnees[i][j] == -1:
                tableauIntermediaire[i][j] = ponderationPremiere(i, j)
                print tableauIntermediaire[i][j]
    return tableauIntermediaire

def donneesCompletes():
    donneesCompletes = donnees
    for i in range(np.shape(donneesCompletes)[0]):
        for j in range(np.shape(donneesCompletes)[1]):
            if donneesCompletes[i][j] == -1:
                donneesCompletes[i][j] = tableauIntermediaire[i][j]
                print donneesCompletes[i][j]
    return donneesCompletes

# savoir si les items les plus aimes ou detestes sont plus note que les autres items
def frequence(item):
    ni = 0
    for i in range(np.shape(donnees)[0]):
        if donnees[i][item] != -1:
            ni += 1
    return log(100) / ni

# Cette suite d'instructions a permit de construire le tableau de donnes estimees
listeMoyennes = remplirListeMoyennes()
tabSimilarite = remplirTabSimilarite()
remplirTabInter()
donneesCompletes = donneesCompletes()

# pickle pour enregistrer nos objets : serialisation
with open('CosinusUser', 'wb') as fichier:
    mon_pickler = pickle.Pickler(fichier)
    mon_pickler.dump(donneesCompletes)
