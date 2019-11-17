#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# Filtrage collabortatif
#Coefficient de corrélation de Pearson
import numpy as np
import csv
import pickle
from math import sqrt
from math import fabs
from math import acos


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

def similariteCosinus(item1, item2):
    sommeNum = 0
    sommeDenumItem1 = 0
    sommeDenumItem2 = 0
    for i in range(np.shape(donneesItem)[0]):
        if donneesItem[i][item1] != -1 and donneesItem[i][item2] != -1:
            sommeNum += donneesItem[i][item1] * donneesItem[i][item2]
            sommeDenumItem1 += donneesItem[i][item1] ** 2
            sommeDenumItem2 += donneesItem[i][item2] ** 2
    resultat = acos(sommeNum / sqrt(sommeDenumItem1 * sommeDenumItem2))
    return resultat

def remplirTabSimilarite():
    for i in range(np.shape(tabSimilarite)[1]):
        for j in range(np.shape(tabSimilarite)[1]):
            tabSimilarite[i][j] = similariteCosinus(i,j)
            print tabSimilarite[i][j]
    return tabSimilarite

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
                tableauIntermediaire[i][j] = ponderationPremiere(i,j)
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