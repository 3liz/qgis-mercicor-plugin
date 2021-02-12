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


class ImportHabitatData(BaseImportAlgorithm):

    INPUT_LAYER = 'INPUT_LAYER'
    NAME_FIELD = 'NAME_FIELD'
    EXPRESSION_FIELD = 'EXPRESSION_FIELD'
    OUTPUT_LAYER = 'OUTPUT_LAYER'

    def __init__(self):
        super().__init__()
        self._output_layer = None

    @property
    def output_layer(self):
        return self._output_layer

    def name(self):
        return 'import_donnees_habitat'

    def displayName(self):
        return 'Import données habitat'

    def shortHelpString(self):
        return 'Import des données des habitats'

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
                self.NAME_FIELD,
                "Champ comportant le nom de l'habitat",
                None,
                self.INPUT_LAYER,
                QgsProcessingParameterField.String,
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
                "Couche des habitats",
                [QgsProcessing.TypeVectorPolygon],
                defaultValue='habitat',
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        input_layer = self.parameterAsVectorLayer(parameters, self.INPUT_LAYER, context)
        expression_field = self.parameterAsExpression(parameters, self.EXPRESSION_FIELD, context)
        name_field = self.parameterAsExpression(parameters, self.NAME_FIELD, context)
        self._output_layer = self.parameterAsVectorLayer(parameters, self.OUTPUT_LAYER, context)

        params = {
            'INPUT': input_layer,
            'OUTPUT': 'memory:'
        }
        results = processing.run(
            "native:multiparttosingleparts",
            params,
            context=context,
            feedback=feedback,
            is_child_algorithm=True,
        )

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

            output_feature = QgsFeature(self.output_layer.fields())
            output_feature.setGeometry(input_feature.geometry())
            output_feature.setAttribute('nom_zni', input_feature[name_field])
            output_feature.setAttribute('sante', value)
            with edit(self.output_layer):
                self.output_layer.addFeature(output_feature)

        return {}

    def postProcess(self, context, feedback):
        self.output_layer.reloadData()
        self.output_layer.triggerRepaint()
