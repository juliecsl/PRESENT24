# 20 minutes
from datetime import datetime
from multiprocessing import Process
global m1, c1, m2, c2

# Partie à mofidier si souhaité:
# (m1, c1) et (m2,c2) les couples de clair/chiffré connus. 
m1 = "ecddfa"
c1 = "3d637b"
m2 = "0583c8"
c2 = "4c34bb"
# ###################
# Ne pas modifier sous cette ligne. 


global dico_substitution, liste_permutation, dico_substitution_inv
dico_substitution = {"0":"c", "1":"5", "2":"6", "3":"b", "4":"9", "5":"0", "6":"a", 
                        "7":"d", "8":"3", "9":"e", "a":"f", "b":"8", "c":"4", "d":"7", 
                        "e":"1", "f":"2"}
    
liste_permutation = [0, 4, 8, 12, 16, 20, 1, 5, 9, 13, 17, 21, 2, 6, 
                         10, 14, 18, 22, 3, 7, 11, 15, 19, 23]

dico_substitution_inv = { "0": "5", "1": "e", "2": "f", "3": "8", "4": "c", "5": "1", "6": "2",
                            "7": "d", "8": "b", "9": "4", "a": "6", "b": "3", "c": "0", "d": "7", 
                            "e": "9", "f": "a"}


def main_chiffrement(m, CLE_MAITRE):
    """
    Algorithme 1 de l'énonce du DM
    Entrée: m le message à chiffrer en hexidécimal sous forme de str de taille 6
            CLE_MAITRE le clé maitre en héxidécimal sous forme de str de taille 6
    Sortie: le message chiffré en hexidécimal.
    """
    K = str(CLE_MAITRE) + str("0"*14)  # registre de 20 bits en hexa
    K = bin(int(K, 16))[2:].zfill(80)  # Convertie de l'hexa vers le binaire  # Si le resultat de la conversion en hex fait moins de 80 bits on rajoute des 0 à gauche. 
    
    j = 0
    etat = bin(int(m, 16))[2:]  # Hexa to binaire
    for i in range(1, 10+1):
        j += 1
        ki = K[79-39:79-16+1]  # en binaire  # determine ki

        # ################
        # MAJ DU REGISTRE K
        k = K[61:] + K[:61] # Fait pivoter le registre K de 61 positions vers la gauche.

        # SUBSTITUTION
        k_prime = ''.join([dico_substitution[elem] for elem in hex(int(k[0:4] ,2))[2:]])

        k_prime = bin(int(k_prime, 16))[2:].zfill(4)  # hexa en binaire + Si le resultat fait moins de 4 bits alors on rajoute des 0 à gauche

        k = k_prime[0:4] + k[4:]# Met le registre K à jour avec les bits permutés

        # XOR
        k_prime = bin(int("".join(k[79-19:79-15+1]),2) ^ i)[2:].zfill(5) # un str binaire # k_prime XOR i  # Si le resultat du XOR fait moins de 5 bits on rajoute des 0 à gauche. 
        ####

        K = k[:79-19] + k_prime + k[79-15+1:] # Met les bits [k19k18...k15 à jour]

        # #####################################

        etat = hex(int(etat, 2) ^ int(ki, 2))[2:].zfill(6)  # renvoie l'etat en hexa du resultat du XOR entre l'état et ki
        # Si le resultat du XOR fait moins de 24 bits on rajoute des 0 à gauche. 
            
        # SUBSTITUTION
        etat = ''.join([dico_substitution[elem] for elem in etat])
        # #####################

        etat = bin(int(etat, 16))[2:].zfill(24)  # Hexa to binaire
        # Si le resultat du XOR fait moins de 24 bits on rajoute des 0 à gauche. 
        
        # PERMUTATION
        etat = ''.join([etat[i] for i in liste_permutation])

    ki = K[79-39:79-16+1]   # k11  # determine ki
    etat = hex(int(etat, 2) ^ int(ki, 2))[2:]  # etat XOR ki
    return etat


