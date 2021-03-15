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
    QgsRelation,
    QgsVectorLayerJoinInfo,
)

from mercicor.processing.project.base import BaseProjectAlgorithm
from mercicor.qgis_plugin_tools import load_csv, resources_path


class LoadStylesAndRelations(BaseProjectAlgorithm):

    PRESSURE_LAYER = 'PRESSURE_LAYER'
    HABITAT_LAYER = 'HABITAT_LAYER'
    PRESSURE_LIST_LAYER = 'PRESSURE_LIST_LAYER'
    HABITAT_ETAT_ECOLOGIQUE_LAYER = 'HABITAT_ETAT_ECOLOGIQUE_LAYER'
    OBSERVATIONS_LAYER = 'OBSERVATIONS_LAYER'
    SCENARIO_PRESSION = 'SCENARIO_PRESSION'
    HABITAT_PRESSION_ETAT_ECOLOGIQUE = 'HABITAT_PRESSION_ETAT_ECOLOGIQUE'

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
                self.OBSERVATIONS_LAYER,
                "Couches des observations",
                [QgsProcessing.TypeVectorPoint],
                defaultValue='observations',
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

        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.SCENARIO_PRESSION,
                "Couche des scénario de pression",
                [QgsProcessing.TypeVectorPolygon],
                defaultValue='scenario_pression',
            )
        )

        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.HABITAT_PRESSION_ETAT_ECOLOGIQUE,
                "Couche du résultat de l'intersection entre les pressions et les habitats.",
                [QgsProcessing.TypeVectorPolygon],
                defaultValue='habitat_pression_etat_ecologique',
            )
        )

        self.addOutput(QgsProcessingOutputNumber(self.RELATIONS_ADDED, 'Nombre de relations chargés'))
        self.addOutput(QgsProcessingOutputNumber(self.QML_LOADED, 'Nombre de QML chargés'))

    def prepareAlgorithm(self, parameters, context, feedback):
        self.fetch_layers(parameters, context)
        self.add_styles(feedback, self.input_layers)
        return True

    def processAlgorithm(self, parameters, context, feedback):
        return {
            self.QML_LOADED: self.success_qml,
            self.RELATIONS_ADDED: self.success_relation,
        }

    def postProcessAlgorithm(self, context, feedback):
        self.add_relations(context, feedback)
        self.add_joins()

        for layer in self.input_layers.values():
            if layer.isSpatial():
                layer.triggerRepaint()

        self.add_alias_from_csv(feedback, self.input_layers)

        return {
            self.QML_LOADED: self.success_qml,
            self.RELATIONS_ADDED: self.success_relation,
        }

    def add_joins(self):
        """ Add all joins between tables. """
        joins_array = [
            {
                'join_field_name': 'id',
                'target_field_name': 'id',
                'join_layer_id': self.input_layers['habitat_etat_ecologique'].id(),
                'join_layer': self.input_layers['habitat_etat_ecologique'],
                'layer_add_join': self.input_layers['habitat'],
                'prefix': '',
            },
            {
                'join_field_name': 'id',
                'target_field_name': 'habitat_id',
                'join_layer_id': self.input_layers['habitat'].id(),
                'join_layer': self.input_layers['habitat'],
                'layer_add_join': self.input_layers['habitat_pression_etat_ecologique'],
                'prefix': 'hab_'
            },
            {
                'join_field_name': 'id',
                'target_field_name': 'pression_id',
                'join_layer_id': self.input_layers['pression'].id(),
                'join_layer': self.input_layers['pression'],
                'layer_add_join': self.input_layers['habitat_pression_etat_ecologique'],
                'prefix': 'pression_',
            },
            {
                'join_field_name': 'id',
                'target_field_name': 'scenario_id',
                'join_layer_id': self.input_layers['scenario_pression'].id(),
                'join_layer': self.input_layers['scenario_pression'],
                'layer_add_join': self.input_layers['habitat_pression_etat_ecologique'],
                'prefix': 'scenario_',
            },
        ]

        for definition in joins_array:
            join_habitat = QgsVectorLayerJoinInfo()
            join_habitat.setJoinFieldName(definition['join_field_name'])
            join_habitat.setTargetFieldName(definition['target_field_name'])
            join_habitat.setJoinLayerId(definition['join_layer_id'])
            join_habitat.setPrefix(definition['prefix'])
            join_habitat.setJoinLayer(definition['join_layer'])
            if not definition['layer_add_join'].addJoin(join_habitat):
                raise Exception('Join not added {}'.format(definition['join_field_name']))

    def add_relations(self, context, feedback):
        """ Add all relations to the QGIS project. """
        relations = [
            {
                'id': 'fk_pression_type',
                'name': 'Lien Pression - Type Pression',
                'referencingLayer': self.input_layers['pression'].id(),
                'referencingField': 'type_pression',
                'referencedLayer': self.input_layers['liste_type_pression'].id(),
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
            {
                'id': 'rel_pression_scenario',
                'name': 'Lien pression - scenario Pression',
                'referencingLayer': self.input_layers['pression'].id(),
                'referencingField': 'scenario_id',
                'referencedLayer': self.input_layers['scenario_pression'].id(),
                'referencedField': 'id',
            },
            {
                'id': 'rel_hab_press_etat_ecolo',
                'name': 'Lien Habitat - Hab_press_etat_ecolo',
                'referencingLayer': self.input_layers['habitat'].id(),
                'referencingField': 'id',
                'referencedLayer': self.input_layers['habitat_pression_etat_ecologique'].id(),
                'referencedField': 'habitat_id',
            },
            {
                'id': 'rel_pression_hab_press_etat_ecolo',
                'name': 'Lien Pression - Hab_press_etat_ecolo',
                'referencingLayer': self.input_layers['pression'].id(),
                'referencingField': 'id',
                'referencedLayer': self.input_layers['habitat_pression_etat_ecologique'].id(),
                'referencedField': 'pression_id',
            },
            {
                'id': 'rel_scenario_hab_press_etat_ecolo',
                'name': 'Lien Scenario pression - Hab_press_etat_ecolo',
                'referencingLayer': self.input_layers['scenario_pression'].id(),
                'referencingField': 'id',
                'referencedLayer': self.input_layers['habitat_pression_etat_ecologique'].id(),
                'referencedField': 'scenario_id',
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

    @staticmethod
    def add_alias_from_csv(feedback, input_layers):
        """ The geopackage has been created from CSV files, but we need to set alias. """
        for name, layer in input_layers.items():
            feedback.pushInfo("Relecture du CSV {} pour réappliquer les alias sur les champs".format(name))
            path = resources_path('data_models', '{}.csv'.format(name))
            csv = load_csv(name, path)

            for csv_feature in csv.getFeatures():
                index = layer.fields().indexOf(csv_feature['name'])
                if not index:
                    continue

                field = layer.fields().field(index)
                field.setAlias(csv_feature['alias'])

    def add_styles(self, feedback, input_layers):
        """ Add all QML style in the resource folder to given layers. """
        feedback.pushInfo("Ajout des styles")
        qml_component = {
            'fields': QgsMapLayer.Fields,
            'form': QgsMapLayer.Forms,
            'style': QgsMapLayer.Symbology,
            'layer_configuration': QgsMapLayer.LayerConfiguration,
        }
        for name, component in qml_component.items():
            for layer_name, vector_layer in input_layers.items():
                qml_file = resources_path('qml', name, '{}.qml'.format(layer_name))
                if not os.path.exists(qml_file):
                    continue
                vector_layer.loadNamedStyle(qml_file, component)
                feedback.pushInfo(vector_layer.name() + " {} for {} successfully loaded".format(
                    name.capitalize(), layer_name))
                self.success_qml += 1

    def fetch_layers(self, parameters, context):
        """ Fetch layers from the form and set them in a dictionary. """
        pressure_layer = self.parameterAsVectorLayer(parameters, self.PRESSURE_LAYER, context)
        habitat_layer = self.parameterAsVectorLayer(parameters, self.HABITAT_LAYER, context)
        list_pressure_layer = self.parameterAsVectorLayer(parameters, self.PRESSURE_LIST_LAYER, context)
        habitat_etat_ecologique = self.parameterAsVectorLayer(
            parameters, self.HABITAT_ETAT_ECOLOGIQUE_LAYER, context)
        observations_layer = self.parameterAsVectorLayer(parameters, self.OBSERVATIONS_LAYER, context)
        scenario_pression = self.parameterAsVectorLayer(parameters, self.SCENARIO_PRESSION, context)
        habitat_pression_etat_ecologique = self.parameterAsVectorLayer(
            parameters, self.HABITAT_PRESSION_ETAT_ECOLOGIQUE, context)

        self.input_layers = {
            "habitat": habitat_layer,
            "pression": pressure_layer,
            "liste_type_pression": list_pressure_layer,
            "observations": observations_layer,
            "habitat_etat_ecologique": habitat_etat_ecologique,
            "scenario_pression": scenario_pression,
            "habitat_pression_etat_ecologique": habitat_pression_etat_ecologique,
        }
