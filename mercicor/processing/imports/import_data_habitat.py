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
    NOM_ZNI_FIELD = 'NOM_ZNI_FIELD'
    SANTE_FIELD = 'SANTE_FIELD'
    OUTPUT_LAYER = 'OUTPUT_LAYER'

    def name(self):
        return 'import_donnees_habitat'

    def displayName(self):
        return 'Import données habitat'

    def shortHelpString(self):
        return 'Import des données concernant l\'habitat'

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
                self.NOM_ZNI_FIELD,
                "Champ pour 'nom_zni'",
                None,
                self.INPUT_LAYER,
            )
        )

        self.addParameter(
            QgsProcessingParameterField(
                self.SANTE_FIELD,
                "Expression pour le champ pour 'sante'",
                None,
                self.INPUT_LAYER,
            )
        )

        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.OUTPUT_LAYER,
                "Couche des habitats",
                [QgsProcessing.TypeVectorPolygon],
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        input_layer = self.parameterAsVectorLayer(parameters, self.INPUT_LAYER, context)
        nom_zni_field = self.parameterAsExpression(parameters, self.NOM_ZNI_FIELD_FIELD, context)
        sante_field = self.parameterAsExpression(parameters, self.SANTE_FIELD_FIELD, context)
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
