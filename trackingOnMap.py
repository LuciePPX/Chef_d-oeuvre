# ________________Importation_________________ 
import folium
import os
from math import radians, sin, cos, sqrt, atan2
import math 
import copy
from tqdm import tqdm
from traitementImage import traitement

#_____________________
def distLatLong(p1, p2):
    lat1, lon1, lat2, lon2 = p1[0], p1[1], p2[0], p2[1]
    # Convertir les coordonnées degrés en radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Formule de la distance haversine
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    # Rayon de la Terre en kilomètres (approximatif)
    radius_earth = 6371.0

    # Calcul de la distance
    distance = radius_earth * c

    #distance *100 mètres
    return distance * 100

#_____________________
#Même si un bâteau a disparu à l'image n, on cherche sur les 3 images d'avant
def dernierElementNonNone(liste):

    for i,elmt in enumerate(reversed(liste)):        
        if elmt!=None and i<3 : 
            return True, liste.index(elmt)
        
    return False,0

#_____________________
#trouver le point le plus proche a partir d'une liste de point = point image n avec image n+1
def findProche(pointBoat,pointImage):

    boatLoc=copy.deepcopy(pointBoat)

    for i, boat in enumerate(pointBoat):
        #le point le plus proche = min distance  
        distmin=math.inf
        #Par défaut il n'a pas de point proche sur l'imae n+1
        pp=None 
        #on prend le dernier coordonnée de suivis 
        #Si il existe sur l'image (n,n-1 ou n-2) on le cherche dans n+1
        b,index=dernierElementNonNone(boat)
        
        for p2 in pointImage:

            if b:
                d= distLatLong(boat[index],p2)
                #Mais il faut que ce point soit suffisamment proche et le plus proche 
                if d<10 and d<distmin:

                    distmin=d
                    pp=p2

        boatLoc[i].append(pp)


    return boatLoc 

#__________________________

def findNewBoat(pointBoat,pointImage):

    boatLoc=copy.deepcopy(pointBoat)

    for p in pointImage:
        balise = False
        for boat in pointBoat:
            if p==boat[-1] : 
                balise = True 

        # si le point n'a pas été associé a un bâteau alors nouveau bâteau
        if not(balise):
            newBoat=[None]*(len(pointBoat[0])-1)
            newBoat.append(p)
            boatLoc.append(newBoat)

    return boatLoc

#__________________________

def lenNonNone(liste):
    cpt=0
    for elmt in liste:
        if elmt!=None:
            cpt+=1
    return cpt
#__________________________
#Enlève les track de moins de 20 points

def nonBoat(allTrack, longTrack=20):

    newTrack=copy.deepcopy(allTrack)

    for i,boat in enumerate(allTrack):
        if lenNonNone(boat)<longTrack:
            newTrack.remove(boat)
    return newTrack
#__________________________

def trackBoat(pParImage, longTrack=20):
    
    boatLoc=[]
    for boat in pParImage[0]:
        boatLoc.append([boat])
    
    for i in tqdm(range(1,len(pParImage)),"tracking des bâteaux"):
        boatLoc=findProche(boatLoc,pParImage[i])
        boatLoc=findNewBoat(boatLoc,pParImage[i])

    boatLoc=nonBoat(boatLoc,longTrack)

    return boatLoc

# Affichage des bâteaux estimé sur une carte Map

import folium
import random
#___________________

def sansNone(AllTrack):

    boatLoc=copy.deepcopy(AllTrack)
    
    for i,boat in enumerate(AllTrack):
        b=[point for point in boat if point is not None]
        boatLoc[i]=b

    return boatLoc

#___________________
def trackOnMap(allTrack, titre="", boat=[], zoom=14):

    couleurs = [
    'red', 'blue', 'green', 'purple', 'orange', 'darkred', 'darkblue', 'darkgreen', 'cadetblue', 'black',
    'gray', 'pink', 'lightblue', 'lightgreen', 'lightgray', 'lightred', 'beige', 'darkpurple', 'darkorange',
    '#FF5733', '#33FF57', '#5733FF', '#FF33B5', '#33B5FF', '#B5FF33', '#FF3333', '#3366FF', '#FFCC33', '#CC33FF',
    '#33FFCC', '#FF6633', '#6633FF', '#33FF99', '#9933FF', '#FF9933', '#33FF33', '#9933CC', '#FF33FF', '#33CCFF',
    '#FFCC99', 'brown', 'cyan', 'olive', 'indigo', 'maroon', 'turquoise', 'gold', 'orchid', 'slateblue'
    ]


    # initialisation
    point_center = 46.14853527580622, -1.247369529243042
    carte = folium.Map(location=[point_center[0], point_center[1]], zoom_start=zoom)
    folium.Marker([46.13407401541297, -1.273552703170837],popup="Phare de chauveau").add_to(carte)


    # Si liste boat est vide alors on affiche tous les tracks de bâteaux 
    if len(boat)==0:
        print(f'{len(allTrack)} bâteaux affichés sur la carte')
        #pour chaque bâteau
        trackSansNone=sansNone(allTrack)
        for boat in trackSansNone:
            print(boat)
            couleur=random.choice(couleurs)
            folium.PolyLine(boat, popup=trackSansNone.index(boat), color=couleur).add_to(carte)
                

        #Dosssier sauvegarde pour tous les bâteaux
        sauvegarde= os.path.join("../OutputImage/", f'AllTRack-{titre}.html')
    #Sinon affichage des bâteaux choisis
    else:
        print(f'{len(boat)} bâteaux affichés sur la carte')
        for b in boat:
            couleur=random.choice(couleurs)
            for p in allTrack[b]:
                if p!=None:
                    folium.Circle(p,radius=1, popup=b,color=couleur).add_to(carte)

        sauvegarde= os.path.join("../OutputImage/", f'TrackBoat{str(boat)}.html')
    
    print(f"{sauvegarde}")
    carte.save(sauvegarde)


