import pandas as pd
import numpy as np

from utils.dataset import Column


# TODO: Setup functions to fill in data gaps for the columns in A101032-5
# TODO: Decide what algorithms should be used for said fields.

def replace_data(data: pd.DataFrame, column: Column):
    data[column.value] = data[column.value].replace(np.NaN, data[column.value].mean())
