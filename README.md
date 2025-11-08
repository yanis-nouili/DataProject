"# DataProject" 
# Projet Data — Analyse du trafic routier à Rennes

## Objectif du projet
Ce projet a pour but d’analyser et de visualiser le **trafic routier sur Rennes Métropole** à partir des données ouvertes disponibles sur la plateforme [Open Data Rennes Métropole](https://www.data.gouv.fr/datasets/etat-du-trafic-en-temps-reel/).  

L’application a été développée en **Python** avec le framework **Dash (Plotly)**, afin de construire un tableau de bord interactif permettant :
- d’explorer les vitesses moyennes des véhicules,  
- de filtrer par statut du trafic ou par vitesse,  
- et de visualiser la situation du trafic sur une carte.


## Contexte et sources de données
Les données proviennent de la plateforme **Open Data Rennes Métropole**, mise à jour en temps réel.  
Elles contiennent des informations sur :
- la vitesse moyenne observée sur chaque tronçon routier,  
- le temps de parcours,  
- le statut du trafic (`freeFlow`, `heavy`, `congested`, `unknown`),  
- les coordonnées géographiques (`Geo Point`),  
- la vitesse maximale autorisée (`vitesse_maxi`),  
- ainsi que des informations de hiérarchie et de dénomination des routes.


## Préparation et nettoyage des données
Un premier travail de nettoyage a été effectué afin de rendre les données exploitables et de garder les plus nécessaires pour notre projet.

### Étapes de préparation :
1. **Lecture du CSV brut** depuis `data/raw/`.
2. **Séparation** de la colonne `Geo Point` en deux colonnes distinctes `lat` et `lon`.
3. **Conversion** du champ `datetime` au format temporel.
4. **Suppression** des colonnes inutiles (informations administratives redondantes).
5. **Sauvegarde** du fichier nettoyé dans `data/processed/etat_du_trafic_clean.csv`.

Ce nettoyage a été réalisé dans le script :
main.py

## Filtres disponibles dans l’application

L’application Dash permet d’explorer les données grâce à plusieurs filtres interactifs :

**Statut du trafic** : Permet de sélectionner un ou plusieurs statuts parmi `freeFlow`, `heavy`, `congested`, `unknown`.
**Vitesse minimale** : Filtre les tronçons dont la vitesse moyenne est **supérieure** à la valeur choisie. 
**Vitesse maximale autorisée** : Filtre les tronçons dont la vitesse limite est **inférieure** à la valeur choisie.

Chaque filtre met automatiquement à jour :
- l’**histogramme** des vitesses moyennes,
- la **carte interactive** représentant le trafic sur Rennes.
![Filtres du dashboard](images/filtres.png)


## Visualisations principales

### Histogramme des vitesses moyennes
Cet histogramme montre la distribution des vitesses moyennes observées sur l’ensemble du réseau routier de Rennes.

![Histogramme](images/histogramme.png)


### Carte du trafic à Rennes
La carte interactive permet de visualiser le trafic en fonction de son **statut** (`freeFlow`, `heavy`, `congested`, `unknown`) et de la **vitesse moyenne des véhicules**.

Chaque point représente un tronçon routier :
- La **couleur** indique le statut du trafic.
- La **taille** correspond à la vitesse moyenne.

![Carte du trafic](images/carte_rennes.png)


