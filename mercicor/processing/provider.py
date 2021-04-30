__copyright__ = "Copyright 2021, 3Liz"
__license__ = "GPL version 3"
__email__ = "info@3liz.org"

from qgis.core import QgsProcessingProvider
from qgis.PyQt.QtGui import QIcon

from mercicor.processing.calcul.calcul_habitat_etat_ecologique import (
    CalculHabitatEtatEcologique,
)
from mercicor.processing.calcul.calcul_habitat_impact_ecologique import (
    CalculHabitatCompensationEtatEcologique,
    CalculHabitatPressionEtatEcologique,
)
from mercicor.processing.calcul.calcul_notes import CalculNotes
from mercicor.processing.calcul.calcul_pertes_gains import (
    CalculGains,
    CalculPertes,
)
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
from mercicor.processing.imports.import_data_pression_compensation import (
    ImportDataCompensation,
    ImportDataPression,
)
from mercicor.processing.project.create_geopackage import (
    CreateGeopackageProjectCompensation,
    CreateGeopackageProjectPression,
)
from mercicor.processing.project.load_layer_config_and_relations import (
    LoadLayerConfigAndRelationsCompensation,
    LoadLayerConfigAndRelationsPression,
)
from mercicor.qgis_plugin_tools import resources_path


class MercicorProvider(QgsProcessingProvider):

    def loadAlgorithms(self):
        self.addAlgorithm(CalculGains())
        self.addAlgorithm(CalculHabitatCompensationEtatEcologique())
        self.addAlgorithm(CalculHabitatEtatEcologique())
        self.addAlgorithm(CalculHabitatPressionEtatEcologique())
        self.addAlgorithm(CalculNotes())
        self.addAlgorithm(CalculUnicityHabitat())
        self.addAlgorithm(CalculPertes())
        self.addAlgorithm(CreateGeopackageProjectCompensation())
        self.addAlgorithm(CreateGeopackageProjectPression())
        self.addAlgorithm(DownloadObservationFile())
        self.addAlgorithm(ImportHabitatData())
        self.addAlgorithm(ImportObservationData())
        self.addAlgorithm(ImportDataCompensation())
        self.addAlgorithm(ImportDataPression())
        self.addAlgorithm(LoadLayerConfigAndRelationsCompensation())
        self.addAlgorithm(LoadLayerConfigAndRelationsPression())

    def id(self):  # NOQA
        return "mercicor"

    def icon(self):
        return QIcon(resources_path("icons", "icon.jpg"))

    def name(self):
        return "Mercicor"
