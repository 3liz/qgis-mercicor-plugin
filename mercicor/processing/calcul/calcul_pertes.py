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
        self.fields = OrderedDict()
        self.aide = OrderedDict()

        self.fields['perte_bsd'] = ['hab_note_bsd', 'note_bsd']
        self.fields['perte_bsm'] = ['hab_note_bsm', 'note_bsm']
        self.fields['perte_man'] = ['hab_note_man', 'note_man']
        self.fields['perte_pmi'] = ['hab_note_pmi', 'note_pmi']
        self.fields['perte_ben'] = ['hab_note_ben', 'note_ben']
        self.fields['perte_mercicor'] = ['hab_score_mercicor', 'score_mercicor']

        for note in self.fields.keys():
            self.aide[note] = (
                'La somme de \'("' + self.fields[note][0] + '" - "' + self.fields[note][1] + '") *'
                ' surface\', filtré par scénario'
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
        for field, formula in self.aide.items():
            message += '{} = {}\n'.format(field, formula)
        return message

    def initAlgorithm(self, config):

        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.HABITAT_PRESSION_ETAT_ECOLOGIQUE,
                "Couche habitat pression état écologique",
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
        scenario_pression = self.parameterAsVectorLayer(parameters, self.SCENARIO_PRESSION, context)

        scenario_pression.startEditing()

        for feat in scenario_pression.getFeatures():
            scenario_id = feat['id']
            for note in self.fields.keys():
                feat[note] = 0

                filter_expression = QgsExpression.createFieldEqualityExpression('scenario_id', scenario_id)
                for feature in hab_etat_ecolo.getFeatures(filter_expression):
                    geom = feature.geometry()
                    substract = (feature[self.fields[note][0]] - feature[self.fields[note][1]])
                    feat[note] += substract * geom.area()

            scenario_pression.updateFeature(feat)
        scenario_pression.commitChanges()

        return {}
