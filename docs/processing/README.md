---
hide:
  - navigation
---

# Processing

## Calcul


### Calcul des notes MERCI-Cor

Calcul des notes MERCI-Cor à partir des indicateurs MERCI-Cor

![algo_id](./mercicor-calcul_notes.png)

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


## Administration


### Créer le geopackage de la zone d'étude

Pour commencer une nouvelle zone d'étude, vous devez d'abord créer le geopackage.

![algo_id](./mercicor-create_geopackage_project.png)

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

Les relations vont aussi être chargés dans le projet.

![algo_id](./mercicor-load_qml_and_relations.png)

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
RELATIONS_ADDED|Nombre de relations chargés|Number||
QML_LOADED|Nombre de QML chargés|Number||


***


## Export


### Télécharger le modèle des observations

Télécharger le modèle de fichier tableur pour les observations.

![algo_id](./mercicor-download_observation_file.png)

#### Parameters

| ID | Description | Type | Info | Required | Advanced | Option |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
INPUT_LAYER|Couche des observations dans le geopackage|VectorLayer|Couche des observations dans le geopackage|✓||Default: observations <br> Type: TypeVectorPoint <br>|
INCLUDE_X_Y|Inclure des colonnes avec latitude/longitude|Boolean|Inclure des colonnes avec latitude/longitude|✓||Default: True <br> |
DESTINATION_FILE|Fichier tableur de destination|FileDestination|Fichier tableur de destination|✓|||


#### Outputs

| ID | Description | Type | Info |
|:-:|:-:|:-:|:-:|
DESTINATION_FILE|Fichier tableur de destination|File||


***


## Import


### Import données habitat

Import des données des habitats. Le champ du faciès doit être correctement formaté.

![algo_id](./mercicor-import_donnees_habitat.png)

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


### Import données pression

Import des données de pression.

Le champ des pressions doit être correctement formaté : 
1, 2, 3, 4, 5, 6, NULL

![algo_id](./mercicor-import_donnees_pression.png)

#### Parameters

| ID | Description | Type | Info | Required | Advanced | Option |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
INPUT_LAYER|Couche pour l'import|VectorLayer||✓||Type: TypeVectorPolygon <br>|
PRESSURE_FIELD|Champ comportant la pression|Field||✓|||
SCENARIO_NAME|Nom du scénario|String|Le nom du scénario en cours pour cette couche des pressions.|✓|||
SCENARIO_LAYER|Couche des scénarios de destination|VectorLayer|La couche de destination des scénarios doit être la couche qui est dans le geopackage.|✓||Default: scenario_pression <br> Type: TypeVector <br>|
OUTPUT_LAYER|Couche des pressions de destination|VectorLayer||✓||Default: pression <br> Type: TypeVectorPolygon <br>|


#### Outputs

| ID | Description | Type | Info |
|:-:|:-:|:-:|:-:|
No output

***

