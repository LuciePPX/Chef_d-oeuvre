import subprocess
import os
import time

def lancer_radar_function(raw_file, images_folder, plots_folder, temp_folder, config_file):
    # Lancer la fonction Scilab avec les arguments spécifiés
    return subprocess.Popen(['scilab', '-f', 'radarLabFunction.sci', raw_file, images_folder, plots_folder, temp_folder, config_file])

def compter_images_dans_dossier(chemin_dossier):
    # Compter le nombre de fichiers avec l'extension .png dans le dossier
    images = [f for f in os.listdir(chemin_dossier) if f.endswith(".png")]
    return len(images)

if __name__ == "__main__":
    # Spécifier le chemin du dossier contenant les fichiers XML
    dossier_config = "/chemin/vers/votre/dossier/config/"

    # Spécifier le chemin du dossier où seront enregistrées les images
    dossier_images = "/chemin/vers/votre/dossier/images/"

    # Spécifier le chemin du dossier où seront enregistrés les graphiques
    dossier_plots = "/chemin/vers/votre/dossier/plots/"

    # Spécifier le chemin du dossier temporaire
    dossier_temp = "/chemin/vers/votre/dossier/temp/"

    # Parcourir tous les fichiers XML dans le dossier config
    fichiers_xml = sorted([f for f in os.listdir(dossier_config) if f.endswith(".xml")])

    # Générer les images pour chaque fichier XML
    for idx, fichier_xml in enumerate(fichiers_xml):
        # Calculer le nombre d'images requis pour le fichier actuel
        images_requises = (idx + 1) * 2

        # Lancer la fonction RadarLabFunction avec le fichier XML
        process_scilab = lancer_radar_function(os.path.join(dossier_config, fichier_xml), dossier_images, dossier_plots, dossier_temp, fichier_xml)

        # Attendre jusqu'à ce que le nombre d'images requis soit atteint
        while compter_images_dans_dossier(dossier_images) < images_requises:
            time.sleep(1)  # Attendre 1 seconde

        # Arrêter le processus Scilab
        process_scilab.terminate()

        print(f"Fichier XML {idx}: {images_requises} images générées.")

    print("Terminé.")
