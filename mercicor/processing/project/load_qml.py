__copyright__ = "Copyright 2020, 3Liz"
__license__ = "GPL version 3"
__email__ = "info@3liz.org"
__revision__ = "$Format:%H$"

import os

from qgis.core import (
    QgsMapLayer,
    QgsProcessing,
    QgsProcessingOutputNumber,
    QgsProcessingParameterVectorLayer,
)

from mercicor.processing.project.base import BaseProjectAlgorithm
from mercicor.qgis_plugin_tools import resources_path, tr


class LoadStyles(BaseProjectAlgorithm):

    PRESSURE_LAYER = 'PRESSURE_LAYER'
    HABITAT_LAYER = 'HABITAT_LAYER'
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
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.PRESSURE_LAYER,
                "Couche des pressions",
                [QgsProcessing.TypeVectorPolygon],
                defaultValue='pression',
                optional=True,
            )
        )
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.HABITAT_LAYER,
                "Couche des habitats",
                [QgsProcessing.TypeVectorPolygon],
                defaultValue='habitat',
                optional=True,
            )
        )
        self.addOutput(QgsProcessingOutputNumber(self.QML_LOADED, 'Nombre de QML chargés'))

    def prepareAlgorithm(self, parameters, context, feedback):

        pressure_layer = self.parameterAsVectorLayer(parameters, self.PRESSURE_LAYER, context)
        habitat_layer = self.parameterAsVectorLayer(parameters, self.HABITAT_LAYER, context)

        input_layers = {
            "habitat": habitat_layer,
            "pression": pressure_layer,
        }

        qml_component = {
            'style': QgsMapLayer.Symbology,
            'form': QgsMapLayer.Forms,
        }

        self.success = 0

        for name, component in qml_component.items():
            for layer_name, vector_layer in input_layers.items():
                qml_file = resources_path('qml', name, '{}.qml'.format(layer_name))
                if not os.path.exists(qml_file):
                    continue
                vector_layer.loadNamedStyle(qml_file, component)
                feedback.pushInfo(vector_layer.name() + "Style for {} successfully loaded")
                self.success += 1

        return True

    def processAlgorithm(self, parameters, context, feedback):
        _, _, _ = parameters, context, feedback
        return {self.QML_LOADED: self.success}
