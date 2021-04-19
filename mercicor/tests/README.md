# Test data

Refaire le geopackage vide de données, mais avec les tables.
Il ne faut changer que le chemin de destination.

```python
processing.run(
    "mercicor:create_geopackage_project_pression",
    {
        'FILE_GPKG':'/home/etienne/dev/python/qgis-mercicor-plugin/mercicor/tests/data/main_geopackage_empty_pression.gpkg',
        'PROJECT_NAME':'test_geopackage',
        'PROJECT_CRS':QgsCoordinateReferenceSystem('EPSG:32738'),
        'PROJECT_EXTENT':'518074.490100000,519295.815100000,8592764.021100000,8594011.393400000 [EPSG:32738]'
    }
)
```

```python
processing.run(
    "mercicor:create_geopackage_project_compensation",
    {
        'FILE_GPKG':'/home/etienne/dev/python/qgis-mercicor-plugin/mercicor/tests/data/main_geopackage_empty_compensation.gpkg',
        'PROJECT_NAME':'test_geopackage',
        'PROJECT_CRS':QgsCoordinateReferenceSystem('EPSG:32738'),
        'PROJECT_EXTENT':'518074.490100000,519295.815100000,8592764.021100000,8594011.393400000 [EPSG:32738]'
    }
)
```
