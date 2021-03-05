""" Test project. """

import os.path
import shutil

from qgis.core import QgsVectorLayer
from qgis.processing import run

from mercicor.qgis_plugin_tools import plugin_test_data_path
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
        self.assertEqual(4, len(layer.dataProvider().subLayers()))

        if debug:
            # Without data
            shutil.copy(file_path, plugin_test_data_path('output_main_geopackage_empty.gpkg'))

            # With data
            name = 'pression'
            pression_layer = QgsVectorLayer('{}|layername={}'.format(file_path, name), name, 'ogr')
            from mercicor.tests.test_algorithms_import import (
                TestImportAlgorithms,
            )
            TestImportAlgorithms.import_data('2154', pression_layer)

            shutil.copy(file_path, plugin_test_data_path('output_main_geopackage_data.gpkg'))

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
        self.assertTrue(habitat_layer.isValid())

        params = {
            "PRESSURE_LAYER": pression_layer,
            "PRESSURE_LIST_LAYER": list_type_pressure,
            "HABITAT_LAYER": habitat_layer,
        }
        result = run("mercicor:load_qml_and_relations", params)
        self.assertEqual(result['QML_LOADED'], 7)
        # self.assertEqual(result['RELATIONS_ADDED'], 1)
