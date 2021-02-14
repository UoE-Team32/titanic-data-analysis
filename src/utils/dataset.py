import os
from enum import Enum

import pandas as pd

from utils.log import Log
from utils.file import File


class Column(Enum):
    PASSENGERID = "PassengerId"
    SURVIVED = "Survived"
    PCLASS = "Pclass"
    NAME = "Name"
    SEX = "Sex"
    AGE = "Age"
    SIBSP = "SibSp"
    PARCH = "Parch"
    TICKET = "Ticket"
    FARE = "Fare"
    CABIN = "Cabin"
    EMBARKED = "Embarked"


class DataSet:
    df = pd.DataFrame()

    def __init__(self, data_file_name, df: pd.DataFrame = None):
        if data_file_name:
            self.read_csv(data_file_name)
        elif df is not None:
            self.df = df
        else:
            Log.error("Invalid constructor arguments")

    def read_csv(self, data_file_name: str):
        """
        Reads the said csv file from $(pwd)/data
        :param data_file_name: file name of csv file containing titanic data
        """
        self.df = pd.read_csv(os.path.join(os.getenv("PROJECT_DIR"), "data", data_file_name),
                              index_col=Column.PASSENGERID.value)

    def save_csv(self, data_file_name: str):
        """
        Writes the said csv file to $(pwd)/data/out
        :param data_file_name: file name of csv file containing titanic data
        """
        file_path = os.path.join(os.getenv("PROJECT_DIR"), "data/out", data_file_name)
        file_path = File.get_safe_file_path(file_path, ".csv")

        Log.info("Saving csv as \"%s\"..." % file_path)
        self.df.to_csv(file_path, index=False)

    @staticmethod
    def get_class_name_str(class_no: int):
        """
        Turns an integer into a string representation.
        :param class_no: class number from 1-3
        :return: a string representation of class_no
        """
        if 3 >= class_no >= 1:
            if class_no == 1:
                return "First"
            elif class_no == 2:
                return "Second"
            elif class_no == 3:
                return "Third"
        else:
            Log.warning("Provided invalid class number %d" % class_no)
