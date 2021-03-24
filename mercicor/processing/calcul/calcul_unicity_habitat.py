__copyright__ = "Copyright 2021, 3Liz"
__license__ = "GPL version 3"
__email__ = "info@3liz.org"

import processing

from qgis.core import (
    QgsCategorizedSymbolRenderer,
    QgsExpression,
    QgsFeatureRequest,
    QgsPalLayerSettings,
    QgsProcessing,
    QgsProcessingLayerPostProcessorInterface,
    QgsProcessingOutputNumber,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterVectorLayer,
    QgsRandomColorRamp,
    QgsRendererCategory,
    QgsSymbol,
    QgsTextBufferSettings,
    QgsVectorLayerSimpleLabeling,
    QgsWkbTypes,
)

from mercicor.processing.calcul.base import CalculAlgorithm


class SetLabelingPostProcessor(QgsProcessingLayerPostProcessorInterface):
    instance = None
    fields = None

    def postProcessLayer(self, layer, context, feedback):
        layer.setLabelsEnabled(True)

        pal = QgsPalLayerSettings()
        # Expression combinant les nom d'habitat et du faciès
        pal.fieldName = "|| ' - ' || ".join(self.fields)
        pal.isExpression = True
        # Mais ce label est trop long
        # utilisation du faciès pour le label
        # et du nom pour le rendu
        pal.fieldName = self.fields[1]
        pal.isExpression = False
        pal.labelPerPart = True
        pal.placement = QgsPalLayerSettings.OverPoint

        txt_buff = QgsTextBufferSettings()
        txt_buff.setEnabled(True)

        txt_format = pal.format()
        txt_format.setBuffer(txt_buff)
        pal.setFormat(txt_format)

        layer.setLabeling(QgsVectorLayerSimpleLabeling(pal))

        renderer = layer.renderer()
        symbol = renderer.symbol()
        symbol.setSize(6)

        # Symbologie à partir du champs nom de l'habitat
        index = layer.fields().indexOf(self.fields[0])
        values = layer.uniqueValues(index)

        color = QgsRandomColorRamp()
        color.setTotalColorCount(len(values))

        categories = []
        for i, value in enumerate(values):
            symbol = QgsSymbol.defaultSymbol(QgsWkbTypes.PointGeometry)
            symbol.setColor(color.color(i))
            symbol.setSize(5)
            category = QgsRendererCategory(value, symbol, value)
            categories.append(category)

        renderer = QgsCategorizedSymbolRenderer(self.fields[0], categories)
        layer.setRenderer(renderer)

        layer.triggerRepaint()

    # Hack to work around sip bug!
    @staticmethod
    def create(fields) -> 'SetLabelingPostProcessor':
        SetLabelingPostProcessor.instance = SetLabelingPostProcessor()
        SetLabelingPostProcessor.fields = fields
        return SetLabelingPostProcessor.instance


