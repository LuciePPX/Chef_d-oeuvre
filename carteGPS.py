import csv

def gpsToListe():
    with open('../SourceExcel/Jetski.csv', 'r') as fichier_csv:
        lecteur_csv = csv.reader(fichier_csv, delimiter=';')

        # Ignorer la première ligne (en-têtes)
        en_tetes = next(lecteur_csv)

        liste_de_donnees = []

        for ligne in lecteur_csv:
            # Séparer la ligne en utilisant le point-virgule comme séparateur
            donnees_ligne = ligne

            # Vous pouvez également ignorer la première colonne si nécessaire
            donnees_ligne = ligne[1:]

            donnees_ligne_float = [float(element) for element in donnees_ligne]

            liste_de_donnees.append(donnees_ligne_float)



    print(liste_de_donnees)
