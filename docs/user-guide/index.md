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

```mermaid
graph TD
Projet[Création du projet : geopackage et style]
click Projet "/private/um3-mercicor/docs/user-guide/initialisation-projet/"
Habitat[Import des données habitat]
click Habitat "/private/um3-mercicor/docs/user-guide/import-donnees-habitats/#import-dans-le-projet"
VérificationUnicité[Vérification de l'unicité nom/faciès]
click VérificationUnicité "/private/um3-mercicor/docs/user-guide/import-donnees-habitats/#verification-de-lunicite-nomfacies"
ObservationsExport[Préparation de la campagne]
click ObservationsExport "/private/um3-mercicor/docs/user-guide/preparation-observations/"
ObservationsImport[Import de la campagne]
click ObservationsImport "/private/um3-mercicor/docs/user-guide/integration-campagne/#integration-des-donnees"
CalculNotesMercicor[Calcul des notes mercicor]
click CalculNotesMercicor "/private/um3-mercicor/docs/user-guide/integration-campagne/#calcul-des-notes-merci-cor"
Pression[Import des pression]
click Pression "/private/um3-mercicor/docs/user-guide/etude-scenario/#integration-des-donnees-pressions"
ScénarioPression{{Création d'un scénario}}
click ScénarioPression "/private/um3-mercicor/docs/user-guide/etude-scenario/#gestion-des-scenarios"
EtatEcologique[État écologique des habitats]
click EtatEcologique "/private/um3-mercicor/docs/user-guide/calcul-etat-ecologique/#calcul-de-letat-ecologique-des-habitats"
EtatEcologiqueHabitatPression[Habitat pression état écologique]
click EtatEcologiqueHabitatPression "/private/um3-mercicor/docs/user-guide/habitat-pression-etat-ecologique/"
Pertes[Calcul des pertes]
click Pertes "/private/um3-mercicor/docs/user-guide/pertes/"

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