def main_dechiffrement(chiffre, cle_maitre):
    """
    Entrée: chiffre le message chiffré de 6 bits en hexadécimal en str
            cle_maitre de 6 bits en hexadécimal en str
    Sortie: message déchiffré de 6 bits en hexadécimal en str. 
    """

    dico_substitution_inv = { "0": "5", "1": "e", "2": "f", "3": "8", "4": "c", "5": "1", "6": "2",
                            "7": "d", "8": "b", "9": "4", "a": "6", "b": "3", "c": "0", "d": "7", 
                            "e": "9", "f": "a"}

    dico_substitution = {"0":"c", "1":"5", "2":"6", "3":"b", "4":"9", "5":"0", "6":"a", 
            "7":"d", "8":"3", "9":"e", "a":"f", "b":"8", "c":"4", "d":"7", 
            "e":"1", "f":"2"}

    liste_permutation = [0, 6, 12, 18, 1, 7, 13, 19, 2, 8, 14, 20, 3, 9, 15, 
                         21, 4, 10, 16, 22, 5, 11, 17, 23]


    K = str(cle_maitre) + str("0"*14)  # registre de 20 bits en hexa
    K = bin(int(K, 16))[2:].zfill(80)  # Convertie de l'hexa vers le binaire  # Si le resultat de la conversion en hex fait moins de 80 bits on rajoute des 0 à gauche. 

    liste_ki = [] # Liste permettant de stocker les ki, le premier element de la liste étant k1

    # Calcul des ki
    for i in range(1, 11+1):  # 11 ki à calculer.
        liste_ki.append(int(K[79-39:79-16+1], 2))  # Ajout de ki à la liste de stockage sous forme de décimal car le XOR se fait entre nb décimaux.
        # K = maj_registreK(K, i, dico_substitution)

    ###################################################################################
    # ################
        # MAJ DU REGISTRE K
        k = K[61:] + K[:61] # Fait pivoter le registre K de 61 positions vers la gauche.

        # SUBSTITUTION
        k_prime = ''.join([dico_substitution[elem] for elem in hex(int(k[0:4] ,2))[2:]])

        k_prime = bin(int(k_prime, 16))[2:].zfill(4)  # hexa en binaire + Si le resultat fait moins de 4 bits alors on rajoute des 0 à gauche

        k = k_prime[0:4] + k[4:]# Met le registre K à jour avec les bits permutés

        # XOR
        k_prime = bin(int("".join(k[79-19:79-15+1]),2) ^ i)[2:].zfill(5) # un str binaire # k_prime XOR i  # Si le resultat du XOR fait moins de 5 bits on rajoute des 0 à gauche. 
        ####

        K = k[:79-19] + k_prime + k[79-15+1:] # Met les bits [k19k18...k15 à jour]


    ######################################################################################

    etat = bin(int(int(chiffre, 16) ^ liste_ki[11-1]))[2:]  # chiffre (etat) XOR k11 (en decimal) # 11-1 car la liste commence à l'indice 0
    etat = etat.zfill(24)

    for i in range(10, 1-1, -1):  # Pour i allant de 10 à 1 inclu
        etat = ''.join([etat[i] for i in liste_permutation])  # Permutation inverse # sous forme de str en binaire
        etat = hex(int(etat, 2))[2:].zfill(6)

        etat = ''.join([dico_substitution_inv[elem] for elem in etat])  # substitution inverse # sous forme de str en hexa
        etat = bin(int((liste_ki[i-1] ^ int(etat, 16))))[2:].zfill(24)  # etat XOR ki # [i-1] car la liste commence à l'indice 0
    
    etat = hex(int(etat, 2))[2:].zfill(6)

    return(etat)


