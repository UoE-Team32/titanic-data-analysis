import pandas as pd
import numpy as np

from utils.dataset import Column


def replace_data(data: pd.DataFrame, column: Column):
    data[column.value] = data[column.value].replace(np.NaN, data[column.value].mean())

