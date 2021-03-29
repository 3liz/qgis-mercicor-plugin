__copyright__ = "Copyright 2021, 3Liz"
__license__ = "GPL version 3"
__email__ = "info@3liz.org"

import processing

from qgis.core import (
    QgsFeature,
    QgsProcessing,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterVectorLayer,
    QgsProcessingUtils,
    QgsVectorLayer,
)
from qgis.PyQt.QtCore import QVariant

from mercicor.processing.calcul.base import CalculAlgorithm


class CalculHabitatEtatEcologique(CalculAlgorithm):

    HABITAT = 'HABITAT'
    OBSERVATIONS = 'OBSERVATIONS'
    HABITAT_ETAT_ECOLOGIQUE = 'HABITAT_ETAT_ECOLOGIQUE'
    OUTPUT_LAYER = 'OUTPUT_LAYER'

    def __init__(self):
        super().__init__()

    def checkParameterValues(self, parameters, context):
        """
        Check if source layer is in the geopackage
        """
        sources = []
        sources.append(self.parameterAsVectorLayer(parameters, self.HABITAT, context))
        sources.append(self.parameterAsVectorLayer(parameters, self.OBSERVATIONS, context))
        sources.append(self.parameterAsVectorLayer(parameters, self.HABITAT_ETAT_ECOLOGIQUE, context))
        for source in sources:
            flag, msg = self.check_layer_is_geopackage(source)
            if not flag:
                return False, msg

        return super().checkParameterValues(parameters, context)

    def name(self):
        return 'calcul_habitat_etat_ecologique'

    def displayName(self):
        return 'Calcul de l\'état écologique des habitats'

    def shortHelpString(self):
        return (
            'Calcul de l\'état écologique des habitats '
            'à partir des données d\'observations :\n'
            '- Vérification de l\'unicité du facies\n'
            '- Jointure de données\n'
            '- Calcul des notes'

        )

    def initAlgorithm(self, config):

        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.HABITAT,
                "Couche habitat",
                [QgsProcessing.TypeVectorPolygon],
                defaultValue='habitat',
            )
        )

        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.OBSERVATIONS,
                "Couche observations",
                [QgsProcessing.TypeVectorPoint],
                defaultValue='observations',
            )
        )

        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.HABITAT_ETAT_ECOLOGIQUE,
                "Table habitat état écologique",
                [QgsProcessing.TypeVectorAnyGeometry],
                defaultValue='habitat_etat_ecologique',
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT_LAYER,
                'Table habitat état écologique en sortie'
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        hab_layer = self.parameterAsVectorLayer(parameters, self.HABITAT, context)
        observ_layer = self.parameterAsVectorLayer(parameters, self.OBSERVATIONS, context)
        hab_etat_ecolo = self.parameterAsVectorLayer(parameters, self.HABITAT_ETAT_ECOLOGIQUE, context)

        # Vérification de l'unicité de la couche habitat pour le couple nom/faciès
        params = {
            'INPUT': hab_layer,
            'OUTPUT': 'TEMPORARY_OUTPUT'
        }
        results = processing.run(
            "mercicor:calcul_unicity_habitat",
            params,
            context=context,
            feedback=feedback,
            is_child_algorithm=True)

        if results['NUMBER_OF_NON_UNIQUE']:
            feedback.pushDebugInfo(
                '{} couple(s) habitat/faciès non unique !'.format(
                    results['NUMBER_OF_NON_UNIQUE']
                )
            )
            feedback.reportError('Les couples habitat/faciès ne sont pas uniques !')
            msg = 'Utiliser l\'algorithme Mercicor : '
            msg += 'Calcul unicité habitat/faciès ; '
            msg += 'pour corriger le problème.'
            feedback.pushInfo(msg)
            return {}

        # Calcul de la moyenne des indicateurs mercicor par habitat/faciès
        params = {
            'DISCARD_NONMATCHING': True,
            'INPUT': hab_layer,
            'JOIN': observ_layer,
            'JOIN_FIELDS': [
                'perc_bsd', 'perc_bsm', 'bsd_recouv_cor', 'bsd_p_acrop', 'bsd_vital_cor',
                'bsd_comp_struc', 'bsd_taille_cor', 'bsd_dens_juv', 'bsd_f_sessile',
                'bsd_recouv_ma', 'bsm_fragm_herb', 'bsm_recouv_her', 'bsm_haut_herb',
                'bsm_dens_herb', 'bsm_div_herb', 'bsm_epibiose', 'man_fragm',
                'man_recouv', 'man_diam_tronc', 'man_dens', 'man_diversit',
                'man_vital', 'pmi_div_poi', 'pmi_predat_poi', 'pmi_scarib_poi', 'pmi_macro_inv'
            ],
            'OUTPUT': 'TEMPORARY_OUTPUT',
            'PREDICATE': [0],  # Intersects
            'SUMMARIES': [6]  # Mean
        }

        results = processing.run(
            "qgis:joinbylocationsummary",
            params,
            context=context,
            feedback=feedback,
            is_child_algorithm=True,
        )

        # Mise en forme du résultat pour enregistrement dans la table habitat_etat_ecologique
        hee_fields = hab_etat_ecolo.fields()
        hee_features = {}
        layer = QgsProcessingUtils.mapLayerFromString(results['OUTPUT'], context, True)
        for feat in layer.getFeatures():
            hee_feature = QgsFeature(hee_fields)
            hee_feature.setAttribute('id', feat['id'])
            hee_feature.setAttribute('nom', feat['nom'])
            hee_feature.setAttribute('facies', feat['facies'])
            for field in params['JOIN_FIELDS']:
                hee_feature.setAttribute(field, feat[field+'_mean'])
            hee_features[feat['id']] = hee_feature

        # Récupération de l'information de station en Mangrove
        params = {
            'DISCARD_NONMATCHING': True,
            'INPUT': hab_layer,
            'JOIN': observ_layer,
            'JOIN_FIELDS': ['station_man'],
            'OUTPUT': 'TEMPORARY_OUTPUT',
            'PREDICATE': [0],  # Intersects
            'SUMMARIES': [3]  # Max
        }

        results = processing.run(
            "qgis:joinbylocationsummary",
            params,
            context=context,
            feedback=feedback,
            is_child_algorithm=True,
        )

        # Ajout de l'information de station en Mangrove aux objets qui
        # seront enregistrés dans la table habitat_etat_ecologique
        layer = QgsProcessingUtils.mapLayerFromString(results['OUTPUT'], context, True)
        for feat in layer.getFeatures():
            hee_feature = hee_features[feat['id']]
            for field in params['JOIN_FIELDS']:
                hee_feature.setAttribute(field, feat[field+'_max'])
            hee_features[feat['id']] = hee_feature

        # Création d'une couche temporaire pour calcul des notes mercicor
        layer = QgsVectorLayer("None", "temporary_hee", "memory")
        pr = layer.dataProvider()
        pr.addAttributes(hee_fields)
        layer.updateFields()
        pr.addFeatures(list(hee_features.values()))

        # Calcul des notes mercicor
        params = {
            'INPUT': layer,
            'OUTPUT': parameters[self.OUTPUT_LAYER]
        }
        results = processing.run(
            "mercicor:calcul_notes",
            params,
            context=context,
            feedback=feedback,
            is_child_algorithm=True,
        )

        # Ajout des notes mercicor aux objets qui seront enregistrés
        # dans la table habitat_etat_ecologique
        layer = QgsProcessingUtils.mapLayerFromString(results['OUTPUT'], context, True)
        layer_fields = layer.fields()
        for feat in layer.getFeatures():
            hee_feature = hee_features[feat['id']]
            for field in layer_fields:
                field_name = field.name()
                if hee_fields.indexOf(field_name) < 0:
                    continue
                field_val = feat[field_name]
                # forcer les valeurs booléenne
                if field.type() == QVariant.Bool:
                    if field_val and str(field_val).lower() == 'true':
                        field_val = 1
                    else:
                        field_val = 0
                #  set attribute
                hee_feature.setAttribute(field_name, field_val)
            hee_features[feat['id']] = hee_feature

        # Début de la modification de la table habitat_etat_ecologique
        hab_etat_ecolo.startEditing()

        # Mise à jour des objets de la table habitat_etat_ecologique
        for existing in hab_etat_ecolo.getFeatures():
            if existing['id'] in hee_features:
                feat = hee_features[existing['id']]
                attributes = dict()
                for field in hee_fields:
                    field_name = field.name()
                    attributes[hee_fields.indexOf(field_name)] = feat[field_name]
                hab_etat_ecolo.changeAttributeValues(existing.id(), attributes)
                del hee_features[existing['id']]

        # Ajout des objets restant de la table habitat_etat_ecologique
        for feat in hee_features.values():
            hab_etat_ecolo.addFeature(feat)

        # Fin et enregistrement de la modification de la table habitat_etat_ecologique
        hab_etat_ecolo.commitChanges()

        return {self.OUTPUT_LAYER: results['OUTPUT']}
