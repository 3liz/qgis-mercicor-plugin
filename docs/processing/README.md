---
hide:
  - navigation
---

# Processing

## Calcul


### Calcul de l'état écologique des habitats

Calcul de l'état écologique des habitats à partir des données d'observations :
- Vérification de l'unicité du facies
- Jointure de données
- Calcul des notes

![algo_id](./mercicor-calcul_habitat_etat_ecologique.jpg)

#### Parameters

| ID | Description | Type | Info | Required | Advanced | Option |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
HABITAT|Couche habitat|VectorLayer||✓||Default: habitat <br> Type: TypeVectorPolygon <br>|
OBSERVATIONS|Couche observations|VectorLayer||✓||Default: observations <br> Type: TypeVectorPoint <br>|
HABITAT_ETAT_ECOLOGIQUE|Table habitat état écologique|VectorLayer||✓||Default: habitat_etat_ecologique <br> Type: TypeVectorAnyGeometry <br>|


#### Outputs

| ID | Description | Type | Info |
|:-:|:-:|:-:|:-:|
No output

***


### Ajout des entités de l'état écologique des habitats en fonction de la pression

Ajout des entités de l'état écologique des habitats en fonction des pressions.

![algo_id](./mercicor-calcul_habitat_pression_etat_ecologique.jpg)

#### Parameters

| ID | Description | Type | Info | Required | Advanced | Option |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
HABITAT_LAYER|Couches des habitats|VectorLayer|Couche des habitats dans le geopackage|✓||Default: habitat <br> Type: TypeVectorPolygon <br>|
PRESSION_LAYER|Couches des pressions|VectorLayer|Couche des pressions dans le geopackage|✓||Default: pression <br> Type: TypeVectorPolygon <br>|
HABITAT_PRESSION_ETAT_ECOLOGIQUE_LAYER|Couches habitat pression état écologique|VectorLayer|Couches habitat pression état écologique dans le geopackage|✓||Default: habitat_pression_etat_ecologique <br> Type: TypeVectorPolygon <br>|


#### Outputs

| ID | Description | Type | Info |
|:-:|:-:|:-:|:-:|
No output

***


### Calcul des notes MERCI-Cor

Calcul des notes MERCI-Cor à partir des indicateurs MERCI-Cor

Liste des notes :
note_bsd = (("bsd_recouv_cor" + "bsd_p_acrop" + "bsd_vital_cor" + "bsd_comp_struc" + "bsd_taille_cor" + "bsd_dens_juv" + "bsd_f_sessile" + "bsd_recouv_ma") / 8.0) * (10.0 / 3.0)
note_bsm = (("bsm_fragm_herb" + "bsm_recouv_her" + "bsm_haut_herb" + "bsm_dens_herb" + "bsm_div_herb" + "bsm_epibiose") / 6.0) * (10.0 / 3.0)
note_ben = CASE WHEN "note_bsd" IS NULL THEN "note_bsm" WHEN "note_bsm" IS NULL THEN "note_bsd" ELSE "note_bsd" * "perc_bsd" + "note_bsm" * "perc_bsm" END
note_man = (("man_fragm" + "man_recouv" + "man_diam_tronc" + "man_dens" + "man_diversit" + "man_vital") / 6.0) * (10.0 / 3.0)
note_pmi = (("pmi_div_poi" + "pmi_predat_poi" + "pmi_scarib_poi" + "pmi_macro_inv") / 4) * (10 / 3)
score_mercicor = CASE WHEN lower(to_string("station_man")) = 'true' THEN ("note_man" + "note_pmi") / 2 ELSE ("note_ben" + "note_pmi") / 2 END


![algo_id](./mercicor-calcul_notes.jpg)

#### Parameters

| ID | Description | Type | Info | Required | Advanced | Option |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
INPUT|Input layer|FeatureSource||✓|||
OUTPUT|output|FeatureSink||✓||Type: TypeVector <br>|


#### Outputs

| ID | Description | Type | Info |
|:-:|:-:|:-:|:-:|
OUTPUT|output|VectorLayer||


***


### Calcul des notes de perte pour le scénario de pression

Calcul des notes de pertes à partir des indicateurs MERCI-Cor

Liste des notes :
perte_bsd = La somme de '("hab_note_bsd" - "note_bsd") * surface', filtré par scénario
perte_bsm = La somme de '("hab_note_bsm" - "note_bsm") * surface', filtré par scénario
perte_man = La somme de '("hab_note_man" - "note_man") * surface', filtré par scénario
perte_pmi = La somme de '("hab_note_pmi" - "note_pmi") * surface', filtré par scénario
perte_ben = La somme de '("hab_note_ben" - "note_ben") * surface', filtré par scénario
perte_mercicor = La somme de '("hab_score_mercicor" - "score_mercicor") * surface', filtré par scénario


