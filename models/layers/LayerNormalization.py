import numpy as np
import tensorflow as tf
from tensorflow.keras.layers import Layer


class LayerNormalization(Layer):
    def __init__(self,
                 eps=np.float32(1e-8),
                 **kwargs):
        self.eps = eps
        super().__init__(**kwargs)

    def build(self, input_shape):
        self.gamma = self.add_weight(name='gamma',
                                     shape=(input_shape[-1]),
                                     initializer='ones')

        self.beta = self.add_weight(name='beta',
                                    shape=(input_shape[-1]),
                                    initializer='zeros')
        super().build(input_shape)

    def call(self, x):
        mean, var = tf.nn.moments(x, axes=-1, keepdims=True)
        std = tf.sqrt(var) + self.eps

        return self.gamma * (x - mean) / std + self.beta

    def compute_output_shape(self, input_shape):
        return input_shape

    def compute_mask(self, inputs, mask):
        return mask
