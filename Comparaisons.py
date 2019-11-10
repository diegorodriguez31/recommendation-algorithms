#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# Filtrage collabortatif
#Comparaisons
import csv
import pickle
import numpy as np
from math import fabs
from math import sqrt


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

donneesJustes = lecture_csvComplet()

#Pickle pour recuperer nos objets : serialisation
with open('PearsonUser', 'rb') as fichier:
    mon_depickler = pickle.Unpickler(fichier)
    pearsonUser = mon_depickler.load()

#Mean Absolute Error (MAE)
def maePearsonUser():
    num = 0
    den = 0
    for i in range(np.shape(donneesJustes)[0]):
        for j in range(np.shape(donneesJustes)[1]):
            num += fabs(pearsonUser[i][j] - donneesJustes[i][j])
            den += 1
    return num/den

#Root Mean Squared Error (RMSE) = dispersion = variance, moyenne quadratique des ecarts
def rmsePearsonUser():
    num = 0
    den = 0
    for i in range(np.shape(donneesJustes)[0]):
        for j in range(np.shape(donneesJustes)[1]):
            num += (pearsonUser[i][j] - donneesJustes[i][j])**2 #erreur²
            den += 1
    return sqrt(num/den)

#Mean Bias Error (MBE)
def mbePersonUser():
    num = 0
    den = 0
    for i in range(np.shape(donneesJustes)[0]):
        for j in range(np.shape(donneesJustes)[1]):
            num += pearsonUser[i][j] - donneesJustes[i][j] #represente l'erreur
            den += 1
    return num/den

print "Mean absolute error :" ,maePearsonUser()
print "Root Mean Squared Error :" ,rmsePearsonUser()
print "Mean Bias Error :" ,mbePersonUser()