""" Test geopackage """

import os.path
import unittest

from os import listdir

import processing

from qgis.core import QgsProcessingContext, QgsProcessingFeedback, QgsProject

from mercicor.processing.provider import MercicorProvider as ProcessingProvider
from mercicor.qgis_plugin_tools import plugin_test_data_path, resources_path

__copyright__ = "Copyright 2019, 3Liz"
__license__ = "GPL version 3"
__email__ = "info@3liz.org"
__revision__ = "$Format:%H$"


class TestGeopackage(unittest.TestCase):

    def test_create_geopackage(self):
        """ test to create geopackage """
        provider = ProcessingProvider()
        project = QgsProject()
        context = QgsProcessingContext()
        context.setProject(project)
        feedback = QgsProcessingFeedback()

        params = {
            "FILE_GPKG": plugin_test_data_path('test.gpkg'),
            "PROJECT_NAME": 'test_geopackage',
            "PROJECT_CRS": 'EPSG:2154',
            "PROJECT_EXTENT": (
                '-338017.34377143125,834663.5259292874,752553.0288248351,1087604.7058821833 ',
                '[EPSG:2154]'
            )
        }
        alg = "{}:create_geopackage_project".format(provider.id())
        processing.run(
            alg, params, context=context, feedback=feedback
        )

        self.assertTrue(os.path.exists(plugin_test_data_path('test.gpkg')))
