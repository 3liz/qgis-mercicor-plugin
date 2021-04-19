__copyright__ = "Copyright 2021, 3Liz"
__license__ = "GPL version 3"
__email__ = "info@3liz.org"

from collections import OrderedDict

from qgis.core import (
    QgsExpression,
    QgsProcessing,
    QgsProcessingParameterVectorLayer,
)

from mercicor.definitions.project_type import ProjectType
from mercicor.processing.calcul.base import CalculAlgorithm


class BaseCalculPertesGains(CalculAlgorithm):

    def __init__(self):
        super().__init__()
        self.fields = OrderedDict()
        self.fields['bsd'] = ['hab_note_bsd', 'note_bsd']
        self.fields['bsm'] = ['hab_note_bsm', 'note_bsm']
        self.fields['man'] = ['hab_note_man', 'note_man']
        self.fields['pmi'] = ['hab_note_pmi', 'note_pmi']
        self.fields['ben'] = ['hab_note_ben', 'note_ben']
        self.fields['mercicor'] = ['hab_score_mercicor', 'score_mercicor']

    @property
    def multiplier(self) -> int:
        raise NotImplementedError

    @property
    def project_type(self) -> ProjectType:
        # noinspection PyTypeChecker
        return NotImplementedError

    def group(self):
        return 'Calcul {}'.format(self.project_type.calcul_type)

    def groupId(self):
        return 'calcul_group_{}'.format(self.project_type.calcul_type)

    def name(self):
        return 'calcul_{}'.format(self.project_type.calcul_type)

    def displayName(self):
        return 'Calcul des notes de {} pour le scénario de pression'.format(self.project_type.calcul_type)

    def checkParameterValues(self, parameters, context):
        sources = [
            self.parameterAsVectorLayer(parameters, self.SCENARIO_IMPACT, context),
            self.parameterAsVectorLayer(parameters, self.HABITAT_IMPACT_ETAT_ECOLOGIQUE, context)
        ]
        for source in sources:
            flag, msg = self.check_layer_is_geopackage(source)
            if not flag:
                return False, msg

        return super().checkParameterValues(parameters, context)

    def shortHelpString(self):
        message = (
            'Calcul des notes de {} à partir des indicateurs MERCI-Cor\n\n'
            'Liste des notes :\n\n'.format(self.project_type.calcul_type)
        )
        for field, formula in self.fields.items():
            message += (
                '{type_calcul}_{output} = '
                'La somme de ("{field_1} {operator} {field_2} ") * surface, filtré par scénario\n\n'.format(
                    type_calcul=self.project_type.calcul_type,
                    output=field,
                    field_1=formula[0],
                    field_2=formula[1],
                    operator='-' if self.multiplier == -1 else '+',
                )
            )
        return message

    def initAlgorithm(self, config):

        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.HABITAT_IMPACT_ETAT_ECOLOGIQUE,
                self.project_type.label_habitat_impact_etat_ecologique,
                [QgsProcessing.TypeVectorPolygon],
                defaultValue=self.project_type.couche_habitat_impact_etat_ecologique,
            )
        )

        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.SCENARIO_IMPACT,
                self.project_type.label_scenario_impact,
                [QgsProcessing.TypeVectorAnyGeometry],
                defaultValue=self.project_type.couche_scenario_impact,
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        hab_etat_ecolo = self.parameterAsVectorLayer(
            parameters, self.HABITAT_IMPACT_ETAT_ECOLOGIQUE, context)
        scenario = self.parameterAsVectorLayer(parameters, self.SCENARIO_IMPACT, context)

        scenario.startEditing()

        for feat in scenario.getFeatures():
            scenario_id = feat['id']
            for note in self.fields.keys():
                feat[note] = 0

                filter_expression = QgsExpression.createFieldEqualityExpression('scenario_id', scenario_id)
                for feature in hab_etat_ecolo.getFeatures(filter_expression):
                    geom = feature.geometry()
                    sub_result = (
                            feature[self.fields[note][0]] +
                            (feature[self.fields[note][1]] * self.multiplier)
                    )
                    feat[note] += sub_result * geom.area()

            scenario.updateFeature(feat)
        scenario.commitChanges()

        return {}


class CalculPertes(BaseCalculPertesGains):

    HABITAT_IMPACT_ETAT_ECOLOGIQUE = 'HABITAT_PRESSION_ETAT_ECOLOGIQUE'
    SCENARIO_IMPACT = 'SCENARIO_PRESSION'

    @property
    def project_type(self):
        return ProjectType.Pression

    @property
    def multiplier(self):
        return -1


class CalculGains(BaseCalculPertesGains):

    HABITAT_IMPACT_ETAT_ECOLOGIQUE = 'HABITAT_COMPENSATION_ETAT_ECOLOGIQUE'
    SCENARIO_IMPACT = 'SCENARIO_COMPENSATION'

    @property
    def project_type(self):
        return ProjectType.Compensation

    @property
    def multiplier(self):
        return 1
