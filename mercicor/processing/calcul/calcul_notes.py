__copyright__ = "Copyright 2020, 3Liz"
__license__ = "GPL version 3"
__email__ = "info@3liz.org"

from qgis.core import (
    QgsExpression,
    QgsField,
    QgsMapLayerType,
    QgsProcessing,
    QgsProcessingFeatureBasedAlgorithm,
)
from qgis.PyQt.QtCore import QVariant


class CalculNotes(QgsProcessingFeatureBasedAlgorithm):

    def __init__(self):
        """
        Fonction d'initialisation
        """
        super().__init__()
        # expression context will be created in prepareAlgorithm
        self.exp_context = None
        # needed fields to calculate notes
        self.fields = [
            "perc_bsd", "perc_bsm", "bsd_recouv_cor", "bsd_p_acrop", "bsd_vital_cor",
            "bsd_comp_struc", "bsd_taille_cor", "bsd_dens_juv", "bsd_f_sessile", "bsd_recouv_ma",
            "bsm_fragm_herb", "bsm_recouv_her", "bsm_haut_herb", "bsm_dens_herb", "bsm_div_herb",
            "bsm_epibiose", "man_fragm", "man_recouv", "man_diam_tronc", "man_dens", "man_diversit",
            "man_vital", "pmi_div_poi", "pmi_predat_poi", "pmi_scarib_poi", "pmi_macro_inv"
        ]

        # note expressions
        self.expressions = {
            "note_bsd": (
                '(("bsd_recouv_cor" + "bsd_p_acrop" + "bsd_vital_cor" + "bsd_comp_struc" + '
                '"bsd_taille_cor" + "bsd_dens_juv" + "bsd_f_sessile" + "bsd_recouv_ma") / 8.0) * (10.0 / 3.0)'
            ),
            "note_bsm": (
                '(("bsm_fragm_herb" + "bsm_recouv_her" + "bsm_haut_herb" + "bsm_dens_herb" + '
                '"bsm_div_herb" + "bsm_epibiose") / 6.0) * (10.0 / 3.0)'
            ),
            "note_ben": (
                '"note_bsd" * "perc_bsd" + "note_bsm" * "perc_bsm"'
            ),
            "note_man": (
                '(("man_fragm" + "man_recouv" + "man_diam_tronc" + "man_dens" + "man_diversit" + '
                '"man_vital") / 6.0) * (10.0 / 3.0)'
            ),
            "note_pmi": (
                '(("pmi_div_poi" + "pmi_predat_poi" + "pmi_scarib_poi" + "pmi_macro_inv") / 4) * (10 / 3)'
            ),
            "score_mercicor": (
                'CASE '
                'WHEN "station_man" THEN ("note_man" + "note_pmi") / 2 '
                'ELSE ("note_ben" + "note_pmi") / 2 '
                'END'
            ),
        }

    def group(self):
        """
        Libellé du groupe de l'algorithme
        """
        return 'Calcul'

    def groupId(self):
        """
        Identifiant du groupe de l'algorithme
        """
        return 'calcul'

    def name(self):
        """
        Identifiant de l'algorithme
        """
        return 'calcul_notes'

    def displayName(self):
        """
        Libellé de l'algorithme
        """
        return 'Calcul des notes MERCI-Cor'

    def shortHelpString(self):
        """
        Description de l'algorithme
        """
        return 'Calcul des notes MERCI-Cor à partir des indicateurs MERCI-Cor'

    def inputParameterName(self):
        """
        Nom du paramètre pour la couche d'entrée
        """
        return super().inputParameterName()

    def inputParameterDescription(self):
        """
        Description du paramètre pour la couche d'entrée
        """
        return super().inputParameterDescription()

    def outputName(self):
        """
        Nom de la couche résultat
        """
        return 'output'

    def inputLayerTypes(self):
        """
        Fonction de définition des types de couches attendues
        """
        return [QgsProcessing.TypeVector]

    def outputLayerType(self):
        """
        Type de la couche de sortie
        """
        return QgsProcessing.TypeVector

    def outputFields(self, input_fields):
        """
        Liste des attributs de la couche résultat à partir de la liste des attributs de la couche d'entrée
        """
        # Ajout des champs correspondant aux notes si il ne sont pas présents
        for field_name in self.expressions.keys():
            field_idx = input_fields.lookupField(field_name)
            if field_idx < 0:
                input_fields.append(QgsField(field_name, QVariant.Double, '', 24, 15))
        return input_fields

    def initAlgorithm(self, config):
        """
        Fonction d'initialisation de l'algorithme
        """
        return super().initAlgorithm(config)

    def initParameters(self, config=None):
        """
        Fonction d'ajout des paramètres autres que la couche à modifier
        """
        pass

    def prepareAlgorithm(self, parameters, context, feedback):
        """
        Fonction de préparation de l'algorithme
        Il est possible de vérifier le paramètre INPUT
        """
        # get source
        source = self.parameterAsSource(parameters, 'INPUT', context)

        # check that field source has needed fields
        if not self.check_fields(source.fields()):
            return False

        # create expression context
        self.exp_context = self.createExpressionContext(parameters, context, source)
        return True

    def processFeature(self, feature, context, feedback):
        """
        Fonction de modification des objets géographiques.

        Application des expressions pour les champs à mettre à jour
        """
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
            feature[note] = expression.evaluate(self.exp_context)
            if expression.hasEvalError():
                feedback.reportError(
                    'Erreur d\'évaluation de l\'expression "{}": {}'.format(
                        expression.expression(),
                        expression.evalErrorString()))
                break

        return [feature]

    def supportInPlaceEdit(self, layer):
        """
        Fonction de vérification que la couche est compatible avec l'algorithme
        """
        # Vérification du type de la couche
        if layer.type() != QgsMapLayerType.VectorLayer:
            return False
        # Vérification que la couche contient les champs nécessaires aux calculs des notes
        return self.checkFields(layer.fields())

    def check_fields(self, layer_fields):
        """
        Fonction de vérification que la couche contient les champs nécessaires
        aux calculs des notes
        """
        for field_name in self.fields:
            field_idx = layer_fields.lookupField(field_name)
            if field_idx < 0:
                return False
        return True

    def createInstance(self):
        return type(self)()
