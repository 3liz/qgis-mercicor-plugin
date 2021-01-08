__copyright__ = "Copyright 2021, 3Liz"
__license__ = "GPL version 3"
__email__ = "info@3liz.org"

import processing

from qgis.core import (
    QgsExpression,
    QgsExpressionContext,
    QgsExpressionContextUtils,
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

from mercicor.processing.imports.base import BaseImportAlgorithm

# from mercicor.processing.post_processor import TriggerRepaintPostProcessor


class ImportPressureData(BaseImportAlgorithm):

    INPUT_LAYER = 'INPUT_LAYER'
    EXPRESSION_FIELD = 'EXPRESSION_FIELD'
    OUTPUT_LAYER = 'OUTPUT_LAYER'

    def name(self):
        return 'import_donnees_pression'

    def displayName(self):
        return 'Import données pression'

    def shortHelpString(self):
        return 'Import des données de pression'

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
                self.EXPRESSION_FIELD,
                "Champ comportant l'expression",
                None,
                self.INPUT_LAYER,
                QgsProcessingParameterField.String,
            )
        )

        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.OUTPUT_LAYER,
                "Couche des pressions",
                [QgsProcessing.TypeVectorPolygon],
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        input_layer = self.parameterAsVectorLayer(parameters, self.INPUT_LAYER, context)
        expression_field = self.parameterAsExpression(parameters, self.EXPRESSION_FIELD, context)
        output_layer = self.parameterAsVectorLayer(parameters, self.OUTPUT_LAYER, context)

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

        if not isinstance(results['OUTPUT'], QgsVectorLayer):
            layer = QgsProcessingUtils.mapLayerFromString(results['OUTPUT'], context, True)
        else:
            layer = results['OUTPUT']

        expression_context = QgsExpressionContext()
        expression_context.appendScope(QgsExpressionContextUtils.globalScope())
        expression_context.appendScope(QgsExpressionContextUtils.projectScope(context.project()))
        expression_context.appendScope(QgsExpressionContextUtils.layerScope(layer))

        request = QgsFeatureRequest()
        request.setSubsetOfAttributes([expression_field], input_layer.fields())
        for input_feature in layer.getFeatures(request):

            if feedback.isCanceled():
                break

            expression_context.setFeature(input_feature)
            expression = QgsExpression(input_feature[expression_field])
            expression.prepare(expression_context)
            if expression.hasEvalError():
                raise QgsProcessingException(
                    '{} : {}'.format(expression.expression(), expression.evalErrorString()))

            value = expression.evaluate(expression_context)

            output_feature = QgsFeature(output_layer.fields())
            output_feature.setGeometry(input_feature.geometry())
            output_feature.setAttribute('type_pression', value)
            with edit(output_layer):
                output_layer.addFeature(output_feature)

        # context.layerToLoadOnCompletionDetails(
        #     output_layer.id()
        # ).setPostProcessor(
        #     TriggerRepaintPostProcessor.create()
        # )

        return {}

    # def postProcess(self, context, feedback):
    #     store = self.temporaryLayerStore()
    #     output_layer = self.parameterAsVectorLayer(parameters, self.OUTPUT_LAYER, context)
    #     out
