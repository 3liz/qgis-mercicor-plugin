__copyright__ = "Copyright 2020, 3Liz"
__license__ = "GPL version 3"
__email__ = "info@3liz.org"
__revision__ = "$Format:%H$"

import os.path

from pathlib import Path

from qgis.core import (
    QgsFeature,
    QgsField,
    QgsFields,
    QgsProcessingContext,
    QgsProcessingException,
    QgsProcessingOutputMultipleLayers,
    QgsProcessingParameterCrs,
    QgsProcessingParameterExtent,
    QgsProcessingParameterFileDestination,
    QgsProcessingParameterString,
    QgsVectorFileWriter,
    QgsVectorLayer,
)

from mercicor.processing.base_algorithm import BaseProcessingAlgorithm
from mercicor.qgis_plugin_tools import load_csv, resources_path, tr


class CreateGeopackageProject(BaseProcessingAlgorithm):

    FILE_GPKG = 'FILE_GPKG'
    PROJECT_CRS = 'PROJECT_CRS'
    PROJECT_NAME = 'PROJECT_NAME'
    PROJECT_EXTENT = 'PROJECT_EXTENT'
    OUTPUT_LAYERS = 'OUTPUT_LAYERS'

    def name(self):
        return 'create_geopackage_project'

    def displayName(self):
        return tr('Create geopackage project')

    def group(self):
        return tr('Administration')

    def groupId(self):
        return 'administration'

    def shortHelpString(self):
        return 'algorithm to create a geopackage file with 3 layers'

    def initAlgorithm(self, config):

        # target project folder
        self.addParameter(
            QgsProcessingParameterFileDestination(
                self.FILE_GPKG,
                'Geopackage File',
                fileFilter='gpkg'
            )
        )

        self.addParameter(
            QgsProcessingParameterString(
                self.PROJECT_NAME,
                tr('Project name'),
                defaultValue='',
                optional=False
            )
        )

        # target project crs
        self.addParameter(
            QgsProcessingParameterCrs(
                self.PROJECT_CRS,
                tr('Project CRS'),
                defaultValue='EPSG:2154',
                optional=False,
            )
        )

        # target project extent
        self.addParameter(
            QgsProcessingParameterExtent(
                self.PROJECT_EXTENT,
                tr('Project extent'),
                defaultValue=''
            )
        )

        self.addOutput(
            QgsProcessingOutputMultipleLayers(
                self.OUTPUT_LAYERS,
                'Couches de sorties'
            )
        )

    def processAlgorithm(self, parameters, context, feedback):

        baseName = self.parameterAsString(parameters, self.FILE_GPKG, context)
        projectName = self.parameterAsString(parameters, self.PROJECT_NAME, context)
        extent = self.parameterAsExtent(parameters, self.PROJECT_EXTENT, context)
        parentBaseName = str(Path(baseName).parent)
        if not baseName.endswith('.gpkg'):
            baseName = os.path.join(parentBaseName, Path(baseName).stem + '.gpkg')

        if os.path.exists(baseName):
            feedback.reportError('Le fichier existe déjà.')

        tables = [
            'habitat',
            'pression',
            'metadata',
        ]

        geometries = {
            'habitat': 'Polygon',
            'pression': 'Polygon',
            'metadata': 'None',
        }

        encoding = 'UTF-8'
        driverName = QgsVectorFileWriter.driverForExtension('gpkg')
        crs = self.parameterAsCrs(parameters, self.PROJECT_CRS, context)

        for tab in tables:
            # create virtual layer
            vl_path = geometries[tab]
            if vl_path != 'None':
                vl_path = "{0}?crs={1}".format(geometries[tab], crs.authid())
            vl = QgsVectorLayer(vl_path, tab, "memory")
            pr = vl.dataProvider()

            # define fields
            fields = QgsFields()

            path = resources_path('data_models', '{0}.csv'.format(tab,))
            csv = load_csv(tab, path)

            for cfeat in csv.getFeatures():
                fields.append(QgsField(name=cfeat['name'], type=int(cfeat['type'])))

            del csv

            # add fields
            pr.addAttributes(fields)
            vl.updateFields()  # tell the vector layer to fetch changes from the provider

            # set create file layer options
            options = QgsVectorFileWriter.SaveVectorOptions()
            options.driverName = driverName
            options.fileEncoding = encoding

            options.actionOnExistingFile = QgsVectorFileWriter.CreateOrOverwriteFile
            if os.path.exists(baseName):
                options.actionOnExistingFile = QgsVectorFileWriter.CreateOrOverwriteLayer

            options.layerName = vl.name()
            options.layerOptions = ['FID=id']

            # write file
            write_result, error_message = QgsVectorFileWriter.writeAsVectorFormat(
                vl,
                baseName,
                options)

            # result
            if write_result != QgsVectorFileWriter.NoError:
                raise QgsProcessingException(
                    '* ERROR: {0}'.format(error_message))

            del fields
            del pr
            del vl

        outputLayers = []
        for tab in tables:
            # Connexion à la couche troncon_rerau_classif dans le Geopackage
            dest_layer = QgsVectorLayer('{0}|layername={1}'.format(baseName, tab), tab, 'ogr')
            if not dest_layer.isValid():
                raise QgsProcessingException(
                    '* ERROR: Can\'t load layer {1} in {0}'.format(baseName, tab))

            feedback.pushInfo('The layer {0} has been created'.format(tab))

            if tab == 'metadata':
                fields = dest_layer.fields()
                feature = QgsFeature()
                feature.setFields(fields)
                feature.setAttribute(fields.indexFromName('project_name'), projectName)
                feature.setAttribute(fields.indexFromName('crs'), str(crs.authid()))
                feature.setAttribute(fields.indexFromName('extent'), str(extent))
                dest_layer.startEditing()
                dest_layer.addFeature(feature)
                dest_layer.commitChanges()

            outputLayers.append(dest_layer.id())
            # Ajout de la couche au projet
            context.temporaryLayerStore().addMapLayer(dest_layer)
            context.addLayerToLoadOnCompletion(
                dest_layer.id(),
                QgsProcessingContext.LayerDetails(
                    tab,
                    context.project(),
                    self.OUTPUT_LAYERS
                )
            )
            context.project().setFileName(projectName)
        return {self.FILE_GPKG: baseName, self.OUTPUT_LAYERS: outputLayers}
