#________IMPORTATIONS__________

def countBoat(pParImage):

    boats=[]
    boatTotaux= 0
    bParImage = []
    for img in pParImage:
        b=0
        for p in img:
            if p not in boats:
                boats.append(p)
                b+=1
                bT+=1
        bParImage.append(b)

    print(f" Nombre de bâteaux sur toutes les images: {boatTotaux}, \n Nombre de bâteaux par image: {bParImage}, \n Nombre de bâteaux max sur une image: {max(bParImage)}")

    return boatTotaux, bParImage

