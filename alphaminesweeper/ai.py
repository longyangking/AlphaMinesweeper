'''
Artificial Intelligence Model for Minesweeper
'''
from __future__ import print_function
from __future__ import absolute_import
import os
import numpy as np

import keras 
import tensorflow as tf
import keras.backend as K

from keras.models import Model 
from keras.layers import Input, Dense, Conv2D, Flatten, BatchNormalization, Activation, LeakyReLU, Add
from keras.optimizers import Adam
from keras import regularizers

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' # Only error will be shown

class NeuralNetwork:
    def __init__(self, input_shape, output_dim, 
        network_structure,
        learning_rate=1e-3,
        l2_const=1e-4,
        verbose=False):

        self.input_shape = input_shape
        self.output_dim = output_dim
        self.network_structure = network_structure

        self.learning_rate = learning_rate
        self.l2_const = l2_const
        self.verbose = verbose

        self.model = self.build_model()

    def build_model(self):
        input_tensor = Input(shape=self.input_shape)

        x = self.__conv_block(input_tensor, self.network_structure[0]['filters'], self.network_structure[0]['kernel_size'])
        if len(self.network_structure) > 1:
            for h in self.network_structure[1:]:
                x = self.__res_block(x, h['filters'], h['kernel_size'])

        value = self.__value_block(x)
        action_prob = self.__action_prob_block(x)

        model = Model(inputs=[input_tensor], outputs=[action_prob, value])
        model.compile(
            loss={'policy': self.__policy_loss_function, 'value': 'mse'},
			optimizer=Adam(self.learning_rate),	
			loss_weights={'policy': 0.5, 'value': 0.5}	
			)
        
        return model

    def __policy_loss_function(self, y_true, y_pred):
        loss = tf.nn.softmax_cross_entropy_with_logits_v2(labels=y_true, logits=y_pred)
	    return loss
        # return K.sum(K.square(y_pred - y_true), axis=-1)

    def __conv_block(self, x, filters, kernel_size):
        '''
        Convolutional Neural Network
        '''
        out = Conv2D(
            filters = filters,
            kernel_size = kernel_size,
            padding = 'same',
            activation='linear',
            kernel_regularizer = regularizers.l2(self.l2_const)
        )(x)
        out = BatchNormalization(axis=1)(out)
        out = LeakyReLU()(out)
        return out

    def __res_block(self, x, filters, kernel_size):
        '''
        Residual Convolutional Neural Network
        '''
        out = Conv2D(
            filters = filters,
            kernel_size = kernel_size,
            padding = 'same',
            activation='linear',
            kernel_regularizer = regularizers.l2(self.l2_const)
        )(x)
        out = BatchNormalization(axis=1)(out)
        out = Add()([out, x])
        out = LeakyReLU()(out)
        return out

    def __action_prob_block(self, x):
        '''
        Action Neural Network
        '''
        out = Conv2D(
            filters = 2,
            kernel_size = 1,
            padding = 'same',
            activation= 'linear',
            kernel_regularizer = regularizers.l2(self.l2_const)
        )(x)
        out = BatchNormalization(axis=1)(out)
        out = LeakyReLU()(out)

        out = Flatten()(out)
        out = Dense(
            2*self.output_dim,
            activation='relu',
            kernel_regularizer=regularizers.l2(self.l2_const),
        )(out)

        out = Dense(
            self.output_dim,
            activation='sigmoid',
            kernel_regularizer=regularizers.l2(self.l2_const),
            name='policy'
        )(out)

        return out

    def __value_block(self, x):
        '''
        Action Neural Network
        '''
        out = Conv2D(
            filters = 1,
            kernel_size = 1,
            padding = 'same',
            activation= 'linear',
            kernel_regularizer = regularizers.l2(self.l2_const)
        )(x)
        out = BatchNormalization(axis=1)(out)
        out = LeakyReLU()(out)

        out = Flatten()(out)
        out = Dense(
            24,
            activation='relu',
            kernel_regularizer=regularizers.l2(self.l2_const),
        )(out)

        out = Dense(
            1,
            activation='tanh',
            kernel_regularizer=regularizers.l2(self.l2_const),
            name='value'
        )(out)

        return out

    def fit(self, Xs, ys, epochs, batch_size):
        history = self.model.fit(Xs, ys, epochs=epochs, batch_size=batch_size)
        return history

    def update(self, Xs, ys):
        loss = self.model.train_on_batch(Xs, ys)
        return loss

    def predict(self, X):
        X = X.reshape(self.input_shape)
        action_prob, value = self.model.predict([X])
        return action_prob[0], value[0]

    def save_model(self, filename):
        self.model.save_weights(filename)

    def load_model(self, filename):
        self.model.load_weights(filename)

    def plot_model(self, filename):
        from keras.utils import plot_model
        plot_model(self.model, show_shapes=True, to_file=filename)

class AI:
    def __init__(self, 
        state_shape, 
        action_dim,
        verbose=False):

        self.state_shape = state_shape
        self.action_dim = action_dim
        self.verbose = verbose

        network_structure = list()
        network_structure.append({'filters':128, 'kernel_size':3})
        network_structure.append({'filters':128, 'kernel_size':3})
        network_structure.append({'filters':128, 'kernel_size':3})
        network_structure.append({'filters':128, 'kernel_size':3})

        self.nnet = NeuralNetwork(
            input_shape=state_shape,
            output_dim=action_dim,
            network_structure=network_structure,
            verbose=verbose)

    def train(self, dataset, epochs, batch_size):
        states, action_probs, values = dataset
        history = self.nnet.fit(
            states, [action_probs, values],
            epochs=epochs, batch_size=batch_size)
        return history

    def update(self, dataset):
        states, action_probs, values = dataset
        loss = self.nnet.update(states, [action_probs, values])
        return loss

    def play(self, state):
        action_prob, value = self.nnet.predict(state)
        action = np.argmax(action_prob)
        return action

    def save_nnet(self, filename):
        self.nnet.save_model(filename)

    def load_nnet(self, filename):
        self.nnet.load_model(filename)

    def plot_nnet(self, filename):
        self.nnet.plot_model(filename)