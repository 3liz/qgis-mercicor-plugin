__copyright__ = "Copyright 2021, 3Liz"
__license__ = "GPL version 3"
__email__ = "info@3liz.org"

from abc import abstractmethod

from mercicor.processing.base_algorithm import BaseProcessingAlgorithm


class BaseExportAlgorithm(BaseProcessingAlgorithm):

    def group(self):
        return 'Export'

    def groupId(self):
        return 'export'

    def checkParameterValues(self, parameters, context):
        """ Check if all given output layers are in the geopackage. """
        destination = self.parameterAsVectorLayer(parameters, self.INPUT_LAYER, context)
        flag, msg = self.check_layer_is_geopackage(destination)
        if not flag:
            return False, msg

        return super().checkParameterValues(parameters, context)

    @abstractmethod
    def shortHelpString(self):
        pass
