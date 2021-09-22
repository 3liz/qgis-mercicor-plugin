__copyright__ = "Copyright 2021, 3Liz"
__license__ = "GPL version 3"
__email__ = "info@3liz.org"

from typing import Optional, Tuple, Union

import processing

from qgis.core import (
    QgsExpression,
    QgsFeature,
    QgsFeatureRequest,
    QgsProcessing,
    QgsProcessingMultiStepFeedback,
    QgsProcessingParameterVectorLayer,
    QgsProcessingUtils,
    edit,
)

from mercicor.definitions.project_type import ProjectType
from mercicor.processing.calcul.base import CalculAlgorithm


class BaseCalculHabitatImpactEtatEcologique(CalculAlgorithm):

    @classmethod
    def fields(cls) -> tuple:
        return (
            "perc_bsd", "perc_bsm", "bsd_recouv_cor", "bsd_p_acrop", "bsd_vital_cor",
            "bsd_comp_struc", "bsd_taille_cor", "bsd_dens_juv", "bsd_f_sessile", "bsd_recouv_ma",
            "bsm_fragm_herb", "bsm_recouv_her", "bsm_haut_herb", "bsm_dens_herb", "bsm_div_herb",
            "bsm_epibiose", "man_fragm", "man_recouv", "man_diam_tronc", "man_dens", "man_diversit",
            "man_vital", "pmi_div_poi", "pmi_predat_poi", "pmi_scarib_poi", "pmi_macro_inv",
            "note_bsd", "note_bsm", "note_ben", "note_man", "note_pmi", "score_mercicor"
        )

    HABITAT_LAYER = 'HABITAT_LAYER'

    def __init__(self):
        self.output_layer = None
        super().__init__()

    @property
    def project_type(self) -> ProjectType:
        # noinspection PyTypeChecker
        return NotImplementedError

    @property
    def impact_id(self) -> str:
        # noinspection PyTypeChecker
        return NotImplementedError

    @property
    def impact_field(self) -> Union[str, None]:
        return None

    @property
    def fields_id(self) -> tuple:
        return 'habitat_id', 'scenario_id', self.impact_id

    def group(self):
        return 'Calcul {}'.format(self.project_type.label)

    def groupId(self):
        return 'calcul_group_{}'.format(self.project_type.label)

    def name(self):
        return 'calcul_habitat_{}_etat_ecologique'.format(self.project_type.label)

    def displayName(self):
        return (
            'Ajout des entités de l\'état écologique des habitats en fonction de la {}'.format(
                self.project_type.label))

    def shortHelpString(self):
        return (
            'Ajout des entités de l\'état écologique des habitats en fonction de la {}.'.format(
                self.project_type.label)
        )

    def initAlgorithm(self, config):
        _ = config
        parameter = QgsProcessingParameterVectorLayer(
            self.HABITAT_LAYER,
            "Couches des habitats",
            [QgsProcessing.TypeVectorPolygon],
            defaultValue='habitat',
        )
        self.set_tooltip_parameter(parameter, "Couche des habitats dans le geopackage")
        self.addParameter(parameter)

        parameter = QgsProcessingParameterVectorLayer(
            self.IMPACT_LAYER,
            self.project_type.label_impact,
            [QgsProcessing.TypeVectorPolygon],
            defaultValue=self.project_type.couche_impact,
        )
        self.set_tooltip_parameter(parameter, self.project_type.label_impact)
        self.addParameter(parameter)

        parameter = QgsProcessingParameterVectorLayer(
            self.HABITAT_IMPACT_ETAT_ECOLOGIQUE_LAYER,
            self.project_type.label_habitat_impact_etat_ecologique,
            [QgsProcessing.TypeVectorPolygon],
            defaultValue=self.project_type.couche_habitat_impact_etat_ecologique,
        )
        self.set_tooltip_parameter(
            parameter, self.project_type.label_habitat_impact_etat_ecologique)
        self.addParameter(parameter)

    def checkParameterValues(self, parameters, context):
        layers = [
            self.parameterAsVectorLayer(parameters, self.HABITAT_LAYER, context),
            self.parameterAsVectorLayer(parameters, self.IMPACT_LAYER, context),
            self.parameterAsVectorLayer(parameters, self.HABITAT_IMPACT_ETAT_ECOLOGIQUE_LAYER, context),
        ]
        for layer in layers:
            flag, msg = self.check_layer_is_geopackage(layer)
            if not flag:
                return False, msg

        return super().checkParameterValues(parameters, context)

    def processAlgorithm(self, parameters, context, feedback):
        habitat = self.parameterAsVectorLayer(parameters, self.HABITAT_LAYER, context)
        impact = self.parameterAsVectorLayer(parameters, self.IMPACT_LAYER, context)
        self.output_layer = self.parameterAsVectorLayer(
            parameters, self.HABITAT_IMPACT_ETAT_ECOLOGIQUE_LAYER, context)

        multi_feedback = QgsProcessingMultiStepFeedback(4, feedback)

        multi_feedback.setCurrentStep(0)
        multi_feedback.pushInfo(
            "Calcul de l'intersection entre les couches habitat et {}".format(self.project_type.label))
        params = {
            'INPUT': habitat,
            'OVERLAY': impact,
            'INPUT_FIELDS': [],  # All fields
            'OVERLAY_FIELDS': ['id', 'scenario_id'],
            'OVERLAY_FIELDS_PREFIX': '{}_'.format(self.project_type.label),
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
        # Rename pression_scenario_id to scenario_id (or compensation_id)
        index_habitat = intersection.fields().indexOf('id')
        index_impact_id = intersection.fields().indexOf('{}_scenario_id'.format(self.project_type.label))

        with edit(intersection):
            intersection.renameAttribute(index_habitat, 'habitat_id')
            intersection.renameAttribute(index_impact_id, 'scenario_id')

        intersection.updateFields()

        multi_feedback.pushInfo(
            "Collect des géométries ayant les couples {} identiques".format(' ,'.join(self.fields_id)))
        multi_feedback.setCurrentStep(2)
        params = {
            'INPUT': intersection,
            'FIELD': list(self.fields_id),
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
                impact_id = feature[self.impact_id]
                scenario_id = feature['scenario_id']

                # TODO need to check for compensation this behavior
                if self.impact_field:
                    # Test du type de pression associé
                    filter_expression = QgsExpression.createFieldEqualityExpression('id', impact_id)
                    filter_request = QgsFeatureRequest(QgsExpression(filter_expression))
                    filter_request.setLimit(1)
                    for press in impact.getFeatures(filter_expression):
                        pression_emprise = (press['type_pression'] == 6)
                        break
                else:
                    pression_emprise = False

                exists, existing_feature = self.feature_exists(
                    self.output_layer, habitat_id, impact_id, scenario_id)

                if exists:
                    self.output_layer.changeGeometry(existing_feature.id(), feature.geometry())

                    attribute_map = {}
                    for field in layer.fields():
                        field_name = field.name()
                        if field_name in self.fields_id:
                            continue

                        if field_name in self.output_layer.fields().names():
                            if pression_emprise and field_name in self.fields():
                                attribute_map[field_map[field_name]] = 0
                            else:
                                attribute_map[field_map[field_name]] = feature[field_name]

                    self.output_layer.changeAttributeValues(existing_feature.id(), attribute_map)

                else:
                    # We create a new feature
                    out_feature = QgsFeature(self.output_layer.fields())
                    out_feature.setAttribute('habitat_id', habitat_id)
                    out_feature.setAttribute(self.impact_id, impact_id)
                    out_feature.setAttribute('scenario_id', scenario_id)
                    out_feature.setGeometry(feature.geometry())

                    for field in layer.fields():
                        field_name = field.name()
                        if field_name in self.fields_id:
                            continue

                        if field_name in self.output_layer.fields().names():
                            if pression_emprise and field_name in self.fields():
                                out_feature.setAttribute(field_name, 0)
                            else:
                                out_feature.setAttribute(field_name, feature[field_name])

                    self.output_layer.addFeature(out_feature)

        return {}

    def postProcess(self, context, feedback):
        _ = context, feedback
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

        return False, None


class CalculHabitatPressionEtatEcologique(BaseCalculHabitatImpactEtatEcologique):

    IMPACT_LAYER = 'PRESSION_LAYER'
    HABITAT_IMPACT_ETAT_ECOLOGIQUE_LAYER = 'HABITAT_PRESSION_ETAT_ECOLOGIQUE_LAYER'

    @property
    def project_type(self):
        return ProjectType.Pression

    @property
    def impact_id(self):
        return 'pression_id'

    @property
    def impact_field(self):
        return 'type_pression'


class CalculHabitatCompensationEtatEcologique(BaseCalculHabitatImpactEtatEcologique):

    IMPACT_LAYER = 'COMPENSATION_LAYER'
    HABITAT_IMPACT_ETAT_ECOLOGIQUE_LAYER = 'HABITAT_COMPENSATION_ETAT_ECOLOGIQUE_LAYER'

    @property
    def project_type(self):
        return ProjectType.Compensation

    @property
    def impact_id(self):
        return 'compensation_id'
