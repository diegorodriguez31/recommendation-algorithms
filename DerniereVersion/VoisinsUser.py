#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# Filtrage collabortatif
# Coefficient de corrélation de Pearson
from __builtin__ import str

import numpy as np
import csv
import pickle
from math import sqrt
from math import fabs
from math import log

""" METTRE LES DIMENSIONS DU TABLEAU PAS EN DUR MAIS EN X, Y
FAIRE UNE PONDERATION TOUTE SIMPLE DE MOYENNE ET GARDER LA PONDERATIONPREMIERE ET ABANDONNER PONDERATIONSECONDE SI MARCHE PAS
CORRIGER CENTREITEM
FINIR COS
FAIRE UNE METHODE QUI CHERCHE LES 10 PLUS PROCHES VOISINS ET 4 PLUS PROCHES
TESTER LES COMPARAISONS DE CHACUN
TOUT COMPARER
FAIRE L'AUTRE METHODE DONT IL PARLAIT
"""


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


# Calcul de la similarité version utilisateur
def similariteFactoring(user1, user2):
    r = 0
    sommeUser1 = 0
    sommeUser2 = 0
    nombreItem = 0
    for i in range(np.shape(donnees)[1]):
        if donnees[user1][i] != -1 and donnees[user2][i] != -1:
            sommeUser1 += donnees[user1][i]
            sommeUser2 += donnees[user2][i]
            nombreItem = nombreItem + 1
    moyenneUser1 = sommeUser1 / nombreItem
    moyenneUser2 = sommeUser2 / nombreItem
    numerateur = 0
    norme1 = 0
    norme2 = 0
    if user1 != user2:
        for i in range(np.shape(donnees)[1]):
            if donnees[user1][i] != -1 and donnees[user2][i] != -1:
                numerateur += (donnees[user1][i] - moyenneUser1) * (donnees[user2][i] - moyenneUser2)
                norme1 += (donnees[user1][i] - moyenneUser1) ** 2
                norme2 += (donnees[user2][i] - moyenneUser2) ** 2
        r = numerateur / (sqrt(norme1) * sqrt(norme2))
    return r

def remplirTabSimilarite():
    for i in range(np.shape(tabSimilarite)[0]):
        for j in range(np.shape(tabSimilarite)[0]):
            tabSimilarite[i][j] = similariteFactoring(i, j)
            print tabSimilarite[i][j]
    return tabSimilarite

def plusProchesVoisins(user):
    listeSim = []
    listeUser = []
    for i in range(np.shape(tabSimilarite)[1]):
        listeSim.append(tabSimilarite[user][i])
    listeUser.append(0)
    for i in range(1, len(listeSim)):
        x = 0
        while x < len(listeUser):
            if fabs(listeSim[i]) > fabs(listeSim[listeUser[x]]):
                listeUser.insert(x, i)
                break
            else:
                x += 1
                if x == len(listeUser):
                    listeUser.append(i)
                    x += 1
                    break
    return listeUser

def plusProchesVoisins10(listeVoisins):
    liste10 = []
    for i in range(0,10):
        liste10.append(listeVoisins[i])
    return liste10

def plusProchesVoisins4(listeVoisins):
    liste4 = []
    for i in range(0,4):
        liste4.append(listeVoisins[i])
    return liste4

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

def ponderationPremiere10(user, item):
    num = 0
    den = 0
    for i in plusProchesVoisins10(plusProchesVoisins(user)):
        if donnees[i][item] != -1:
            num += tabSimilarite[user][i] * (donnees[i][item] - listeMoyennes[i])
            den += fabs(tabSimilarite[user][i])
    if den == 0:
        return -1
    return round(listeMoyennes[user] + num / den, 2)

def ponderationPremiere4(user, item):
    num = 0
    den = 0
    for i in plusProchesVoisins4(plusProchesVoisins(user)):
        if donnees[i][item] != -1:
            num += tabSimilarite[user][i] * (donnees[i][item] - listeMoyennes[i])
            den += fabs(tabSimilarite[user][i])
    if den == 0:
        return -1
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
                tableauIntermediaire[i][j] = fabs(ponderationPremiere10(i, j))
                print tableauIntermediaire[i][j]
    return tableauIntermediaire

#Complete le tableau avec les notes calculées
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
with open('Voisins10User', 'wb') as fichier:
    mon_pickler = pickle.Pickler(fichier)
    mon_pickler.dump(donneesCompletes)
