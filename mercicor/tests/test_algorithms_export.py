""" Test export data. """

from pathlib import Path

from qgis.core import (
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

        self.assertTrue(observations.isValid())
        self.assertEqual(observations.featureCount(), 0)
        self.assertEqual(observations.crs(), QgsCoordinateReferenceSystem(32738))

        field_count = observations.fields().count()
        feature_count = observations.featureCount()

        return observations, field_count, feature_count

    def test_export_observation_with_data(self):
        """ Test to export the observation layer with data. """
        observations, field_count, feature_count = self._observation_layer_empty()

        # Add a feature
        feature = QgsFeature(observations.fields())
        feature.setAttribute('id', 1)
        feature.setAttribute('nom_station', 'Nom de la station')
        feature.setGeometry(QgsGeometry.fromWkt('POINT(0 0)'))
        with edit(observations):
            observations.addFeature(feature)
        feature_count = observations.featureCount()
        self.assertEqual(feature_count, 1)

        # Without geom
        params = {
            'INPUT_LAYER': observations,
            'INCLUDE_X_Y': False,
            'DESTINATION_FILE': plugin_test_data_path('output', 'export.xlsx')
        }
        results = run("mercicor:download_observation_file", params)

        self.assertTrue(Path(results['DESTINATION_FILE']).is_file())
        output = QgsVectorLayer(results['DESTINATION_FILE'], 'export', 'ogr')
        self.assertTrue(output.isValid())

        # Everything is fine with QGIS when there is a feature in the source layer.
        self.assertEqual(output.fields().count(), field_count)
        self.assertEqual(output.featureCount(), feature_count)

        # With geom
        params['INCLUDE_X_Y'] = True
        results = run("mercicor:download_observation_file", params)
        output = QgsVectorLayer(results['DESTINATION_FILE'], 'export', 'ogr')
        self.assertEqual(output.fields().count(), field_count + 2)

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

    def test_export_observation_empty(self):
        """ Test to export the observation layer when it is empty. """
        observations, field_count, feature_count = self._observation_layer_empty()

        # Without geom
        params = {
            'INPUT_LAYER': observations,
            'INCLUDE_X_Y': False,
            'DESTINATION_FILE': plugin_test_data_path('output', 'export.xlsx')
        }
        results = run("mercicor:download_observation_file", params)

        self.assertTrue(Path(results['DESTINATION_FILE']).is_file())
        output = QgsVectorLayer(results['DESTINATION_FILE'], 'export', 'ogr')
        self.assertTrue(output.isValid())

        self.assertEqual(output.fields().count(), field_count)
        self.assertEqual(output.featureCount(), feature_count + 1)

        # With geom
        params['INCLUDE_X_Y'] = True
        results = run("mercicor:download_observation_file", params)
        output = QgsVectorLayer(results['DESTINATION_FILE'], 'export', 'ogr')
        self.assertEqual(output.fields().count(), field_count + 2)
        self.assertEqual(output.featureCount(), feature_count + 1)
