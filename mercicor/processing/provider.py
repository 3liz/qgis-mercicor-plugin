__copyright__ = "Copyright 2020, 3Liz"
__license__ = "GPL version 3"
__email__ = "info@3liz.org"

from qgis.core import QgsProcessingProvider
from qgis.PyQt.QtGui import QIcon

from mercicor.qgis_plugin_tools import resources_path


class MercicorProvider(QgsProcessingProvider):

    def loadAlgorithms(self):
        pass

    def id(self):  # NOQA
        return "mercicor"

    def icon(self):
        return QIcon(resources_path("icons", "icon.png"))

    def name(self):
        return "Mercicor"