def genere_chiffre(clair, range_min, range_max, filename):
    """
    Génère toutes les messages chiffrés possibles pour les clés allant de 000000 à ffffff en hexadécimal.
    Et met le résultat dans un fichier.
    Entrée: chiffré: le chiffre en hexadécimal en format string.
            filename: le nom du fichier où stocker le résultat.
            range_min: int en décimal (compris entre 00000 et ffffff dans la notation en hexa) 
            et plus petit que range_max
            range_max: int en décimal (compris entre 00000 et ffffff dans la notation en hexa) 
            et plus grand que range_min
    """
    print("C'est parti pour Lm!", datetime.now())

    # Ouverture du fichier pour écrire dedans
    with open(filename, "w") as fichier:
        j = 0
        for i in range(range_min, range_max+1):
                
            # Message de print pour afficher l'avancement de la fonction 
            j += 1
            if j == 200000:
                print(i, "--> Avancement Lm :", int((i-range_min)/(range_max)*100),"%", datetime.now())
                j = 0
            # #########

            k = hex(int(i))[2:].zfill(6)  # decimal to hexa # Verification que k soit de taille 6 sinon met des 0 à sa gauche.
            res = main_chiffrement(clair, k)  # Lancement fonction de chiffrement
            res = res.zfill(6)  # Verification que res soit de taille 6 sinon met des 0 à sa gauche.
            # Lm.append((res, k))
            fichier.write(f"{res, k}\n")  # Ecriture du resultat dans le fichier.



def genere_clair(chiffre, range_min, range_max, filename):
    """
    Génère, Lc, tous les messages clairs possibles pour les clés allant de 000000 à ffffff en hexadécimal.
    Et met le résultat dans un fichier.
    Entrée: chiffré: le chiffre en hexadécimal en format string.
            filename: le nom du fichier où stocker le résultat.
            range_min: int en décimal (compris entre 00000 et ffffff dans la notation en hexa) 
            et plus petit que range_max
            range_max: int en décimal (compris entre 00000 et ffffff dans la notation en hexa) 
            et plus grand que range_min
    """
    print("C'est parti pour Lc !", datetime.now())

    # Ouverture du fichier pour écrire dedans 
    with open(filename, "w") as fichier:
        j = 0

        for i in range(range_min, range_max+1):

            # Message de print pour afficher l'avancement de la fonction 
            j += 1
            if j == 200000:
                print(i, "--> Avancement Lc :", int(i/(range_max)*100),"%", datetime.now())
                j = 0
            # ###################

            k = hex(int(i))[2:].zfill(6)  # decimal to hexa # Verification que k soit de taille 6 sinon met des 0 à sa gauche.
            res = main_dechiffrement(chiffre, k)  # Lancement déchiffrement
            res = res.zfill(6)  # Verification que res soit de taille 6 sinon met des 0 à sa gauche.
            # Lc.append((res, k))
            fichier.write(f"{res, k}\n")  # Ecriture du résultat dans fichier.



# #################################################################################################################################################################



# #############################################
# FONCTIONS

def elem_commun(Lc, Lm):
    """
    Fonction qui trouve les élements communs entre la liste Lm et Lc.
    Entrée: Lc et Lm des listes triées de la forme 
            [(msg1 crypté ou clair, indice1), (msg1 crypté ou clair, indice1)]
    Sortie: retourne la liste des indices dont les élements sont communs
            de la forme [(k1, k2), (k1', k2'), ...]
    """
    print("Lancement du trouvage d'élément commun", datetime.now())
    l_commun = []

    cpt = 0
    j = 0  # Indice de la liste Lc.
    j_prec = 0  # Pour mémoriser le j precedent dans le cas où on a plusieurs fois 
                # la meme occurence dans la liste Lm.
    for i in range(len(Lm)):  # Parcours de toute la liste Lm.

        # Partie pour print le pourcentage de l'avancement de la fonction.
        cpt += 1
        if cpt == 5000000:
            print(i, "--> Avancement elem commun :", int(i/len(Lm)*100),"%", datetime.now())
            cpt = 1


        j = j_prec
        premier_trouve = False
        # Tant que j est encore un indice de la liste
        # et que le msg dans Lm est plus petit ou égale à au msg dans Lc, on parcourt Lc
        while j < (len(Lc)) and Lm[i][0] >= Lc[j][0]:
            if Lm[i][0] == Lc[j][0]:  # Si msg égaux
                l_commun.append((Lm[i][1], Lc[j][1]))  # Ajout des indices (k1, k2) correspondant aux msg dans liste.
                if premier_trouve == False:
                    premier_trouve = True
                    j_prec = j  # Comme mot commun trouvé on ne veut pas que le j avance au qu'à où 
                                # il y ait plusieurs element dans Lm qui soient égaux à l'élément dans Lc.
            j += 1
        
    return l_commun


