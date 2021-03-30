# CHANGELOG

## 0.6.0 - 2021-03-XX

* Ajout de plusieurs champs à la couche "scenario_pression"
* Ajout de l'algorithme concernant l'habitat pression état écologique
* Ajout de la correction des géométries dans les algorithmes d'import
* Ajout d'une vérification pour que les couches soient dans le geopackage
* Ajout de l'algorithme pour compléter la couche "habitat_pression_etat_ecologique"
* Correction d'une jointure sur la couche "habitat"
* Correction d'une erreur lors de la génération du projet
* Correction de l'application des jointures sur l'ensemble du projet
* Mise à jour de la documentation

## 0.5.0 - 2021-03-24

* Ajout de l'algorithme du calcul des états écologiques des habitats
* Ajout d'une documentation concernant le modèle de données https://packages.3liz.org/private/um3-mercicor/docs/model/
* Ajout du nom de l'habitat lors de l'export en XLSX
* Ajout d'un bouton pour ouvrir l'aide en ligne depuis le menu d'aide
* Correction pour les algorithmes devant utiliser un fichier de destination
* Correction de l'action QGIS pour changer de scénario depuis la table attributaire
* Mise à jour de la documentation https://packages.3liz.org/private/um3-mercicor/docs/

## 0.4.0 - 2021-03-23

* Ajout d'une action sur la table des "scénarios" pour changer le filtre en cours
* Ajout du champ "profondeur" pour les observations
* Ajout des alias sur les champs pour une meilleure compréhension des champs
* Ajout d'un style par défaut lors de l'import des habitats avec une catégorisation
* Ajout du support de la mise à jour des observations depuis le fichier tableur pour des observations existantes
* Ajout d'un algorithme pour vérifier l'unicité nom/faciès dans la couche habitat
* Ajout du faciès lors de l'export des observations au format XLSX
* Ajout d'une correction automatique pour les géométries lors de l'import des habitats et des pressions
* Ajout d'une transformation en multipolygons des habitats et des pressions lors de l'import
* Amélioration de la documentation

## 0.3.1 - 2021-03-16

* Modification de l'aide des algorithmes
* Mise à jour de la documentation

## 0.3.0 - 2021-03-16

* Ajout du type de pression "Emprise"
* Ajout de la couche "habitat_pression_etat_ecologique"
* Ajout de la notion de scénario lors de l'import des pressions
* Ajout de l'algorithme de calcul des notes mercicor
* Ajout de l'export de la couche des observations au format tableur
* Ajout de l'algorithme d'import des données observations
* Mise à jour de la documentation utilisateur
* Mise à jour du formulaire des observations
* Remplacement du champ "score_station" par "score_mercicor"

## 0.2.0 - 2021-03-09

* Mise à jour de la table habitat et de l'import des données
* Mise à jour de la table des pressions et de l'import des données
* Ajout de la table des observations
* Ajout de la table des résultats des observations ramenées à l'habitat
* Ajout de la table des scénarios
* Relecture des étiquettes dans les algorithmes Processing
* Lancement des tests unitaires sur QGIS 3.10 et QGIS 3.16

## 0.1.0 - 2021-02-23

* Première version de l'extension
* Import des données pressions et habitats

##
