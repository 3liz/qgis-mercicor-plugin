# Intégration des données de la campagne d'observation

Concernant l'intégration des données d'observations on fait soit une saisie via QGIS et le formulaire 
pour l'ajout d'observation :

![form_observation](media/mercicor-form_observ.png)

Soit par l'import fichier Excel.

Enfin pour le calcul des notes Merci-cor des observations et calcul de l'état écologique des habitats
où un algorithme y est dédié.

Il y deux façons de l'utiliser :

* Première façon. Comme tout autre algorithme on le lance, rempli les paramètres puis on l'exécute. Il faut lui renseigner :
    * la couche sur laquelle on effectue les calculs
    * Si l'algorithme effectue les calculs uniquement sur les entités sélectionnées ou pas
    * Si on veut exporter le résultat dans une couche
    * puis si l'on veut ajouter la couche résultat au projet
![calcul_notes](media/mercicor-calcul_notes.png)

* Deuxième façon. On sélectionne la couche dans l'arbre des couches et on entre en mode éditions (image 1 ci-dessous), dans la 
boîte à outils on clique sur `Editer les entités sur place` (bouton sélectionné sur l'image 2 ci-dessous), 
puis on exécute l'algorithme. Si l'on souhaite l'exécuter uniquement sur certaines entités il faut les 
sélectionner avant l'exécution de l'algorithme.

!!! note
    Contrairement à une exécution normale ici aucune boîte de dialogue n'apparaît.

![select_layer_tree](media/mercicor-select_layer.png) ![edit_in_place](media/mercicor-edit_in_place.png)