class CalculUnicityHabitat(CalculAlgorithm):

    INPUT = 'INPUT'
    OUTPUT = 'OUTPUT'
    NUMBER_OF_UNIQUE = 'NUMBER_OF_UNIQUE'
    NUMBER_OF_NON_UNIQUE = 'NUMBER_OF_NON_UNIQUE'

    def __init__(self):
        """
        Fonction d'initialisation
        """
        super().__init__()
        # needed fields to check unicity
        self.fields = ['nom', 'facies']

    def name(self):
        return 'calcul_unicity_habitat'

    def displayName(self):
        return 'Calcul unicité habitat/faciès'

    def shortHelpString(self):
        return (
            'Vérification des données des habitats.\n'
            'Les champs nom et faciès doivent être unique '
            'par objet géographique.\n'
        )

    def initAlgorithm(self, config):

        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT,
                "Couche habitat",
                [QgsProcessing.TypeVectorPolygon],
                defaultValue='habitat',
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT,
                "Couche des habitat/faciès à unifier",
                QgsProcessing.TypeVectorPoint,
                optional=True,
            )
        )

        self.addOutput(
            QgsProcessingOutputNumber(
                self.NUMBER_OF_UNIQUE,
                'Nombre de couple habitat/faciès unique'
            )
        )

        self.addOutput(
            QgsProcessingOutputNumber(
                self.NUMBER_OF_NON_UNIQUE,
                'Nombre de couple habitat/faciès non unique'
            )
        )

    def checkParameterValues(self, parameters, context):
        """
        Check if source layer is in the geopackage and has fields nom and facies
        """
        source = self.parameterAsVectorLayer(parameters, self.INPUT, context)
        flag, msg = self.check_layer_is_geopackage(source)
        if not flag:
            return False, msg

        layer_fields = source.fields()
        for field_name in self.fields:
            field_idx = layer_fields.lookupField(field_name)
            if field_idx < 0:
                return False, 'Le champs {} manque'.format(field_name)

        return super().checkParameterValues(parameters, context)

    def processAlgorithm(self, parameters, context, feedback):
        source = self.parameterAsSource(parameters, self.INPUT, context)

        request = QgsFeatureRequest()
        request.setFlags(QgsFeatureRequest.NoGeometry)
        request.setSubsetOfAttributes(self.fields, source.fields())
        request.addOrderBy("|| ' - ' || ".join(self.fields))

        unique_couples = []
        non_unique_couples = []
        for src_feature in source.getFeatures(request):
            couple = (
                src_feature[self.fields[0]],
                src_feature[self.fields[1]]
            )

            if couple not in unique_couples:
                unique_couples.append(couple)
            else:
                non_unique_couples.append(couple)

        if not non_unique_couples:
            feedback.pushInfo('L\'ensemble des couples noms/faciès sont uniques')
            (sink, dest_id) = self.parameterAsSink(
                parameters, self.OUTPUT, context,
                source.fields(), source.wkbType(), source.sourceCrs())
            return {
                self.OUTPUT: dest_id,
                self.NUMBER_OF_UNIQUE: len(unique_couples),
                self.NUMBER_OF_NON_UNIQUE: 0
            }

        feedback.pushInfo('Certains couples ne sont pas uniques :')
        for couple in non_unique_couples:
            feedback.pushInfo('   {} - {}'.format(couple[0], couple[1]))

        expressions = []
        for couple in non_unique_couples:
            exp = ' AND '.join([
                QgsExpression.createFieldEqualityExpression(self.fields[0], couple[0]),
                QgsExpression.createFieldEqualityExpression(self.fields[1], couple[1])
            ])
            expressions.append(exp)
        exp = '('
        exp += ') OR ('.join(expressions)
        exp += ')'
        feedback.pushDebugInfo(exp)
        exp_context = self.createExpressionContext(parameters, context, source)

        request = QgsFeatureRequest()
        request.setFilterExpression(exp)
        request.setExpressionContext(exp_context)

        layer = source.materialize(request)

        params = {
            'ALL_PARTS': True,
            'INPUT': layer,
            'OUTPUT': 'TEMPORARY_OUTPUT'
        }
        results = processing.run(
            "native:pointonsurface",
            params,
            context=context,
            feedback=feedback,
            is_child_algorithm=True,
        )

        params = {
            'INPUT': results['OUTPUT'],
            'FIELD': self.fields,
            'OUTPUT': parameters[self.OUTPUT]
        }
        results = processing.run(
            "native:collect",
            params,
            context=context,
            feedback=feedback,
            is_child_algorithm=True,
        )

        output_layer = results['OUTPUT']
        if context.willLoadLayerOnCompletion(output_layer):
            layer_details = context.layerToLoadOnCompletionDetails(output_layer)
            output_def = self.parameterDefinition(self.OUTPUT)
            layer_details.name = output_def.description()
            layer_details.setPostProcessor(
                SetLabelingPostProcessor.create(self.fields)
            )

        return {
            self.OUTPUT: output_layer,
            self.NUMBER_OF_UNIQUE: len(unique_couples),
            self.NUMBER_OF_NON_UNIQUE: len(non_unique_couples)
        }
