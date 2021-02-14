import unittest

from utils.file import File
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


class FileTestCase(unittest.TestCase):

    def test_get_safe_file_name(self):
        unsafe_filenames = \
            {
                "i#am#unsafe": File.get_safe_file_name("i AM unsaFE\\/:*?\"<>|"),
                "#": File.get_safe_file_name("")
            }
        for expected, actual in unsafe_filenames.items():
            self.assertEqual(expected, actual)

    def test_get_safe_file_path(self):
        # TODO(M-Whitaker): Setup mocking system to check file saving
        pass

    def test_check_file_exists(self):
        # TODO(M-Whitaker): Setup mocking system to check file saving
        pass
