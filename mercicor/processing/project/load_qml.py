__copyright__ = "Copyright 2020, 3Liz"
__license__ = "GPL version 3"
__email__ = "info@3liz.org"
__revision__ = "$Format:%H$"

import os

from qgis.core import (
    QgsMapLayer,
    QgsProcessingOutputNumber,
    QgsProcessingParameterBoolean,
)

from mercicor.processing.project.base import BaseProjectAlgorithm
from mercicor.qgis_plugin_tools import resources_path, tr


class LoadStyles(BaseProjectAlgorithm):

    CHECK = 'CHECK'
    QML_LOADED = 'QML_LOADED'

    def __init__(self):
        super().__init__()
        self.success = 0

    def name(self):
        return "load_qml"

    def displayName(self):
        return tr("Charger les styles")

    def shortHelpString(self):
        return tr("Charger les styles pour les différentes couches.")

    def initAlgorithm(self, config):
        self.addParameter(QgsProcessingParameterBoolean(self.CHECK, "Appliquer les styles"))
        self.addOutput(QgsProcessingOutputNumber(self.QML_LOADED, 'Nombre de QML chargés'))

    def checkParameterValues(self, parameters, context):
        flag = self.parameterAsBoolean(parameters, self.CHECK, context)
        if not flag:
            return False, 'Vous devez utiliser la case à cocher pour l\'application des styles.'

        return super().checkParameterValues(parameters, context)

    def prepareAlgorithm(self, parameters, context, feedback):
        _ = parameters

        expected_names = ["habitat", "pression"]
        qml_component = {
            'style': QgsMapLayer.Symbology,
            'form': QgsMapLayer.Forms,
        }

        self.success = 0

        for name, component in qml_component.items():
            for layer_name in expected_names:
                layers = context.project().mapLayersByName(layer_name)
                for layer in layers:
                    qml_file = resources_path('qml', name, '{}.qml'.format(layer_name))
                    if not os.path.exists(qml_file):
                        continue
                    layer.loadNamedStyle(qml_file, component)
                    feedback.pushInfo(layer.name() + "Style for {} successfully loaded")
                    self.success += 1

        return True

    def processAlgorithm(self, parameters, context, feedback):
        _, _, _ = parameters, context, feedback
        return {self.QML_LOADED: self.success}
