#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# Filtrage collabortatif
# Coefficient de corrélation de Pearson
import numpy as np
import csv
import random
import pickle

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

# Lire le fichier csv complet et le mettre dans un tableau
def lecture_csvComplet():
    n = 100
    m = 1000

    fichier = './toy_complet.csv'
    donnees = np.zeros((n, m))
    i = 0
    with open(fichier, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            for j in range(m):
                donnees[i, j] = row[j]
            i += 1
    return donnees

def tableauPourcentage(pourcentage):
    n = 100000*pourcentage/100
    x = 0
    while x < n:
        i = random.randint(0, 99)
        j = random.randint(0, 999)
        if toyComplet[i][j] != -1:
            toyComplet[i][j] = -1
        else:
            x -= 1
        x += 1
    return toyComplet

def ecriture_pickle(donnees,nom):
    with open(nom, 'wb') as fichier:
        mon_pickler = pickle.Pickler(fichier)
        mon_pickler.dump(donnees)

def ecriture_csv(donnees,nom):
    with open(nom,'w') as csvfile:
        filewriter = csv.writer(csvfile)
        for i in range(np.shape(donnees)[0]):
            chaine = ''
            for j in range(np.shape(donnees)[1]):
                chaine += str(donnees[i][j])+' '
            filewriter.writerow([chaine])

toyComplet = lecture_csvComplet()
ecriture_pickle(tableauPourcentage(75),'75%NotesEffacees')
ecriture_pickle(tableauPourcentage(90),'90%NotesEffacees')
ecriture_pickle(tableauPourcentage(99),'90%NotesEffacees')
ecriture_csv(tableauPourcentage(75),'75%NotesEffacees')
ecriture_csv(tableauPourcentage(90),'90%NotesEffacees')
ecriture_csv(tableauPourcentage(99),'90%NotesEffacees')