import unittest

from src.utils.graph import TK_IMPLEMENTED


class GraphTestCase(unittest.TestCase):

    def test_tk_implemented(self):
        self.assertTrue(TK_IMPLEMENTED, msg="TK is not implemented in python")
