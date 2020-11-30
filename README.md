# Mercicor

Extension MERCICOR pour QGIS

## Links

* Doc https://packages.3liz.org/private/mercicor/docs/
* Dépôt QGIS https://packages.3liz.org/private/mercicor/plugins.xml

## Running tests

* In Docker

```bash
make start_tests
make run_tests
# Run a custom pattern
cd .docker/ && ./exec_tests.sh test_*.py
make stop_tests

# All in one, but slower
make tests
```

* In your QGIS Desktop itself
  * Open the QGIS console

```python
from qgis.utils import plugins
plugins['mercicor'].run_tests()

# Custom pattern
plugins['mercicor'].run_tests('test_*.py')
```

* In your IDE, with linked QGIS library
    * Setup your `QGIS_PREFIX_PATH` etc
    * Right click on a test and launch it
