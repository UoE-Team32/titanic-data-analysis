import os
import re


class File:

    @classmethod
    def get_safe_file_path(cls, file_path: str, file_ext: str):
        """
        Creates a pats that will not overwrite other files and not error
        on case sensitive systems.
        :param file_path: An absolute file path including file name and extension.
        :param file_ext: File extension including the dot i.e ".csv".
        :return: A file path that can be used.
        """
        file_name = os.path.basename(file_path)
        file_path = file_path.replace(file_name, cls.get_safe_file_name(file_name))
        iteration = 0
        while cls.check_file_exists(file_path):
            iteration += 1
            if iteration == 1:
                split_path = file_path.split(file_ext)
                file_path = "".join((split_path[0] + "_%d" % iteration) + file_ext)
            else:
                regex = r"_\d*" + file_ext
                split_path = re.split(regex, file_path)
                file_path = "".join((split_path[0] + "_%d" % iteration) + file_ext)

        return file_path

    @staticmethod
    def get_safe_file_name(file_name: str):
        file_name = file_name\
                        .replace(" ", "_")\
                        .lower()

        return file_name

    @staticmethod
    def check_file_exists(filename: str):
        if os.path.isfile(filename):
            return True
        else:
            return False
