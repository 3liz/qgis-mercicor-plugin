""" Test geopackage """

import os.path

from qgis.core import QgsProcessingContext, QgsProcessingFeedback, QgsProject
from qgis.processing import run

from mercicor.processing.provider import MercicorProvider as ProcessingProvider
from mercicor.tests.base_processing import BaseTestProcessing

__copyright__ = "Copyright 2019, 3Liz"
__license__ = "GPL version 3"
__email__ = "info@3liz.org"
__revision__ = "$Format:%H$"


class TestGeopackage(BaseTestProcessing):

    def test_create_geopackage(self):
        """ Test to create geopackage. """
        provider = ProcessingProvider()
        project = QgsProject()
        context = QgsProcessingContext()
        context.setProject(project)
        feedback = QgsProcessingFeedback()

        params = {
            "FILE_GPKG": '/tmp/test_create_geopackage.gpkg',
            "PROJECT_NAME": 'test_geopackage',
            "PROJECT_CRS": 'EPSG:2154',
            "PROJECT_EXTENT": (
                '-338017.34377143125,834663.5259292874,752553.0288248351,1087604.7058821833'
            )
        }
        alg = "{}:create_geopackage_project".format(provider.id())
        run(
            alg, params, context=context, feedback=feedback
        )

        self.assertTrue(os.path.exists('/tmp/test_create_geopackage.gpkg'))
