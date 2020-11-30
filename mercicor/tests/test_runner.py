import os
import unittest

from mercicor.tests.conftest import pytest_report_header

__copyright__ = "Copyright 2019, 3Liz"
__license__ = "GPL version 3"
__email__ = "info@3liz.org"
__revision__ = "$Format:%H$"


def _run_tests(test_suite, package_name, pattern):
    """Core function to test a test suite.
    :param test_suite: Unittest test suite
    """
    count = test_suite.countTestCases()
    print("######## Environment   ########")
    print(pytest_report_header(None))
    print("{} tests has been discovered in {} with pattern {}".format(count, package_name, pattern))
    print("######## Running tests ########")
    results = unittest.TextTestRunner(verbosity=2).run(test_suite)
    print("######## Summary       ########")
    print("Errors               : {}".format(len(results.errors)))
    print("Failures             : {}".format(len(results.failures)))
    print("Expected failures    : {}".format(len(results.expectedFailures)))
    print("Unexpected successes : {}".format(len(results.unexpectedSuccesses)))
    print("Skip                 : {}".format(len(results.skipped)))
    successes = (
        results.testsRun - (
            len(results.errors) + len(results.failures) + len(results.expectedFailures)
            + len(results.unexpectedSuccesses) + len(results.skipped)))
    print("Successes            : {}".format(successes))
    print("TOTAL                : {}".format(results.testsRun))


def test_package(package="..", pattern="test_*.py"):
    """Test package.
    This function is called by CLI without arguments.

    :param package: The package to test.
    :type package: str

    :param pattern: The pattern of files to discover.
    :type pattern: str
    """
    pattern_environment = os.environ.get('TEST_PATTERN')
    if pattern_environment and pattern_environment != 'default_pattern':
        print("Pattern from environment : {}".format(pattern_environment))
        pattern = pattern_environment

    test_loader = unittest.defaultTestLoader
    test_suite = test_loader.discover(package, pattern=pattern)
    _run_tests(test_suite, package, pattern)


if __name__ == "__main__":
    test_package()