![algo_id](./mercicor-calcul_pertes.jpg)

#### Parameters

| ID | Description | Type | Info | Required | Advanced | Option |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
HABITAT_PRESSION_ETAT_ECOLOGIQUE|Couche habitat pression état écologique|VectorLayer||✓||Default: habitat_pression_etat_ecologique <br> Type: TypeVectorPolygon <br>|
SCENARIO_PRESSION|Table scénario pression|VectorLayer||✓||Default: scenario_pression <br> Type: TypeVectorAnyGeometry <br>|


#### Outputs

| ID | Description | Type | Info |
|:-:|:-:|:-:|:-:|
No output

***


### Calcul unicité habitat/faciès

Vérification des données des habitats.
Les champs nom et faciès doivent être unique par objet géographique.


![algo_id](./mercicor-calcul_unicity_habitat.jpg)

#### Parameters

| ID | Description | Type | Info | Required | Advanced | Option |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
INPUT|Couche habitat|VectorLayer||✓||Default: habitat <br> Type: TypeVectorPolygon <br>|
OUTPUT|Couche des habitat/faciès à unifier|FeatureSink||||Type: TypeVectorPoint <br>|


#### Outputs

| ID | Description | Type | Info |
|:-:|:-:|:-:|:-:|
OUTPUT|Couche des habitat/faciès à unifier|VectorLayer||
NUMBER_OF_UNIQUE|Nombre de couple habitat/faciès unique|Number||
NUMBER_OF_NON_UNIQUE|Nombre de couple habitat/faciès non unique|Number||


***


## Administration


### Créer le geopackage de la zone d'étude

Pour commencer une nouvelle zone d'étude, vous devez d'abord créer le geopackage.

![algo_id](./mercicor-create_geopackage_project.jpg)

#### Parameters

| ID | Description | Type | Info | Required | Advanced | Option |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
FILE_GPKG|Fichier Geopackage|FileDestination||✓|||
PROJECT_NAME|Nom de la zone d'étude|String||✓|||
PROJECT_CRS|CRS du project|Crs||✓||Default: EPSG:2154 <br> |
PROJECT_EXTENT|Emprise du projet|Extent||✓|||


#### Outputs

| ID | Description | Type | Info |
|:-:|:-:|:-:|:-:|
FILE_GPKG|Fichier Geopackage|File||
OUTPUT_LAYERS|Couches de sorties|MultipleLayers||


***


### Charger les styles

Charger les styles pour les différentes couches.

Les relations et les jointures vont également être chargés dans le projet.

![algo_id](./mercicor-load_qml_and_relations.jpg)

#### Parameters

| ID | Description | Type | Info | Required | Advanced | Option |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
PRESSURE_LAYER|Couche des pressions|VectorLayer||✓||Default: pression <br> Type: TypeVectorPolygon <br>|
HABITAT_LAYER|Couche des habitats|VectorLayer||✓||Default: habitat <br> Type: TypeVectorPolygon <br>|
PRESSURE_LIST_LAYER|Liste des types de pression|VectorLayer||✓||Default: liste_type_pression <br> Type: TypeVectorPolygon <br>|
OBSERVATIONS_LAYER|Couches des observations|VectorLayer||✓||Default: observations <br> Type: TypeVectorPoint <br>|
HABITAT_ETAT_ECOLOGIQUE_LAYER|Table des observations ramenées à l'habitat|VectorLayer||✓||Default: habitat_etat_ecologique <br> Type: TypeVectorPolygon <br>|
SCENARIO_PRESSION|Couche des scénario de pression|VectorLayer||✓||Default: scenario_pression <br> Type: TypeVectorPolygon <br>|
HABITAT_PRESSION_ETAT_ECOLOGIQUE|Couche du résultat de l'intersection entre les pressions et les habitats.|VectorLayer||✓||Default: habitat_pression_etat_ecologique <br> Type: TypeVectorPolygon <br>|


#### Outputs

| ID | Description | Type | Info |
|:-:|:-:|:-:|:-:|
JOINS_ADDED|Nombre de jointures chargées|Number||
ACTIONS_ADDED|Nombre d'actions chargées|Number||
RELATIONS_ADDED|Nombre de relations chargées|Number||
QML_LOADED|Nombre de QML chargés|Number||


