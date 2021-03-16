""" Test calcul. """

from qgis.core import (
    QgsExpression,
    QgsExpressionContext,
    QgsExpressionContextUtils,
    QgsVectorLayer,
)

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
        layer = QgsVectorLayer('{}|layername=habitat_pression_etat_ecologique'.format(gpkg), 'test', 'ogr')

        context = QgsExpressionContext()
        context.appendScope(QgsExpressionContextUtils.layerScope(layer))

        expressions = CalculNotes().expressions
        for field, formula in expressions.items():
            self.assertGreater(layer.fields().indexOf(field), -1)

            expression = QgsExpression(formula)
            expression.prepare(context)
            self.assertFalse(expression.hasParserError())
