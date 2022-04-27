__copyright__ = "Copyright 2021, 3Liz"
__license__ = "GPL version 3"
__email__ = "info@3liz.org"

from collections import OrderedDict

from qgis.core import (
    QgsExpression,
    QgsProcessing,
    QgsProcessingParameterVectorLayer,
)
from qgis.PyQt.QtCore import NULL

from mercicor.definitions.project_type import ProjectType
from mercicor.processing.calcul.base import CalculAlgorithm


class BaseCalculPertesGains(CalculAlgorithm):

    def __init__(self):
        super().__init__()
        self.fields = OrderedDict()
        self.fields['bsd'] = ('hab_note_bsd', 'note_bsd', 'perc_bsd')
        self.fields['bsm'] = ('hab_note_bsm', 'note_bsm', 'perc_bsm')
        self.fields['man'] = ('hab_note_man', 'note_man')
        self.fields['pmi'] = ('hab_note_pmi', 'note_pmi')
        self.fields['ben'] = ('hab_note_ben', 'note_ben')
        self.fields['mercicor'] = ('hab_score_mercicor', 'score_mercicor')

    @property
    def project_type(self) -> ProjectType:
        # noinspection PyTypeChecker
        return NotImplementedError

    def group(self):
        return 'Calcul {}'.format(self.project_type.label)

    def groupId(self):
        return 'calcul_group_{}'.format(self.project_type.label)

    def name(self):
        return 'calcul_{}'.format(self.project_type.label)

    # noinspection PyPep8Naming
    def displayName(self):
        return (
            'Calcul des notes de {} pour le scénario de {}'.format(
                self.project_type.calcul_type, self.project_type.label))

    # noinspection PyPep8Naming
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
            divider = '' if self.project_type == ProjectType.Pression else ' / (coeff_risque * coeff_delais)'
            bsd_bsm = '' if len(formula) == 2 else '{} * '.format(formula[2])
            message += (
                '{type_calcul}_{output} = '
                'La somme de '
                '{bsd_bsm}("{field_1} - {field_2} ") * surface{divider}'
                ', filtré par scénario\n\n'.format(
                    type_calcul=self.project_type.calcul_type,
                    output=field,
                    field_1=formula[0] if self.project_type == ProjectType.Pression else formula[1],
                    field_2=formula[1] if self.project_type == ProjectType.Pression else formula[0],
                    bsd_bsm=bsd_bsm,
                    divider=divider
                )
            )
        return message

    # noinspection PyMethodOverriding
    def initAlgorithm(self, config):
        _ = config

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
        scenario_impact = self.parameterAsVectorLayer(parameters, self.SCENARIO_IMPACT, context)

        scenario_impact.startEditing()

        feedback.pushInfo("Lancement des calculs")
        for feat in scenario_impact.getFeatures():
            scenario_id = feat['id']
            feedback.pushDebugInfo("Lancement sur le scénario ID {}".format(scenario_id))
            for note, fields in self.fields.items():
                # from "bsd" to "perte_bsd" or "gain_bsd"
                field_name = '{calcul_type}_{note}'.format(
                    calcul_type=self.project_type.calcul_type, note=note)
                feat[field_name] = 0
                feedback.pushDebugInfo(
                    "Initialisation scénario {} champ {} = 0".format(scenario_id, field_name))

                filter_expression = QgsExpression.createFieldEqualityExpression('scenario_id', scenario_id)
                for feature in hab_etat_ecolo.getFeatures(filter_expression):

                    feedback.pushInfo(
                        "Lecture d'une nouvelle entité habitat état écologique ID {} dont le "
                        "scénario = {}".format(
                            hab_etat_ecolo.id(), scenario_id))

                    if feature[fields[1]] == NULL:
                        feedback.pushDebugInfo(
                            "Omission du calcul {} pour l'entité {} car le champ est NULL".format(
                                field_name, feature.id()))
                        continue

                    if self.project_type == ProjectType.Pression:
                        sub_result = feature[fields[0]] - feature[fields[1]]
                        feedback.pushDebugInfo("Sous résultat {} - {} = {}".format(
                            fields[0], fields[1], sub_result))
                        divide = 1
                    else:
                        # Compensation
                        # Tenir compte des délais et du risque
                        sub_result = feature[fields[1]] - feature[fields[0]]
                        feedback.pushDebugInfo(
                            "Sous résultat {} - {} = {}".format(fields[1], fields[0], sub_result))
                        divide = feature['compensation_coeff_risque'] * feature['compensation_coeff_delais']
                        feedback.pushDebugInfo(
                            "Division compensation_coeff_risque * compensation_coeff_delais = {}".format(
                                divide))

                    if len(fields) == 3:
                        # Pour le calcul de perte_bsd, perte_bsm, gain_bsd et gain_bsm,
                        # il faut tenir compte des valeurs des champs perc_bsd et perc_bsm.
                        multiply = feature[fields[2]]
                    else:
                        multiply = 1
                    feedback.pushDebugInfo("Coefficient multiplicateur : {}".format(multiply))

                    temporary_result = multiply * (sub_result * feature.geometry().area()) / divide
                    feat[field_name] += temporary_result

                    # Tentative explication de la formule
                    feedback.pushDebugInfo(
                        "Scénario {scenario_id} entité habitat état écologique {id} : "
                        "{field_name} += {multiply} * ( {sub_result} * surface {surface}) / {divide}".format(
                            scenario_id=scenario_id,
                            id=feature.id(),
                            field_name=field_name,
                            multiply=multiply,
                            sub_result=sub_result,
                            surface=feature.geometry().area(),
                            divide=divide,
                        )
                    )
                    feedback.pushDebugInfo(
                        "Incrémentation scénario ID {} champ {} de {}. Nouvelle valeur temporaire {}. "
                        "Passage à l'entité suivante…".format(
                            scenario_id, field_name, temporary_result, feat[field_name]))

                feedback.pushDebugInfo(
                    "Fin sur le scénario ID {} champ {} = {}, passage au champ suivant avec le même "
                    "scénario…".format(scenario_id, field_name, feat[field_name]))

            scenario_impact.updateFeature(feat)
            feedback.pushDebugInfo("Fin sur le scénario ID {}, passage au scénario suivant…".format(
                scenario_id))
        feedback.pushInfo("Fin des calculs, enregistrement de la couche…")
        scenario_impact.commitChanges()

        return {}


class CalculPertes(BaseCalculPertesGains):

    HABITAT_IMPACT_ETAT_ECOLOGIQUE = 'HABITAT_PRESSION_ETAT_ECOLOGIQUE'
    SCENARIO_IMPACT = 'SCENARIO_PRESSION'

    @property
    def project_type(self):
        return ProjectType.Pression


class CalculGains(BaseCalculPertesGains):

    HABITAT_IMPACT_ETAT_ECOLOGIQUE = 'HABITAT_COMPENSATION_ETAT_ECOLOGIQUE'
    SCENARIO_IMPACT = 'SCENARIO_COMPENSATION'

    @property
    def project_type(self):
        return ProjectType.Compensation
