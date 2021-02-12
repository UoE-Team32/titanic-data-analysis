# Tensorflow
import tensorflow.compat.v2.feature_column as fc
import tensorflow as tf
import pandas as pd

from utils.dataset import Column

class Model:
    # BASE FEATURE COLUMNS
    # Our data columns
    CATEGORICAL_COLUMNS = [Column.SEX.value, Column.SIBSP.value, Column.PARCH.value, Column.PCLASS.value, Column.EMBARKED.value]
    NUMERIC_COLUMNS = [Column.AGE.value, Column.FARE.value]

    FEATURE_COLUMNS = []

    def __init__(self, df_train, df_test):
        self.df_train = df_train
        self.df_test = df_test

        self.y_train = df_train.pop(Column.SURVIVED.value)

    @staticmethod
    def make_input_fn(data_df, label_df, num_epochs=10, shuffle=True, batch_size=32):
        def input_function():
            ds = tf.data.Dataset.from_tensor_slices((dict(data_df), label_df))

            if shuffle:
                ds = ds.shuffle(1000)

            ds = ds.batch(batch_size).repeat(num_epochs)
            return ds
        
        return input_function

    # Train
    def train(self):
        for feature_name in self.CATEGORICAL_COLUMNS:
            vocabulary = self.df_train[feature_name].unique()
            self.FEATURE_COLUMNS.append(tf.feature_column.categorical_column_with_vocabulary_list(feature_name, vocabulary))

        for feature_name in self.NUMERIC_COLUMNS:
            self.NUMERIC_COLUMNS.append(tf.feature_column.numeric_column(feature_name, dtype=tf.float32))

        # Creating and training testing inputs
        train_input_fn = self.make_input_fn(self.df_train, self.y_train)
        eval_input_fn = self.make_input_fn(self.df_test, Column.SURVIVED.value, num_epochs=1, shuffle=False)

        # Train the model
        linear_est = tf.estimator.LinearClassifier(feature_columns=self.FEATURE_COLUMNS)
        linear_est.train(train_input_fn)
        result = linear_est.evaluate(eval_input_fn)

        # Output
        pred_dicts = list(linear_est.predict(eval_input_fn))
        probs = pd.Series([pred['probabilities'][1] for pred in pred_dicts])
        print(probs)