__copyright__ = "Copyright 2021, 3Liz"
__license__ = "GPL version 3"
__email__ = "info@3liz.org"

from collections import namedtuple
from enum import Enum, unique

Project = namedtuple(
    "Project",
    [
        "label",
        "calcul_type",
        "label_impact_scenario",
        "couche_impact_scenario",
        "label_habitat_impact_etat_ecologique",
        "couche_habitat_impact_etat_ecologique",
    ])


@unique
class ProjectType(Project, Enum):

    Pression = Project(
        label='pression',
        calcul_type='perte',
        label_impact_scenario='Table scénario pression',
        couche_impact_scenario='scenario_pression',
        label_habitat_impact_etat_ecologique='Couche habitat pression état écologique',
        couche_habitat_impact_etat_ecologique='habitat_pression_etat_ecologique',
    )
    Compensation = Project(
        label='compensation',
        calcul_type='gain',
        label_impact_scenario='Table scénario compensation',
        couche_impact_scenario='compensation_pression',
        label_habitat_impact_etat_ecologique='Couche habitat compensation état écologique',
        couche_habitat_impact_etat_ecologique='habitat_compensation_etat_ecologique',
    )
