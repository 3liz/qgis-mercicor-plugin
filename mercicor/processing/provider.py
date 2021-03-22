__copyright__ = "Copyright 2021, 3Liz"
__license__ = "GPL version 3"
__email__ = "info@3liz.org"

from qgis.core import QgsProcessingProvider
from qgis.PyQt.QtGui import QIcon

from mercicor.processing.calcul.calcul_notes import CalculNotes
from mercicor.processing.calcul.calcul_unicity_habitat import (
    CalculUnicityHabitat,
)
from mercicor.processing.exports.download_observation import (
    DownloadObservationFile,
)
from mercicor.processing.imports.import_data_habitat import ImportHabitatData
from mercicor.processing.imports.import_data_observations import (
    ImportObservationData,
)
from mercicor.processing.imports.import_data_pressure import ImportPressureData
from mercicor.processing.project.create_geopackage import (
    CreateGeopackageProject,
)
from mercicor.processing.project.load_qml_and_relations import (
    LoadStylesAndRelations,
)
from mercicor.qgis_plugin_tools import resources_path


class MercicorProvider(QgsProcessingProvider):

    def loadAlgorithms(self):
        self.addAlgorithm(CalculNotes())
        self.addAlgorithm(CalculUnicityHabitat())
        self.addAlgorithm(CreateGeopackageProject())
        self.addAlgorithm(DownloadObservationFile())
        self.addAlgorithm(ImportHabitatData())
        self.addAlgorithm(ImportObservationData())
        self.addAlgorithm(ImportPressureData())
        self.addAlgorithm(LoadStylesAndRelations())

    def id(self):  # NOQA
        return "mercicor"

    def icon(self):
        return QIcon(resources_path("icons", "icon.jpg"))

    def name(self):
        return "Mercicor"
