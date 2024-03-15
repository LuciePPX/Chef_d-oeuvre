# _____ IMPORTATIONS ___________

from traitementImage import contour_image,  traitement
import cv2
import numpy as np
import os 
from tqdm import tqdm

# ________ FONCTIONS __________

def plotImage(image, typeImg, seuil_y, aire=False, contour=True, marqueur=True, position = False):

    contours, points = contour_image(image,typeImg, seuil_y)

    img = image.copy()
    

    if typeImg=='rectangulaire':
        # ligne de de séparation entre données utilisables ou non 
        cv2.line(img,  (0, seuil_y), (img.shape[1], seuil_y), (200, 30, 255), 2)
    else: #'circulaire'

        cv2.circle(img, (int(img.shape[1]/2),int(img.shape[0]/2)), seuil_y,(200, 30, 255), 2)

    for c in range (len(contours)):

        if contour :
            # le contour de la ième tâche de la liste  
            cv2.drawContours(img, [contours[c][0]], -1, (0, 255, 0), 1)
        if aire :
            #affichage de l'aire 
            cv2.putText(img,f" s: {np.round(contours[c][1],0)}",(contours[c][6]),cv2.FONT_HERSHEY_SIMPLEX,1,(255, 255, 255),10) 
        if position: 
            #Affichage Lat, Long 
            cv2.putText(img, f"{np.round(points[c],2)}",(contours[c][6]),cv2.FONT_HERSHEY_SIMPLEX,2.5,(255, 255, 255),10)
        if marqueur:
            #Affichage d'une croix au centre 
            cv2.drawMarker(img, contours[c][6],(255, 0, 167), 5 , 2)
        
    return img

#_________________

def imagesDraw(imageRead, typeImg, seuil_y,aire):

    imageDraw=[]

    for image in tqdm(imageRead, "Traitement images"):
                    
        imageDraw.append(plotImage(image, typeImg, seuil_y,aire))

    return imageDraw


#_________________

def imageToVideo(Limages):

    height, width, _ = Limages[0].shape

    chemin_sortie=os.path.join("../OutputVideo/2014",f'VideoAlltask2014-360.mp4')

    # Définition VideoWriter
    video = cv2.VideoWriter(chemin_sortie,cv2.VideoWriter_fourcc(*'mp4v'), 30, (width, height))

    # Ajout des images à la vidéo
    for image in tqdm(Limages, desc="Réalisation de la vidéo"):
        video.write(image)

    print(chemin_sortie)
    # Fermeture de l'objet VideoWriter
    video.release()
#_________________
    
def visualisation(path,typeImg, video=True, image = [], aire=False):
    
    _, _, imagesRead, seuil_y = traitement(path,typeImg)   

    if video:
        Limages=imagesDraw(imagesRead, typeImg, seuil_y,aire)
        imageToVideo(Limages)

    if len(image)!=0 :
        imgRead=[]
        for numImg in image :
            imgRead.append(imagesRead[numImg])

        return imagesDraw(imgRead, typeImg, seuil_y,aire)
    
    else:
        return imagesDraw(imagesRead, typeImg, seuil_y,aire)
    

