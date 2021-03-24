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
    QgsProcessingParameterString,
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
    SCENARIO_NAME = 'SCENARIO_NAME'
    SCENARIO_LAYER = 'SCENARIO_LAYER'
    OUTPUT_LAYER = 'OUTPUT_LAYER'

    def __init__(self):
        super().__init__()
        self._output_layer = None
        self.scenario_id = None

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
            '{values}\n'
            'Un scénario sera également crée et la couche sera filtrée pour ce scénario.'.format(
                values=', '.join([str(i) for i in self.expected_values]))
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

        parameter = QgsProcessingParameterString(
            self.SCENARIO_NAME,
            "Nom du scénario",
        )
        self.set_tooltip_parameter(
            parameter, 'Le nom du scénario en cours pour cette couche des pressions.')
        self.addParameter(parameter)

        parameter = QgsProcessingParameterVectorLayer(
            self.SCENARIO_LAYER,
            "Couche des scénarios de destination",
            [QgsProcessing.TypeVector],
            defaultValue="scenario_pression",
        )
        self.set_tooltip_parameter(
            parameter,
            'La couche de destination des scénarios doit être la couche qui est dans le geopackage.')
        self.addParameter(parameter)

        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.OUTPUT_LAYER,
                "Couche des pressions de destination",
                [QgsProcessing.TypeVectorPolygon],
                defaultValue="pression",
            )
        )

    def checkParameterValues(self, parameters, context):
        scenario_layer = self.parameterAsVectorLayer(parameters, self.SCENARIO_LAYER, context)
        flag, msg = self.check_layer_is_geopackage(scenario_layer)
        if not flag:
            return False, msg

        return super().checkParameterValues(parameters, context)

    def processAlgorithm(self, parameters, context, feedback):
        input_layer = self.parameterAsVectorLayer(parameters, self.INPUT_LAYER, context)
        pressure_field = self.parameterAsExpression(parameters, self.PRESSURE_FIELD, context)
        scenario_name = self.parameterAsString(parameters, self.SCENARIO_NAME, context)
        scenario_layer = self.parameterAsVectorLayer(parameters, self.SCENARIO_LAYER, context)
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
            'FIELD': [pressure_field],
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
            is_child_algorithm=True)

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

        self.scenario_id = self.insert_scenario(scenario_layer, scenario_name)
        feedback.pushInfo('Création du scénario numéro {} : {}'.format(self.scenario_id, scenario_name))

        request = QgsFeatureRequest()
        request.setSubsetOfAttributes([pressure_field], input_layer.fields())
        for input_feature in layer.getFeatures(request):

            if feedback.isCanceled():
                break

            output_feature = QgsFeature(self.output_layer.fields())
            output_feature.setGeometry(input_feature.geometry())
            output_feature.setAttribute('scenario_id', self.scenario_id)
            output_feature.setAttribute('type_pression', input_feature[pressure_field])
            with edit(self.output_layer):
                self.output_layer.addFeature(output_feature)

        if not self.output_layer.setSubsetString('"scenario_id" = {}'.format(self.scenario_id)):
            raise QgsProcessingException('Subset string is not valid')

        return {}

    @staticmethod
    def insert_scenario(layer: QgsVectorLayer, name: str) -> int:
        """ Insert the new scenario and get its ID. """
        feature = QgsFeature(layer.fields())
        feature.setAttribute('nom', name)
        with edit(layer):
            layer.addFeature(feature)

        request = QgsFeatureRequest()
        request.setLimit(1)
        request.addOrderBy('id', False)
        feature = QgsFeature()
        layer.getFeatures(request).nextFeature(feature)
        return feature['id']

    def postProcess(self, context, feedback):
        self.output_layer.reloadData()
        self.output_layer.triggerRepaint()
