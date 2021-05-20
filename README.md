# Mercicor

Extension MERCICOR pour QGIS

[![Tests 🎳](https://github.com/3liz/qgis-mercicor-plugin/actions/workflows/ci.yml/badge.svg)](https://github.com/3liz/qgis-mercicor-plugin/actions/workflows/ci.yml)

## Links

* Doc https://docs.3liz.org/qgis-mercicor-plugin/

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

If you want to disable the geopackage check for input layers :

```python
import os
os.environ['TESTING_MERCICOR'] = 'True'
```

## Credits

* Coral icon by [Tezar Tantular from the Noun Project](https://thenounproject.com/search/?q=coral&i=3657551)
