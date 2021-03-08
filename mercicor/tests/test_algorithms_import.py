""" Test import data. """

from qgis.core import (
    Qgis,
    QgsFeature,
    QgsGeometry,
    QgsPointXY,
    QgsProcessingContext,
    QgsProcessingException,
    QgsProject,
    QgsRectangle,
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

    @classmethod
    def import_data(cls, pression_layer):
        """ Internal function to import data. """
        layer_to_import = QgsVectorLayer(
            'MultiPolygon?crs=epsg:2154&field=id:integer&field=pression:integer&index=yes',
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
                            QgsPointXY(0 + x, 0 + y), QgsPointXY(5 + x, 0 + y), QgsPointXY(5 + x, 5 + y),
                            QgsPointXY(0 + x, 5 + y), QgsPointXY(0 + x, 0 + y)
                        ]
                    ],
                    [
                        [
                            QgsPointXY(5 + x, 0 + y), QgsPointXY(10 + x, 0 + y), QgsPointXY(10 + x, 5 + y),
                            QgsPointXY(5 + x, 5 + y), QgsPointXY(5 + x, 0 + y)
                        ]
                    ]
                ]
            ))
            feature.setAttributes([1, 1])
            layer_to_import.addFeature(feature)

        assert 1 == layer_to_import.featureCount()

        count = pression_layer.featureCount()

        params = {
            "INPUT_LAYER": layer_to_import,
            "PRESSURE_FIELD": 'pression',
            "OUTPUT_LAYER": pression_layer,
        }
        run("mercicor:import_donnees_pression", params)

        assert count + 2 == pression_layer.featureCount()
        return layer_to_import

    def test_import_pressure_fail(self):
        """ Test to import pressure data with wrong data. """
        layer_to_import = QgsVectorLayer(
            'MultiPolygon?crs=epsg:2154&field=id:integer&field=pression:integer&index=yes',
            'polygon',
            'memory')
        with edit(layer_to_import):
            feature = QgsFeature(layer_to_import.fields())
            feature.setGeometry(QgsGeometry.fromWkt('MULTIPOLYGON (((0 0, 5 0, 5 5 , 0 5)))'))
            feature.setAttributes([1, 10])
            layer_to_import.addFeature(feature)

        self.assertEqual(1, layer_to_import.featureCount())

        gpkg = plugin_test_data_path('main_geopackage_empty.gpkg', copy=True)
        pression_layer = QgsVectorLayer('{}|layername=pression'.format(gpkg), 'test', 'ogr')
        params = {
            "INPUT_LAYER": layer_to_import,
            "PRESSURE_FIELD": 'pression',
            "OUTPUT_LAYER": pression_layer,
        }
        with self.assertRaises(QgsProcessingException) as context:
            run("mercicor:import_donnees_pression", params)

        if Qgis.QGIS_VERSION_INT < 31600:
            self.assertEqual(str(context.exception), 'There were errors executing the algorithm.')
        else:
            self.assertEqual(str(context.exception), 'Valeur inconnue pour la pression : 10')

    def test_import_pressure_data(self):
        """ Test to import pressure data. """
        project = QgsProject()
        context = QgsProcessingContext()
        context.setProject(project)

        gpkg = plugin_test_data_path('main_geopackage_empty.gpkg', copy=True)

        name = 'pression'
        pression_layer = QgsVectorLayer('{}|layername={}'.format(gpkg, name), name, 'ogr')
        self.assertTrue(pression_layer.isValid())
        project.addMapLayer(pression_layer)

        layer_to_import = self.import_data(pression_layer)

        self.assertEqual(2, pression_layer.featureCount())

        index = pression_layer.fields().indexOf('type_pression')
        self.assertSetEqual({1}, pression_layer.uniqueValues(index))

        self.assertEqual(layer_to_import.extent(), QgsRectangle(700000, 7000000, 700010, 7000005))

    def test_import_habitat_data(self):
        """ Test to import habitat data. """
        gpkg = plugin_test_data_path('main_geopackage_empty.gpkg', copy=True)
        target_layer = QgsVectorLayer('{}|layername={}'.format(gpkg, 'habitat'), 'habitat', 'ogr')
        self.assertEqual(0, target_layer.featureCount())

        import_layer = QgsVectorLayer(plugin_test_data_path('import_habitat.geojson'), 'habitat', 'ogr')
        self.assertTrue(import_layer.isValid())
        self.assertEqual(1, import_layer.featureCount())
        params = {
            "INPUT_LAYER": import_layer,
            "FACIES_FIELD": 'facies',
            "NAME_FIELD": 'nom',
            "OUTPUT_LAYER": target_layer,
        }
        run("mercicor:import_donnees_habitat", params)
        index = target_layer.fields().indexOf('facies')

        self.assertEqual(2, target_layer.featureCount())
        self.assertSetEqual({'bon'}, target_layer.uniqueValues(index))
        # self.assertEqual(target_layer.extent(), QgsRectangle(700000, 7000000, 700010, 7000005))