***


## Export


### Télécharger le modèle des observations

Télécharger le modèle de fichier tableur pour les observations.

![algo_id](./mercicor-download_observation_file.jpg)

#### Parameters

| ID | Description | Type | Info | Required | Advanced | Option |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
INPUT_LAYER|Couche des observations dans le geopackage|VectorLayer|Couche des observations dans le geopackage|✓||Default: observations <br> Type: TypeVectorPoint <br>|
INCLUDE_X_Y|Inclure des colonnes avec latitude/longitude|Boolean|Inclure des colonnes avec latitude/longitude|✓||Default: True <br> |
HABITAT_LAYER|Couche des habitats dans le geopackage|VectorLayer|Couche des habitats dans le geopackage|||Default: habitat <br> Type: TypeVectorPolygon <br>|
DESTINATION_FILE|Fichier tableur de destination|FileDestination|Fichier tableur de destination|✓|||


#### Outputs

| ID | Description | Type | Info |
|:-:|:-:|:-:|:-:|
DESTINATION_FILE|Fichier tableur de destination|File||


***


## Import


### Import données habitat

Import des données des habitats.
Le champ du faciès doit être correctement formaté.
Un style pour les habitats sera ajouté.


![algo_id](./mercicor-import_donnees_habitat.jpg)

#### Parameters

| ID | Description | Type | Info | Required | Advanced | Option |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
INPUT_LAYER|Couche pour l'import|VectorLayer||✓||Type: TypeVectorPolygon <br>|
NAME_FIELD|Champ comportant le nom de l'habitat|Field||✓|||
FACIES_FIELD|Champ comportant le faciès|Field||✓|||
OUTPUT_LAYER|Couche des habitats de destination|VectorLayer||✓||Default: habitat <br> Type: TypeVectorPolygon <br>|


#### Outputs

| ID | Description | Type | Info |
|:-:|:-:|:-:|:-:|
No output

***


### Import données observation

Import des données des observations.

L'algortihme peut soit mettre à jour des observations existantes ou alors les rajouter dans la table destinaton.
Pour cela, l'algorithme s'appuie sur le ID de la station.


![algo_id](./mercicor-import_donnees_observation.jpg)

#### Parameters

| ID | Description | Type | Info | Required | Advanced | Option |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
INPUT_LAYER|Couche pour l'import des observations|VectorLayer||✓||Type: TypeVector <br>|
OUTPUT_LAYER|Couche des observations de destination|VectorLayer||✓||Default: observations <br> Type: TypeVectorPoint <br>|


#### Outputs

| ID | Description | Type | Info |
|:-:|:-:|:-:|:-:|
No output

***


### Import données pression

Import des données de pression.

Le champ des pressions doit être correctement formaté : 
1, 2, 3, 4, 5, 6, NULL
Un scénario sera également crée et la couche sera filtrée pour ce scénario.
Il est également possible de lancer directement le calcul de l'état écologique des habitats en fonction de la pression à l'aide de la case à cocher.

![algo_id](./mercicor-import_donnees_pression.jpg)

#### Parameters

| ID | Description | Type | Info | Required | Advanced | Option |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
INPUT_LAYER|Couche pour l'import|VectorLayer||✓||Type: TypeVectorPolygon <br>|
PRESSURE_FIELD|Champ comportant la pression|Field||✓|||
SCENARIO_NAME|Nom du scénario|String|Le nom du scénario en cours pour cette couche des pressions.|✓|||
SCENARIO_LAYER|Couche des scénarios de destination|VectorLayer|La couche de destination des scénarios doit être la couche qui est dans le geopackage.|✓||Default: scenario_pression <br> Type: TypeVector <br>|
OUTPUT_LAYER|Couche des pressions de destination|VectorLayer||✓||Default: pression <br> Type: TypeVectorPolygon <br>|
APPLY_CALCUL_HABITAT_PRESSION_ETAT_ECOLOGIQUE|Ajout des entités de l'état écologique des habitats en fonction de la pression.|Boolean||✓|||
HABITAT_LAYER|Couche des habitats de destination|VectorLayer||||Default: habitat <br> Type: TypeVectorPolygon <br>|
HABITAT_PRESSION_LAYER|Couche des habitats pressions état écologique de destination|VectorLayer||||Default: habitat_pression_etat_ecologique <br> Type: TypeVectorPolygon <br>|


#### Outputs

| ID | Description | Type | Info |
|:-:|:-:|:-:|:-:|
No output

***

