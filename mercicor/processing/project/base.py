__copyright__ = "Copyright 2021, 3Liz"
__license__ = "GPL version 3"
__email__ = "info@3liz.org"

from abc import abstractmethod

from mercicor.processing.base_algorithm import BaseProcessingAlgorithm


class BaseProjectAlgorithm(BaseProcessingAlgorithm):

    def group(self):
        return 'Administration'

    def groupId(self):
        return 'administration'

    @abstractmethod
    def shortHelpString(self):
        pass
