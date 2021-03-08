"""Tools to work with resource files."""

import configparser
import shutil
import tempfile

from os.path import abspath, dirname, join

from qgis.core import QgsProcessingException, QgsVectorLayer


def plugin_path(*args):
    """Get the path to plugin root folder.

    :param args List of path elements e.g. ['img', 'logos', 'image.png']
    :type args: str

    :return: Absolute path to the plugin path.
    :rtype: str
    """
    path = dirname(__file__)
    path = abspath(abspath(path))
    for item in args:
        path = abspath(join(path, item))

    return path


def metadata_config() -> configparser:
    """Get the INI config parser for the metadata file.

    :return: The config parser object.
    :rtype: ConfigParser
    """
    path = plugin_path("metadata.txt")
    config = configparser.ConfigParser()
    config.read(path)
    return config


def plugin_test_data_path(*args, copy=False):
    """Get the path to the plugin test data path.

    :param args List of path elements e.g. ['img', 'logos', 'image.png']
    :type args: str

    :param copy: If the file must be copied into a temporary directory first.
    :type copy: bool

    :return: Absolute path to the resources folder.
    :rtype: str
    """
    path = abspath(abspath(join(plugin_path(), "tests", "data")))
    for item in args:
        path = abspath(join(path, item))

    if copy:
        temp = tempfile.mkdtemp()
        shutil.copy(path, temp)
        return join(temp, args[-1])
    else:
        return path


def resources_path(*args):
    """Get the path to our resources folder.

    :param args List of path elements e.g. ['img', 'logos', 'image.png']
    :type args: str

    :return: Absolute path to the resources folder.
    :rtype: str
    """
    path = abspath(abspath(join(plugin_path(), "resources")))
    for item in args:
        path = abspath(join(path, item))

    return path


def load_csv(csv_filename: str, path=None) -> QgsVectorLayer:
    """Load a named CSV as a vector layer."""
    if not path:
        path = resources_path('data', '{}.csv'.format(csv_filename))
    layer = QgsVectorLayer(path, csv_filename, 'ogr')
    layer.setProviderEncoding('UTF-8')
    if not layer.isValid():
        raise QgsProcessingException(
            '* ERREUR: Impossible de charger le CSV "{}"'.format(path))

    return layer
