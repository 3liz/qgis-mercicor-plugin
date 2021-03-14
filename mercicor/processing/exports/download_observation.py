__copyright__ = "Copyright 2021, 3Liz"
__license__ = "GPL version 3"
__email__ = "info@3liz.org"

import os.path

from pathlib import Path

from qgis.core import (
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransform,
    QgsFeature,
    QgsFeatureRequest,
    QgsField,
    QgsGeometry,
    QgsProcessing,
    QgsProcessingParameterBoolean,
    QgsProcessingParameterFileDestination,
    QgsProcessingParameterVectorLayer,
    QgsVectorFileWriter,
    QgsVectorLayer,
    edit,
)
from qgis.PyQt.QtCore import QVariant

from mercicor.processing.exports.base import BaseExportAlgorithm


class DownloadObservationFile(BaseExportAlgorithm):

    INPUT_LAYER = 'INPUT_LAYER'
    INCLUDE_X_Y = 'INCLUDE_X_Y'
    DESTINATION_FILE = 'DESTINATION_FILE'

    def name(self):
        return 'download_observation_file'

    def displayName(self):
        return 'Télécharger le modèle des observations'

    def shortHelpString(self):
        return "Télécharger le modèle de fichier tableur pour les observations."

    def initAlgorithm(self, config):

        tooltip = "Couche des observations dans le geopackage"
        parameter = QgsProcessingParameterVectorLayer(
            self.INPUT_LAYER,
            tooltip,
            [QgsProcessing.TypeVectorPoint],
            defaultValue='observations',
        )
        self.set_tooltip_parameter(parameter, tooltip)
        self.addParameter(parameter)

        tooltip = "Inclure des colonnes avec latitude/longitude"
        parameter = QgsProcessingParameterBoolean(
            self.INCLUDE_X_Y,
            tooltip,
            defaultValue=True,
        )
        self.set_tooltip_parameter(parameter, tooltip)
        self.addParameter(parameter)

        tooltip = 'Fichier tableur de destination'
        parameter = QgsProcessingParameterFileDestination(
            self.DESTINATION_FILE,
            tooltip,
            fileFilter='xlsx',
        )
        self.set_tooltip_parameter(parameter, tooltip)
        self.addParameter(parameter)

    def processAlgorithm(self, parameters, context, feedback):
        input_layer = self.parameterAsVectorLayer(parameters, self.INPUT_LAYER, context)
        file_path = self.parameterAsFile(parameters, self.DESTINATION_FILE, context)
        include_geom = self.parameterAsBool(parameters, self.INCLUDE_X_Y, context)

        empty_layer = input_layer.featureCount() == 0
        if empty_layer:
            # Bug from QGIS not exporting fields if the attribute table is empty
            # Let's make a copy in memory and add a feature
            layer = input_layer.materialize(QgsFeatureRequest())
            feature = QgsFeature(layer.fields())
            feature.setAttribute('id', 1)
            feature.setAttribute('nom_station', 'Nom de la station')
            with edit(layer):
                layer.addFeature(feature)
        else:
            layer = input_layer

        if include_geom:
            if not empty_layer:
                # Let's make a copy first, we do not want to edit the original layer
                layer = layer.materialize(QgsFeatureRequest())

            feedback.pushInfo('Ajout des colonnes longitude et latitude en EPSG:4326')
            self.add_geom_columns(context, layer)

        parent_base_name = str(Path(file_path).parent)
        if not file_path.endswith('.xlsx'):
            file_path = os.path.join(parent_base_name, Path(file_path).stem + '.xlsx')

        if os.path.exists(file_path):
            feedback.reportError('Le fichier existe déjà. Ré-écriture du fichier…')

        feedback.pushInfo('Écriture du fichier tableur')
        self.export_as_xlsx(context, file_path, layer)

        return {self.DESTINATION_FILE: file_path}

    @staticmethod
    def add_geom_columns(context, layer: QgsVectorLayer) -> None:
        """ Add latitude and longitude columns in the layer. """
        fields = [
            QgsField('longitude', type=QVariant.Double),
            QgsField('latitude', type=QVariant.Double),
        ]
        transform = QgsCoordinateTransform(
            layer.crs(),
            QgsCoordinateReferenceSystem(4326),
            context.project())

        with edit(layer):
            for field in fields:
                layer.addAttribute(field)

            request = QgsFeatureRequest()
            request.setSubsetOfAttributes(['latitude', 'longitude'], layer.fields())
            for feature in layer.getFeatures(request):
                geom = QgsGeometry(feature.geometry())
                if not geom:
                    continue

                geom.transform(transform)
                geom = geom.centroid().asPoint()
                feature.setAttribute('longitude', geom.x())
                feature.setAttribute('latitude', geom.y())
                layer.updateFeature(feature)

    @staticmethod
    def export_as_xlsx(context, file_path, input_layer) -> None:
        """ Export the layer to XLSX to the given path. """
        options = QgsVectorFileWriter.SaveVectorOptions()
        options.driverName = QgsVectorFileWriter.driverForExtension('xlsx')
        options.fileEncoding = 'UTF-8'
        options.layerName = input_layer.name()
        options.actionOnExistingFile = QgsVectorFileWriter.CreateOrOverwriteFile
        if os.path.exists(file_path):
            options.actionOnExistingFile = QgsVectorFileWriter.CreateOrOverwriteLayer

        file_writer = QgsVectorFileWriter.create(
            file_path,
            input_layer.fields(),
            input_layer.type(),
            QgsCoordinateReferenceSystem.fromEpsgId(4326),
            context.project().transformContext(),
            options)

        for feature in input_layer.getFeatures():
            file_writer.addFeature(feature)
