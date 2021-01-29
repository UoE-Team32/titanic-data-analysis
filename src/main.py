from utils.dataset import Column, DataSet
import data_gaps


def main():
    """

    """
    data_set = DataSet("test.csv")
    data = data_set.train

    print(data.isnull().sum())
    data_gaps.replace_data(data, Column.AGE)
    print("-" * 5 + " FILLED DATA " + "-" * 5)
    print(data.isnull().sum())


if __name__ == '__main__':
    main()

