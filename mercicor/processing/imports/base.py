__copyright__ = "Copyright 2021, 3Liz"
__license__ = "GPL version 3"
__email__ = "info@3liz.org"

from abc import abstractmethod

from mercicor.processing.base_algorithm import BaseProcessingAlgorithm


class BaseImportAlgorithm(BaseProcessingAlgorithm):

    def group(self):
        return 'Import'

    def groupId(self):
        return 'import'

    @abstractmethod
    def shortHelpString(self):
        pass
