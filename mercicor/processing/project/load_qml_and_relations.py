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

from mercicor.actions import actions_list
from mercicor.definitions.joins import attribute_joins
from mercicor.definitions.relations import relations
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
            "Les relations et les jointures vont également être chargés dans le projet."
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

        feedback.pushInfo('\n')
        self.add_alias_from_csv(feedback, self.input_layers)

        return {
            self.QML_LOADED: self.success_qml,
            self.RELATIONS_ADDED: self.success_relation,
        }

    def postProcessAlgorithm(self, context, feedback):
        feedback.pushInfo('\n')
        self.add_relations(context, feedback)

        feedback.pushInfo('\n')
        self.add_joins(feedback)

        feedback.pushInfo('\n')
        self.add_actions(feedback)

        for layer in self.input_layers.values():
            if layer.isSpatial():
                layer.triggerRepaint()

        return {
            self.QML_LOADED: self.success_qml,
            self.RELATIONS_ADDED: self.success_relation,
        }

    def add_actions(self, feedback):
        """ Add actions for layers. """
        for action in actions_list.values():
            # We remove multiple times actions on a layer :(
            self.input_layers[action.layer].actions().clearActions()

        for action in actions_list.values():
            feedback.pushInfo('Ajout de l\'action sur {}'.format(action.layer))
            self.input_layers[action.layer].actions().addAction(action.action)

    def add_joins(self, feedback):
        """ Add all joins between tables. """
        for definition in attribute_joins:
            join_layer = definition['join_layer']
            layer_add_join = definition['layer_add_join']

            feedback.pushInfo('Ajout de la jointure {} sur {}'.format(
                join_layer, layer_add_join))

            definition['join_layer'] = self.input_layers[join_layer]

            definition['layer_add_join'] = self.input_layers[layer_add_join]

            join_habitat = QgsVectorLayerJoinInfo()
            join_habitat.setJoinFieldName(definition['join_field_name'])
            join_habitat.setJoinLayer(definition['join_layer'])
            join_habitat.setJoinLayerId(definition['join_layer'].id())
            join_habitat.setTargetFieldName(definition['target_field_name'])
            join_habitat.setPrefix(definition['prefix'])
            if not definition['layer_add_join'].addJoin(join_habitat):
                raise Exception('Join not added {}'.format(definition['join_field_name']))

    def add_relations(self, context, feedback):
        """ Add all relations to the QGIS project. """
        relation_manager = context.project().relationManager()
        for definition in relations:

            definition = dict(definition)
            if relation_manager.relation(definition['id']):
                relation_manager.removeRelation(definition['id'])
                feedback.pushDebugInfo('Removing pre-existing relation {}'.format(definition['id']))

            referencing = definition['referencing_layer']
            definition['referencing_layer'] = self.input_layers[referencing].id()

            referenced = definition['referenced_layer']
            definition['referenced_layer'] = self.input_layers[referenced].id()

            feedback.pushInfo(definition['name'])
            relation = QgsRelation()
            relation.setId(definition['id'])
            relation.setName(definition['name'])
            relation.setReferencingLayer(definition['referencing_layer'])
            relation.setReferencedLayer(definition['referenced_layer'])
            relation.addFieldPair(definition['referencing_field'], definition['referenced_field'])
            relation.setStrength(QgsRelation.Association)
            if not relation.isValid():
                raise QgsProcessingException('{} is not valid'.format(definition['name']))

            relation_manager.addRelation(relation)
            self.success_relation += 1

    @staticmethod
    def add_alias_from_csv(feedback, input_layers):
        """ The geopackage has been created from CSV files, but we need to set alias. """
        feedback.pushInfo("Relecture du CSV pour réappliquer les alias sur les champs sur")

        for name, layer in input_layers.items():
            feedback.pushInfo("   {}".format(name))
            path = resources_path('data_models', '{}.csv'.format(name))
            csv = load_csv(name, path)

            for csv_feature in csv.getFeatures():
                index = layer.fields().indexOf(csv_feature['name'])
                if not index:
                    continue

                layer.setFieldAlias(index, csv_feature['alias'])

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
