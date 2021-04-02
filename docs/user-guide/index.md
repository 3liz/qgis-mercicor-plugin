# Guide d'utilisation

## Déroulement

Une fois [installé](./installation.md), pour utiliser l'outil, il faut se rendre dans la boîte à outils de traitements de QGIS.

Il y a plusieurs étapes : 

* [Création du projet](./initialisation-projet.md)
* [Import des données habitats](./import-donnees-habitats.md)
* [Préparation de la campagne d'observations](./preparation-observations.md)
* [Intégration des données d'observations](./integration-campagne.md)
* [Calcul de l'état écologique des habitats](./calcul-etat-ecologique.md)
* [Étude des scénarios](./etude-scenario.md)

## Diagramme

```mermaid
graph TD
Projet[Création du projet : geopackage et style]
Habitat[Import des données habitat]
VérificationUnicité[Vérification de l'unicité nom/faciès]
ObservationsExport[Préparation de la campagne]
ObservationsImport[Import de la campagne]
CalculNotesMercicor[Calcul des notes mercicor]
Pression[Import des pression]
ScénarioPression{{Création d'un scénario}}
EtatEcologique[État écologique des habitats]
EtatEcologiqueHabitatPression[Habitat pression état écologique]
Pertes[Calcul des pertes]

Projet --> Habitat
Projet --> ObservationsExport
Projet --> Pression

subgraph Données Habitats
Habitat <--> VérificationUnicité
end
subgraph Données Observations
ObservationsExport --> ObservationsImport
ObservationsImport --> CalculNotesMercicor
end
subgraph Données Pressions
Pression-- Implique ---ScénarioPression
end
Habitat --> EtatEcologique
CalculNotesMercicor --> EtatEcologique
EtatEcologique -->EtatEcologiqueHabitatPression
Pression --> EtatEcologiqueHabitatPression
EtatEcologiqueHabitatPression --> Pertes
ScénarioPression --> Pertes
```

![create_gpkg](media/mercicor-barre_outils.jpg)