def trouve_cles(k1, k2):
    """
    Fonction qui permet de trouver les couples de clés (k1, k2) 
    et print dans le terminal ce couple de clé lorsqu'il est trouvé.
    Entrée: k1 et k2 des clés potentielles, de taille 6 ecrit en binaire.
    """
    chiffre_intermediaire = main_chiffrement(m2, k1)  # m2, k1 (potentiel)
    chiffre = main_chiffrement(chiffre_intermediaire, k2)  # chiffre intermediaire, k2 (potentiel)
    if chiffre == c2:  # Si le chiffré par le k1 et k2 potentiel est égale a notre c2, on print ce couple de clé.
        print("La bi-clé de chiffrement est:", k1, k2)


def lancement(range_min, range_max, l_commun, n_process):
    """
    Permet de lancer, selon la répartition donnée aux process,  la fonction pour trouver les couples de clés. 
    Entrée: range_min & range_max des int correspondant à l'intervalle de la liste des elements communs que traite le process
            l_commun: la liste des éléments commun
            n_process: un int correspondant au n° du process qui effectue le calcul. 
    """
    j = 0
    for i in range(range_min, range_max):

        # Partie pour print le pourcentage de l'avancement de la fonction.
        j += 1
        if j == 500000:  
            print("Processeur:", n_process, i,   "--> Avancement trouve cle :", int((i-range_min)/(range_max-range_min)*100),"%", datetime.now())
            j = 0

        # Lancement de la fonction pour trouver les couples de clés.
        # trouve_cles(l_commun[i][0], l_commun[i][1])
        k1 = l_commun[i][0]
        k2 = l_commun[i][1]
        chiffre_intermediaire = main_chiffrement(m2, k1)  # m2, k1 (potentiel)
        chiffre = main_chiffrement(chiffre_intermediaire, k2)  # chiffre intermediaire, k2 (potentiel)
        if chiffre == c2:  # Si le chiffré par le k1 et k2 potentiel est égale a notre c2, on print ce couple de clé.
            print("La bi-clé de chiffrement est:", k1, k2)



