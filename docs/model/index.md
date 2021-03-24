---
hide:
  - navigation
---

# Modèle des données

## Relations

??? info "Légende"
    Flèche pleine : relation de projet

    Losange vide : jointure spatiale

```mermaid
classDiagram
habitat_pression_etat_ecologique
pression
habitat
scenario_pression
liste_type_pression
observations
habitat_etat_ecologique
liste_type_pression <|-- pression
scenario_pression <|-- pression
scenario_pression <|-- habitat_pression_etat_ecologique
habitat_etat_ecologique <|-- habitat
habitat_pression_etat_ecologique <|-- habitat
habitat_pression_etat_ecologique <|-- pression
habitat o-- observations
habitat_pression_etat_ecologique : geom MultiPolygon
habitat_pression_etat_ecologique : id PK
habitat_pression_etat_ecologique : habitat_id FK
habitat_pression_etat_ecologique : pression_id FK
habitat_pression_etat_ecologique : scenario_id FK
habitat_pression_etat_ecologique : note_bsd
habitat_pression_etat_ecologique : note_bsm
habitat_pression_etat_ecologique : note_ben
habitat_pression_etat_ecologique : note_man
habitat_pression_etat_ecologique : note_pmi
habitat_pression_etat_ecologique : score_mercicor
habitat_pression_etat_ecologique : ...
pression : geom MultiPolygon
pression : id PK
pression : type_pression
pression : scenario_id FK
habitat : geom MultiPolygon
habitat : id PK
habitat : nom
habitat : facies
scenario_pression : id PK
scenario_pression : nom
liste_type_pression : id PK
liste_type_pression : key
liste_type_pression : label
observations : geom Point
observations : id PK
observations : nom_station
observations : station_man
observations : perc_bsd
observations : perc_bsm
observations : datetime_obs
observations : profondeur
observations : note_bsd
observations : note_bsm
observations : note_ben
observations : ...
habitat_etat_ecologique : id PK
habitat_etat_ecologique : nom
habitat_etat_ecologique : facies
habitat_etat_ecologique : note_bsd
habitat_etat_ecologique : note_bsm
habitat_etat_ecologique : note_ben
habitat_etat_ecologique : note_man
habitat_etat_ecologique : note_pmi
habitat_etat_ecologique : score_mercicor
habitat_etat_ecologique : bsd_recouv_cor
habitat_etat_ecologique : ...
```

## Tables

??? info "Légende"
    Champ géométrique en *italique*

    Champ de clé primaire en **gras**

    Champ de clé étrangère cliquable avec la mention "FK"

### Habitat Pression Etat Ecologique

