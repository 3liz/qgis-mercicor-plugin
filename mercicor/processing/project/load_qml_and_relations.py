__copyright__ = "Copyright 2020, 3Liz"
__license__ = "GPL version 3"
__email__ = "info@3liz.org"

import os

from qgis.core import (
    QgsMapLayer,
    QgsProcessing,
    QgsProcessingException,
    QgsProcessingOutputNumber,
    QgsProcessingParameterVectorLayer,
    QgsProviderRegistry,
    QgsRelation,
)

from mercicor.processing.project.base import BaseProjectAlgorithm
from mercicor.qgis_plugin_tools import resources_path


class LoadStylesAndRelations(BaseProjectAlgorithm):

    PRESSURE_LAYER = 'PRESSURE_LAYER'
    HABITAT_LAYER = 'HABITAT_LAYER'
    PRESSURE_LIST_LAYER = 'PRESSURE_LIST_LAYER'
    HABITAT_ETAT_ECOLOGIQUE_LAYER = 'HABITAT_ETAT_ECOLOGIQUE_LAYER'

    RELATIONS_ADDED = 'RELATIONS_ADDED'
    QML_LOADED = 'QML_LOADED'

    def __init__(self):
        super().__init__()
        self.success_qml = 0
        self.success_relation = 0
        self.input_layers = None

    def name(self):
        return "load_qml_and_relations"

    def displayName(self):
        return "Charger les styles"

    def shortHelpString(self):
        return (
            "Charger les styles pour les différentes couches.\n\n"
            "Les relations vont aussi être chargés dans le projet."
        )

    def fetch_layers(self, parameters, context):
        """ Fetch layers from the form and set them in a dictionary. """
        pressure_layer = self.parameterAsVectorLayer(parameters, self.PRESSURE_LAYER, context)
        habitat_layer = self.parameterAsVectorLayer(parameters, self.HABITAT_LAYER, context)
        list_pressure_layer = self.parameterAsVectorLayer(parameters, self.PRESSURE_LIST_LAYER, context)
        habitat_etat_ecologique = self.parameterAsVectorLayer(
            parameters, self.HABITAT_ETAT_ECOLOGIQUE_LAYER, context)

        self.input_layers = {
            "habitat": habitat_layer,
            "pression": pressure_layer,
            "list_pressure": list_pressure_layer,
            "habitat_etat_ecologique": habitat_etat_ecologique,
        }

    def checkParameterValues(self, parameters, context):
        """ Check if all given output layers are in the geopackage. """
        self.fetch_layers(parameters, context)

        for layer in self.input_layers.values():
            flag, msg = self.check_layer_is_geopackage(layer)
            if not flag:
                return False, msg

        return super().checkParameterValues(parameters, context)

    def initAlgorithm(self, config):
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.PRESSURE_LAYER,
                "Couche des pressions",
                [QgsProcessing.TypeVectorPolygon],
                defaultValue='pression',
            )
        )
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.HABITAT_LAYER,
                "Couche des habitats",
                [QgsProcessing.TypeVectorPolygon],
                defaultValue='habitat',
            )
        )
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.PRESSURE_LIST_LAYER,
                "Liste des types de pression",
                [QgsProcessing.TypeVectorPolygon],
                defaultValue='liste_type_pression',
            )
        )

        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.HABITAT_ETAT_ECOLOGIQUE_LAYER,
                "Table des observations ramenées à l'habitat",
                [QgsProcessing.TypeVectorPolygon],
                defaultValue='habitat_etat_ecologique',
            )
        )

        self.addOutput(QgsProcessingOutputNumber(self.RELATIONS_ADDED, 'Nombre de relations chargés'))
        self.addOutput(QgsProcessingOutputNumber(self.QML_LOADED, 'Nombre de QML chargés'))

    def prepareAlgorithm(self, parameters, context, feedback):
        self.fetch_layers(parameters, context)

        qml_component = {
            'fields': QgsMapLayer.Fields,
            'form': QgsMapLayer.Forms,
            'style': QgsMapLayer.Symbology,
            'layer_configuration': QgsMapLayer.LayerConfiguration,
        }

        self.add_styles(feedback, self.input_layers, qml_component)
        return True

    def add_styles(self, feedback, input_layers, qml_component):
        """ Add all QML style in the resource folder to given layers. """
        feedback.pushInfo("Ajout des styles")
        for name, component in qml_component.items():
            for layer_name, vector_layer in input_layers.items():
                qml_file = resources_path('qml', name, '{}.qml'.format(layer_name))
                if not os.path.exists(qml_file):
                    continue
                vector_layer.loadNamedStyle(qml_file, component)
                feedback.pushInfo(vector_layer.name() + " {} for {} successfully loaded".format(
                    name.capitalize(), layer_name))
                self.success_qml += 1

    def processAlgorithm(self, parameters, context, feedback):
        return {
            self.QML_LOADED: self.success_qml,
            self.RELATIONS_ADDED: self.success_relation,
        }

    def postProcessAlgorithm(self, context, feedback):

        relations = [
            {
                'id': 'fk_pression_type',
                'name': 'Lien Pression - Type Pression',
                'referencingLayer': self.input_layers['pression'].id(),
                'referencingField': 'type_pression',
                'referencedLayer': self.input_layers['list_pressure'].id(),
                'referencedField': 'key',
            },
            {
                'id': 'fk_habitat',
                'name': 'Lien habitat - Type Pression',
                'referencingLayer': self.input_layers['habitat'].id(),
                'referencingField': 'id',
                'referencedLayer': self.input_layers['habitat_etat_ecologique'].id(),
                'referencedField': 'id',
            },
        ]
        relation_manager = context.project().relationManager()
        for definition in relations:

            if relation_manager.relation(definition['id']):
                relation_manager.removeRelation(definition['id'])
                feedback.pushDebugInfo('Removing pre-existing relation {}'.format(definition['id']))

            feedback.pushInfo(definition['name'])
            relation = QgsRelation()
            relation.setId(definition['id'])
            relation.setName(definition['name'])
            relation.setReferencingLayer(definition['referencingLayer'])
            relation.setReferencedLayer(definition['referencedLayer'])
            relation.addFieldPair(definition['referencingField'], definition['referencedField'])
            relation.setStrength(QgsRelation.Association)
            if not relation.isValid():
                raise QgsProcessingException('{} is not valid'.format(definition['name']))

            relation_manager.addRelation(relation)
            self.success_relation += 1

        for layer in self.input_layers.values():
            if layer.isSpatial():
                layer.triggerRepaint()

        return {
            self.QML_LOADED: self.success_qml,
            self.RELATIONS_ADDED: self.success_relation,
        }
