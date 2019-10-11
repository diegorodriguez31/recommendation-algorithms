#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# Filtrage collabortatif
import numpy as np
import csv
from math import sqrt
from math import fabs
from CentreUser import lecture_csv

"""Pour un filtrage base sur l’item, il faut definir une mesure de la similarite entre items. Plusieurs options sont possibles pour les mesures de similarite.
    Le systeme de filtrage collaboratif a ete popularise par Amazon avec la fonctionnalite : les gens qui ont achete x ont aussi achete y. 
    Le systeme d'Amazon etait un systeme passif qui se basait sur les achats des gens pour construire la matrice de relation entre les objets.

    Batir une matrice item-item déterminant des relations entre des objets "pairs"
    Utiliser cette matrice pour proposer des objets."""

#On recree le tableau du code centre user
donnees = lecture_csv()

#On transpose le tableau de base afin de faire la meme prediction centree item
donneesItem = np.transpose(donnees)


# Calcul de la similarité version item
def similaritefactoring(user1, user2):
    sommeUser1 = 0
    sommeUser2 = 0
    nombreItem = 0
    for i in range(np.shape(donneesItem)[1]):
        if donneesItem[user1][i] != -1 and donneesItem[user2][i] != -1:
            sommeUser1 += donneesItem[user1][i]
            sommeUser2 += donneesItem[user2][i]
            nombreItem = nombreItem + 1
    moyenneUser1 = sommeUser1 / nombreItem
    moyenneUser2 = sommeUser2 /nombreItem
    numerateur = 0
    norme1 = 0
    norme2 = 0
    if user1 != user2:
        for i in range(np.shape(donneesItem)[1]):
            if donneesItem[user1][i] != -1 and donneesItem[user2][i] != -1:
                numerateur += (donneesItem[user1][i] - moyenneUser1) * (donneesItem[user2][i] - moyenneUser2)
                norme1 += (donneesItem[user1][i] - moyenneUser1) ** 2
                norme2 += (donneesItem[user2][i] - moyenneUser2) ** 2
        r = numerateur / (sqrt(norme1) * sqrt(norme2))
    return r

def moyenneItems(user):
    somme = 0
    nombre = 0
    for i in range(np.shape(donneesItem)[1]):
        if donneesItem[user][i] != -1:
            somme += donneesItem[user][i]
            nombre += 1
    moyenne = somme/nombre
    return moyenne

def predictionNoteUtilisateur(user,item):
    num = 0
    den = 0
    for i in range(np.shape(donneesItem)[0]):
            if donneesItem[i][item] != -1:
                sim = similaritefactoring(user,i)
                num += sim * (donneesItem[i][item] - moyenneItems(i))
                den += fabs(sim)
    return round(moyenneItems(user) + num/den,2)

def donneesCompletes():
    donneesCompletes = donneesItem
    for i in range(np.shape(donneesCompletes)[0]):
        for j in range(np.shape(donneesCompletes)[1]):
            if donneesCompletes[i][j] == -1:
                donneesCompletes[i][j] = predictionNoteUtilisateur(i,j)
                print donneesCompletes[i][j]
    return donneesCompletes

donneesCompletes = donneesCompletes()