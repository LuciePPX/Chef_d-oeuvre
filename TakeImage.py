import os
import shutil

def parcourir_dossiers(dossier_racine):
    # Parcours de tous les dossiers et fichiers dans le dossier racine
    for dossier_parent, _, fichiers in os.walk(dossier_racine):
        # Filtrer les fichiers images (vous pouvez ajouter d'autres extensions si nécessaire)
        images = [fichier for fichier in fichiers if fichier.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]

        # Déplacer et renommer les images dans le dossier racine
        for image in images:
            chemin_source = os.path.join(dossier_parent, image)
            nouveau_nom = f"{os.path.basename(dossier_parent)}_{image}"
            chemin_destination = os.path.join(dossier_racine, nouveau_nom)

            # Vérifier si le fichier de destination existe déjà (ajouter un suffixe numérique si nécessaire)
            index = 1
            while os.path.exists(chemin_destination):
                nouveau_nom = f"{os.path.basename(dossier_parent)}_{index}_{image}"
                chemin_destination = os.path.join(dossier_racine, nouveau_nom)
                index += 1

            # Déplacer et renommer le fichier
            shutil.move(chemin_source, chemin_destination)
            print(f"Image déplacée : {chemin_source} -> {chemin_destination}")

if __name__ == "__main__":
    dossier_racine = input("Entrez le chemin du dossier racine : ")

    if os.path.exists(dossier_racine):
        parcourir_dossiers(dossier_racine)
        print("Opération terminée.")
    else:
        print("Le dossier spécifié n'existe pas.")
