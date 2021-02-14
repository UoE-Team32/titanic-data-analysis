import argparse
import logging

import missingno as msno

from utils.log import Log
from utils.dataset import Column, DataSet
from utils.graph import Graph
from utils.model import Model
import data_gaps

# Supress warnings (used to hide Tensorflow warnings)
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

def args():
    parser = argparse.ArgumentParser(description='Description.')
    parser.add_argument('--train-dataset', metavar='filename.csv', type=str, default="train.csv",
                        help='a titanic dataset csv file.', dest="train_data")
    parser.add_argument('--log', default="INFO", dest="loglevel", help='the logging level')
    parser.add_argument('--rootlog', dest="rootloglevel", help='the logging level')
    parser.add_argument('--test-dataset', metavar='filename.csv', type=str, default="test.csv",
                        help='a test titanic dataset csv file.', dest="test_data")

    def get_log_level(log_level):
        numeric_level = getattr(logging, log_level, None)
        if not isinstance(numeric_level, int):
            raise ValueError('Invalid log level: %s' % log_level)
        return numeric_level

    arguments = parser.parse_args()

    if arguments.loglevel and not arguments.rootloglevel:
        arguments.loglevel = get_log_level(arguments.loglevel)

        Log.set_up(arguments.loglevel)
    if arguments.rootloglevel:
        arguments.rootloglevel = get_log_level(arguments.rootloglevel)
        Log.set_up(arguments.rootloglevel, root_logger=True)

    return arguments


def main(argv):
    """

    """
    Log.info("Starting application...")

    # Train dataset
    data_set = DataSet(argv.train_data)
    data = data_set.train

    # Remove Cabin header from the dataset
    data.pop(Column.CABIN.value)

    # Fill gaps in age by using mean avg for adults and ... for children
    data = data_gaps.replace_age_na_values_w_estimates(data, Column.AGE)
    # Fill gaps in embarked by using a weighted avg
    data = data_gaps.replace_weighted_avg(data, Column.EMBARKED)

    # Fill gaps in fare by using a weighted avg
    data = data_gaps.replace_weighted_avg(data, Column.FARE)

    # Check that there are no more errors in the dataset
    if data.isna().values.any():
        data_set.save_csv("ERROR.csv")
        Log.critical("There is N/A data within the dataset please check \"ERROR.csv\"",
                     data.isna().sum())

    # Test dataset
    test_dataset = DataSet(argv.test_data)
    test_data = test_dataset.train

    # Remove Cabin header from the dataset
    test_data.pop(Column.CABIN.value)

    # Fill gaps in age by using mean avg for adults and ... for children
    test_data = data_gaps.replace_age_na_values_w_estimates(test_data, Column.AGE)
    # Fill gaps in embarked by using a weighted avg
    test_data = data_gaps.replace_weighted_avg(test_data, Column.EMBARKED)

    # Fill gaps in fare by using a weighted avg
    test_data = data_gaps.replace_weighted_avg(test_data, Column.FARE)

    # Check that there are no more errors in the dataset
    if test_data.isna().values.any():
        data_set.save_csv("ERROR.csv")
        Log.critical("There is N/A data within the dataset please check \"ERROR.csv\"",
                     test_data.isna().sum())

    model = Model(data, test_data)
    model.train()

    # Output to a CSV
    output_csv = model.test()
    output_csv.to_csv("output.csv", index=None)

if __name__ == '__main__':
    main(args())
