__copyright__ = "Copyright 2021, 3Liz"
__license__ = "GPL version 3"
__email__ = "info@3liz.org"

from collections import Callable

from qgis.core import Qgis, QgsAction, QgsExpression, QgsMessageLog, QgsProject
from qgis.utils import iface

from mercicor.definitions.relations import (
    relations_compensation,
    relations_pression,
    scenario_compensation__compensation,
    scenario_compensation__habitat_compensation_etat_ecologique,
    scenario_pression__habitat_pression_etat_ecologique,
    scenario_pression__pression,
)

CALL = (
    "from qgis.utils import plugins\n"
    "plugins['mercicor'].run_action('{action_name}', {params})"
)


def change_scenario(*args, project: QgsProject = None):
    """ Action used to change the scenario and apply filter. """
    scenario_id = int(args[0])
    scenario_name = args[1]
    type_scenario = args[2]

    if project is None:
        project = QgsProject.instance()

    if type_scenario == 'pression':
        relations_ids = [
            scenario_pression__pression.qgis_id,
            scenario_pression__habitat_pression_etat_ecologique.qgis_id,
        ]
    else:
        relations_ids = [
            scenario_compensation__compensation.qgis_id,
            scenario_compensation__habitat_compensation_etat_ecologique.qgis_id,
        ]

    for ids in relations_ids:
        relation = project.relationManager().relation(ids)
        if not relation.isValid():
            QgsMessageLog.logMessage(
                'Impossible de trouver la relation {}, est-ce qu\'elle est présente '
                'avec un autre nom ?'.format(ids),
                'Mercicor',
                Qgis.Warning
            )
            continue

        layer = relation.referencingLayer()
        layer.setSubsetString('"scenario_id" = {}'.format(scenario_id))

    iface.messageBar().pushSuccess(
        'Mercicor',
        'Changement du scénario vers {}, ID {}'.format(scenario_name, scenario_id)
    )


def delete_scenario(*args, project: QgsProject = None):
    """ Action used to delete the scenario and his entities child """
    scenario_id = int(args[0])
    scenario_name = args[1]
    layer_name = 'scenario_' + args[2]
    scenario_layer = None

    if project is None:
        project = QgsProject.instance()

    relations = []
    relations.extend(relations_compensation)
    relations.extend(relations_pression)
    for relation in relations:
        if relation.referenced_layer == layer_name:
            relation = project.relationManager().relation(relation.qgis_id)
            if not relation.isValid():
                QgsMessageLog.logMessage(
                    'Impossible de trouver la relation {}, est-ce qu\'elle est présente '
                    'avec un autre nom ?'.format(relation.qgis_id),
                    'Mercicor',
                    Qgis.Warning
                )
                continue
            scenario_layer = relation.referencedLayer()
            layer = relation.referencingLayer()
            layer.startEditing()
            filter_expression = QgsExpression.createFieldEqualityExpression('scenario_id', scenario_id)
            for feature in layer.getFeatures(filter_expression):
                layer.deleteFeature(feature.id())
            layer.commitChanges()

    scenario_layer = QgsProject.instance().mapLayersByName(scenario_layer.name())[0]
    scenario_layer.startEditing()
    filter_expression = QgsExpression.createFieldEqualityExpression('id', scenario_id)
    for feature in scenario_layer.getFeatures(filter_expression):
        scenario_layer.deleteFeature(feature.id())
    scenario_layer.commitChanges()

    iface.messageBar().pushSuccess(
        'Mercicor',
        'Suppression du scénario {}, ID {}'.format(scenario_name, scenario_id)
    )


action_change_scenario_pression = QgsAction(
    QgsAction.GenericPython,
    'Mettre ce scénario par défaut',
    CALL.format(action_name=change_scenario.__name__, params='[% "id" %], \'[% "nom" %]\', \'pression\''),
    '',
    False,
    'Permet de changer de scénario pour les couches pression et habitat écologique',
    ['Feature', 'Field'],
    ''
)

action_delete_scenario_pression = QgsAction(
    QgsAction.GenericPython,
    'Supprimer ce scénario',
    CALL.format(action_name=delete_scenario.__name__, params='[% "id" %], \'[% "nom" %]\', \'pression\''),
    '',
    False,
    'Permet de supprimer le scénario en supprimant les entités enfants',
    ['Feature', 'Field'],
    ''
)

action_change_scenario_compensation = QgsAction(
    QgsAction.GenericPython,
    'Mettre ce scénario par défaut',
    CALL.format(action_name=change_scenario.__name__, params='[% "id" %], \'[% "nom" %]\', \'compensation\''),
    '',
    False,
    'Permet de changer de scénario pour les couches pression et habitat écologique',
    ['Feature', 'Field'],
    ''
)

action_delete_scenario_compensation = QgsAction(
    QgsAction.GenericPython,
    'Supprimer ce scénario',
    CALL.format(action_name=delete_scenario.__name__, params='[% "id" %], \'[% "nom" %]\', \'compensation\''),
    '',
    False,
    'Permet de supprimer le scénario en supprimant les entités enfants',
    ['Feature', 'Field'],
    ''
)


class Action:

    def __init__(self, layer: str, count: int, function: Callable, action: QgsAction):
        self.layer = layer
        self.count = count
        self.function = function
        self.action = action


actions_list_pression = {
    change_scenario.__name__: Action(
        'scenario_pression',
        3,
        change_scenario,
        action_change_scenario_pression
    ),
    delete_scenario.__name__: Action(
        'scenario_pression',
        3,
        delete_scenario,
        action_delete_scenario_pression
    )
}

actions_list_compensation = {
    change_scenario.__name__: Action(
        'scenario_compensation',
        3,
        change_scenario,
        action_change_scenario_compensation
    ),
    delete_scenario.__name__: Action(
        'scenario_compensation',
        3,
        delete_scenario,
        action_delete_scenario_compensation
    )
}
