__copyright__ = "Copyright 2021, 3Liz"
__license__ = "GPL version 3"
__email__ = "info@3liz.org"

from typing import Optional, Tuple

import processing

from qgis.core import (
    QgsFeature,
    QgsFeatureRequest,
    QgsProcessing,
    QgsProcessingMultiStepFeedback,
    QgsProcessingParameterVectorLayer,
    QgsProcessingUtils,
    edit,
)

from mercicor.processing.calcul.base import CalculAlgorithm


class CalculHabitatPressionEtatEcologique(CalculAlgorithm):

    HABITAT_LAYER = 'HABITAT_LAYER'
    PRESSION_LAYER = 'PRESSION_LAYER'
    HABITAT_PRESSION_ETAT_ECOLOGIQUE_LAYER = 'HABITAT_PRESSION_ETAT_ECOLOGIQUE_LAYER'

    def __init__(self):
        self.output_layer = None
        super().__init__()

    def name(self):
        return 'calcul_habitat_pression_etat_ecologique'

    def displayName(self):
        return 'Ajout des entités de l\'état écologique des habitats en fonction de la pression'

    def shortHelpString(self):
        return (
            'Ajout des entités de l\'état écologique des habitats en fonction des pressions.'
        )

    def initAlgorithm(self, config):

        parameter = QgsProcessingParameterVectorLayer(
            self.HABITAT_LAYER,
            "Couches des habitats",
            [QgsProcessing.TypeVectorPolygon],
            defaultValue='habitat',
        )
        self.set_tooltip_parameter(parameter, "Couche des habitats dans le geopackage")
        self.addParameter(parameter)

        parameter = QgsProcessingParameterVectorLayer(
            self.PRESSION_LAYER,
            "Couches des pressions",
            [QgsProcessing.TypeVectorPolygon],
            defaultValue='pression',
        )
        self.set_tooltip_parameter(parameter, "Couche des pressions dans le geopackage")
        self.addParameter(parameter)

        parameter = QgsProcessingParameterVectorLayer(
            self.HABITAT_PRESSION_ETAT_ECOLOGIQUE_LAYER,
            "Couches habitat pression habitat pression écologique",
            [QgsProcessing.TypeVectorPolygon],
            defaultValue='habitat_pression_etat_ecologique',
        )
        self.set_tooltip_parameter(
            parameter, "Couches habitat pression habitat pression écologique dans le geopackage")
        self.addParameter(parameter)

    def checkParameterValues(self, parameters, context):
        layers = [
            self.parameterAsVectorLayer(parameters, self.HABITAT_LAYER, context),
            self.parameterAsVectorLayer(parameters, self.PRESSION_LAYER, context),
            self.parameterAsVectorLayer(parameters, self.HABITAT_PRESSION_ETAT_ECOLOGIQUE_LAYER, context),
        ]
        for layer in layers:
            flag, msg = self.check_layer_is_geopackage(layer)
            if not flag:
                return False, msg

        return super().checkParameterValues(parameters, context)

    def processAlgorithm(self, parameters, context, feedback):
        habitat = self.parameterAsVectorLayer(parameters, self.HABITAT_LAYER, context)
        pression = self.parameterAsVectorLayer(parameters, self.PRESSION_LAYER, context)
        self.output_layer = self.parameterAsVectorLayer(
            parameters, self.HABITAT_PRESSION_ETAT_ECOLOGIQUE_LAYER, context)

        multi_feedback = QgsProcessingMultiStepFeedback(4, feedback)

        multi_feedback.setCurrentStep(0)
        multi_feedback.pushInfo("Calcul de l'intersection entre les couches habitats et pressions")
        params = {
            'INPUT': habitat,
            'OVERLAY': pression,
            'INPUT_FIELDS': [],  # All fields
            'OVERLAY_FIELDS': ['id', 'scenario_id'],
            'OVERLAY_FIELDS_PREFIX': 'pression_',
            'OUTPUT': 'TEMPORARY_OUTPUT',
        }
        results = processing.run(
            "native:intersection",
            params,
            context=context,
            feedback=multi_feedback,
            is_child_algorithm=True,
        )
        intersection = QgsProcessingUtils.mapLayerFromString(results['OUTPUT'], context, True)

        multi_feedback.pushInfo("Renommage des champs")
        multi_feedback.setCurrentStep(1)
        # Rename id to habitat_id
        # Rename pression_scenario_id to scenario_id
        index_habitat = intersection.fields().indexOf('id')
        index_scenario = intersection.fields().indexOf('pression_scenario_id')

        with edit(intersection):
            intersection.renameAttribute(index_habitat, 'habitat_id')
            intersection.renameAttribute(index_scenario, 'scenario_id')

        intersection.updateFields()

        fields = ['habitat_id', 'pression_id', 'scenario_id']
        multi_feedback.pushInfo(
            "Collect des géométries ayant les couples {} identiques".format(' ,'.join(fields)))
        multi_feedback.setCurrentStep(2)
        params = {
            'INPUT': intersection,
            'FIELD': fields,
            'OUTPUT': 'TEMPORARY_OUTPUT',
        }
        results = processing.run(
            "native:collect",
            params,
            context=context,
            feedback=multi_feedback,
            is_child_algorithm=True,
        )

        multi_feedback.pushInfo("Correction des géométries")
        multi_feedback.setCurrentStep(3)

        params = {
            'INPUT': results['OUTPUT'],
            'DISTANCE': 0,
            'OUTPUT': 'TEMPORARY_OUTPUT',
        }
        results = processing.run(
            "native:buffer",
            params,
            context=context,
            feedback=multi_feedback,
            is_child_algorithm=True)

        layer = QgsProcessingUtils.mapLayerFromString(results['OUTPUT'], context, True)

        multi_feedback.pushInfo("Import des entités dans la couche du geopackage")
        multi_feedback.setCurrentStep(4)
        field_map = {}
        for i, field in enumerate(self.output_layer.fields()):
            field_map[field.name()] = i

        with edit(self.output_layer):
            for feature in layer.getFeatures():
                habitat_id = feature['habitat_id']
                pression_id = feature['pression_id']
                scenario_id = feature['scenario_id']

                exists, existing_feature = self.feature_exists(
                    self.output_layer, habitat_id, pression_id, scenario_id)

                if exists:
                    self.output_layer.changeGeometry(existing_feature.id(), feature.geometry())

                    attribute_map = dict()
                    for field in layer.fields():
                        if field.name() in ('habitat_id', 'pression_id', 'scenario_id'):
                            continue

                        if field.name() in self.output_layer.fields().names():
                            attribute_map[field_map[field.name()]] = feature[field.name()]

                    self.output_layer.changeAttributeValues(existing_feature.id(), attribute_map)

                else:
                    # We create a new feature
                    out_feature = QgsFeature(self.output_layer.fields())
                    out_feature.setAttribute('habitat_id', habitat_id)
                    out_feature.setAttribute('pression_id', pression_id)
                    out_feature.setAttribute('scenario_id', scenario_id)
                    out_feature.setGeometry(feature.geometry())

                    for field in layer.fields():
                        if field.name() in ('habitat_id', 'pression_id', 'scenario_id'):
                            continue

                        if field.name() in self.output_layer.fields().names():
                            out_feature.setAttribute(field.name(), feature[field.name()])

                    self.output_layer.addFeature(out_feature)

        return {}

    def postProcess(self, context, feedback):
        self.output_layer.triggerRepaint()

    @staticmethod
    def feature_exists(layer, habitat_id, pression_id, scenario_id) -> Tuple[bool, Optional[QgsFeature]]:
        """ Check if the given feature exists. """
        request = QgsFeatureRequest()
        request.setLimit(1)
        request.setFilterExpression(
            '"habitat_id" = {habitat} AND "pression_id" = {pression} AND "scenario_id" = {scenario}'.format(
                habitat=habitat_id,
                pression=pression_id,
                scenario=scenario_id,
            ))
        feature = QgsFeature()
        if layer.getFeatures(request).nextFeature(feature):
            return True, feature
        else:
            return False, None
