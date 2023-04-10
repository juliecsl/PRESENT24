
# ####################################
# LIBRAIRIE
import numpy as np
import time

t1 = time.time()

# ####################################
# FONCTIONS


def cle_str_en_cle_liste(cle):
    """ Transforme un str en liste un mettant un caractère dans une case de la liste."""
    return [car for car in cle]


def cle_liste_en_cle_str(cle):
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


def determine_ki(K):
    """
    Determine Ki.
    Entrée: K le registre de 80 bits en str
    Sortie: Ki la sous-clé de 24 bits en str
    """

    return K[79-39:79-16+1]  # On garde les bits de k39 à k16  


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
    


def permutation(etat):
    """
    Fonction de permutation du DM
    Entrée: etat un str de longueur 24 en binaire
    Sortie: res un str de longueur 24 en binaire
    """

    liste_permutation = [0, 4, 8, 12, 16, 20, 1, 5, 9, 13, 17, 21, 2, 6, 
                         10, 14, 18, 22, 3, 7, 11, 15, 19, 23]
    return ''.join([etat[i] for i in liste_permutation])


def maj_registreK(K, i):
    """
    Met à jour le registre K après avoir déterminer Ki.
    Entrée: K le registre de 80 bits, str
    Sortie:
    """
    liste = cle_str_en_cle_liste(K)
    k = np.roll(liste, -61)  # Fait pivoter le registre K de 61 positions vers la gauche.

    # SUBSTITUTION
    k_prime = cle_liste_en_cle_str(k[0:4])  # liste en str de [k79k78k77k76]
    k_prime = substitution(binaire_to_hexa(k_prime))

    k_prime = hexa_to_binaire(k_prime).zfill(4)  # hexa en binaire + Si le resultat fait moins de 4 bits alors on rajoute des 0 à gauche

    for j in range(0,4):  # Met le registre K à jour avec les bits permutés
        k[j] = k_prime[j]

    # XOR
    k_prime = k[79-19:79-15+1]  # une liste
    k_prime = decimal_to_binaire(XOR(binaire_to_decimal(cle_liste_en_cle_str(k_prime)), i))  # un str binaire

    k_prime = k_prime.zfill(5) # Si le resultat du XOR fait moins de 5 bits on rajoute des 0 à gauche. 
    k_prime = cle_str_en_cle_liste(k_prime)


    j = 0
    for i in range(79-19,79-15+1):  # Met les bits [k19k18...k15 à jour]
        k[i] = k_prime[j]
        j += 1

    return cle_liste_en_cle_str(k)



def main_chiffrement(m, CLE_MAITRE):
    """
    Algorithme 1 de l'énonce du DM
    Entrée: m le message à chiffrer en hexidécimal sous forme de str de taille 6
            CLE_MAITRE le clé maitre en héxidécimal sous forme de str de taille 6
    Sortie: le message chiffré en hexidécimal.
    """

    K = str(CLE_MAITRE) + str("0"*14)  # registre de 20 bits en hexa
    K = hexa_to_binaire(K)
    K = K.zfill(80)  # Si le resultat de la conversion en hex fait moins de 80 bits on rajoute des 0 à gauche. 
    
    j = 0
    etat = hexa_to_binaire(m)
    for i in range(1, 10+1):
        j += 1
        ki = determine_ki(K)  # en binaire
        K = maj_registreK(K, i)

        etat = decimal_to_hexa(XOR(binaire_to_decimal(etat), (binaire_to_decimal(ki))))  # renvoie l'etat en hexa du resultat du XOR entre l'état et ki
        etat = etat.zfill(6) # Si le resultat du XOR fait moins de 24 bits on rajoute des 0 à gauche. 
            

        etat = substitution(etat)  # etat toujours en hexadecimal en str

        etat = hexa_to_binaire(etat)
        etat = etat.zfill(24) # Si le resultat du XOR fait moins de 24 bits on rajoute des 0 à gauche. 
        etat = permutation(etat)  # str de 24 bits en binaire

    ki = determine_ki(K)  # k11
    etat = decimal_to_hexa(XOR(binaire_to_decimal(etat), binaire_to_decimal(ki)))
    return etat


print(main_chiffrement("aaabbb", "000003"))
t2 = time.time()
print(t2-t1)
