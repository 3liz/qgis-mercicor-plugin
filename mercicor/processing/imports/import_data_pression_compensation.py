__copyright__ = "Copyright 2021, 3Liz"
__license__ = "GPL version 3"
__email__ = "info@3liz.org"

import processing

from qgis.core import (
    QgsFeature,
    QgsFeatureRequest,
    QgsProcessing,
    QgsProcessingException,
    QgsProcessingParameterBoolean,
    QgsProcessingParameterField,
    QgsProcessingParameterString,
    QgsProcessingParameterVectorLayer,
    QgsProcessingUtils,
    QgsVectorLayer,
    edit,
)
from qgis.PyQt.QtCore import NULL

from mercicor.definitions.project_type import ProjectType
from mercicor.processing.imports.base import BaseImportAlgorithm


class BaseImportImpactData(BaseImportAlgorithm):

    INPUT_LAYER = 'INPUT_LAYER'
    SCENARIO_NAME = 'SCENARIO_NAME'
    SCENARIO_LAYER = 'SCENARIO_LAYER'
    OUTPUT_LAYER = 'OUTPUT_LAYER'
    HABITAT_LAYER = 'HABITAT_LAYER'

    def __init__(self):
        super().__init__()
        self._output_layer = None
        self.scenario_id = None

    @property
    def output_layer(self):
        return self._output_layer

    @property
    def project_type(self) -> ProjectType:
        # noinspection PyTypeChecker
        return NotImplementedError

    @property
    def expected_values(self) -> set:
        """ Expected values for the input layer. """
        return set()

    @property
    def destination_impact_field(self) -> str:
        """ Destination impact field. """
        # noinspection PyTypeChecker
        return NotImplementedError

    def name(self):
        return 'import_donnees_{}'.format(self.project_type.label)

    def displayName(self):
        return 'Import données {}'.format(self.project_type.label)

    def shortHelpString(self):
        return (
            'Import des données de {project_type}.\n\n'
            'Un scénario sera également crée et la couche sera filtrée pour ce scénario.\n'
            'Il est également possible de lancer directement le calcul de l\'état écologique des '
            'habitats en fonction de la {project_type} à l\'aide de la case à cocher.'.format(
                project_type=self.project_type.label,
            )
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
                self.IMPACT_FIELD,
                "Champ comportant la {}".format(self.project_type.label),
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
            parameter, 'Le nom du scénario en cours pour cette couche de {}.'.format(self.project_type.label))
        self.addParameter(parameter)

        parameter = QgsProcessingParameterVectorLayer(
            self.SCENARIO_LAYER,
            self.project_type.label_scenario_impact,
            [QgsProcessing.TypeVector],
            defaultValue=self.project_type.couche_scenario_impact,
        )
        self.set_tooltip_parameter(
            parameter,
            'La couche de destination des scénarios doit être la couche qui est dans le geopackage.')
        self.addParameter(parameter)

        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.OUTPUT_LAYER,
                self.project_type.label_impact,
                [QgsProcessing.TypeVectorPolygon],
                defaultValue=self.project_type.couche_impact,
            )
        )

        self.addParameter(
            QgsProcessingParameterBoolean(
                self.APPLY_CALCUL_HABITAT_IMPACT_ETAT_ECOLOGIQUE,
                "Ajout des entités de l'état écologique des habitats en fonction de la {}.".format(
                    self.project_type.label)
            )
        )

        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.HABITAT_LAYER,
                "Couche des habitats de destination",
                [QgsProcessing.TypeVectorPolygon],
                defaultValue="habitat",
                optional=True,
            )
        )

        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.HABITAT_IMPACT_LAYER,
                self.project_type.label_habitat_impact_etat_ecologique,
                [QgsProcessing.TypeVectorPolygon],
                defaultValue=self.project_type.couche_habitat_impact_etat_ecologique,
                optional=True,
            )
        )

    def checkParameterValues(self, parameters, context):
        layers = [
            self.parameterAsVectorLayer(parameters, self.SCENARIO_LAYER, context),
            self.parameterAsVectorLayer(parameters, self.OUTPUT_LAYER, context),
        ]

        apply_calcul = self.parameterAsBoolean(
            parameters, self.APPLY_CALCUL_HABITAT_IMPACT_ETAT_ECOLOGIQUE, context)
        if apply_calcul:
            layers.append(self.parameterAsVectorLayer(parameters, self.HABITAT_LAYER, context))
            layers.append(self.parameterAsVectorLayer(parameters, self.HABITAT_IMPACT_LAYER, context))

        for layer in layers:
            flag, msg = self.check_layer_is_geopackage(layer)
            if not flag:
                return False, msg

        return super().checkParameterValues(parameters, context)

    def processAlgorithm(self, parameters, context, feedback):
        input_layer = self.parameterAsVectorLayer(parameters, self.INPUT_LAYER, context)
        impact_field = self.parameterAsExpression(parameters, self.IMPACT_FIELD, context)
        scenario_name = self.parameterAsString(parameters, self.SCENARIO_NAME, context)
        scenario_layer = self.parameterAsVectorLayer(parameters, self.SCENARIO_LAYER, context)
        self._output_layer = self.parameterAsVectorLayer(parameters, self.OUTPUT_LAYER, context)

        index = input_layer.fields().indexOf(impact_field)
        unique_values = input_layer.uniqueValues(index)
        if len(self.expected_values) and not unique_values.issubset(self.expected_values):
            feedback.reportError(
                'Valeur possible pour la {} : {}'.format(
                    self.project_type.label,
                    ', '.join([str(i) for i in self.expected_values])
                )
            )
            diff = unique_values - self.expected_values
            raise QgsProcessingException(
                'Valeur inconnue pour la {} : {}'.format(
                    self.project_type.label,
                    ', '.join([str(i) for i in diff])
                )
            )

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
            'FIELD': [impact_field],
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
        request.setSubsetOfAttributes([impact_field], input_layer.fields())
        for input_feature in layer.getFeatures(request):

            if feedback.isCanceled():
                break

            output_feature = QgsFeature(self.output_layer.fields())
            output_feature.setGeometry(input_feature.geometry())
            output_feature.setAttribute('scenario_id', self.scenario_id)
            output_feature.setAttribute(self.destination_impact_field, input_feature[impact_field])
            with edit(self.output_layer):
                self.output_layer.addFeature(output_feature)

        if not self.output_layer.setSubsetString('"scenario_id" = {}'.format(self.scenario_id)):
            raise QgsProcessingException('Subset string is not valid')

        apply_calcul = self.parameterAsBoolean(
            parameters, self.APPLY_CALCUL_HABITAT_IMPACT_ETAT_ECOLOGIQUE, context)

        # Si apply_calcul = False
        # Alors l'algo s'arrête ici
        if not apply_calcul:
            return {}

        habitat = self.parameterAsVectorLayer(parameters, self.HABITAT_LAYER, context)
        habitat_impact = self.parameterAsVectorLayer(parameters, self.HABITAT_IMPACT_LAYER, context)

        # Vérification de l'unicité des couples habitat/faciès
        params = {
            'INPUT': habitat,
            'OUTPUT': 'TEMPORARY_OUTPUT'
        }
        results = processing.run(
            "mercicor:calcul_unicity_habitat",
            params,
            context=context,
            feedback=feedback,
            is_child_algorithm=True)

        # Si les couple habitat/faciès ne sont pas unique
        # Alors le calcul ne se fait pas
        if results['NUMBER_OF_NON_UNIQUE']:
            feedback.pushDebugInfo(
                '{} couple(s) habitat/faciès non unique !'.format(results['NUMBER_OF_NON_UNIQUE']))
            feedback.reportError('Les couples habitat/faciès ne sont pas uniques !')
            msg = (
                'Utiliser l\'algorithme Mercicor "Calcul unicité habitat/faciès" pour corriger le problème.')
            feedback.pushInfo(msg)
            return {}

        params = {
            'HABITAT_LAYER': habitat,
            '{}_LAYER'.format(self.project_type.label.upper()): self.output_layer,
            'HABITAT_{}_ETAT_ECOLOGIQUE_LAYER'.format(self.project_type.label.upper()): habitat_impact
        }
        processing.run(
            "mercicor:calcul_habitat_{}_etat_ecologique".format(self.project_type.label),
            params,
            context=context,
            feedback=feedback,
            is_child_algorithm=True,
        )

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


