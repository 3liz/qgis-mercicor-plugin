""" Test export data. """

from pathlib import Path

from qgis.core import (
    Qgis,
    QgsCoordinateReferenceSystem,
    QgsFeature,
    QgsGeometry,
    QgsVectorLayer,
    edit,
)
from qgis.processing import run

from mercicor.qgis_plugin_tools import plugin_test_data_path
from mercicor.tests.base_processing import BaseTestProcessing

__copyright__ = "Copyright 2021, 3Liz"
__license__ = "GPL version 3"
__email__ = "info@3liz.org"


class TestExportAlgorithms(BaseTestProcessing):

    def _observation_layer_empty(self) -> tuple:
        """ Internal function to get the observation layer. """
        gpkg = plugin_test_data_path('main_geopackage_empty.gpkg', copy=True)
        name = 'observations'
        observations = QgsVectorLayer('{}|layername={}'.format(gpkg, name), name, 'ogr')

        name = 'habitat'
        habitat = QgsVectorLayer('{}|layername={}'.format(gpkg, name), name, 'ogr')

        self.assertTrue(observations.isValid())
        self.assertEqual(observations.featureCount(), 0)
        self.assertEqual(observations.crs(), QgsCoordinateReferenceSystem('EPSG:32738'))

        field_count = observations.fields().count()
        feature_count = observations.featureCount()

        return observations, field_count, feature_count, habitat

    def test_export_observation_with_data(self):
        """ Test to export the observation layer with data. """
        observations, field_count, feature_count, habitat = self._observation_layer_empty()

        # Add an observation feature
        feature = QgsFeature(observations.fields())
        feature.setAttribute('id', 1)
        feature.setAttribute('nom_station', 'Nom de la station')
        feature.setGeometry(QgsGeometry.fromWkt('POINT(0 0)'))
        with edit(observations):
            observations.addFeature(feature)
        feature_count = observations.featureCount()
        self.assertEqual(feature_count, 1)

        # Add an habitat feature
        feature = QgsFeature(habitat.fields())
        feature.setAttribute('id', 1)
        feature.setAttribute('nom', 'Nom habitat')
        feature.setAttribute('facies', 'Faciès habitat')
        feature.setGeometry(QgsGeometry.fromWkt('POINT(0 0)').buffer(20, 20))
        with edit(habitat):
            habitat.addFeature(feature)

        # Without geom
        params = {
            'INPUT_LAYER': observations,
            'HABITAT_LAYER': habitat,
            'INCLUDE_X_Y': False,
            'DESTINATION_FILE': plugin_test_data_path('output', 'export_data_no_geom.xlsx')
        }
        results = run("mercicor:download_observation_file", params)

        self.assertTrue(Path(results['DESTINATION_FILE']).is_file())
        output = QgsVectorLayer(results['DESTINATION_FILE'], 'export', 'ogr')
        self.assertTrue(output.isValid())

        # Everything is fine with QGIS when there is a feature in the source layer.
        # + 2, because there is the join with the habitat layer
        self.assertEqual(output.fields().count(), field_count + 2)

        # if 31000 <= Qgis.QGIS_VERSION_INT <= 31099:
        #     # Header recognised as a row by default, integer as text
        #     self.assertSetEqual(output.uniqueValues(0), {'id', '1'})
        #     self.assertEqual(output.featureCount(), 2)
        # else:  # QGIS 3.16+
        # Single row, no header, integer recognised as integer
        self.assertSetEqual(output.uniqueValues(0), {1})
        self.assertEqual(output.featureCount(), 1)

        # With geom
        params['INCLUDE_X_Y'] = True
        params['DESTINATION_FILE'] = plugin_test_data_path('output', 'export_data_geom.xlsx')
        results = run("mercicor:download_observation_file", params)
        output = QgsVectorLayer(results['DESTINATION_FILE'], 'export', 'ogr')

        #  With geom, same result between QGIS 3.10 and 3.16 !
        self.assertSetEqual(output.uniqueValues(0), {1})
        self.assertEqual(output.featureCount(), 1)

        # + 2 for the geom latitude and longitude
        # + 2 for the join with the habitat layer
        self.assertEqual(output.fields().count(), field_count + 4)

        # Test the integer part only about 4326 reprojection of the geometry
        expected = {
            'latitude': -85,
            'longitude': -45,
        }
        for field, expected_value in expected.items():
            index = output.fields().indexOf(field)
            unique = list(output.uniqueValues(index))
            self.assertEqual(len(unique), 1)
            self.assertEqual(int(unique[0]), expected_value)

        # Check the layer join
        index = output.fields().indexOf('habitat_facies')
        self.assertSetEqual({'Faciès habitat'}, output.uniqueValues(index))
        index = output.fields().indexOf('habitat_nom')
        self.assertSetEqual({'Nom habitat'}, output.uniqueValues(index))

    def test_export_observation_empty(self):
        """ Test to export the observation layer when it is empty. """
        observations, field_count, feature_count, _ = self._observation_layer_empty()

        # Without geom
        params = {
            'INPUT_LAYER': observations,
            'INCLUDE_X_Y': False,
            'DESTINATION_FILE': plugin_test_data_path('output', 'export_no_data_no_geom.xlsx')
        }
        results = run("mercicor:download_observation_file", params)

        self.assertTrue(Path(results['DESTINATION_FILE']).is_file())
        output = QgsVectorLayer(results['DESTINATION_FILE'], 'export', 'ogr')
        self.assertTrue(output.isValid())

        self.assertEqual(output.fields().count(), field_count)
        if 31000 <= Qgis.QGIS_VERSION_INT <= 31099:
            # Header recognised as a row by default, integer as text
            self.assertSetEqual(output.uniqueValues(0), {'id', '1'})
            self.assertEqual(output.featureCount(), feature_count + 2)
        else:  # QGIS 3.16+
            # Single row, no header, integer recognised as integer
            self.assertSetEqual(output.uniqueValues(0), {1})
            self.assertEqual(output.featureCount(), feature_count + 1)

        # With geom
        params['INCLUDE_X_Y'] = True
        params['DESTINATION_FILE'] = plugin_test_data_path('output', 'export_no_data_geom.xlsx')
        results = run("mercicor:download_observation_file", params)
        output = QgsVectorLayer(results['DESTINATION_FILE'], 'export', 'ogr')
        self.assertEqual(output.fields().count(), field_count + 2)

        #  With geom, NOT the same result between QGIS 3.10 and 3.16 like the test before
        if 31000 <= Qgis.QGIS_VERSION_INT <= 31099:
            self.assertSetEqual(output.uniqueValues(0), {'id', '1'})
            self.assertEqual(output.featureCount(), feature_count + 2)
        else:  # QGIS 3.16+
            self.assertSetEqual(output.uniqueValues(0), {1})
            self.assertEqual(output.featureCount(), feature_count + 1)
