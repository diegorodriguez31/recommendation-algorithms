#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# Filtrage collabortatif
#Coefficient de corrélation de Pearson
import numpy as np
import csv
import pickle
from math import sqrt
from math import fabs


"""Pour un filtrage base sur l’item, il faut definir une mesure de la similarite entre items. Plusieurs options sont possibles pour les mesures de similarite.
    Le systeme de filtrage collaboratif a ete popularise par Amazon avec la fonctionnalite : les gens qui ont achete x ont aussi achete y. 
    Le systeme d'Amazon etait un systeme passif qui se basait sur les achats des gens pour construire la matrice de relation entre les objets.

    Batir une matrice item-item déterminant des relations entre des objets "pairs"
    Utiliser cette matrice pour proposer des objets."""

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

donneesItem = lecture_csv()
tableauIntermediaire = np.zeros((100,1000))
listeMoyennes = []
tabSimilarite = np.zeros((1000,1000))

# Calcul de la similarité version item
def similaritePearson(item1, item2):
    r = 0
    sommeItem1 = 0
    sommeItem2 = 0
    nombreItem = 0
    for i in range(np.shape(donneesItem)[0]):
        if donneesItem[i][item1] != -1 and donneesItem[i][item2] != -1:
            sommeItem1 += donneesItem[i][item1]
            sommeItem2 += donneesItem[i][item2]
            nombreItem = nombreItem + 1
    moyenneItem1 = sommeItem1 / nombreItem
    moyenneItem2 = sommeItem2 /nombreItem
    numerateur = 0
    norme1 = 0
    norme2 = 0
    if item1 != item2:
        for i in range(np.shape(donneesItem)[0]):
            if donneesItem[i][item1] != -1 and donneesItem[i][item2] != -1:
                numerateur += (donneesItem[i][item1] - moyenneItem1) * (donneesItem[i][item2] - moyenneItem2)
                norme1 += (donneesItem[i][item1] - moyenneItem1) ** 2
                norme2 += (donneesItem[i][item2] - moyenneItem2) ** 2
        r = numerateur / (sqrt(norme1) * sqrt(norme2))
    return r

def remplirTabSimilarite():
    for i in range(np.shape(tabSimilarite)[1]):
        for j in range(np.shape(tabSimilarite)[1]):
            tabSimilarite[i][j] = similaritePearson(i,j)
            print tabSimilarite[i][j]
    return tabSimilarite

def plusProchesVoisins(item):
    listeSim = []
    listeUser = []
    for i in range(np.shape(tabSimilarite)[0]):
        listeSim.append(tabSimilarite[i][item])
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

def moyenneUser(item):
    somme = 0
    nombre = 0
    for i in range(np.shape(donneesItem)[0]):
        if donneesItem[i][item] != -1:
            somme += donneesItem[i][item]
            nombre += 1
    moyenne = somme/nombre
    return moyenne

def remplirListeMoyennes():
    for i in range(np.shape(donneesItem)[1]):
        listeMoyennes.append(moyenneUser(i))
    return listeMoyennes

def ponderationPremiere(user,item):
    num = 0
    den = 0
    for i in range(np.shape(donneesItem)[1]):
            if donneesItem[user][i] != -1:
                num += tabSimilarite[item][i] * (donneesItem[user][i] - listeMoyennes[i])
                den += fabs(tabSimilarite[item][i])
    return round(moyenneUser(user) + num/den,2)

def ponderationPremiere10(user, item):
    num = 0
    den = 0
    for i in plusProchesVoisins10(plusProchesVoisins(user)):
        if donneesItem[user][i] != -1:
            num += tabSimilarite[item][i] * (donneesItem[user][i] - listeMoyennes[i])
            den += fabs(tabSimilarite[item][i])
    if den == 0:
        return -1
    return round(listeMoyennes[user] + num / den, 2)

def ponderationPremiere4(user, item):
    num = 0
    den = 0
    for i in plusProchesVoisins4(plusProchesVoisins(user)):
        if donneesItem[user][i] != -1:
            num += tabSimilarite[item][i] * (donneesItem[user][i] - listeMoyennes[i])
            den += fabs(tabSimilarite[item][i])
    if den == 0:
        return -1
    return round(listeMoyennes[user] + num / den, 2)

#ponderation avec la moyenne
def moyenneItems(user):
    somme = 0
    nombre = 0
    for i in range(np.shape(donneesItem)[1]):
        if donneesItem[user][i] != -1:
            somme += donneesItem[user][i]
            nombre += 1
    moyenne = somme / nombre
    return moyenne

def remplirTabInter():
    for i in range(np.shape(donneesItem)[0]):
        for j in range(np.shape(donneesItem)[1]):
            if donneesItem [i][j] == -1:
                tableauIntermediaire[i][j] = fabs(ponderationPremiere10(i,j))
                print tableauIntermediaire[i][j]
    return tableauIntermediaire

def donneesCompletes():
    donneesCompletes = donneesItem
    for i in range(np.shape(donneesCompletes)[0]):
        for j in range(np.shape(donneesCompletes)[1]):
            if donneesCompletes[i][j] == -1:
                donneesCompletes[i][j] = tableauIntermediaire[i][j]
                print donneesCompletes[i][j]
    return donneesCompletes

listeMoyennes = remplirListeMoyennes()
tabSimilarite = remplirTabSimilarite()
remplirTabInter()
donneesCompletes = donneesCompletes()

#pickle pour enregistrer nos objets : serialisation
with open('PearsonItem', 'wb') as fichier:
    mon_pickler = pickle.Pickler(fichier)
    mon_pickler.dump(donneesCompletes)