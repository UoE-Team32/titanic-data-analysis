# Tensorflow
import tensorflow.compat.v2.feature_column as fc
import tensorflow as tf
import pandas as pd

from pprint import pprint
from utils.dataset import Column


class Model:
    # BASE FEATURE COLUMNS
    # Our data columns
    CATEGORICAL_COLUMNS = [Column.SEX.value, Column.SIBSP.value, Column.PARCH.value,
                           Column.PCLASS.value, Column.EMBARKED.value]
    NUMERIC_COLUMNS = [Column.AGE.value, Column.FARE.value]

    FEATURE_COLUMNS = []

    linear_est = None

    def __init__(self, df_train, df_test):
        self.df_train = df_train
        self.df_eval = self.df_train.sample(frac=0.2, random_state=33)
        self.df_train.drop(self.df_eval.index, inplace=True)

        self.y_train = df_train.pop(Column.SURVIVED.value)
        self.y_eval = self.df_eval.pop(Column.SURVIVED.value)

        # Testing
        self.df_test = df_test
        self.y_test = pd.Series([-1] * self.df_test.shape[0])  # Dummy row

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
            self.FEATURE_COLUMNS.append(
                tf.feature_column.categorical_column_with_vocabulary_list(feature_name, vocabulary))

        for feature_name in self.NUMERIC_COLUMNS:
            self.FEATURE_COLUMNS.append(tf.feature_column.numeric_column(feature_name, dtype=tf.float32))

        # Creating and training testing inputs
        train_input_fn = self.make_input_fn(self.df_train, self.y_train, num_epochs=20)
        eval_input_fn = self.make_input_fn(self.df_eval, self.y_eval, num_epochs=1, shuffle=False)

        # Create a dataset
        self.make_input_fn(self.df_train, self.y_train, batch_size=10)()

        age_times_sex = fc.crossed_column(['Age', 'Sex'], hash_bucket_size=100)
        derived_feature_columns = [age_times_sex]

        # Train the model
        # TODO: Suppress WARNING:tensorflow:Using temporary folder as model directory: x
        self.linear_est = tf.estimator.LinearClassifier(feature_columns=self.FEATURE_COLUMNS+derived_feature_columns)
        self.linear_est.train(train_input_fn)
        result = self.linear_est.evaluate(eval_input_fn)

        pprint(result)

    # Testing method
    def test(self):
        test_input_fn = self.make_input_fn(self.df_test, self.y_test, num_epochs=1, shuffle=False)

        pred_dicts = list(self.linear_est.predict(test_input_fn))
        probabilities = pd.Series([pred['probabilities'][1] for pred in pred_dicts])

        # Determine whether or not the passenger survived
        predictions = []

        for p in probabilities:
            if p < 0.5:
                predictions.append(0)
            else:
                predictions.append(1)
        
        predictions = pd.Series(predictions)

        # Create new dataframe to be used as submission
        sub_df = pd.DataFrame(data={
            'PassengerId':  self.df_test.index,
            'Survived': predictions
        })

        print(sub_df.Survived.value_counts())

        return sub_df
