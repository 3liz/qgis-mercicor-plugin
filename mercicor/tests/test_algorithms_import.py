""" Test import data. """

from qgis.core import (
    QgsFeature,
    QgsGeometry,
    QgsPointXY,
    QgsProcessingContext,
    QgsProject,
    QgsVectorLayer,
    edit,
)
from qgis.processing import run

from mercicor.qgis_plugin_tools import plugin_test_data_path
from mercicor.tests.base_processing import BaseTestProcessing

__copyright__ = "Copyright 2021, 3Liz"
__license__ = "GPL version 3"
__email__ = "info@3liz.org"


class TestImportAlgorithms(BaseTestProcessing):

    def test_import_pressure_data(self):
        """ Test to import pressure data. """
        project = QgsProject()
        context = QgsProcessingContext()
        context.setProject(project)

        gpkg = plugin_test_data_path('main_geopackage.gpkg', copy=True)

        name = 'pression'
        pression_layer = QgsVectorLayer('{}|layername={}'.format(gpkg, name), name, 'ogr')
        self.assertTrue(pression_layer.isValid())
        project.addMapLayer(pression_layer)

        name = 'habitat'
        habitat_layer = QgsVectorLayer('{}|layername={}'.format(gpkg, name), name, 'ogr')
        self.assertTrue(habitat_layer.isValid())
        project.addMapLayer(habitat_layer)

        layer_to_import = QgsVectorLayer(
            'MultiPolygon?crs=epsg:2154&field=id:integer&field=expression:string(20)&index=yes',
            'polygon',
            'memory')

        x = 700000  # NOQA VNE001
        y = 7000000  # NOQA VNE001

        with edit(layer_to_import):
            feature = QgsFeature(layer_to_import.fields())
            feature.setGeometry(QgsGeometry.fromMultiPolygonXY(
                [
                    [
                        [
                            QgsPointXY(0+x, 0+y), QgsPointXY(5+x, 0+y), QgsPointXY(5+x, 5+y),
                            QgsPointXY(0+x, 5+y), QgsPointXY(0+x, 0+y)
                        ]
                    ],
                    [
                        [
                            QgsPointXY(5+x, 0+y), QgsPointXY(10+x, 0+y), QgsPointXY(10+x, 5+y),
                            QgsPointXY(5+x, 5+y), QgsPointXY(5+x, 0+y)
                        ]
                    ]
                ]
            ))
            feature.setAttributes([1, "area($geometry)"])
            layer_to_import.addFeature(feature)

        self.assertEqual(1, layer_to_import.featureCount())

        params = {
            "INPUT_LAYER": layer_to_import,
            "EXPRESSION_FIELD": 'expression',
            "OUTPUT_LAYER": pression_layer,
        }
        run("mercicor:import_donnees_pression", params)

        self.assertEqual(2, pression_layer.featureCount())
        index = pression_layer.fields().indexOf('type_pression')
        self.assertSetEqual({'25'}, pression_layer.uniqueValues(index))
