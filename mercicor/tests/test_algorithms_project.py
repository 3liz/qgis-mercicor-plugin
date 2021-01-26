""" Test project. """

import os.path

from qgis.core import QgsVectorLayer
from qgis.processing import run

from mercicor.qgis_plugin_tools import plugin_test_data_path
from mercicor.tests.base_processing import BaseTestProcessing

__copyright__ = "Copyright 2021, 3Liz"
__license__ = "GPL version 3"
__email__ = "info@3liz.org"
__revision__ = "$Format:%H$"


class TestProjectAlgorithms(BaseTestProcessing):

    def test_create_geopackage(self):
        """ Test to create a geopackage. """
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
        self.assertEqual(5, len(layer.dataProvider().subLayers()))

    def test_apply_qml_styles(self):
        """ Test to apply some QML to loaded layers in the canvas. """
        gpkg = plugin_test_data_path('main_geopackage.gpkg', copy=True)

        name = 'pression'
        pression_layer = QgsVectorLayer('{}|layername={}'.format(gpkg, name), name, 'ogr')
        self.assertTrue(pression_layer.isValid())

        name = 'habitat'
        habitat_layer = QgsVectorLayer('{}|layername={}'.format(gpkg, name), name, 'ogr')
        self.assertTrue(habitat_layer.isValid())

        params = {
            "PRESSURE_LAYER": pression_layer,
            "HABITAT_LAYER": habitat_layer,
        }
        result = run("mercicor:load_qml", params)
        self.assertGreaterEqual(2, result['QML_LOADED'])
