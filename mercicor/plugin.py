__copyright__ = "Copyright 2020, 3Liz"
__license__ = "GPL version 3"
__email__ = "info@3liz.org"

from qgis.core import Qgis, QgsApplication, QgsMessageLog
from qgis.PyQt.QtCore import QUrl
from qgis.PyQt.QtGui import QDesktopServices, QIcon
from qgis.PyQt.QtWidgets import QAction, QMessageBox

from mercicor.actions import actions_list_compensation, actions_list_pression
from mercicor.processing.provider import MercicorProvider
from mercicor.qgis_plugin_tools import resources_path


class Mercicor:

    def __init__(self, iface):
        self.iface = iface
        self.provider = None
        self.help_action = None

    def initProcessing(self):
        if not self.provider:
            self.provider = MercicorProvider()
            QgsApplication.processingRegistry().addProvider(self.provider)

    def initGui(self):
        self.initProcessing()

        # Open the online help
        self.help_action = QAction(
            QIcon(resources_path('icons', 'icon.jpg')),
            'Mercicor',
            self.iface.mainWindow())
        self.iface.pluginHelpMenu().addAction(self.help_action)
        self.help_action.triggered.connect(self.open_help)

    def unload(self):
        if self.provider:
            QgsApplication.processingRegistry().removeProvider(self.provider)

        if self.help_action:
            self.iface.pluginHelpMenu().removeAction(self.help_action)
            del self.help_action

    @staticmethod
    def open_help():
        """ Open the online help. """
        QDesktopServices.openUrl(QUrl('https://packages.3liz.org/private/um3-mercicor/docs/'))

    @staticmethod
    def run_action(name, *args):
        """ Run a specific action. """
        actions_list = dict(actions_list_compensation, **actions_list_pression)
        if name not in actions_list:
            QMessageBox.critical(
                None, 'Action non trouvée', 'L\'action n\'a pas été trouvée.')
            return

        if actions_list[name].count != len(args):
            QMessageBox.critical(
                None, 'Mauvais nombre d\'arguments', 'Mauvais nombre d\'arguments pour l\'action.')
            return

        params = list(args)
        msg = 'Appel de l\'action {} avec les arguments: {}'
        QgsMessageLog.logMessage(
            msg.format(name, ', '.join(['{}'.format(i) for i in params])),
            'Mercicor', Qgis.Info)
        actions_list[name].function(*params)

    @staticmethod
    def run_tests(pattern='test_*.py', package=None):
        """Run the test inside QGIS."""
        # pylint: disable=import-outside-toplevel
        from pathlib import Path
        try:
            from mercicor.tests.test_runner import test_package
            if package is None:
                package = '{}.__init__'.format(Path(__file__).parent.name)
            test_package(package, pattern)
        except (AttributeError, ModuleNotFoundError):
            message = 'Could not load tests. Are you using a production package?'
            print(message)  # NOQA
