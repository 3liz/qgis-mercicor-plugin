__copyright__ = "Copyright 2021, 3Liz"
__license__ = "GPL version 3"
__email__ = "info@3liz.org"

from collections import namedtuple
from enum import Enum, unique


class Project(namedtuple(
        "Project",
        [
            "label",
            "calcul_type",
            "label_habitat",
            "couche_habitat",
            "label_impact",
            "couche_impact",
            "label_liste_type_pression",
            "couche_liste_type_pression",
            "label_observations",
            "couche_observations",
            "label_habitat_etat_ecologique",
            "couche_habitat_etat_ecologique",
            "label_scenario_impact",
            "couche_scenario_impact",
            "label_habitat_impact_etat_ecologique",
            "couche_habitat_impact_etat_ecologique",
        ])):

    @property
    def layers(self) -> list:
        data = []
        existing = [layer for layer in self._fields if layer.startswith('couche_')]
        for layer in existing:
            if getattr(self, layer) is None:
                continue

            name = layer.replace('couche_', '')
            if self.label == 'pression':
                name = name.replace('impact', 'pression')
            else:
                name = name.replace('impact', 'compensation')
            data.append(name)

        data.append('metadata')
        return data


@unique
class ProjectType(Project, Enum):

    Pression = Project(
        label='pression',
        calcul_type='perte',
        label_habitat="Couche des habitats",
        couche_habitat="habitat",
        label_impact="Couche des pressions",
        couche_impact="pression",
        label_liste_type_pression='Liste des types de pression',
        couche_liste_type_pression='liste_type_pression',
        label_observations="Couche des observations",
        couche_observations="observations",
        label_habitat_etat_ecologique="Table des observations ramenées à l'habitat",
        couche_habitat_etat_ecologique="habitat_etat_ecologique",
        label_scenario_impact='Table scénario pression',
        couche_scenario_impact='scenario_pression',
        label_habitat_impact_etat_ecologique='Couche habitat pression état écologique',
        couche_habitat_impact_etat_ecologique='habitat_pression_etat_ecologique',
    )

    Compensation = Project(
        label='compensation',
        calcul_type='gain',
        label_habitat="Couche des habitats",
        couche_habitat="habitat",
        label_impact="Couche des compensations",
        couche_impact="compensation",
        label_liste_type_pression=None,
        couche_liste_type_pression=None,
        label_observations="Couche des observations",
        couche_observations="observations",
        label_habitat_etat_ecologique="Table des observations ramenées à l'habitat",
        couche_habitat_etat_ecologique="habitat_etat_ecologique",
        label_scenario_impact='Table scénario compensation',
        couche_scenario_impact='scenario_compensation',
        label_habitat_impact_etat_ecologique='Couche habitat compensation état écologique',
        couche_habitat_impact_etat_ecologique='habitat_compensation_etat_ecologique',
    )
