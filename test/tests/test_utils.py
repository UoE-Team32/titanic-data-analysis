import unittest

from utils.graph import TK_IMPLEMENTED
from utils.dataset import DataSet


class GraphTestCase(unittest.TestCase):

    def test_tk_implemented(self):
        self.assertTrue(TK_IMPLEMENTED, msg="TK is not implemented in python")


class DatasetTestCase(unittest.TestCase):

    def test_get_class_name_str(self):
        self.assertEqual("First", DataSet.get_class_name_str(1))
        self.assertEqual("Second", DataSet.get_class_name_str(2))
        self.assertEqual("Third", DataSet.get_class_name_str(3))
