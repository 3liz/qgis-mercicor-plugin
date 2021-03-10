__copyright__ = "Copyright 2021, 3Liz"
__license__ = "GPL version 3"
__email__ = "info@3liz.org"

import processing

from qgis.core import (
    QgsFeature,
    QgsFeatureRequest,
    QgsProcessing,
    QgsProcessingException,
    QgsProcessingParameterField,
    QgsProcessingParameterVectorLayer,
    QgsProcessingUtils,
    QgsVectorLayer,
    edit,
)
from qgis.PyQt.QtCore import NULL

from mercicor.processing.imports.base import BaseImportAlgorithm


class ImportPressureData(BaseImportAlgorithm):

    INPUT_LAYER = 'INPUT_LAYER'
    PRESSURE_FIELD = 'PRESSURE_FIELD'
    OUTPUT_LAYER = 'OUTPUT_LAYER'

    def __init__(self):
        super().__init__()
        self._output_layer = None

        # Values for "pression"
        self.expected_values = {1, 2, 3, 4, 5, 6, NULL}

    @property
    def output_layer(self):
        return self._output_layer

    def name(self):
        return 'import_donnees_pression'

    def displayName(self):
        return 'Import données pression'

    def shortHelpString(self):
        return (
            'Import des données de pression.\n\n'
            'Le champ des pressions doit être correctement formaté : \n'
            '{}'.format(', '.join([str(i) for i in self.expected_values]))
        )

    def initAlgorithm(self, config):

        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT_LAYER,
                "Couche pour l'import",
                [QgsProcessing.TypeVectorPolygon],
            )
        )

        self.addParameter(
            QgsProcessingParameterField(
                self.PRESSURE_FIELD,
                "Champ comportant la pression",
                None,
                self.INPUT_LAYER,
                QgsProcessingParameterField.Numeric,
            )
        )

        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.OUTPUT_LAYER,
                "Couche des pressions de destination",
                [QgsProcessing.TypeVectorPolygon],
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        input_layer = self.parameterAsVectorLayer(parameters, self.INPUT_LAYER, context)
        pressure_field = self.parameterAsExpression(parameters, self.PRESSURE_FIELD, context)
        self._output_layer = self.parameterAsVectorLayer(parameters, self.OUTPUT_LAYER, context)

        index = input_layer.fields().indexOf(pressure_field)
        unique_values = input_layer.uniqueValues(index)
        if not unique_values.issubset(self.expected_values):
            feedback.reportError(
                'Valeur possible pour la pression : ' + ', '.join([str(i) for i in self.expected_values]))
            diff = unique_values - self.expected_values
            raise QgsProcessingException(
                'Valeur inconnue pour la pression : ' + ', '.join([str(i) for i in diff]))

        params = {
            'INPUT': input_layer,
            'OUTPUT': 'memory:'
        }
        results = processing.run(
            "native:multiparttosingleparts",
            params,
            context=context,
            feedback=feedback,
            is_child_algorithm=True)

        if input_layer.crs() != self.output_layer.crs():
            feedback.pushInfo(
                'Le CRS de la couche de destination est différent. Reprojection en {}…'.format(
                    self.output_layer.crs().authid()))

            params = {
                'INPUT': results['OUTPUT'],
                'TARGET_CRS': self.output_layer.crs(),
                'OUTPUT': 'memory:'
            }
            results = processing.run(
                "native:reprojectlayer",
                params,
                context=context,
                feedback=feedback,
                is_child_algorithm=True)

        if not isinstance(results['OUTPUT'], QgsVectorLayer):
            layer = QgsProcessingUtils.mapLayerFromString(results['OUTPUT'], context, True)
        else:
            layer = results['OUTPUT']

        request = QgsFeatureRequest()
        request.setSubsetOfAttributes([pressure_field], input_layer.fields())
        for input_feature in layer.getFeatures(request):

            if feedback.isCanceled():
                break

            output_feature = QgsFeature(self.output_layer.fields())
            output_feature.setGeometry(input_feature.geometry())
            output_feature.setAttribute('type_pression', input_feature[pressure_field])
            with edit(self.output_layer):
                self.output_layer.addFeature(output_feature)

        return {}

    def postProcess(self, context, feedback):
        self.output_layer.reloadData()
        self.output_layer.triggerRepaint()
