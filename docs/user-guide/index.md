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
* [Habitat pression état écologique](./habitat-pression-etat-ecologique.md)
* [Pertes](./pertes.md)

## Diagramme

### Projet de pression

```mermaid
graph TD
Projet[Création du projet : geopackage et style]
click Projet "/qgis-mercicor-plugin/user-guide/initialisation-projet/"
Habitat[Import des données habitat]
click Habitat "/qgis-mercicor-plugin/user-guide/import-donnees-habitats/#import-dans-le-projet"
VérificationUnicité[Vérification de l'unicité nom/faciès]
click VérificationUnicité "/qgis-mercicor-plugin/user-guide/import-donnees-habitats/#verification-de-lunicite-nomfacies"
ObservationsExport[Préparation de la campagne]
click ObservationsExport "/qgis-mercicor-plugin/user-guide/preparation-observations/"
ObservationsImport[Import de la campagne]
click ObservationsImport "/qgis-mercicor-plugin/user-guide/integration-campagne/#integration-des-donnees"
CalculNotesMercicor[Calcul des notes mercicor]
click CalculNotesMercicor "/qgis-mercicor-plugin/user-guide/integration-campagne/#calcul-des-notes-merci-cor"
Pression[Import des pression]
click Pression "/qgis-mercicor-plugin/user-guide/etude-scenario/#integration-des-donnees-pressions"
ScénarioPression{{Création d'un scénario}}
click ScénarioPression "/qgis-mercicor-plugin/user-guide/etude-scenario/#gestion-des-scenarios"
EtatEcologique[État écologique des habitats]
click EtatEcologique "/qgis-mercicor-plugin/user-guide/calcul-etat-ecologique/#calcul-de-letat-ecologique-des-habitats"
EtatEcologiqueHabitatPression[Habitat pression état écologique]
click EtatEcologiqueHabitatPression "/qgis-mercicor-plugin/user-guide/habitat-pression-etat-ecologique/"
Pertes[Calcul des pertes]
click Pertes "/qgis-mercicor-plugin/user-guide/pertes/"

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

### Projet de compensation

```mermaid
graph TD
Projet[Création du projet : geopackage et style]
Habitat[Import des données habitat]
VérificationUnicité[Vérification de l'unicité nom/faciès]
ObservationsExport[Préparation de la campagne]
ObservationsImport[Import de la campagne]
CalculNotesMercicor[Calcul des notes mercicor]
Compensation[Import des compensations]
ScénarioCompensation{{Création d'un scénario}}
EtatEcologique[État écologique des habitats]
EtatEcologiqueHabitatCompensation[Habitat compensation état écologique]
Gains[Calcul des gains]

Projet --> Habitat
Projet --> ObservationsExport
Projet --> Compensation

subgraph Données Habitats
Habitat <--> VérificationUnicité
end
subgraph Données Observations
ObservationsExport --> ObservationsImport
ObservationsImport --> CalculNotesMercicor
end
subgraph Données Compensation
Compensation-- Implique ---ScénarioCompensation
end
Habitat --> EtatEcologique
CalculNotesMercicor --> EtatEcologique
EtatEcologique -->EtatEcologiqueHabitatCompensation
Compensation --> EtatEcologiqueHabitatCompensation
EtatEcologiqueHabitatCompensation --> Gains
ScénarioCompensation --> Gains
```

![create_gpkg](media/mercicor-barre_outils.jpg)
