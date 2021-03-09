"""Base class algorithm."""

__copyright__ = "Copyright 2021, 3Liz"
__license__ = "GPL version 3"
__email__ = "info@3liz.org"

from abc import abstractmethod
from os.path import isfile
from typing import Tuple

from qgis.core import Qgis, QgsProcessingAlgorithm, QgsProviderRegistry, QgsMapLayer
from qgis.PyQt.QtGui import QIcon

from mercicor.qgis_plugin_tools import resources_path


class BaseProcessingAlgorithm(QgsProcessingAlgorithm):

    def __init__(self):
        super().__init__()

    def createInstance(self):
        return type(self)()

    def flags(self):
        return super().flags() | QgsProcessingAlgorithm.FlagHideFromModeler

    def icon(self):
        icon = resources_path('icons', 'icon.jpg')
        if isfile(icon):
            return QIcon(icon)
        else:
            return super().icon()

    def parameters_help_string(self) -> str:
        """ Return a formatted help string for all parameters. """
        help_string = ''

        for param in self.parameterDefinitions():
            template = '{} : {}\n\n'
            if hasattr(param, 'tooltip_3liz'):
                info = param.tooltip_3liz
            else:
                info = ''

            if Qgis.QGIS_VERSION_INT >= 31500:
                info = param.help()

            if info:
                help_string += template.format(param.name(), info)

        return help_string

    @abstractmethod
    def shortHelpString(self):
        pass

    @staticmethod
    def check_layer_is_geopackage(layer: QgsMapLayer) -> Tuple[bool, str]:
        uri = QgsProviderRegistry.instance().decodeUri('ogr', layer.source())
        if not uri['path'].lower().endswith('.gpkg') or not uri['layerName']:
            message = (
                'La couche doit être le geopackage de la zone d\'étude et non pas {}'.format(
                    layer.source())
            )
            return False, message

        return True, ''
