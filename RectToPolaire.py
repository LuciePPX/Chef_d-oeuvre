import matplotlib.pyplot as plt 
from PIL import Image
import numpy as np
import os
from tqdm import tqdm
import cv2

def pngToMatrix(image_path):
    # Open the PNG image
    img = Image.open(image_path)

    # Convert the image to grayscale
    gray_img = img.convert('L')

    # Convert the PIL Image to a NumPy array
    gray_matrix = np.array(gray_img)

    return gray_matrix

#______________________

def matrixToPolaire(gray_matrix, outPath, name):

    matrix = np.flipud(gray_matrix)

    N, M = matrix.shape
    theta, rho = np.linspace(0,2*np.pi,N)[::-1], np.linspace(0, 4e3, M)
    theta_M, rho_M = np.meshgrid(theta, rho)


    fig1, ax1 = plt.subplots(subplot_kw={'projection': 'polar'})
    ax1.set_axis_off()
    plt.pcolormesh(theta_M, rho_M, matrix, cmap='gray')
    
    filepath = os.path.join(outPath, name)
    fig1.savefig(filepath, facecolor='black')

#______________________

def polarisation(path):

    # Liste des noms de fichiers des images PNG
    images = [img for img in os.listdir(path) if img.endswith(".png")]
    images.sort()  # Pour s'assurer que les images sont dans l'ordre

    for img in tqdm(images, desc="Polarisation"):
        p=os.path.join(path,img)
        grayscale_matrix = pngToMatrix(p)
        matrixToPolaire(grayscale_matrix, "../Image/2014/Polaire2014" ,img)
        