| ID | Name | Type | Alias |
|:-:|:-:|:-:|:-:|
||*geom*|MultiPolygon||
|1|**id**|qlonglong|Identifiant|
|2|[habitat_id FK](#habitat)|qlonglong|Identifiant habitat|
|3|[pression_id FK](#pression)|qlonglong|Identifiant de pression|
|4|[scenario_id FK](#scenario-pression)|qlonglong|Identifiant du scenario de pression|
|5|note_bsd|double|Note Mercicor Benthique de substrats durs|
|6|note_bsm|double|Note Mercicor Benthique de substrats meubles|
|7|note_ben|double|Note Mercicor Benthique|
|8|note_man|double|Note Mercicor Mangrove|
|9|note_pmi|double|Note Mercicor Poissons et Macro-invertébrés|
|10|score_mercicor|double|Score Mercicor|
|11|bsd_recouv_cor|double|Recouvrement corallien (Scléractiniaires)|
|12|bsd_p_acrop|double|Pourcentage du recouvrement corallien représenté par les coraux acropores|
|13|bsd_vital_cor|double|Vitalité et taux de mortalité corallienne|
|14|bsd_comp_struc|double|Complexité structurelle des peuplements coralliens|
|15|bsd_taille_cor|double|Taille des coraux vivants|
|16|bsd_dens_juv|double|Densité de coraux juvéniles|
|17|bsd_f_sessile|double|Recouvrement par la faune sessile non corallienne|
|18|bsd_recouv_ma|double|Recouvrement par les macroalgues|
|19|bsm_fragm_herb|double|Fragmentation de l’herbier|
|20|bsm_recouv_her|double|Recouvrement par l’herbier (patchs)|
|21|bsm_haut_herb|double|Hauteur de l’herbier (patchs)|
|22|bsm_dens_herb|double|Densité des phanérogames (patchs)|
|23|bsm_div_herb|double|Diversité spécifique des phanérogames (patchs)|
|24|bsm_epibiose|double|Epibiose de l’herbier (patchs)|
|25|man_fragm|double|Fragmentation de la mangrove|
|26|man_recouv|double|Recouvrement par la mangrove (patchs)|
|27|man_diam_tronc|double|Diamètre des troncs (patchs)|
|28|man_dens|double|Densité des palétuviers (patchs)|
|29|man_diversit|double|Diversité spécifique des palétuviers (patchs)|
|30|man_vital|double|Vitalité des palétuviers (patchs)|
|31|pmi_div_poi|double|Diversité spécifique des peuplements de poissons|
|32|pmi_predat_poi|double|Abondance et maturité des prédateurs supérieurs récifaux|
|33|pmi_scarib_poi|double|Abondance et maturité des poissons perroquets|
|34|pmi_macro_inv|double|Abondance des macro-invertébrés|

### Pression

| ID | Name | Type | Alias |
|:-:|:-:|:-:|:-:|
||*geom*|MultiPolygon||
|1|**id**|qlonglong|ID|
|2|type_pression|qlonglong|Type de pression|
|3|[scenario_id FK](#scenario-pression)|qlonglong|ID Scénario|

### Habitat

| ID | Name | Type | Alias |
|:-:|:-:|:-:|:-:|
||*geom*|MultiPolygon||
|1|**id**|qlonglong|Id|
|2|nom|QString|Nom|
|3|facies|QString|Faciès|

### Scenario Pression

| ID | Name | Type | Alias |
|:-:|:-:|:-:|:-:|
|1|**id**|qlonglong|Identifiant|
|2|nom|QString|libellé du scenario|

### Liste Type Pression

| ID | Name | Type | Alias |
|:-:|:-:|:-:|:-:|
|1|**id**|qlonglong|Id|
|2|key|qlonglong|Clé|
|3|label|QString|Étiquette|

### Observations

| ID | Name | Type | Alias |
|:-:|:-:|:-:|:-:|
||*geom*|Point||
|1|**id**|qlonglong|Id|
|2|nom_station|QString|Nom de la station d'observations|
|3|station_man|bool|Station en Mangrove|
|4|perc_bsd|double|Pourcentage Benthique de substrats durs |
|5|perc_bsm|double|Pourcentage Benthique de substrats meubles|
|6|datetime_obs|QDateTime|Date et heure d'observations|
|7|profondeur|double|Profondeur|
|8|note_bsd|double|Note Mercicor Benthique de substrats durs|
|9|note_bsm|double|Note Mercicor Benthique de substrats meubles|
|10|note_ben|double|Note Mercicor Benthique|
|11|note_man|double|Note Mercicor Mangrove|
|12|note_pmi|double|Note Mercicor Poissons et Macro-invertébrés|
|13|score_mercicor|double|Score Mercicor|
|14|phch_temp|double|Température de l'eau|
|15|phch_dop|double|Oxygène dissous en pourcentage|
|16|phch_do|double|Oxygène dissous en mg/L|
|17|phch_cond|double|Conductivité en ms par cm|
|18|phch_sal|double|Salinité de l'eau|
|19|phch_ph|double|PH de l'eau|
|20|phch_turb|double|Turbidité de l'eau|
|21|phch_sedi|double|Sédimentation|
|22|bsd_recouv_cor|double|Recouvrement corallien (Scléractiniaires)|
|23|bsd_p_acrop|double|Pourcentage du recouvrement corallien représenté par les coraux acropores|
|24|bsd_vital_cor|double|Vitalité et taux de mortalité corallienne|
|25|bsd_comp_struc|double|Complexité structurelle des peuplements coralliens|
|26|bsd_taille_cor|double|Taille des coraux vivants|
|27|bsd_dens_juv|double|Densité de coraux juvéniles|
|28|bsd_f_sessile|double|Recouvrement par la faune sessile non corallienne|
|29|bsd_recouv_ma|double|Recouvrement par les macroalgues|
|30|bsm_fragm_herb|double|Fragmentation de l’herbier|
|31|bsm_recouv_her|double|Recouvrement par l’herbier (patchs)|
|32|bsm_haut_herb|double|Hauteur de l’herbier (patchs)|
|33|bsm_dens_herb|double|Densité des phanérogames (patchs)|
|34|bsm_div_herb|double|Diversité spécifique des phanérogames (patchs)|
|35|bsm_epibiose|double|Epibiose de l’herbier (patchs)|
|36|man_fragm|double|Fragmentation de la mangrove|
|37|man_recouv|double|Recouvrement par la mangrove (patchs)|
|38|man_diam_tronc|double|Diamètre des troncs (patchs)|
|39|man_dens|double|Densité des palétuviers (patchs)|
|40|man_diversit|double|Diversité spécifique des palétuviers (patchs)|
|41|man_vital|double|Vitalité des palétuviers (patchs)|
|42|pmi_div_poi|double|Diversité spécifique des peuplements de poissons|
|43|pmi_predat_poi|double|Abondance et maturité des prédateurs supérieurs récifaux|
|44|pmi_scarib_poi|double|Abondance et maturité des poissons perroquets|
|45|pmi_macro_inv|double|Abondance des macro-invertébrés|

### Habitat Etat Ecologique

| ID | Name | Type | Alias |
|:-:|:-:|:-:|:-:|
|1|**id**|qlonglong|Identifiant|
|2|nom|QString|Nom de l'habitat|
|3|facies|QString|Faciès de l'habitat|
|4|note_bsd|double|Note Mercicor Benthique de substrats durs|
|5|note_bsm|double|Note Mercicor Benthique de substrats meubles|
|6|note_ben|double|Note Mercicor Benthique|
|7|note_man|double|Note Mercicor Mangrove|
|8|note_pmi|double|Note Mercicor Poissons et Macro-invertébrés|
|9|score_mercicor|double|Score Mercicor|
|10|bsd_recouv_cor|double|Recouvrement corallien (Scléractiniaires)|
|11|bsd_p_acrop|double|Pourcentage du recouvrement corallien représenté par les coraux acropores|
|12|bsd_vital_cor|double|Vitalité et taux de mortalité corallienne|
|13|bsd_comp_struc|double|Complexité structurelle des peuplements coralliens|
|14|bsd_taille_cor|double|Taille des coraux vivants|
|15|bsd_dens_juv|double|Densité de coraux juvéniles|
|16|bsd_f_sessile|double|Recouvrement par la faune sessile non corallienne|
|17|bsd_recouv_ma|double|Recouvrement par les macroalgues|
|18|bsm_fragm_herb|double|Fragmentation de l’herbier|
|19|bsm_recouv_her|double|Recouvrement par l’herbier (patchs)|
|20|bsm_haut_herb|double|Hauteur de l’herbier (patchs)|
|21|bsm_dens_herb|double|Densité des phanérogames (patchs)|
|22|bsm_div_herb|double|Diversité spécifique des phanérogames (patchs)|
|23|bsm_epibiose|double|Epibiose de l’herbier (patchs)|
|24|man_fragm|double|Fragmentation de la mangrove|
|25|man_recouv|double|Recouvrement par la mangrove (patchs)|
|26|man_diam_tronc|double|Diamètre des troncs (patchs)|
|27|man_dens|double|Densité des palétuviers (patchs)|
|28|man_diversit|double|Diversité spécifique des palétuviers (patchs)|
|29|man_vital|double|Vitalité des palétuviers (patchs)|
|30|pmi_div_poi|double|Diversité spécifique des peuplements de poissons|
|31|pmi_predat_poi|double|Abondance et maturité des prédateurs supérieurs récifaux|
|32|pmi_scarib_poi|double|Abondance et maturité des poissons perroquets|
|33|pmi_macro_inv|double|Abondance des macro-invertébrés|
