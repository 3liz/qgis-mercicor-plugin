__copyright__ = "Copyright 2020, 3Liz"
__license__ = "GPL version 3"
__email__ = "info@3liz.org"

from qgis.core import QgsApplication

from mercicor.processing.provider import MercicorProvider


class Mercicor:

    def __init__(self, iface):
        _ = iface
        self.provider = None

    def initProcessing(self):
        if not self.provider:
            self.provider = MercicorProvider()
            QgsApplication.processingRegistry().addProvider(self.provider)

    def initGui(self):
        self.initProcessing()

    def unload(self):
        if self.provider:
            QgsApplication.processingRegistry().removeProvider(self.provider)

    @staticmethod
    def run_tests(pattern='test_*.py', package=None):
        """Run the test inside QGIS."""
        from pathlib import Path
        try:
            from mercicor.tests.test_runner import test_package
            if package is None:
                package = '{}.__init__'.format(Path(__file__).parent.name)
            test_package(package, pattern)
        except (AttributeError, ModuleNotFoundError):
            message = 'Could not load tests. Are you using a production package?'
            print(message) # NOQA
