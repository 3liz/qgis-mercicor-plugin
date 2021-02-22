---
hide:
  - navigation
---

# Processing

## Administration


### Create geopackage project

To start a blank new project, you need to create first a geopackage file.

![algo_id](./mercicor-create_geopackage_project.png)

#### Parameters

| ID | Description | Type | Info | Required | Advanced | Option |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
FILE_GPKG|Geopackage File|FileDestination||✓|||
PROJECT_NAME|Project name|String||✓|||
PROJECT_CRS|Project CRS|Crs||✓||Default: EPSG:2154 <br> |
PROJECT_EXTENT|Project extent|Extent||✓|||


#### Outputs

| ID | Description | Type | Info |
|:-:|:-:|:-:|:-:|
FILE_GPKG|Geopackage File|File||
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
HABITAT_LIST_LAYER|Liste des types d'habitat|VectorLayer||✓||Default: liste_sante <br> Type: TypeVectorPolygon <br>|


#### Outputs

| ID | Description | Type | Info |
|:-:|:-:|:-:|:-:|
RELATIONS_ADDED|Nombre de relations chargés|Number||
QML_LOADED|Nombre de QML chargés|Number||


***


## Import


### Import données habitat

Import des données des habitats

![algo_id](./mercicor-import_donnees_habitat.png)

#### Parameters

| ID | Description | Type | Info | Required | Advanced | Option |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
INPUT_LAYER|Couche pour l'import|VectorLayer||✓||Type: TypeVectorPolygon <br>|
NAME_FIELD|Champ comportant le nom de l'habitat|Field||✓|||
EXPRESSION_FIELD|Champ comportant l'expression|Field||✓|||
OUTPUT_LAYER|Couche des habitats|VectorLayer||✓||Default: habitat <br> Type: TypeVectorPolygon <br>|


#### Outputs

| ID | Description | Type | Info |
|:-:|:-:|:-:|:-:|
No output

***


### Import données pression

Import des données de pression

![algo_id](./mercicor-import_donnees_pression.png)

#### Parameters

| ID | Description | Type | Info | Required | Advanced | Option |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
INPUT_LAYER|Couche pour l'import|VectorLayer||✓||Type: TypeVectorPolygon <br>|
EXPRESSION_FIELD|Champ comportant l'expression|Field||✓|||
OUTPUT_LAYER|Couche des pressions|VectorLayer||✓||Type: TypeVectorPolygon <br>|


#### Outputs

| ID | Description | Type | Info |
|:-:|:-:|:-:|:-:|
No output

***

