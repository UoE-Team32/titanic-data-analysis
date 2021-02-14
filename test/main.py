import unittest
import sys


if __name__ == '__main__':
    sys.path.append(r'/app/src')

    loader = unittest.TestLoader()
    tests = loader.discover('tests')
    testRunner = unittest.runner.TextTestRunner()
    testRunner.run(tests)
