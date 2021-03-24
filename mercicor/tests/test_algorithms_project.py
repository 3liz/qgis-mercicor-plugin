""" Test project. """

import os.path
import shutil

from qgis.core import QgsVectorLayer
from qgis.processing import run

from mercicor.qgis_plugin_tools import (
    load_csv,
    plugin_test_data_path,
    resources_path,
)
from mercicor.tests.base_processing import BaseTestProcessing

__copyright__ = "Copyright 2021, 3Liz"
__license__ = "GPL version 3"
__email__ = "info@3liz.org"


class TestProjectAlgorithms(BaseTestProcessing):

    def test_create_geopackage(self):
        """ Test to create a geopackage. """
        # Only for debug, for regenerating the test input file
        debug = False
        if debug and os.environ.get('GITLAB_USER_ID', False):
            raise Exception('Do not commit with debug=True on GitLab')

        file_path = '/tmp/test_create_geopackage.gpkg'

        params = {
            "FILE_GPKG": file_path,
            "PROJECT_NAME": 'test_geopackage',
            "PROJECT_CRS": 'EPSG:2154',
            "PROJECT_EXTENT": '0,10,0,10',
        }
        run("mercicor:create_geopackage_project", params)

        self.assertTrue(os.path.exists(file_path))

        layer = QgsVectorLayer(file_path, "test", "ogr")
        self.assertTrue(layer.isValid())
        self.assertEqual(8, len(layer.dataProvider().subLayers()))

        if debug:
            # Without data
            shutil.copy(file_path, plugin_test_data_path('output_main_geopackage_empty.gpkg'))

            # With data
            name = 'pression'
            pression_layer = QgsVectorLayer('{}|layername={}'.format(file_path, name), name, 'ogr')
            from mercicor.tests.test_algorithms_import import (
                TestImportAlgorithms,
            )
            TestImportAlgorithms.import_data(pression_layer)

            shutil.copy(file_path, plugin_test_data_path('output_main_geopackage_data.gpkg'))

    def test_empty_geopackage(self):
        """ Test if the empty geopackage is up to date with CSV files. """
        gpkg = plugin_test_data_path('main_geopackage_empty.gpkg', copy=True)

        files = os.listdir(resources_path('data_models'))
        for csv_file in files:
            with self.subTest(i=csv_file):
                csv = load_csv(csv_file, resources_path('data_models', csv_file))
                gpkg_layer = QgsVectorLayer('{}|layername={}'.format(gpkg, csv_file[0:-4]), csv_file, 'ogr')

                gpkg_fields = gpkg_layer.fields().names()
                gpkg_fields.sort()

                csv_fields = list(csv.uniqueValues(1))
                csv_fields.sort()

                self.assertListEqual(gpkg_fields, csv_fields)

    def test_apply_qml_styles(self):
        """ Test to apply some QML to loaded layers in the canvas. """
        gpkg = plugin_test_data_path('main_geopackage_empty.gpkg', copy=True)

        name = 'pression'
        pression_layer = QgsVectorLayer('{}|layername={}'.format(gpkg, name), name, 'ogr')
        self.assertTrue(pression_layer.isValid())

        name = 'habitat'
        habitat_layer = QgsVectorLayer('{}|layername={}'.format(gpkg, name), name, 'ogr')
        self.assertTrue(habitat_layer.isValid())

        name = 'liste_type_pression'
        list_type_pressure = QgsVectorLayer('{}|layername={}'.format(gpkg, name), name, 'ogr')
        self.assertTrue(list_type_pressure.isValid())

        name = 'habitat_etat_ecologique'
        habitat_etat_ecologique = QgsVectorLayer('{}|layername={}'.format(gpkg, name), name, 'ogr')
        self.assertTrue(habitat_etat_ecologique.isValid())

        name = 'observations'
        observations = QgsVectorLayer('{}|layername={}'.format(gpkg, name), name, 'ogr')
        self.assertTrue(observations.isValid())

        name = 'scenario_pression'
        scenario_pression = QgsVectorLayer('{}|layername={}'.format(gpkg, name), name, 'ogr')
        self.assertTrue(scenario_pression.isValid())

        name = 'habitat_pression_etat_ecologique'
        habitat_pression_etat_ecologique = QgsVectorLayer('{}|layername={}'.format(gpkg, name), name, 'ogr')
        self.assertTrue(habitat_pression_etat_ecologique.isValid())

        params = {
            "PRESSURE_LAYER": pression_layer,
            "PRESSURE_LIST_LAYER": list_type_pressure,
            "HABITAT_LAYER": habitat_layer,
            "HABITAT_ETAT_ECOLOGIQUE_LAYER": habitat_etat_ecologique,
            "OBSERVATIONS_LAYER": observations,
            "SCENARIO_PRESSION": scenario_pression,
            "HABITAT_PRESSION_ETAT_ECOLOGIQUE": habitat_pression_etat_ecologique,
        }
        result = run("mercicor:load_qml_and_relations", params)
        self.assertEqual(result['QML_LOADED'], 8)
        # self.assertEqual(result['JOINS_ADDED'], 4)
        # self.assertEqual(result['ACTIONS_ADDED'], 1)
        # self.assertEqual(result['RELATIONS_ADDED'], 1)

        # Check alias
        field = pression_layer.fields().field(1)
        self.assertEqual('type_pression', field.name())
        self.assertEqual('Type de pression', field.alias())
