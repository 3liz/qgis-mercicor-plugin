__copyright__ = "Copyright 2020, 3Liz"
__license__ = "GPL version 3"
__email__ = "info@3liz.org"
__revision__ = "$Format:%H$"

import os

from qgis.core import (
    QgsMapLayer,
    QgsProcessingParameterDefinition,
    QgsProcessingParameterString,
)

from mercicor.processing.project.base import BaseProjectAlgorithm
from mercicor.qgis_plugin_tools import resources_path, tr


class LoadStyles(BaseProjectAlgorithm):

    INPUT = "INPUT"
    OUTPUT_MSG = "OUTPUT MSG"

    def name(self):
        return "load_qml"

    def displayName(self):
        return tr("Charger les styles")

    def shortHelpString(self):
        return tr("Charger les styles pour les différentes couches.")

    def initAlgorithm(self, config):
        parameter = QgsProcessingParameterString(self.INPUT, "Champ qui ne sert à rien.")
        parameter.setFlags(parameter.flags() | QgsProcessingParameterDefinition.FlagHidden)
        self.addParameter(parameter)

    def prepareAlgorithm(self, parameters, context, feedback):
        _ = parameters
        expected_names = ["habitat", "pression"]
        qml_component = {
            'style': QgsMapLayer.Symbology,
            'form': QgsMapLayer.Forms,
        }

        for name, component in qml_component.items():
            for layer_name in expected_names:
                layers = context.project().mapLayersByName(layer_name)
                for layer in layers:
                    qml_file = resources_path('qml', name, '{}.qml'.format(layer_name))
                    if not os.path.exists(qml_file):
                        continue
                    layer.loadNamedStyle(qml_file, component)
                    feedback.pushInfo(layer.name() + "Style for {} successfully loaded")

        return True

    def processAlgorithm(self, parameters, context, feedback):
        _, _, _ = parameters, context, feedback
        return {}
