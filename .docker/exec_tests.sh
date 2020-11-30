#!/usr/bin/env bash
export $(grep -v '^#' .env | xargs)

TEST_PATTERN=${1:default_pattern}

docker exec -it qgis sh \
  -c "export TEST_PATTERN=${TEST_PATTERN} && cd /tests_directory/${PLUGIN_NAME} && qgis_testrunner.sh tests.test_runner.test_package"
