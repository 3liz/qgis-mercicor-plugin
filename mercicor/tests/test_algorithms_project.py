""" Test geopackage """

import os.path

from qgis.core import QgsProcessingContext, QgsProject, QgsVectorLayer
from qgis.processing import run

from mercicor.qgis_plugin_tools import plugin_test_data_path
from mercicor.tests.base_processing import BaseTestProcessing

__copyright__ = "Copyright 2019, 3Liz"
__license__ = "GPL version 3"
__email__ = "info@3liz.org"
__revision__ = "$Format:%H$"


class TestProjectAlgorithms(BaseTestProcessing):

    def test_create_geopackage(self):
        """ Test to create a geopackage. """
        params = {
            "FILE_GPKG": '/tmp/test_create_geopackage.gpkg',
            "PROJECT_NAME": 'test_geopackage',
            "PROJECT_CRS": 'EPSG:2154',
            "PROJECT_EXTENT": '0,10,0,10',
        }
        run("mercicor:create_geopackage_project", params)

        self.assertTrue(os.path.exists('/tmp/test_create_geopackage.gpkg'))

    def test_apply_qml_styles(self):
        """ Test to apply some QML to loaded layers in the canvas. """
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

        params = {
            "CHECK": True,
        }
        result = run("mercicor:load_qml", params, context=context)
        self.assertGreaterEqual(1, result['QML_LOADED'])
