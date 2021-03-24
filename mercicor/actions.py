__copyright__ = "Copyright 2021, 3Liz"
__license__ = "GPL version 3"
__email__ = "info@3liz.org"

from collections import Callable

from qgis.core import Qgis, QgsAction, QgsMessageLog, QgsProject
from qgis.utils import iface

from mercicor.definitions.relations import (
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

    if project is None:
        project = QgsProject.instance()

    relations_ids = [
        scenario_pression__pression['id'],
        scenario_pression__habitat_pression_etat_ecologique['id'],
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


action_change_scenario = QgsAction(
    QgsAction.GenericPython,
    'Mettre ce scénario par défaut',
    CALL.format(action_name=change_scenario.__name__, params='[% "id" %], \'[% "nom" %]\''),
    '',
    False,
    'Permet de changer de scénario pour les couches pression et habitat écologique',
    ['Feature', 'Field'],
    ''
)


class Action:

    def __init__(self, layer: str, count: int, function: Callable, action: QgsAction):
        self.layer = layer
        self.count = count
        self.function = function
        self.action = action


actions_list = {
    change_scenario.__name__: Action(
        'scenario_pression',
        2,
        change_scenario,
        action_change_scenario
    )
}
