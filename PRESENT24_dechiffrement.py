
# ####################################
# LIBRAIRIE
import numpy as np
import time
# tps1 = time.time_ns()

# ####################################
# FONCTIONS

def maj_registreK(K, i, dico_substitution):
    """
    Met à jour le registre K après avoir déterminer Ki.
    Entrée: K le registre de 80 bits, str
    Sortie:
    """
    k = K[61:] + K[:61] # Fait pivoter le registre K de 61 positions vers la gauche.

    # SUBSTITUTION
    k_prime = k[0:4]


    res = [dico_substitution[elem] for elem in hex(int(k_prime,2))[2:]]
    k_prime = ''.join(res)


    k_prime = bin(int(k_prime, 16))[2:].zfill(4)  # hexa en binaire + Si le resultat fait moins de 4 bits alors on rajoute des 0 à gauche

    k = k_prime[0:4] + k[4:]# Met le registre K à jour avec les bits permutés

    # XOR
    k_prime = k[79-19:79-15+1]  # une liste
    k_prime = bin(int("".join(k_prime),2) ^ i)[2:]  # un str binaire # k_prime XOR i

    k_prime = k_prime.zfill(5) # Si le resultat du XOR fait moins de 5 bits on rajoute des 0 à gauche. 
    k_prime = [car for car in k_prime]  # str en liste
    ####

    k = [car for car in k]

    j = 0
    for i in range(79-19,79-15+1):  # Met les bits [k19k18...k15 à jour]
        k[i] = k_prime[j]
        j += 1

    return "".join(k)



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
        K = maj_registreK(K, i, dico_substitution)

    etat = bin(int(int(chiffre, 16) ^ liste_ki[11-1]))[2:]  # chiffre (etat) XOR k11 (en decimal) # 11-1 car la liste commence à l'indice 0
    etat = etat.zfill(24)

    for i in range(10, 1-1, -1):  # Pour i allant de 10 à 1 inclu
        etat = ''.join([etat[i] for i in liste_permutation])  # Permutation inverse # sous forme de str en binaire
        etat = hex(int(etat, 2))[2:].zfill(6)

        etat = ''.join([dico_substitution_inv[elem] for elem in etat])  # substitution inverse # sous forme de str en hexa
        etat = bin(int((liste_ki[i-1] ^ int(etat, 16))))[2:].zfill(24)  # etat XOR ki # [i-1] car la liste commence à l'indice 0
    
    etat = hex(int(etat, 2))[2:].zfill(6)

    return(etat)


# ####################################
# Enlever les # des 3 lignes précédentes pour executer:
# chiffre = "4c4b41"  # le message chiffre de longueur 6 ecrit en hexa
# cle = "3d637b"  # le msg chiffré de longueur 6 écrit en hexa
# print(main_dechiffrement(chiffre, cle))

