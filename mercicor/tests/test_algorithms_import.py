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

from mercicor.processing.imports.import_data_observations import (
    ImportObservationData,
)
from mercicor.qgis_plugin_tools import plugin_test_data_path
from mercicor.tests.base_processing import BaseTestProcessing

__copyright__ = "Copyright 2021, 3Liz"
__license__ = "GPL version 3"
__email__ = "info@3liz.org"


class TestImportAlgorithms(BaseTestProcessing):

    @classmethod
    def import_data(cls, pression_layer: QgsVectorLayer, scenario_layer: QgsVectorLayer):
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

        assert layer_to_import.featureCount() == 1

        count = pression_layer.featureCount()

        params = {
            "INPUT_LAYER": layer_to_import,
            "PRESSION_FIELD": 'pression',
            "SCENARIO_NAME": 'testing scenario',
            "SCENARIO_LAYER": scenario_layer,
            "APPLY_CALCUL_HABITAT_PRESSION_ETAT_ECOLOGIQUE": False,
            "OUTPUT_LAYER": pression_layer,
        }
        run("mercicor:import_donnees_pression", params)

        assert count + layer_to_import.featureCount() == pression_layer.featureCount()
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

        gpkg = plugin_test_data_path('main_geopackage_empty_pression.gpkg', copy=True)
        pression_layer = QgsVectorLayer('{}|layername=pression'.format(gpkg), 'test', 'ogr')
        scenario_pression_layer = QgsVectorLayer(
            '{}|layername=scenario_pression'.format(gpkg), 'test scenario', 'ogr')
        params = {
            "INPUT_LAYER": layer_to_import,
            "PRESSION_FIELD": 'pression',
            "SCENARIO_NAME": 'scenario',
            "SCENARIO_LAYER": scenario_pression_layer,
            "APPLY_CALCUL_HABITAT_PRESSION_ETAT_ECOLOGIQUE": False,
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

        gpkg = plugin_test_data_path('main_geopackage_empty_pression.gpkg', copy=True)

        name = 'pression'
        pression_layer = QgsVectorLayer('{}|layername={}'.format(gpkg, name), name, 'ogr')
        self.assertTrue(pression_layer.isValid())
        project.addMapLayer(pression_layer)

        name = 'scenario_pression'
        scenario_pression_layer = QgsVectorLayer('{}|layername={}'.format(gpkg, name), name, 'ogr')
        self.assertTrue(scenario_pression_layer.isValid())
        project.addMapLayer(scenario_pression_layer)

        layer_to_import = self.import_data(pression_layer, scenario_pression_layer)

        # Couche pression
        self.assertEqual(1, pression_layer.featureCount())

        index = pression_layer.fields().indexOf('type_pression')
        self.assertSetEqual({1}, pression_layer.uniqueValues(index))

        self.assertEqual(layer_to_import.extent(), QgsRectangle(700000, 7000000, 700010, 7000005))

        # Couche scénario
        self.assertEqual(1, scenario_pression_layer.featureCount())
        self.assertSetEqual(scenario_pression_layer.uniqueValues(0), {1})
        self.assertSetEqual(scenario_pression_layer.uniqueValues(1), {'testing scenario'})

        index = pression_layer.fields().indexOf('scenario_id')
        self.assertSetEqual({1}, pression_layer.uniqueValues(index))
        self.assertEqual(pression_layer.subsetString(), '"scenario_id" = 1')

    def test_import_pressure_data_calcul(self):
        """ Test to import pressure data. """
        project = QgsProject()
        context = QgsProcessingContext()
        context.setProject(project)

        gpkg = plugin_test_data_path('main_geopackage_empty_pression.gpkg', copy=True)

        name = 'pression'
        pression_layer = QgsVectorLayer('{}|layername={}'.format(gpkg, name), name, 'ogr')
        self.assertTrue(pression_layer.isValid())
        project.addMapLayer(pression_layer)

        name = 'scenario_pression'
        scenario_pression_layer = QgsVectorLayer('{}|layername={}'.format(gpkg, name), name, 'ogr')
        self.assertTrue(scenario_pression_layer.isValid())
        project.addMapLayer(scenario_pression_layer)

        name = 'habitat'
        habitat_layer = QgsVectorLayer('{}|layername={}'.format(gpkg, name), name, 'ogr')
        self.assertTrue(scenario_pression_layer.isValid())
        project.addMapLayer(scenario_pression_layer)

        name = 'habitat_pression_etat_ecologique'
        habitat_pression_layer = QgsVectorLayer('{}|layername={}'.format(gpkg, name), name, 'ogr')
        self.assertTrue(scenario_pression_layer.isValid())
        project.addMapLayer(scenario_pression_layer)

        # import habitat
        import_layer = QgsVectorLayer(plugin_test_data_path('import_habitat.geojson'), 'habitat', 'ogr')
        self.assertTrue(import_layer.isValid())
        self.assertEqual(1, import_layer.featureCount())
        params = {
            "INPUT_LAYER": import_layer,
            "FACIES_FIELD": 'facies',
            "NAME_FIELD": 'nom',
            "OUTPUT_LAYER": habitat_layer,
        }
        run("mercicor:import_donnees_habitat", params)
        index = habitat_layer.fields().indexOf('facies')

        self.assertEqual(1, habitat_layer.featureCount())

        # import pression
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
        self.assertTrue(layer_to_import.isValid())
        self.assertEqual(1, layer_to_import.featureCount())

        params = {
            "INPUT_LAYER": layer_to_import,
            "PRESSION_FIELD": 'pression',
            "SCENARIO_NAME": 'testing scenario',
            "SCENARIO_LAYER": scenario_pression_layer,
            "APPLY_CALCUL_HABITAT_PRESSION_ETAT_ECOLOGIQUE": True,
            "HABITAT_LAYER": habitat_layer,
            "HABITAT_PRESSION_LAYER": habitat_pression_layer,
            "OUTPUT_LAYER": pression_layer,
        }
        run("mercicor:import_donnees_pression", params)

        # Couche pression
        self.assertEqual(1, pression_layer.featureCount())

        index = pression_layer.fields().indexOf('type_pression')
        self.assertSetEqual({1}, pression_layer.uniqueValues(index))

        self.assertEqual(layer_to_import.extent(), QgsRectangle(700000, 7000000, 700010, 7000005))

        # Couche scénario
        self.assertEqual(1, scenario_pression_layer.featureCount())
        self.assertSetEqual(scenario_pression_layer.uniqueValues(0), {1})
        self.assertSetEqual(scenario_pression_layer.uniqueValues(1), {'testing scenario'})

        # Couche habitat_pression_etat_ecologique
        self.assertEqual(1, habitat_pression_layer.featureCount())

        index = pression_layer.fields().indexOf('scenario_id')
        self.assertSetEqual({1}, pression_layer.uniqueValues(index))
        self.assertEqual(pression_layer.subsetString(), '"scenario_id" = 1')

    def test_import_habitat_data(self):
        """ Test to import habitat data. """
        gpkg = plugin_test_data_path('main_geopackage_empty_pression.gpkg', copy=True)
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

        self.assertEqual(1, target_layer.featureCount())
        self.assertSetEqual({'bon'}, target_layer.uniqueValues(index))
        # self.assertEqual(target_layer.extent(), QgsRectangle(700000, 7000000, 700010, 7000005))

        # Check the default style
        names = target_layer.uniqueValues(1)
        self.assertSetEqual(names, {'zone 1'})
        self.assertEqual(1, len(target_layer.renderer().categories()))
        self.assertEqual('zone 1', target_layer.renderer().categories()[0].label())

    def test_import_observation_exist(self):
        """ Test to retrieve a specific observation feature. """
        gpkg = plugin_test_data_path('main_geopackage_empty_pression.gpkg', copy=True)
        name = 'observations'
        observations = QgsVectorLayer('{}|layername={}'.format(gpkg, name), name, 'ogr')

        feature = QgsFeature(observations.fields())
        feature.setAttribute('id', 1)
        feature.setAttribute('nom_station', 'Nom de la station')
        feature.setGeometry(QgsGeometry.fromWkt('POINT(0 0)'))
        with edit(observations):
            observations.addFeature(feature)

        self.assertTrue(ImportObservationData.observation_exists(observations, 1)[0])
        self.assertFalse(ImportObservationData.observation_exists(observations, 100)[0])

    def test_import_observations(self):
        """ Test to import observations with a geometry from a vector layer. """
        gpkg = plugin_test_data_path('main_geopackage_empty_pression.gpkg', copy=True)
        name = 'observations'
        observations = QgsVectorLayer('{}|layername={}'.format(gpkg, name), name, 'ogr')

        layer_to_import = QgsVectorLayer(
            'None?'
            'field=id:integer&'
            'field=nom_station:string(20)&'
            'field=note_man:integer&'
            'field=another_field:integer&'
            'field=latitude:double&'
            'field=longitude:double&'
            'index=yes',
            'obs',
            'memory')
        feature = QgsFeature(layer_to_import.fields())
        feature.setAttribute('id', 1)
        feature.setAttribute('nom_station', 'TEST 01')
        feature.setAttribute('note_man', 10)
        feature.setAttribute('another_field', 10)
        feature.setAttribute('latitude', -12.72)
        feature.setAttribute('longitude', 45.17)

        with edit(layer_to_import):
            layer_to_import.addFeature(feature)

        params = {
            "INPUT_LAYER": layer_to_import,
            "OUTPUT_LAYER": observations,
        }
        run("mercicor:import_donnees_observation", params)
        self.assertEqual(observations.featureCount(), 1)

        # Test geom
        self.assertAlmostEqual(int(observations.extent().center().x()), 518455, 0)
        self.assertAlmostEqual(int(observations.extent().center().y()), 8593822, 0)

        # Test the new feature attributes
        self.assertSetEqual(observations.uniqueValues(0), {1})
        index = observations.fields().indexOf('note_man')
        self.assertSetEqual(observations.uniqueValues(index), {10})

        # Update the feature
        feature_id = 1
        self.assertTrue(layer_to_import.getFeature(feature_id).isValid())
        note_man_index = layer_to_import.fields().indexOf('note_man')
        another_field_index = layer_to_import.fields().indexOf('another_field')
        latitude_index = layer_to_import.fields().indexOf('latitude')
        longitude_index = layer_to_import.fields().indexOf('longitude')

        attributes = {
            note_man_index: 1000,
            another_field_index: 1000,
            latitude_index: -12.6,
            longitude_index: 45.0,
        }
        with edit(layer_to_import):
            layer_to_import.changeAttributeValues(feature_id, attributes)

        run("mercicor:import_donnees_observation", params)
        self.assertEqual(observations.featureCount(), 1)

        # Test geom
        self.assertAlmostEqual(int(observations.extent().center().x()), 500000, 0)
        self.assertAlmostEqual(int(observations.extent().center().y()), 8607098, 0)

        # Test attributes
        self.assertSetEqual(observations.uniqueValues(0), {1})
        index = observations.fields().indexOf('note_man')
        self.assertSetEqual(observations.uniqueValues(index), {1000})
