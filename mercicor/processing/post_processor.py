__copyright__ = "Copyright 2021, 3Liz"
__license__ = "GPL version 3"
__email__ = "info@3liz.org"

from qgis.core import QgsProcessingLayerPostProcessorInterface

""" Post processor which are used in Processing algorithms. """


class TriggerRepaintPostProcessor(QgsProcessingLayerPostProcessorInterface):
    instance = None

    def postProcessLayer(self, layer, context, feedback):
        layer.triggerRepaint()

    @staticmethod
    def create() -> 'TriggerRepaintPostProcessor':
        TriggerRepaintPostProcessor.instance = TriggerRepaintPostProcessor()
        return TriggerRepaintPostProcessor.instance
