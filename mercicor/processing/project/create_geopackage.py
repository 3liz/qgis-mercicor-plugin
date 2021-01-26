__copyright__ = "Copyright 2020, 3Liz"
__license__ = "GPL version 3"
__email__ = "info@3liz.org"

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
    edit,
)

from mercicor.processing.project.base import BaseProjectAlgorithm
from mercicor.qgis_plugin_tools import load_csv, resources_path, tr


class CreateGeopackageProject(BaseProjectAlgorithm):

    FILE_GPKG = 'FILE_GPKG'
    PROJECT_CRS = 'PROJECT_CRS'
    PROJECT_NAME = 'PROJECT_NAME'
    PROJECT_EXTENT = 'PROJECT_EXTENT'
    OUTPUT_LAYERS = 'OUTPUT_LAYERS'

    def name(self):
        return 'create_geopackage_project'

    def displayName(self):
        return tr('Create geopackage project')

    def shortHelpString(self):
        return 'To start a blank new project, you need to create first a geopackage file.'

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

        base_name = self.parameterAsString(parameters, self.FILE_GPKG, context)
        project_name = self.parameterAsString(parameters, self.PROJECT_NAME, context)
        extent = self.parameterAsExtent(parameters, self.PROJECT_EXTENT, context)
        crs = self.parameterAsCrs(parameters, self.PROJECT_CRS, context)

        parent_base_name = str(Path(base_name).parent)
        if not base_name.endswith('.gpkg'):
            base_name = os.path.join(parent_base_name, Path(base_name).stem + '.gpkg')

        if os.path.exists(base_name):
            feedback.reportError('Le fichier existe déjà. Ré-écriture du fichier…')

        tables = {
            'habitat': 'Polygon',
            'pression': 'Polygon',
            'metadata': 'None',
            # 'liste_type_pression': 'None',
            # 'liste_sante': 'None',
        }

        self.create_geopackage(base_name, crs, tables)

        output_layers = self.load_layers(base_name, feedback, tables)

        # Add metadata
        fields = output_layers['metadata'].fields()
        feature = QgsFeature(fields)
        feature.setAttribute(fields.indexFromName('project_name'), project_name)
        feature.setAttribute(fields.indexFromName('crs'), str(crs.authid()))
        feature.setAttribute(fields.indexFromName('extent'), str(extent))
        with edit(output_layers['metadata']):
            output_layers['metadata'].addFeature(feature)

        # Load layers in the project
        output_id = []
        for layer in output_layers.values():
            context.temporaryLayerStore().addMapLayer(layer)
            context.addLayerToLoadOnCompletion(
                layer.id(),
                QgsProcessingContext.LayerDetails(
                    layer.name(),
                    context.project(),
                    self.OUTPUT_LAYERS
                )
            )
            context.project().setFileName(project_name)
            output_id.append(layer.id())

        return {self.FILE_GPKG: base_name, self.OUTPUT_LAYERS: output_id}

    @staticmethod
    def load_layers(base_name, feedback, tables):
        """ Create vector layer object from URI. """
        output_layers = {}
        for table in tables.keys():
            destination = QgsVectorLayer('{}|layername={}'.format(base_name, table), table, 'ogr')
            if not destination.isValid():
                raise QgsProcessingException(
                    '* ERROR: Can\'t load layer {} in {}'.format(table, base_name))

            feedback.pushInfo('The layer {} has been created'.format(table))
            output_layers[table] = destination

        return output_layers

    @staticmethod
    def create_geopackage(file_path, crs, tables) -> None:
        """ Create the geopackage for the given"""
        encoding = 'UTF-8'
        driver_name = QgsVectorFileWriter.driverForExtension('gpkg')
        for table, geometry in tables.items():

            layer_path = str(geometry)
            if layer_path != 'None':
                layer_path += "?crs={}".format(crs.authid())

            vector_layer = QgsVectorLayer(layer_path, table, "memory")
            data_provider = vector_layer.dataProvider()

            fields = QgsFields()

            path = resources_path('data_models', '{}.csv'.format(table))
            csv = load_csv(table, path)

            for csv_feature in csv.getFeatures():
                field = QgsField(name=csv_feature['name'], type=int(csv_feature['type']))
                field.setComment(csv_feature['comment'])
                field.setAlias(csv_feature['alias'])
                fields.append(field)

            del csv

            # add fields
            data_provider.addAttributes(fields)
            vector_layer.updateFields()

            # set create file layer options
            options = QgsVectorFileWriter.SaveVectorOptions()
            options.driverName = driver_name
            options.fileEncoding = encoding

            options.actionOnExistingFile = QgsVectorFileWriter.CreateOrOverwriteFile
            if os.path.exists(file_path):
                options.actionOnExistingFile = QgsVectorFileWriter.CreateOrOverwriteLayer

            options.layerName = vector_layer.name()
            options.layerOptions = ['FID=id']

            # write file
            write_result, error_message = QgsVectorFileWriter.writeAsVectorFormat(
                vector_layer,
                file_path,
                options)

            # result
            if write_result != QgsVectorFileWriter.NoError:
                raise QgsProcessingException('* ERROR: {}'.format(error_message))

            del fields
            del data_provider
            del vector_layer