if __name__ == '__main__':


    # Creation des process pour découper la génération des listes Lm et Lc. 
    process1 = Process(target=genere_chiffre, args=(m1, 0, 5000000, "Lm1.txt"))
    process2 = Process(target=genere_chiffre, args=(m1, 5000001, 10000000, "Lm2.txt"))
    process3 = Process(target=genere_chiffre, args=(m1, 10000001, 15000000, "Lm3.txt"))
    process4 = Process(target=genere_chiffre, args=(m1, 15000001,16777215, "Lm4.txt"))

    process5 = Process(target=genere_clair, args=(c1, 0, 5000000, "Lc1.txt"))
    process6 = Process(target=genere_clair, args=(c1, 5000001, 10000000, "Lc2.txt"))
    process7 = Process(target=genere_clair, args=(c1, 10000001, 15000000, "Lc3.txt"))
    process8 = Process(target=genere_clair, args=(c1, 15000001,16777215, "Lc4.txt"))

    # Lancement des process
    process1.start()
    process2.start()
    process3.start()
    process4.start()
    process5.start()
    process6.start()
    process7.start()
    process8.start()

    # Attente de la fin de tout les process pour finir
    print('Waiting for the process...')
    process1.join()
    process2.join()
    process3.join()
    process4.join()
    process5.join()
    process6.join()
    process7.join()
    process8.join()

    print("Ecriture de Lm et Lc dans fichiers fini.")

    # ############################################################################################


    Lm = []
    Lc = []

    # Lecture des fichiers contenants Lm et Lc 
    # et écriture du contenu des fichiers dans les listes Lc et Lm
    with open("Lc1.txt", "r") as fichier:
        lignes = fichier.readlines()
        for ligne in lignes:
            indice = ligne.find(",")
            mot = ligne[2:indice-2+1]
            Lc.append((mot, ligne[indice+3:len(ligne)-3]))

    with open("Lc2.txt", "r") as fichier:
        lignes = fichier.readlines()
        for ligne in lignes:
            indice = ligne.find(",")
            mot = ligne[2:indice-2+1]
            Lc.append((mot, ligne[indice+3:len(ligne)-3]))


    with open("Lc3.txt", "r") as fichier:
        lignes = fichier.readlines()
        for ligne in lignes:
            indice = ligne.find(",")
            mot = ligne[2:indice-2+1]
            Lc.append((mot, ligne[indice+3:len(ligne)-3]))

    with open("Lc4.txt", "r") as fichier:
        lignes = fichier.readlines()
        for ligne in lignes:
            indice = ligne.find(",")
            mot = ligne[2:indice-2+1]
            Lc.append((mot, ligne[indice+3:len(ligne)-3]))

    with open("Lm1.txt", "r") as fichier:
        lignes = fichier.readlines()
        for ligne in lignes:
            indice = ligne.find(",")
            mot = ligne[2:indice-2+1]
            Lm.append((mot, ligne[indice+3:len(ligne)-3]))

    with open("Lm2.txt", "r") as fichier:
        lignes = fichier.readlines()
        for ligne in lignes:
            indice = ligne.find(",")
            mot = ligne[2:indice-2+1]
            Lm.append((mot, ligne[indice+3:len(ligne)-3]))

    with open("Lm3.txt", "r") as fichier:
        lignes = fichier.readlines()
        for ligne in lignes:
            indice = ligne.find(",")
            mot = ligne[2:indice-2+1]
            Lm.append((mot, ligne[indice+3:len(ligne)-3]))

    with open("Lm4.txt", "r") as fichier:
        lignes = fichier.readlines()
        for ligne in lignes:
            indice = ligne.find(",")
            mot = ligne[2:indice-2+1]
            Lm.append((mot, ligne[indice+3:len(ligne)-3]))


    # Trie des listes Lm et Lc en par rapport aux msg cryptés/clairs.
    Lm.sort(key=lambda x: x[0])
    Lc.sort(key=lambda x: x[0])
    print("Listes Lm et Lc Triées")
    print("Longueur de Lm et Lc", len(Lm), len(Lc))

    l_commun = elem_commun(Lc, Lm)
    print("Elements communs trouvés.")

    Lm = []  # Libération de la mémoire. Lm avait une taille de plus de 16 millions.
    Lc = []  # Libération de la mémoire. Lc avait une taille de plus de  16 millions.

    # Lancement de 4 processus pour définir le(s) couple(s) de clés.
    # Seulement 4 processus pour ne pas saturer la mémoire.
    nb_paquets = len(l_commun) // 4  # 4 etant le nb de processus

    print("Lancement des processus de lancement pour trouver la clé.")
    process1_bis = Process(target=lancement, args=(0, nb_paquets, l_commun, 1))
    process2_bis = Process(target=lancement, args=(nb_paquets, nb_paquets*2, l_commun,2))
    process3_bis = Process(target=lancement, args=(nb_paquets*2, nb_paquets*3,l_commun, 3))
    process4_bis = Process(target=lancement, args=(nb_paquets*3, len(l_commun), l_commun, 4))


    # Lancement des processus
    process1_bis.start()
    process2_bis.start()
    process3_bis.start()
    process4_bis.start()

    # Attente de la fin de tous les process
    print('Waiting for the process...')
    process1_bis.join()
    process2_bis.join()
    process3_bis.join()
    process4_bis.join()

    print("Fin du programme")
