
# ####################################
# LIBRAIRIE
import numpy as np
import time

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
    # k_prime = "".join(k[0:4])  # liste en str de [k79k78k77k76]
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



def main_chiffrement(m, CLE_MAITRE):
    """
    Algorithme 1 de l'énonce du DM
    Entrée: m le message à chiffrer en hexidécimal sous forme de str de taille 6
            CLE_MAITRE le clé maitre en héxidécimal sous forme de str de taille 6
    Sortie: le message chiffré en hexidécimal.
    """
    dico_substitution = {"0":"c", "1":"5", "2":"6", "3":"b", "4":"9", "5":"0", "6":"a", 
                        "7":"d", "8":"3", "9":"e", "a":"f", "b":"8", "c":"4", "d":"7", 
                        "e":"1", "f":"2"}
    
    liste_permutation = [0, 4, 8, 12, 16, 20, 1, 5, 9, 13, 17, 21, 2, 6, 
                         10, 14, 18, 22, 3, 7, 11, 15, 19, 23]

    K = str(CLE_MAITRE) + str("0"*14)  # registre de 20 bits en hexa
    K = bin(int(K, 16))[2:].zfill(80)  # Convertie de l'hexa vers le binaire  # Si le resultat de la conversion en hex fait moins de 80 bits on rajoute des 0 à gauche. 
    
    j = 0
    etat = bin(int(m, 16))[2:]  # Hexa to binaire
    for i in range(1, 10+1):
        j += 1
        ki = K[79-39:79-16+1]  # en binaire  # determine ki
        K = maj_registreK(K, i, dico_substitution)

        etat = hex(int(etat, 2) ^ int(ki, 2))[2:]  # renvoie l'etat en hexa du resultat du XOR entre l'état et ki
        etat = etat.zfill(6) # Si le resultat du XOR fait moins de 24 bits on rajoute des 0 à gauche. 
            
        # SUBSTITUTION

        res = [dico_substitution[elem] for elem in etat]
        etat = ''.join(res)

        # #####################

        etat = bin(int(etat, 16))[2:]  # Hexa to binaire
        etat = etat.zfill(24) # Si le resultat du XOR fait moins de 24 bits on rajoute des 0 à gauche. 
        
        # PERMUTATION
        etat = ''.join([etat[i] for i in liste_permutation])
        # ########################

    ki = K[79-39:79-16+1]   # k11  # determine ki
    etat = hex(int(etat, 2) ^ int(ki, 2))[2:]  # etat XOR ki
    return etat


# ####################################
# Enlever les # des 3 lignes précédentes pour executer:
# clair = "aaabbb"  # msg clair de longueur 6 écrit un hexadécimal
# cle = "000003"  # clé de longueur 6 écrit un hexadécimal
# print(main_chiffrement(clair, cle))
