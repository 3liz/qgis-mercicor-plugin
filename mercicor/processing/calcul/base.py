__copyright__ = "Copyright 2021, 3Liz"
__license__ = "GPL version 3"
__email__ = "info@3liz.org"

from abc import abstractmethod

from mercicor.processing.base_algorithm import BaseProcessingAlgorithm


class CalculAlgorithm(BaseProcessingAlgorithm):

    def group(self):
        return 'Calcul'

    def groupId(self):
        return 'calcul'

    @abstractmethod
    def shortHelpString(self):
        pass
