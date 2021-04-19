""" Test actions. """

import unittest

from qgis.core import QgsProject, QgsRelation, QgsVectorLayer

from mercicor.actions import change_scenario
from mercicor.definitions.relations import relations
from mercicor.qgis_plugin_tools import plugin_test_data_path

__copyright__ = "Copyright 2021, 3Liz"
__license__ = "GPL version 3"
__email__ = "info@3liz.org"


class TestActions(unittest.TestCase):

    @unittest.expectedFailure
    def test_action_scenario(self):
        """ Test we can change the scenario. """
        project = QgsProject.instance()
        project.clear()

        gpkg = plugin_test_data_path('main_geopackage_empty_pression.gpkg', copy=True)

        for layer_name in ('pression', 'habitat_pression_etat_ecologique', 'scenario_pression'):
            layer = QgsVectorLayer('{}|layername={}'.format(gpkg, layer_name), layer_name, 'ogr')
            project.addMapLayer(layer)
            self.assertTrue(layer.isValid())

        ids = [
            'scenario_pression-pression',
            'scenario_pression-habitat_pression_etat_ecologique',
        ]
        for definition in relations:
            if definition['id'] not in ids:
                continue

            referenced = definition['referenced_layer']
            layer_referenced = project.mapLayersByName(referenced)[0]
            definition['referenced_layer'] = layer_referenced.id()

            referencing = definition['referencing_layer']
            layer_referencing = project.mapLayersByName(referencing)[0]
            definition['referencing_layer'] = layer_referencing.id()

            relation = QgsRelation()
            relation.setId(definition['id'])
            relation.setName(definition['name'])
            relation.setReferencingLayer(definition['referencing_layer'])
            relation.setReferencedLayer(definition['referenced_layer'])
            relation.addFieldPair(definition['referencing_field'], definition['referenced_field'])
            relation.setStrength(QgsRelation.Association)
            if not relation.isValid():
                raise Exception('{} is not valid'.format(definition['name']))

            project.relationManager().addRelation(relation)

        self.assertEqual(2, len(project.relationManager().relations()))

        for layer in project.mapLayers().values():
            self.assertEqual(layer.subsetString(), '')

        change_scenario('1000', 'test', project=project)

        for layer in project.mapLayers().values():
            self.assertEqual(layer.subsetString(), '"scenario_id" = 1000')
