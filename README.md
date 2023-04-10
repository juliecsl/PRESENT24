# PRESENT24
## Présentation du projet
* Chiffrement et déchiffrement du chiffrement par bloc PRESENT24 inspiré du chiffrement PRESENT.
* Implantation de l’attaque par le milieu (meet in the middle) sur la version double 2PRESENT24.
* Pour plus d'information vous pouvez lire le pdf: [sujet_projet.pdf](https://github.com/juliecsl/PRESENT24/blob/main/sujet_projet.pdf)


## Prérequis
### Matériel nécessaire
Il est nécessaire d'executer le code sur un ordinateur ayant au moins 8 CPU, en effet, à un moment le programme s'execute sur 8 CPU pour accélérer les calculs. 

### Execution du code
Pour executer, il faut l'executer sur VSCODE, éditeur de code pour Windows, Linux et macOS.

### Librairies nécessaires
Les librairies nécessaires à l'execution du code sont normalement déjà installées par défaut, dans le cas contraire il est nécessaire de les télécharger:

- datetime

```bash
pip install datetime
```
- multiprocessing

```bash
pip install multiprocessing
```

### Version Python
3.8.16


## Utilisation du projet
Pour entrer ses propres clés, messages chiffrés, messages clairs, il est necessaire de modifier direcement les valeurs dans le code.
- [PRESENT24_chiffrement.py](https://github.com/juliecsl/PRESENT24/blob/main/src/PRESENT24_chiffrement.py) les valeurs sont à changer dans le **bas** du code: lignes 101 et 102.
- [PRESENT24_dechiffrement.py](https://github.com/juliecsl/PRESENT24/blob/main/src/PRESENT24_dechiffrement.py) les valeurs sont à changer dans le **bas** du code: lignes 96 et 97.
- Attaque_par_le_milieu: les valeurs sont à changer dans le **haut** du code: lignes 8 à 11.

Pour executer le fichier [PRESENT_24_chiffrement.py](https://github.com/juliecsl/PRESENT24/blob/main/src/PRESENT24_chiffrement.py) et [PRESENT_24_déchiffrement.py](https://github.com/juliecsl/PRESENT24/blob/main/src/PRESENT24_dechiffrement.py) il est necessaire d'appeler la fonction en bas du programme en enlevant les # lignes:
- 101 à 103 pour le chiffrement
- 96 à 98 pour le déchiffrement.

Pour faire l'attaque par le milieu, il faut executer le programme [attaque_par_le_milieu.py](https://github.com/juliecsl/PRESENT24/blob/main/src/attaque_par_le_milieu.py) (qui va créer 8 fichiers .txt) et qui prend environ 20 minutes.
(Le résultat des clés trouvées peut se cacher dans les prints du terminal, pensez à remonter dans le terminal pour voir tous les couples de clés trouvés.)

## Autre
Vous trouverez dans le dossier des programmes .py nommés PRESENT24_dechiffrement_avec_fonctions.py et PRESENT24_dechiffrement_avec_fonctions.py qui sont des programmes faisant la meme chose que [PRESENT24_chiffrement.py](https://github.com/juliecsl/PRESENT24/blob/main/src/PRESENT24_chiffrement.py) et [PRESENT24_dechiffrement.py](https://github.com/juliecsl/PRESENT24/blob/main/src/PRESENT24_dechiffrement.py) mais qui diffèrent en grande partie par leur implémentation avec plein de petites fonctions pour rendre la lecture du programme plus simple.