class ImportDataPression(BaseImportImpactData):

    IMPACT_FIELD = 'PRESSION_FIELD'
    APPLY_CALCUL_HABITAT_IMPACT_ETAT_ECOLOGIQUE = 'APPLY_CALCUL_HABITAT_PRESSION_ETAT_ECOLOGIQUE'
    HABITAT_IMPACT_LAYER = 'HABITAT_PRESSION_LAYER'

    @property
    def project_type(self):
        return ProjectType.Pression

    def shortHelpString(self):
        help_string = super().shortHelpString()
        help_string += (
            '\n\n'
            'Le champ de pressions doit être correctement formaté : \n'
            '{values}\n'.format(values=', '.join([str(i) for i in self.expected_values]))
        )
        return help_string

    @property
    def expected_values(self) -> set:
        """ Expected values for the input layer. """
        return {1, 2, 3, 4, 5, 6, NULL}

    @property
    def destination_impact_field(self) -> str:
        """ Destination impact field. """
        return 'type_pression'


class ImportDataCompensation(BaseImportImpactData):

    IMPACT_FIELD = 'COMPENSATION_FIELD'
    APPLY_CALCUL_HABITAT_IMPACT_ETAT_ECOLOGIQUE = 'APPLY_CALCUL_HABITAT_COMPENSATION_ETAT_ECOLOGIQUE'
    HABITAT_IMPACT_LAYER = 'HABITAT_COMPENSATION_LAYER'

    @property
    def project_type(self):
        return ProjectType.Compensation

    @property
    def destination_impact_field(self) -> str:
        """ Destination impact field. """
        return 'nom'
