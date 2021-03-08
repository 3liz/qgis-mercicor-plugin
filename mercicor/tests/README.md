# Test data

Refaire le geopackage vide :

```python
processing.run(
    "mercicor:create_geopackage_project",
    {
        'FILE_GPKG':'/home/etienne/dev/python/qgis-mercicor-plugin/mercicor/tests/data/main_geopackage_empty.gpkg',
        'PROJECT_NAME':'test_geopackage',
        'PROJECT_CRS':QgsCoordinateReferenceSystem('EPSG:32738'),
        'PROJECT_EXTENT':'518074.490100000,519295.815100000,8592764.021100000,8594011.393400000 [EPSG:32738]'
    }
)
```