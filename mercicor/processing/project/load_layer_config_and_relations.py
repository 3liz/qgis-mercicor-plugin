__copyright__ = "Copyright 2020, 3Liz"
__license__ = "GPL version 3"
__email__ = "info@3liz.org"

import os

from collections import OrderedDict
from pathlib import Path

from qgis.core import (
    Qgis,
    QgsMapLayer,
    QgsProcessing,
    QgsProcessingException,
    QgsProcessingOutputNumber,
    QgsProcessingParameterVectorLayer,
    QgsRelation,
    QgsVectorLayerJoinInfo,
)

from mercicor.actions import actions_list_compensation, actions_list_pression
from mercicor.definitions.joins import (
    attribute_joins_compensation,
    attribute_joins_pression,
)
from mercicor.definitions.project_type import ProjectType
from mercicor.definitions.relations import (
    relations_compensation,
    relations_pression,
)
from mercicor.processing.project.base import BaseProjectAlgorithm
from mercicor.qgis_plugin_tools import load_csv, resources_path


class BaseLoadLayerConfigAndRelations(BaseProjectAlgorithm):

    HABITAT_LAYER = 'HABITAT_LAYER'
    HABITAT_ETAT_ECOLOGIQUE_LAYER = 'HABITAT_ETAT_ECOLOGIQUE_LAYER'
    OBSERVATIONS_LAYER = 'OBSERVATIONS_LAYER'

    ACTIONS_ADDED = 'ACTIONS_ADDED'
    JOINS_ADDED = 'JOINS_ADDED'
    RELATIONS_ADDED = 'RELATIONS_ADDED'
    QML_LOADED = 'QML_LOADED'

    def __init__(self):
        super().__init__()
        self.success_qml = 0
        self.success_relation = 0
        self.success_join = 0
        self.success_action = 0
        self.input_layers = None

    @property
    def project_type(self) -> ProjectType:
        # noinspection PyTypeChecker
        return NotImplementedError

    @property
    def attribute_joins(self) -> list:
        """ List of all attribute joins. """
        return NotImplementedError

    @property
    def relations(self) -> list:
        """ List of all relations. """
        return NotImplementedError

    @property
    def actions_list(self) -> list:
        """ List of all actions. """
        return NotImplementedError

    def name(self):
        return "load_qml_and_relations_{}".format(self.project_type.label)

    def displayName(self):
        return "Charger les propriétés de {} pour toutes les couches".format(self.project_type.label)

    def shortHelpString(self):
        return (
            "Charger les propriétés pour les différentes couches : symbologie, formulaire, actions, "
            "configuration des champs.\n\n"
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
        _ = config
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.IMPACT_LAYER,
                self.project_type.label_impact,
                [QgsProcessing.TypeVectorPolygon],
                defaultValue=self.project_type.couche_impact,
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
                self.SCENARIO_IMPACT,
                self.project_type.label_scenario_impact,
                [QgsProcessing.TypeVectorPolygon],
                defaultValue=self.project_type.couche_scenario_impact,
            )
        )

        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.HABITAT_IMPACT_ETAT_ECOLOGIQUE,
                self.project_type.label_habitat_impact_etat_ecologique,
                [QgsProcessing.TypeVectorPolygon],
                defaultValue=self.project_type.couche_habitat_impact_etat_ecologique,
            )
        )

        self.addOutput(QgsProcessingOutputNumber(self.JOINS_ADDED, 'Nombre de jointures chargées'))
        self.addOutput(QgsProcessingOutputNumber(self.ACTIONS_ADDED, 'Nombre d\'actions chargées'))
        self.addOutput(QgsProcessingOutputNumber(self.RELATIONS_ADDED, 'Nombre de relations chargées'))
        self.addOutput(QgsProcessingOutputNumber(self.QML_LOADED, 'Nombre de QML chargés'))

    def prepareAlgorithm(self, parameters, context, feedback):
        self.fetch_layers(parameters, context)
        self.add_styles(feedback, self.input_layers)
        return True

    def processAlgorithm(self, parameters, context, feedback):
        _ = parameters, context

        feedback.pushInfo('\n')
        self.add_alias_from_csv(feedback, self.input_layers)

        return {
            self.QML_LOADED: self.success_qml,
            self.RELATIONS_ADDED: self.success_relation,
            self.JOINS_ADDED: self.success_join,
            self.ACTIONS_ADDED: self.success_action,
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
            self.JOINS_ADDED: self.success_join,
            self.ACTIONS_ADDED: self.success_action,
        }

    def add_actions(self, feedback):
        """ Add actions for layers. """
        for action in self.actions_list.values():
            # We remove multiple times actions on a layer :(
            self.input_layers[action.layer].actions().clearActions()

        for action in self.actions_list.values():
            feedback.pushInfo('Ajout de l\'action sur {}'.format(action.layer))
            self.input_layers[action.layer].actions().addAction(action.action)
            self.success_action += 1

    def add_joins(self, feedback):
        """ Add all joins between tables. """
        for definition in self.attribute_joins:
            definition = dict(definition)
            join_layer = definition['join_layer']
            layer_add_join = definition['layer_add_join']

            feedback.pushInfo('Ajout de la jointure {} sur {}'.format(
                join_layer, layer_add_join))

            definition['join_layer'] = self.input_layers[join_layer]

            definition['layer_add_join'] = self.input_layers[layer_add_join]

            for join in definition['layer_add_join'].vectorJoins():
                if definition['join_layer'] == join.joinLayer():
                    definition['layer_add_join'].removeJoin(join.joinLayer().id())
                    feedback.pushDebugInfo(
                        'Removing pre-existing join between {} and {}'.format(
                            definition['layer_add_join'].name(), definition['join_layer'].name()))

            join_habitat = QgsVectorLayerJoinInfo()
            join_habitat.setJoinFieldName(definition['join_field_name'])
            join_habitat.setJoinLayerId(definition['join_layer'].id())
            join_habitat.setTargetFieldName(definition['target_field_name'])
            join_habitat.setPrefix(definition['prefix'])
            join_habitat.setJoinLayer(definition['join_layer'])
            if 'block_list' in definition:
                if Qgis.QGIS_VERSION_INT >= 31400:
                    join_habitat.setJoinFieldNamesBlockList(definition['block_list'])
                else:
                    join_habitat.setJoinFieldNamesBlackList(definition['block_list'])
            if not definition['layer_add_join'].addJoin(join_habitat):
                raise Exception('Join not added {}'.format(definition['join_field_name']))
            self.success_join += 1

    def add_relations(self, context, feedback):
        """ Add all relations to the QGIS project. """
        relation_manager = context.project().relationManager()
        for definition in self.relations:
            # definition: Relation

            if relation_manager.relation(definition.qgis_id):
                relation_manager.removeRelation(definition.qgis_id)
                feedback.pushDebugInfo('Removing pre-existing relation {}'.format(definition.qgis_id))

            referencing = self.input_layers[definition.referencing_layer].id()
            referenced = self.input_layers[definition.referenced_layer].id()

            feedback.pushInfo(definition.name)
            relation = QgsRelation()
            relation.setId(definition.qgis_id)
            relation.setName(definition.name)
            relation.setReferencingLayer(referencing)
            relation.setReferencedLayer(referenced)
            relation.addFieldPair(definition.referencing_field, definition.referenced_field)
            relation.setStrength(QgsRelation.Association)
            if not relation.isValid():
                raise QgsProcessingException('{} is not valid'.format(definition.name))

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
        qml_component = OrderedDict()
        qml_component['style'] = QgsMapLayer.Symbology
        qml_component['fields'] = QgsMapLayer.Fields
        qml_component['form'] = QgsMapLayer.Forms
        qml_component['labels'] = QgsMapLayer.Labeling
        qml_component['layer_configuration'] = QgsMapLayer.LayerConfiguration

        for layer_name, vector_layer in input_layers.items():
            qml_list = []
            has_labels = False
            for name, component in qml_component.items():
                qml_file = resources_path('qml', name, '{}.qml'.format(layer_name))
                if not os.path.exists(qml_file):
                    continue
                self.success_qml += 1
                qml_list.append(qml_file)
                if component == QgsMapLayer.Labeling:
                    has_labels = True

            if not qml_list:
                continue

            output_file = str(self.combine_qml(layer_name, qml_list, has_labels))
            feedback.pushDebugInfo(output_file)
            message, flag = vector_layer.loadNamedStyle(output_file)
            if flag:
                feedback.reportError(message)
            feedback.pushInfo(vector_layer.name() + " QML for {} successfully loaded".format(layer_name))

    @staticmethod
    def combine_qml(layer_name: str, qml_list: list, has_labels: bool) -> Path:
        """ Combine a few QML together in a single file. """
        # Actions is missing from categories because it is managed with Python code
        qml_str = (
            '<!DOCTYPE qgis PUBLIC \'http://mrcc.com/qgis.dtd\' \'SYSTEM\'>\n'
            '<qgis simplifyAlgorithm="0" readOnly="0" simplifyLocal="1" simplifyDrawingHints="1" '
            'simplifyMaxScale="1" hasScaleBasedVisibilityFlag="0" maxScale="0" labelsEnabled="{label}" '
            'styleCategories="LayerConfiguration|Symbology|Symbology3D|Labeling|Fields|Forms|MapTips|Diagrams'
            '|AttributeTable|Rendering|CustomProperties|GeometryOptions|Relations|Temporal|Legend|Elevation" '
            'simplifyDrawingTol="1" version="{version}" minScale="100000000">\n'.format(
                label='1' if has_labels else '0',
                version=Qgis.QGIS_VERSION)
        )

        for qml in qml_list:
            with open(qml, 'r', encoding='utf-8') as f:
                qml_str += ''.join(f.readlines()[2:-1])

        qml_str += '</qgis>'

        output_file = Path(resources_path('qml', 'auto_generated', '{}.qml'.format(layer_name)))
        if output_file.exists():
            # Do not use missing_ok, Python 3.8 min
            output_file.unlink()

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(qml_str)

        return output_file

    def fetch_layers(self, parameters, context):
        """ Fetch layers from the form and set them in a dictionary. """
        impact_layer = self.parameterAsVectorLayer(parameters, self.IMPACT_LAYER, context)
        habitat_layer = self.parameterAsVectorLayer(parameters, self.HABITAT_LAYER, context)
        habitat_etat_ecologique = self.parameterAsVectorLayer(
            parameters, self.HABITAT_ETAT_ECOLOGIQUE_LAYER, context)
        observations_layer = self.parameterAsVectorLayer(parameters, self.OBSERVATIONS_LAYER, context)
        scenario_impact = self.parameterAsVectorLayer(parameters, self.SCENARIO_IMPACT, context)
        habitat_impact_etat_ecologique = self.parameterAsVectorLayer(
            parameters, self.HABITAT_IMPACT_ETAT_ECOLOGIQUE, context)

        self.input_layers = {
            "habitat": habitat_layer,
            self.project_type.couche_impact: impact_layer,
            "observations": observations_layer,
            "habitat_etat_ecologique": habitat_etat_ecologique,
            self.project_type.couche_scenario_impact: scenario_impact,
            self.project_type.couche_habitat_impact_etat_ecologique: habitat_impact_etat_ecologique,
        }


