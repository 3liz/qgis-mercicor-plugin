#!/usr/bin/env bash
export $(grep -v '^#' .env | xargs)

TEST_PATTERN=${1:default_pattern}

docker exec -t qgis sh \
  -c "export TEST_PATTERN=${TEST_PATTERN} && cd /tests_directory/${PLUGIN_NAME} && qgis_testrunner.sh tests.test_runner.test_package"

docker exec -t qgis sh \
  -c "chown -R `stat -c "%u:%g" ../${PLUGIN_NAME}` /tests_directory/${PLUGIN_NAME}"
