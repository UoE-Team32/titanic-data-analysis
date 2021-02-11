from collections import Counter

import pandas as pd

from src.utils.dataset import Column, DataSet
from src.utils.log import Log


def replace_age_na_values_w_estimates(data: pd.DataFrame, column: Column):
    """
    Replaces values of NaN/null age values with estimates based
    on other fields.
    :param data: Pandas dataframe including NaN age data.
    :param column: age column from the dataframe.
    :return: Pandas dataframe with age filled in.
    """

    # Here we are saying that anyone that is along on the boat is
    # defiantly over 18 so we are taking a mean value of over 18s.
    mean = data.loc[data[column.value] >= 18, column.value].mean()
    Log.debug("Replacing age >= 18 with mean avg: %s" % mean)
    data.loc[(data[Column.SIBSP.value] == 0) & (data[column.value].isnull()), [column.value]] = mean

    # Here we are saying that anyone that has mr/mrs is married and is
    # defiantly over 18 so we are taking a mean value of over 18s.
    # This is quite a long step because Mr is sometimes given at 16 but it is close enough.
    data.loc[(data[Column.NAME.value].str.contains(r".*Mr\.|.*Mrs\.")) & (data[column.value].isnull()), [column.value]] = mean

    # Here we are taking the remaining and taking a best guess
    # By using the
    # based on the fact that we known that it is < 18.
    mean = data.loc[data[column.value] < 18, column.value].mean()
    Log.debug("Replacing age < 18 with mean avg: %s" % mean)
    data.loc[data[column.value].isnull(), [column.value]] = mean

    return data


def replace_age_na_values_w_web_data(data: pd.DataFrame, column: Column):
    """
    Replaces values of NaN/null age values with values from the
    online database (https://www.encyclopedia-titanica.org/titanic-passenger-list/).
    (This might be cheating).
    :param data: Pandas dataframe including NaN age data.
    :param column: age column from the dataframe.
    :return: Pandas dataframe with age filled in.
    """
    raise NotImplementedError


def replace_weighted_avg(data: pd.DataFrame, column: Column):
    """
    Replaces values of NaN/null with values different waited values
    depending on the column provided.
    :param data: a pandas dataframe containing the column with NaN data.
    :param column: the column you would like to replace.
    :return: a pandas dataframe with data for the column filled in.
    """

    def passenger_class_mode_generator():
        for p_class in range(1, 4):
            values = data.loc[data[Column.PCLASS.value] == p_class, column.value].values
            yield Counter(values).most_common(1)[0]

    if column.EMBARKED:
        for idx, (mean, no_of_occurrences) in enumerate(passenger_class_mode_generator()):
            idx = idx + 1
            Log.debug("Replacing %s class setoff Embarked mean with %s" % (DataSet.get_class_name_str(idx), mean))

            data.loc[(data[Column.PCLASS.value] == idx) & (data[column.value].isnull()), [column.value]] = mean

    return data
