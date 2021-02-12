# Tensorflow
import tensorflow.compat.v2.feature_column as fc
import tensorflow as tf

class Train:
    def __init__(self):
        self

    @classmethod
    def make_input_fn(data_df, label_df, num_epochs=10, shuffle=True, batch_size=32):
        def input_function():
            ds = tf.data.Dataset.from_tensor_slices((dict(data_df), label_df))

            if shuffle:
                ds = ds.shuffle(1000)

            ds = ds.batch(batch_size).repeat(num_epochs)
            return ds
        
        return input_function
