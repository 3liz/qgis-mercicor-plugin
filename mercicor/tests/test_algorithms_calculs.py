""" Test calcul. """

from qgis.core import (
    QgsExpression,
    QgsExpressionContext,
    QgsExpressionContextUtils,
    QgsFeature,
    QgsGeometry,
    QgsVectorLayer,
    edit,
)
from qgis.processing import run

from mercicor.processing.calcul.calcul_notes import CalculNotes
from mercicor.qgis_plugin_tools import plugin_test_data_path
from mercicor.tests.base_processing import BaseTestProcessing

__copyright__ = "Copyright 2021, 3Liz"
__license__ = "GPL version 3"
__email__ = "info@3liz.org"


class TestCalculsAlgorithms(BaseTestProcessing):

    def test_expressions_mercicor(self):
        """ Test that expressions are valid. """
        gpkg = plugin_test_data_path('main_geopackage_empty.gpkg', copy=True)
        layer = QgsVectorLayer('{}|layername=observations'.format(gpkg), 'test', 'ogr')

        # Fields
        for field in CalculNotes().fields:
            with self.subTest(i=field):
                self.assertGreater(layer.fields().indexOf(field), -1, field)

        # Expressions
        context = QgsExpressionContext()
        context.appendScope(QgsExpressionContextUtils.layerScope(layer))

        for field, formula in CalculNotes().expressions.items():
            with self.subTest(i=field):
                self.assertGreater(layer.fields().indexOf(field), -1)

                expression = QgsExpression(formula)
                expression.prepare(context)
                self.assertFalse(expression.hasParserError())

    def test_unicity_facies_name(self):
        """ Test the unicity between name and facies. """
        gpkg = plugin_test_data_path('main_geopackage_empty.gpkg', copy=True)
        layer = QgsVectorLayer('{}|layername=habitat'.format(gpkg), 'test', 'ogr')
        self.assertTrue(layer.isValid())

        feature_1 = QgsFeature(layer.fields())
        feature_1.setAttribute('id', 1)
        feature_1.setAttribute('nom', 'nom 1')
        feature_1.setAttribute('facies', 'facies 1')
        feature_1.setGeometry(QgsGeometry.fromWkt('POINT(0 0)').buffer(1, 20))

        feature_2 = QgsFeature(layer.fields())
        feature_2.setAttribute('id', 2)
        feature_2.setAttribute('nom', 'nom 2')
        feature_2.setAttribute('facies', 'facies 2')
        feature_2.setGeometry(QgsGeometry.fromWkt('POINT(1 1)').buffer(1, 20))

        with edit(layer):
            layer.addFeature(feature_1)
            layer.addFeature(feature_2)

        params = {
            'INPUT': layer,
            'OUTPUT': 'memory:'
        }
        results = run("mercicor:calcul_unicity_habitat", params)
        self.assertEqual(2, results['NUMBER_OF_UNIQUE'])
        self.assertEqual(0, results['NUMBER_OF_NON_UNIQUE'])
        self.assertEqual(0, results['OUTPUT'].featureCount())

        feature_3 = QgsFeature(layer.fields())
        feature_3.setAttribute('id', 3)
        feature_3.setAttribute('nom', 'nom 1')
        feature_3.setAttribute('facies', 'facies 1')
        feature_3.setGeometry(QgsGeometry.fromWkt('POINT(2 2)').buffer(1, 20))

        with edit(layer):
            layer.addFeature(feature_3)

        results = run("mercicor:calcul_unicity_habitat", params)
        self.assertEqual(2, results['NUMBER_OF_UNIQUE'])
        self.assertEqual(1, results['NUMBER_OF_NON_UNIQUE'])
        self.assertEqual(1, results['OUTPUT'].featureCount())
        self.assertSetEqual({1}, results['OUTPUT'].uniqueValues(0))
        self.assertSetEqual({'nom 1'}, results['OUTPUT'].uniqueValues(1))
        self.assertSetEqual({'facies 1'}, results['OUTPUT'].uniqueValues(2))
