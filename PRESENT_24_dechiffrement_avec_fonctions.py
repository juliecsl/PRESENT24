
# ####################################
# LIBRAIRIE
import numpy as np
import time
tps1 = time.time()

# ####################################
# FONCTIONS
def str_en_liste(cle):
    """ Transforme un str en liste un mettant un caractère dans une case de la liste."""
    return [car for car in cle]


def liste_en_str(cle):
    """Transforme une liste en str"""
    return "".join(cle)


def hexa_to_decimal(nb):
    """Convertie en nombre en hexidecimal vers le décimal"""
    return int(nb, 16)


def decimal_to_hexa(nb):
    """Convertie un nombre en décimal en hexadecimal"""
    nb = (hex(int(nb)))  # Donne quelque chose de la forme 0x1ab....
    return nb[2:len(nb)]  # Enlève le 0x


def binaire_to_decimal(nb):
    """Convertie un nombre en binaire en decimal"""
    return int(nb, 2)


def hexa_to_binaire(nb):
    """Convertie un nombre en hexadécimal en binaire"""
    return bin(int(nb, 16))[2:]


def decimal_to_binaire(nb):
    """Convertie un nombre en décimal en binaire"""
    nb = bin(int(nb))
    return nb[2:len(nb)]


def binaire_to_hexa(nb):
    """Convertie un nombre en binaire en hexadecimal"""
    nb = hex(int(nb,2))
    return nb[2:len(nb)]


def XOR(b1, b2):
    """
    Permet de faire le XOR entre b1 et b2
    Entrée: b1 et b2 en décimal
    Sortie: renvoie un décimal
    """
    return b1^b2



def permutation_inv(etat):
    """
    Fonction de permutation du DM
    Entrée: etat un str de longueur 24 en binaire
    Sortie: res un str de longueur 24 en binaire
    """

    liste_permutation = [0, 6, 12, 18, 1, 7, 13, 19, 2, 8, 14, 20, 3, 9, 15, 
                         21, 4, 10, 16, 22, 5, 11, 17, 23]
    return ''.join([etat[i] for i in liste_permutation])


def substitution(etat):
    """
    Fonction de substitution du DM
    Entrée: etat en hexadécimal en str
    Sortie: le resultat de la substitution en hexidécimal en str
    """
    dico = {"0":"c", "1":"5", "2":"6", "3":"b", "4":"9", "5":"0", "6":"a", 
            "7":"d", "8":"3", "9":"e", "a":"f", "b":"8", "c":"4", "d":"7", 
            "e":"1", "f":"2"}

    res = [dico[elem] for elem in etat]
    return ''.join(res)


def substitution_inv(etat):
    """"
    Fonction de substitution inverse
    Entrée: etat en hexadécimal en str
    Sortie: le resultat de la substitution en hexidécimal en str
    """

    dico = { "0": "5", "1": "e", "2": "f", "3": "8", "4": "c", "5": "1", "6": "2",
            "7": "d", "8": "b", "9": "4", "a": "6", "b": "3", "c": "0", "d": "7", 
            "e": "9", "f": "a"}

    res = [dico[elem] for elem in etat]
    return ''.join(res)



def maj_registreK(K, i):
    """
    Met à jour le registre K après avoir déterminer Ki.
    Entrée: K le registre de 80 bits, str
    Sortie:
    """
    liste = str_en_liste(K)
    k = np.roll(liste, -61)  # Fait pivoter le registre K de 61 positions vers la gauche.

    # SUBSTITUTION
    k_prime = k[0:4]  # [k79k78k77k76]
    k_prime = liste_en_str(k_prime)
    k_prime = substitution(binaire_to_hexa(k_prime))

    k_prime = hexa_to_binaire(k_prime)
    while len(k_prime) < 4:  # Si le resultat fait moins de 4 bits alors on rajoute des 0 à gauche
        k_prime = "0" + k_prime

    for j in range(0,4):  # Met le registre K à jour avec les bits permutés
        k[j] = k_prime[j]

    # XOR
    k_prime = k[79-19:79-15+1]  # une liste
    k_prime = decimal_to_binaire(XOR(binaire_to_decimal(liste_en_str(k_prime)), i))  # un str binaire

    while len(k_prime) < 5:  # Si le resultat du XOR fait moins de 5 bits on rajoute des 0 à gauche. 
        k_prime = "0" + k_prime
    k_prime = str_en_liste(k_prime)


    j = 0
    for i in range(79-19,79-15+1):  # Met les bits [k19k18...k15 à jour]
        k[i] = k_prime[j]
        j += 1

    return liste_en_str(k)


def determine_ki(K):
    """
    Determine Ki.
    Entrée: K le registre de 80 bits en str
    Sortie: Ki la sous-clé de 24 bits en str
    """
    liste = str_en_liste(K)
    ki = liste[79-39:79-16+1]  # On garde les bits de k39 à k16

    return liste_en_str(ki)


def main_dechiffrement(chiffre, cle_maitre):
    """
    Entrée: chiffre le message chiffré de 6 bits en hexadécimal en str
            cle_maitre de 6 bits en hexadécimal en str
    Sortie: message déchiffré de 6 bits en hexadécimal en str. 
    """
    K = str(cle_maitre) + str("0"*14)  # registre de 20 bits en hexa
    K = hexa_to_binaire(K)
    K = K.zfill(80)  # verifie que k fait 80 bits, sinon rajoute des 0 à gauche

    liste_ki = [] # Liste permettant de sotcker les ki, le premier element de la liste étant k1

    # Calcul des ki
    for i in range(1, 11+1):  # 11 ki à calculer.
        liste_ki.append(binaire_to_decimal(determine_ki(K)))  # Ajout de ki à la liste de stockage sous forme de décimal car le XOR se fait entre nb décimaux.
        K = maj_registreK(K, i)

    etat = decimal_to_binaire(XOR(hexa_to_decimal(chiffre), liste_ki[11-1]))  # chiffre (etat) XOR k11 (en decimal) # 11-1 car la liste commence à l'indice 0
    etat = etat.zfill(24)

    for i in range(10, 1-1, -1):  # Pour i allant de 10 à 1 inclu
        etat = permutation_inv(etat)  # sous forme de str en binaire
        etat = binaire_to_hexa(etat)
        etat = etat.zfill(6)
        etat = substitution_inv(etat)  # sous forme de str en hexa
        etat = decimal_to_binaire(XOR(liste_ki[i-1], hexa_to_decimal(etat)))  # etat XOR ki # [i-1] car la liste commence à l'indice 0
        etat = etat.zfill(24)
    
    etat = binaire_to_hexa(etat)
    etat = etat.zfill(6)

    return(etat)


print(main_dechiffrement("3d637b", "4c4b41"))