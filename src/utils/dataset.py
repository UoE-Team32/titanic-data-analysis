import os
from enum import Enum

import pandas as pd


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
    train = pd.DataFrame()

    def __init__(self, data_file_name: str):
        self.read_csv(data_file_name)

    def read_csv(self, data_file_name: str):
        """

        :param data_file_name:
        """
        self.train = pd.read_csv(os.path.join(os.getenv("PROJECT_DIR"), "data", data_file_name))
