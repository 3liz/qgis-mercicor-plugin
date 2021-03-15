__copyright__ = "Copyright 2020, 3Liz"
__license__ = "GPL version 3"
__email__ = "info@3liz.org"

from PyQt5.QtCore import QVariant
from qgis.core import (
    QgsExpression,
    QgsField,
    QgsMapLayerType,
    QgsProcessing,
    QgsProcessingFeatureBasedAlgorithm,
)


class CalculNotes(QgsProcessingFeatureBasedAlgorithm):

    def __init__(self):
        super().__init__()
        self.exp_context = None
        self.fields = [
            "perc_bsd", "perc_bsm", "bsd_recouv_cor", "bsd_p_acrop", "bsd_vital_cor",
            "bsd_comp_struc", "bsd_taille_cor", "bsd_dens_juv", "bsd_f_sessile", "bsd_recouv_ma",
            "bsm_fragm_herb", "bsm_recouv_her", "bsm_haut_herb", "bsm_dens_herb", "bsm_div_herb",
            "bsm_epibiose", "man_fragm", "man_recouv", "man_diam_tronc", "man_dens", "man_diversit",
            "man_vital", "pmi_div_poi", "pmi_predat_poi", "pmi_scarib_poi", "pmi_macro_inv"
        ]
        self.notes = ["note_bsd", "note_bsm", "note_ben", "note_man", "note_pmi"]
        self.expressions = {
            "note_bsd": '(("bsd_recouv_cor" + "bsd_p_acrop" + "bsd_vital_cor" + "bsd_comp_struc" + '
            '"bsd_taille_cor" + "bsd_dens_juv" + "bsd_f_sessile" + "bsd_recouv_ma") / 8.0) * (10.0 / 3.0)',
            "note_bsm": '(("bsm_fragm_herb" + "bsm_recouv_her" + "bsm_haut_herb" + "bsm_dens_herb" + '
            '"bsm_div_herb" + "bsm_epibiose") / 6.0) * (10.0 / 3.0)',
            "note_ben": '"note_bsd" * "perc_bsd" + "note_bsm" * "perc_bsm"',
            "note_man": '(("man_fragm" + "man_recouv" + "man_diam_tronc" + "man_dens" + "man_diversit" + '
            '"man_vital") / 6.0) * (10.0 / 3.0)',
            "note_pmi": '(("pmi_div_poi" + "pmi_predat_poi" + "pmi_scarib_poi" + "pmi_macro_inv") / 4) * (10 '
            '/ 3)',
            "score_station": 'CASE WHEN "station_man" THEN ("note_man" + "note_pmi") / 2 ELSE ("note_ben" + '
            '"note_pmi") / 2 END'
        }

    def group(self):
        return 'Calcul'

    def groupId(self):
        return 'calcul'

    def name(self):
        return 'calcul_notes'

    def displayName(self):
        return 'Calcul des notes MERCI-Cor'

    def shortHelpString(self):
        return 'Calcul des notes MERCI-Cor à partir des indicateurs MERCI-Cor'

    # def inputParameterName(self):
    #    return super().inputParameterName()

    # def inputParameterDescription(self):
    #    return super().inputParameterDescription()

    def outputName(self):
        return 'calcul_done'

    def inputLayerTypes(self):
        """
        Fonction de définition des types de couches attendues
        """
        return [QgsProcessing.TypeVector]

    def createInstance(self):
        return type(self)()

    def outputType(self):
        return QgsProcessing.TypeVector

    def outputFields(self, inputFields):
        """
        Liste des attributs de la couche résultat
        à partir de la liste des attributs de la
        couche d'entrée
        """
        for field_name in self.notes:
            field_idx = inputFields.lookupField(field_name)
            if field_idx < 0:
                inputFields.append(QgsField(field_name, QVariant.Double, '', 24, 15))
        return inputFields

    def initAlgorithm(self, config):
        """
        Fonction d'initialisation de l'algorithme
        Ajout des paramètres autres que la couche à modifier
        """
        return super().initAlgorithm(config)

    def prepareAlgorithm(self, parameters, context, feedback):
        """
        Fonction de préparation de l'algorithm
        Il est possible de vérifier le paramètre INPUT
        """
        # get source
        source = self.parameterAsSource(parameters, 'INPUT', context)
        # check that field source has needed fields
        if not self.checkFields(source.fields()):
            return False
        # create expression context
        self.exp_context = self.createExpressionContext(parameters, context, source)
        return True

    def processFeature(self, feature, context, feedback):
        """
        Fonction de modification des objets géographiques
        Application des expressions pour les champs à mettre à jour
        """
        for note in self.notes:
            expression = QgsExpression(self.expressions[note])
            expression.prepare(self.exp_context)
            if expression.hasEvalError():
                feedback.reportError(
                    self.tr(u'Prepare error in expression "{}": {}')
                        .format(expression.expression(),
                                expression.evalErrorString()))
                continue
            self.exp_context.setFeature(feature)
            feature[note] = expression.evaluate(self.exp_context)
            if expression.hasEvalError():
                feedback.reportError(
                        self.tr(u'Eval error in expression "{}": {}')
                            .format(expression.expression(),
                                    expression.evalErrorString()))
                break
        return [feature]

    def supportInPlaceEdit(self, layer):
        """
        Fonction de vérification que la couche est compatible avec l'algorithme
        - Vérification que la couche est vectorielle
        - Vérification que la couche contient les champs nécessaires aux calculs des notes
        """
        if layer.type() != QgsMapLayerType.VectorLayer:
            return False
        return self.checkFields(layer.fields())

    def checkFields(self, layer_fields):
        for field_name in self.fields:
            field_idx = layer_fields.lookupField(field_name)
            if field_idx < 0:
                return False
        return True
