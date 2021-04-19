""" Test definitions. """

import unittest

from mercicor.definitions.project_type import ProjectType

__copyright__ = "Copyright 2021, 3Liz"
__license__ = "GPL version 3"
__email__ = "info@3liz.org"


class TestDefinitions(unittest.TestCase):

    def test_project_type(self):
        """ Test about project type definitions. """
        project_pression = ProjectType.Pression
        self.assertListEqual(
            [
                'habitat',
                'pression',
                'liste_type_pression',
                'observations',
                'habitat_etat_ecologique',
                'scenario_pression',
                'habitat_pression_etat_ecologique',
                'metadata',
            ],
            project_pression.layers
        )

        projet_compensation = ProjectType.Compensation
        self.assertListEqual(
            [
                'habitat',
                'compensation',
                'observations',
                'habitat_etat_ecologique',
                'scenario_compensation',
                'habitat_compensation_etat_ecologique',
                'metadata',
            ],
            projet_compensation.layers
        )
