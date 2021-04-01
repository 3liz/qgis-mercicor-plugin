__copyright__ = "Copyright 2021, 3Liz"
__license__ = "GPL version 3"
__email__ = "info@3liz.org"

from collections import OrderedDict

from qgis.core import (
    QgsExpression,
    QgsProcessing,
    QgsProcessingParameterVectorLayer,
)

from mercicor.processing.calcul.base import CalculAlgorithm


class CalculPertes(CalculAlgorithm):

    HABITAT_PRESSION_ETAT_ECOLOGIQUE = 'HABITAT_PRESSION_ETAT_ECOLOGIQUE'
    SCENARIO_PRESSION = 'SCENARIO_PRESSION'

    def __init__(self):
        super().__init__()
        self.exp_context = None
        self.expressions = OrderedDict()
        self.expressions['perte_bsd'] = (
            'sum( ("hab_note_bsd" - "note_bsd") * $area, group_by: "scenario_id")'
        )

        self.expressions['perte_bsm'] = (
            'sum( ("hab_note_bsm" - "note_bsm") * $area, group_by: "scenario_id")'
        )

        self.expressions['perte_man'] = (
            'sum( ("hab_note_man" - "note_man") * $area, group_by: "scenario_id")'
        )

        self.expressions['perte_pmi'] = (
            'sum( ("hab_note_pmi" - "note_pmi") * $area, group_by: "scenario_id")'
        )

        self.expressions['perte_mercicor'] = (
            'sum( ("hab_score_mercicor" - "note_score_mercicor") * $area, group_by: "scenario_id")'
        )

    def checkParameterValues(self, parameters, context):
        """
        Check if source layer is in the geopackage
        """
        sources = [
            self.parameterAsVectorLayer(parameters, self.SCENARIO_PRESSION, context),
            self.parameterAsVectorLayer(parameters, self.HABITAT_PRESSION_ETAT_ECOLOGIQUE, context)
        ]
        for source in sources:
            flag, msg = self.check_layer_is_geopackage(source)
            if not flag:
                return False, msg

        return super().checkParameterValues(parameters, context)

    def name(self):
        return 'calcul_pertes'

    def displayName(self):
        return 'Calcul des notes de perte pour le scénario de pression'

    def shortHelpString(self):
        message = 'Calcul des notes de pertes à partir des indicateurs MERCI-Cor\n\n'
        message += 'Liste des notes :\n'
        for field, formula in self.expressions.items():
            message += '{} = {}\n'.format(field, formula)
        return message

    def initAlgorithm(self, config):

        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.HABITAT_PRESSION_ETAT_ECOLOGIQUE,
                "Table habitat pression état écologique",
                [QgsProcessing.TypeVectorPolygon],
                defaultValue='habitat_pression_etat_ecologique',
            )
        )

        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.SCENARIO_PRESSION,
                "Table scénario pression",
                [QgsProcessing.TypeVectorAnyGeometry],
                defaultValue='scenario_pression',
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        hab_etat_ecolo = self.parameterAsVectorLayer(
            parameters, self.HABITAT_PRESSION_ETAT_ECOLOGIQUE, context)
        source = self.parameterAsSource(parameters, self.HABITAT_PRESSION_ETAT_ECOLOGIQUE, context)
        scenario_pression = self.parameterAsVectorLayer(parameters, self.SCENARIO_PRESSION, context)

        self.exp_context = self.createExpressionContext(parameters, context, source)

        scenario_pression.startEditing()
        for feature in hab_etat_ecolo.getFeatures():
            scenario_id = feature['scenario_id']

            feat_scenario = scenario_pression.selectByExpression('"id"='+scenario_id)[0]

            # boucle sur les champs des notes merci-cor
            for note in self.expressions.keys():
                # création de l'expression
                expression = QgsExpression(self.expressions[note])
                # préparation de l'expression
                expression.prepare(self.exp_context)
                if expression.hasEvalError():
                    feedback.reportError(
                        'Erreur lors de la préparation de l\'expression "{}": {}'.format(
                            expression.expression(),
                            expression.evalErrorString()))
                    continue

                # Ajout de l'objet géographique au context de l'expression
                self.exp_context.setFeature(feature)
                # Evaluation de l'expression
                feat_scenario[note] = expression.evaluate(self.exp_context)
                if expression.hasEvalError():
                    feedback.reportError(
                        'Erreur d\'évaluation de l\'expression "{}": {}'.format(
                            expression.expression(),
                            expression.evalErrorString()))
                    break
        scenario_pression.commitChanges()

        return {}
