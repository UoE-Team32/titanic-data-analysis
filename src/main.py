import argparse

import missingno as msno

from src.utils.dataset import Column, DataSet
from src.utils.graph import Graph
import data_gaps


def args():
    parser = argparse.ArgumentParser(description='Description.')
    parser.add_argument('--dataset', metavar='filename.csv', type=str, default="test.csv",
                        help='a titanic dataset csv file.')

    return parser


def main(args):
    """

    """
    data_set = DataSet(args.dataset)
    data = data_set.train
    msno.matrix(data)
    Graph.plot_graph()
    data_gaps.replace_data(data, Column.AGE)
    msno.matrix(data)
    Graph.plot_graph()


if __name__ == '__main__':
    args = args().parse_args()
    main(args)

