import argparse
import logging

import missingno as msno

import data_gaps
from model import BoostedTreesModel
from utils.dataset import Column, DataSet
from utils.graph import Graph
from utils.log import Log


# Suppress warnings (used to hide Tensorflow warnings)
# os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"


def args():
    parser = argparse.ArgumentParser(description='TensorFlow Model for the Kaggle Titanic Dataset.')
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
    Program Entry Point
    """
    Log.info("Starting application...")

    datasets = {
        "testing": None,
        "training": None
    }

    for dataset_name in datasets.keys():
        # Create a dataset object
        _dataset = DataSet(argv.train_data if dataset_name == "training" else argv.test_data)
        data = _dataset.df

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
            _dataset.save_csv("ERROR.csv")
            Log.critical("There is N/A data within the dataset please check \"ERROR.csv\"",
                         data.isna().sum())

        # Print fixed dataset
        msno.matrix(data)
        Graph.plot_graph("Missing data Fix", to_file=True)

        # Append dataset object to array
        datasets[dataset_name] = _dataset

    model = BoostedTreesModel(datasets['training'].df, datasets['testing'].df)  # Change depending on algorithm
    model.train()

    # Output to a CSV
    output_df = model.test()
    output_dataset = DataSet(None, output_df)
    output_dataset.save_csv("output.csv")


if __name__ == '__main__':
    main(args())
