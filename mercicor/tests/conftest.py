"""Configuration file for PyTest."""

import sys

from osgeo import gdal
from qgis.core import Qgis
from qgis.PyQt import Qt

__copyright__ = "Copyright 2020, 3Liz"
__license__ = "GPL version 3"
__email__ = "info@3liz.org"


def pytest_report_header(config):
    """Used by PyTest and Unittest."""
    message = "QGIS : {}\n".format(Qgis.QGIS_VERSION_INT)
    message += "Python GDAL : {}\n".format(gdal.VersionInfo("VERSION_NUM"))
    message += "Python : {}\n".format(sys.version)
    # message += 'Python path : {}'.format(sys.path)
    message += "QT : {}".format(Qt.QT_VERSION_STR)
    return message
