import unittest
import doctest
from uvc.rest.testing import test_rest_layer


def test_suite():
    suite = unittest.TestSuite(
        [
            unittest.defaultTestLoader.loadTestsFromName(__name__),
            doctest.DocTestSuite(),
            doctest.DocFileSuite(
                "../README.txt",
                optionflags=doctest.ELLIPSIS,
                globs={"layer": test_rest_layer},
            ),
        ]
    )
    suite.layer = test_rest_layer
    return suite
