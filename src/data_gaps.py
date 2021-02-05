from collections import Counter

import pandas as pd

from src.utils.dataset import Column
from src.utils.log import Log


# TODO(M-Whitaker): Setup functions to fill in data gaps for the age column for under 18s in A101032-5
# TODO(M-Whitaker): Document functions


def replace_age_na_values(data: pd.DataFrame, column: Column):
    """
    Replaces values of NaN/null with values.
    :param data: Pandas dataframe including age data.
    :param column: age column from the dataframe.
    :return: the changed Pandas dataframe.
    """

    Log.debug("Replacing age >= 18 with mean avg")
    mean = data.loc[data[column.value] >= 18, column.value].mean()
    Log.debug(mean)
    data.loc[(data[Column.SIBSP.value] == 0) & (data[column.value].isnull())] = mean

    return data


def replace_weighted_avg(data: pd.DataFrame, column: Column):
    """
    Replaces values of NaN/null with values.
    :param data:
    :param column:
    :return:
    """

    def pclass_mode_generator():
        for p_class in range(1, 4):
            values = data.loc[data[Column.PCLASS.value] == p_class, column.value].values
            yield Counter(values).most_common(1)[0]

    if column.EMBARKED:
        for idx, (mean, no_of_occurrences) in enumerate(pclass_mode_generator()):
            idx = idx + 1
            Log.debug("%s, %d" % (mean, no_of_occurrences))
            data.loc[(data[Column.PCLASS.value] == idx) & (data[column.value].isnull())] = mean

    return data
