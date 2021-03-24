__copyright__ = "Copyright 2021, 3Liz"
__license__ = "GPL version 3"
__email__ = "info@3liz.org"

import processing

from qgis.core import (
    QgsCategorizedSymbolRenderer,
    QgsFeature,
    QgsFeatureRequest,
    QgsGeometry,
    QgsProcessing,
    QgsProcessingParameterField,
    QgsProcessingParameterVectorLayer,
    QgsProcessingUtils,
    QgsRandomColorRamp,
    QgsRendererCategory,
    QgsSymbol,
    QgsWkbTypes,
)

from mercicor.processing.imports.base import BaseImportAlgorithm


class ImportHabitatData(BaseImportAlgorithm):

    INPUT_LAYER = 'INPUT_LAYER'
    NAME_FIELD = 'NAME_FIELD'
    FACIES_FIELD = 'FACIES_FIELD'
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
        return (
            'Import des données des habitats.\n'
            'Le champ du faciès doit être correctement formaté.\n'
            'Un style pour les habitats sera ajouté.\n'
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
                self.NAME_FIELD,
                "Champ comportant le nom de l'habitat",
                None,
                self.INPUT_LAYER,
                QgsProcessingParameterField.String,
            )
        )

        self.addParameter(
            QgsProcessingParameterField(
                self.FACIES_FIELD,
                "Champ comportant le faciès",
                None,
                self.INPUT_LAYER,
                QgsProcessingParameterField.String,
            )
        )

        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.OUTPUT_LAYER,
                "Couche des habitats de destination",
                [QgsProcessing.TypeVectorPolygon],
                defaultValue='habitat',
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        input_layer = self.parameterAsVectorLayer(parameters, self.INPUT_LAYER, context)
        facies_field = self.parameterAsExpression(parameters, self.FACIES_FIELD, context)
        name_field = self.parameterAsExpression(parameters, self.NAME_FIELD, context)
        self._output_layer = self.parameterAsVectorLayer(parameters, self.OUTPUT_LAYER, context)

        params = {
            'INPUT': input_layer,
            'DISTANCE': 0,
            'OUTPUT': 'TEMPORARY_OUTPUT'
        }
        results = processing.run(
            "native:buffer",
            params,
            context=context,
            feedback=feedback,
            is_child_algorithm=True)

        params = {
            'INPUT': results['OUTPUT'],
            'FIELD': [name_field, facies_field],
            'OUTPUT': 'TEMPORARY_OUTPUT'
        }
        results = processing.run(
            "native:collect",
            params,
            context=context,
            feedback=feedback,
            is_child_algorithm=True,
        )

        params = {
            'INPUT': results['OUTPUT'],
            'OUTPUT': 'TEMPORARY_OUTPUT'
        }
        results = processing.run(
            "native:promotetomulti",
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
                'OUTPUT': 'TEMPORARY_OUTPUT'
            }
            results = processing.run(
                "native:reprojectlayer",
                params,
                context=context,
                feedback=feedback,
                is_child_algorithm=True)

        params = {
            'INPUT': results['OUTPUT'],
            'DISTANCE': 0,
            'OUTPUT': 'memory:'
        }
        results = processing.run(
            "native:buffer",
            params,
            context=context,
            feedback=feedback,
            is_child_algorithm=True)

        layer = QgsProcessingUtils.mapLayerFromString(results['OUTPUT'], context, True)

        self.output_layer.startEditing()
        request = QgsFeatureRequest()
        request.setSubsetOfAttributes([name_field, facies_field], input_layer.fields())
        for input_feature in layer.getFeatures(request):

            if feedback.isCanceled():
                break

            output_feature = QgsFeature(self.output_layer.fields())
            geometry = QgsGeometry(input_feature.geometry())
            output_feature.setGeometry(geometry)
            output_feature.setAttribute('nom', input_feature[name_field])
            output_feature.setAttribute('facies', input_feature[facies_field])
            self.output_layer.addFeature(output_feature)

        self.output_layer.commitChanges()
        self.set_style()
        return {}

    def set_style(self):
        """ Set the categorized style using random color. """
        index = self.output_layer.fields().indexOf('nom')
        values = self.output_layer.uniqueValues(index)

        color = QgsRandomColorRamp()
        color.setTotalColorCount(len(values))

        categories = []
        for i, value in enumerate(values):
            symbol = QgsSymbol.defaultSymbol(QgsWkbTypes.PolygonGeometry)
            symbol.setColor(color.color(i))
            category = QgsRendererCategory(value, symbol, value)
            categories.append(category)

        renderer = QgsCategorizedSymbolRenderer('nom', categories)
        self.output_layer.setRenderer(renderer)

    def postProcess(self, context, feedback):
        self.output_layer.triggerRepaint()
