# __________IMPORTAIONS____________
import cv2
import numpy as np
from geopy.distance import distance
from tqdm import tqdm
import os
import sys
#_____________ Functions _____________

# Extraire les contours de l'image pour créer des features
def extract_features(edges): 
    features = []

    # Recherche des contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        # Calcul de l'aire
        area = np.sum(contour)
        
        # Calcul du périmètre
        perimeter = len(contour) 
        
        # Calcul de la circularité
        circularity = (4 * np.pi * area) / (perimeter ** 2)

        # Calcul du rectangle englobant
        _, _, w, h = cv2.boundingRect(contour)
        aspect_ratio = float(w) / h

        # Calcul des moments et des moments de Hu
        moment = cv2.moments(contour)
        # hu_moments = cv2.HuMoments(moments).flatten()
        # print("hu", hu_moments)

        # Calcul du point centre à partir de moment 
        if moment["m00"]!=0:
            cx = int(moment["m10"] / moment["m00"])
            cy = int(moment["m01"] / moment["m00"])

        else : 
            cx,cy= 0,0

        # Ajout des caractéristiques à la liste des features
        features.append([contour, area, perimeter, circularity, aspect_ratio, moment, (cx,cy)])  #A modifier selon les features que l'on veut area, perimeter, circularity, aspect_ratio, moment, (cx,cy)
    
    #print(f"features liste: {np.array(features)}")
    return features

#_________________

# Calcul de (longitude, latitude) à partir long/lat du radar, taille image (en pixel), largeur image (en °), hauteur de l'image (en mètre) 

def rectLongLat(cx,cy, start_point=(46.154533,-1.233523),taille=4096, largeur=360, hauteur=4000):

    # Distance en kilomètres
    distance_km = ((cy*hauteur)/taille) / 1000

    # Angle en degrés (0 degré est le nord, 90 degrés est l'est, etc.)
    angle_degrees = ((cx*largeur)/taille)

    # Calcul de la nouvelle position
    new_point = distance(kilometers=distance_km).destination(point=start_point, bearing=angle_degrees)

    # Affichage de la nouvelle position
    return( new_point.latitude,new_point.longitude)

#_____________________


def cirlceLongLat(cx, cy, centreImg, start_point=(46.154533,-1.233523)):

    # Coordonnées du point de référence au centre de l'image
    lat_ref, lon_ref = start_point[0],start_point[1]

    # Coordonnées du point de référence au centre de l'image dans l'image (centre)
    x_ref, y_ref = centreImg[0], centreImg[1]

    # Coordonnées du point dans l'image que vous souhaitez convertir
    x, y = cx,cy

    # Différence entre les coordonnées du point de référence au centre de l'image et le point de référence dans l'image
    delta_lat = lat_ref - lat_ref
    delta_lon = lon_ref - lon_ref

    # Ajuster les coordonnées du point dans l'image
    lat = lat_ref + delta_lat * (y - y_ref) / x_ref
    long = lon_ref + delta_lon * (x - x_ref) / y_ref


    return lat,long 

import math
#_____________________

def distCarte(A,B):
    xa,ya=A[0],A[1]
    xb,yb=B[0],B[1]

    return math.sqrt((xb - xa)**2 + (yb - ya)**2)

#_____________________

# Détecter les contour de l'image + filtrage des contours viables
def contour_image(image,typeImg, seuil_y, s_aire=500):

    # Convertir en niveaux de gris 
    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    centreImg =(int(image.shape[1]/2),int(image.shape[0]/2))
    print(centreImg)
    # Appliquer l'algorithme de détection de contours Canny
    edges = cv2.Canny(image, 0, 255)                                                          # à établir 

    # extraire les features
    feature = extract_features(edges)
    # Filtrer les contours situés en dessous de la ligne verticale
    filtered_contours = []
    points=[]

    for contour in feature:
        #définiton des caractéristiques 
        a=contour[1]
        cx,cy = contour[6]
        if typeImg=='rectangulaire':
        # contour viable si : le centre de la tache est au dessus de la ligne radar ET si son aire > seuil_aire
            if cy < seuil_y and a>s_aire:
                filtered_contours.append(contour)
                
                lat,long = rectLongLat(cx,cy)
                points.append((lat,long))

        else: 
            
            if seuil_y<distCarte(centreImg,(cx,cy)):
                filtered_contours.append(contour)
                
                lat,long=cirlceLongLat(cx,cy,centreImg)
                points.append((lat,long))

    return filtered_contours,points

#_____________________
def traitement(path, typeImg):
    # Liste des noms de fichiers des images PNG
    images = [img for img in os.listdir(path) if img.endswith(".png")]
    images.sort()  # Pour s'assurer que les images_2014 sont dans l'ordre


    imageRead=[]
    for img in tqdm(images, desc="Lecture des images"):
        imageRead.append(cv2.imread(os.path.join(path,img)))

    if typeImg=='rectangulaire':
        seuil_y = imageRead[0].shape[1]-500
    if typeImg=='circulaire':
        seuil_y = 10
    
    print(f'seuil de viabilité du radar : {seuil_y}')

    #Traitement des images 

    pParImage = []
    cParImage = []

    for img in tqdm(imageRead, desc="Recherche des bateaux"):
        coutours, points = contour_image(img,typeImg,seuil_y)
        cParImage.append(coutours)
        pParImage.append(points)


    return cParImage, pParImage, imageRead, seuil_y