class LoadLayerConfigAndRelationsPression(BaseLoadLayerConfigAndRelations):

    IMPACT_LAYER = 'PRESSION_LAYER'
    SCENARIO_IMPACT = 'SCENARIO_PRESSION'
    HABITAT_IMPACT_ETAT_ECOLOGIQUE = 'HABITAT_PRESSION_ETAT_ECOLOGIQUE'
    PRESSURE_LIST_LAYER = 'PRESSURE_LIST_LAYER'

    @property
    def project_type(self):
        return ProjectType.Pression

    def initAlgorithm(self, config=None):

        super().initAlgorithm(config)
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.PRESSURE_LIST_LAYER,
                "Liste des types de pression",
                [QgsProcessing.TypeVectorPolygon],
                defaultValue='liste_type_pression',
            )
        )

    def fetch_layers(self, parameters, context):

        super().fetch_layers(parameters, context)
        list_pressure_layer = self.parameterAsVectorLayer(parameters, self.PRESSURE_LIST_LAYER, context)

        self.input_layers["liste_type_pression"] = list_pressure_layer

    @property
    def attribute_joins(self) -> list:
        """ List of all attribute joins. """
        return attribute_joins_pression

    @property
    def relations(self) -> list:
        """ List of all relations. """
        return relations_pression

    @property
    def actions_list(self) -> list:
        """ List of all actions. """
        return actions_list_pression


class LoadLayerConfigAndRelationsCompensation(BaseLoadLayerConfigAndRelations):

    IMPACT_LAYER = 'COMPENSATION_LAYER'
    SCENARIO_IMPACT = 'SCENARIO_COMPENSATION'
    HABITAT_IMPACT_ETAT_ECOLOGIQUE = 'HABITAT_COMPENSATION_ETAT_ECOLOGIQUE'

    @property
    def project_type(self):
        return ProjectType.Compensation

    @property
    def attribute_joins(self) -> list:
        """ List of all attribute joins. """
        return attribute_joins_compensation

    @property
    def relations(self) -> list:
        """ List of all relations. """
        return relations_compensation

    @property
    def actions_list(self) -> list:
        """ List of all actions. """
        return actions_list_compensation
