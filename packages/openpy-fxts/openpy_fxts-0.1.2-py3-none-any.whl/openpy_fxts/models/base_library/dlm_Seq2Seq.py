from openpy_fxts.baseline_mdl import baseline_mdl
from openpy_fxts.preprocessing.prepare_data import pre_processing_data

import tensorflow as tf

from openpy_fxts.base_tf import tkm, tkl, tku
from openpy_fxts.preprocessing.prepare_data import pre_processing_data
import keras.utils.vis_utils
from importlib import reload

reload(keras.utils.vis_utils)
from keras.utils.vis_utils import plot_model
from openpy_fxts.models.utils import _callbacks, _learning_curve, _values_preliminary
from openpy_fxts.models.utils import _values_preliminary, _values_preliminary_2D
from openpy_fxts.models.utils import _mdl_caracteristic, _process_values_preliminary

tkl = tf.keras.layers
tko = tf.keras.optimizers
tkm = tf.keras.models
tkloss = tf.keras.losses
tku = tf.keras.utils
tkr = tf.keras.regularizers


class Seq2Seq_LSTM_class(baseline_mdl):

    def __init__(self, config_data=None, config_fit=None, config_sim=None, config_arch=None):
        super().__init__(config_data, config_fit, config_sim, config_arch)
        self.name_model = 'Seq2Seq_LSTM'
        self.type_mdl = 'Seq2Seq'

    def building(self):
        base_model = Seq2Seq_LSTM_class(self.config_data, self.config_mdl, self.config_sim, self.config_arch)
        model = base_model._architecture_model(self.name_model, self.type_mdl)
        return model

    def training(self, filepath: str = None):
        base_model = Seq2Seq_LSTM_class(self.config_data, self.config_mdl, self.config_sim, self.config_arch)
        base_model._training_model(pre_processing_data, filepath, self.name_model, self.type_mdl)

    def prediction(self, model, filepath):
        base_model = Seq2Seq_LSTM_class(self.config_data, self.config_mdl, self.config_sim, self.config_arch)
        yhat = base_model._prediction_model(pre_processing_data, model, self.type_mdl, filepath)
        return yhat


class Seq2Seq_LSTM2_class(baseline_mdl):

    def __init__(self, config_data=None, config_fit=None, config_sim=None, config_arch=None):
        super().__init__(config_data, config_fit, config_sim, config_arch)
        self.name_model = 'Seq2Seq_LSTM2'
        self.type_mdl = 'Seq2Seq'

    def building(self):
        base_model = Seq2Seq_LSTM2_class(self.config_data, self.config_mdl, self.config_sim, self.config_arch)
        model = base_model._architecture_model(self.name_model, self.type_mdl)
        return model

    def training(self, filepath: str = None):
        base_model = Seq2Seq_LSTM2_class(self.config_data, self.config_mdl, self.config_sim, self.config_arch)
        base_model._training_model(pre_processing_data, filepath, self.name_model, self.type_mdl)

    def prediction(self, model, filepath):
        base_model = Seq2Seq_LSTM2_class(self.config_data, self.config_mdl, self.config_sim, self.config_arch)
        yhat = base_model._prediction_model(pre_processing_data, model, self.type_mdl, filepath)
        return yhat


class Seq2Seq_LSTM_Batch_Drop_class(baseline_mdl):

    def __init__(self, config_data=None, config_fit=None, config_sim=None, config_arch=None):
        super().__init__(config_data, config_fit, config_sim, config_arch)
        self.name_model = 'Seq2Seq_LSTM_Batch_Drop'
        self.type_mdl = 'Seq2Seq'

    def building(self):
        base_model = Seq2Seq_LSTM_Batch_Drop_class(self.config_data, self.config_mdl, self.config_sim, self.config_arch)
        model = base_model._architecture_model(self.name_model, self.type_mdl)
        return model

    def training(self, filepath: str = None):
        base_model = Seq2Seq_LSTM_Batch_Drop_class(self.config_data, self.config_mdl, self.config_sim, self.config_arch)
        base_model._training_model(pre_processing_data, filepath, self.name_model, self.type_mdl)

    def prediction(self, model, filepath):
        base_model = Seq2Seq_LSTM_Batch_Drop_class(self.config_data, self.config_mdl, self.config_sim, self.config_arch)
        yhat = base_model._prediction_model(pre_processing_data, model, self.type_mdl, filepath)
        return yhat


class Seq2Seq_BiLSTM_class(baseline_mdl):

    def __init__(self, config_data=None, config_fit=None, config_sim=None, config_arch=None):
        super().__init__(config_data, config_fit, config_sim, config_arch)
        self.name_model = 'Seq2Seq_BiLSTM'
        self.type_mdl = 'Seq2Seq'

    def building(self):
        base_model = Seq2Seq_BiLSTM_class(self.config_data, self.config_mdl, self.config_sim, self.config_arch)
        model = base_model._architecture_model(self.name_model, self.type_mdl)
        return model

    def training(self, filepath: str = None):
        base_model = Seq2Seq_BiLSTM_class(self.config_data, self.config_mdl, self.config_sim, self.config_arch)
        base_model._training_model(pre_processing_data, filepath, self.name_model, self.type_mdl)

    def prediction(self, model, filepath):
        base_model = Seq2Seq_BiLSTM_class(self.config_data, self.config_mdl, self.config_sim, self.config_arch)
        yhat = base_model._prediction_model(pre_processing_data, model, self.type_mdl, filepath)
        return yhat

class Seq2Seq_BiLSTM_class(baseline_mdl):

    def __init__(self, config_data=None, config_fit=None, config_sim=None, config_arch=None):
        super().__init__(config_data, config_fit, config_sim, config_arch)
        self.name_model = 'Seq2Seq_BiLSTM'
        self.type_mdl = 'Seq2Seq'

    def building(self):
        base_model = Seq2Seq_BiLSTM_class(self.config_data, self.config_mdl, self.config_sim, self.config_arch)
        model = base_model._architecture_model(self.name_model, self.type_mdl)
        return model

    def training(self, filepath: str = None):
        base_model = Seq2Seq_BiLSTM_class(self.config_data, self.config_mdl, self.config_sim, self.config_arch)
        base_model._training_model(pre_processing_data, filepath, self.name_model, self.type_mdl)

    def prediction(self, model, filepath):
        base_model = Seq2Seq_BiLSTM_class(self.config_data, self.config_mdl, self.config_sim, self.config_arch)
        yhat = base_model._prediction_model(pre_processing_data, model, self.type_mdl, filepath)
        return yhat


class Seq2Seq_BiLSTM2_class(baseline_mdl):

    def __init__(self, config_data=None, config_fit=None, config_sim=None, config_arch=None):
        super().__init__(config_data, config_fit, config_sim, config_arch)
        self.name_model = 'Seq2Seq_BiLSTM2'
        self.type_mdl = 'Seq2Seq'

    def building(self):
        base_model = Seq2Seq_BiLSTM2_class(self.config_data, self.config_mdl, self.config_sim, self.config_arch)
        model = base_model._architecture_model(self.name_model, self.type_mdl)
        return model

    def training(self, filepath: str = None):
        base_model = Seq2Seq_BiLSTM2_class(self.config_data, self.config_mdl, self.config_sim, self.config_arch)
        base_model._training_model(pre_processing_data, filepath, self.name_model, self.type_mdl)

    def prediction(self, model, filepath):
        base_model = Seq2Seq_BiLSTM2_class(self.config_data, self.config_mdl, self.config_sim, self.config_arch)
        yhat = base_model._prediction_model(pre_processing_data, model, self.type_mdl, filepath)
        return yhat


class Seq2Seq_Conv1D_BiLSTM_class(baseline_mdl):

    def __init__(self, config_data=None, config_fit=None, config_sim=None, config_arch=None):
        super().__init__(config_data, config_fit, config_sim, config_arch)
        self.name_model = 'Seq2Seq_Conv1D_BiLSTM'
        self.type_mdl = 'Seq2Seq'

    def building(self):
        base_model = Seq2Seq_Conv1D_BiLSTM_class(self.config_data, self.config_mdl, self.config_sim, self.config_arch)
        model = base_model._architecture_model(self.name_model, self.type_mdl)
        return model

    def training(self, filepath: str = None):
        base_model = Seq2Seq_Conv1D_BiLSTM_class(self.config_data, self.config_mdl, self.config_sim, self.config_arch)
        base_model._training_model(pre_processing_data, filepath, self.name_model, self.type_mdl)

    def prediction(self, model, filepath):
        base_model = Seq2Seq_Conv1D_BiLSTM_class(self.config_data, self.config_mdl, self.config_sim, self.config_arch)
        yhat = base_model._prediction_model(pre_processing_data, model, self.type_mdl, filepath)
        return yhat


class Seq2Seq_Multi_Head_Conv1D_BiLSTM_class(baseline_mdl):

    def __init__(self, config_data=None, config_fit=None, config_sim=None, config_arch=None):
        super().__init__(config_data, config_fit, config_sim, config_arch)
        self.name_model = 'Seq2Seq_Multi_Head_Conv1D_BiLSTM'
        self.type_mdl = 'Seq2Seq'

    def building(self):
        base_model = Seq2Seq_Multi_Head_Conv1D_BiLSTM_class(self.config_data, self.config_mdl, self.config_sim, self.config_arch)
        model = base_model._architecture_model(self.name_model, self.type_mdl)
        return model

    def training(self, filepath: str = None):
        base_model = Seq2Seq_Multi_Head_Conv1D_BiLSTM_class(self.config_data, self.config_mdl, self.config_sim, self.config_arch)
        base_model._training_model(pre_processing_data, filepath, self.name_model, self.type_mdl)

    def prediction(self, model, filepath):
        base_model = Seq2Seq_Multi_Head_Conv1D_BiLSTM_class(self.config_data, self.config_mdl, self.config_sim, self.config_arch)
        yhat = base_model._prediction_model(pre_processing_data, model, self.type_mdl, filepath)
        return yhat


class Seq2Seq_BiLSTM_with_Attention_class(baseline_mdl):

    def __init__(self, config_data=None, config_fit=None, config_sim=None, config_arch=None):
        super().__init__(config_data, config_fit, config_sim, config_arch)
        self.name_model = 'Seq2Seq_BiLSTM_with_Attention'
        self.type_mdl = 'Seq2Seq'

    def building(self):
        base_model = Seq2Seq_BiLSTM_with_Attention_class(self.config_data, self.config_mdl, self.config_sim, self.config_arch)
        model = base_model._architecture_model(self.name_model, self.type_mdl)
        return model

    def training(self, filepath: str = None):
        base_model = Seq2Seq_BiLSTM_with_Attention_class(self.config_data, self.config_mdl, self.config_sim, self.config_arch)
        base_model._training_model(pre_processing_data, filepath, self.name_model, self.type_mdl)

    def prediction(self, model, filepath):
        base_model = Seq2Seq_BiLSTM_with_Attention_class(self.config_data, self.config_mdl, self.config_sim, self.config_arch)
        yhat = base_model._prediction_model(pre_processing_data, model, self.type_mdl, filepath)
        return yhat


class Seq2Seq_LSTM_with_Luong_Attention_class(baseline_mdl):

    def __init__(self, config_data=None, config_fit=None, config_sim=None, config_arch=None):
        super().__init__(config_data, config_fit, config_sim, config_arch)
        self.name_model = 'Seq2Seq_LSTM_with_Luong_Attention'
        self.type_mdl = 'Seq2Seq'

    def building(self):
        base_model = Seq2Seq_LSTM_with_Luong_Attention_class(self.config_data, self.config_mdl, self.config_sim, self.config_arch)
        model = base_model._architecture_model(self.name_model, self.type_mdl)
        return model

    def training(self, filepath: str = None):
        base_model = Seq2Seq_LSTM_with_Luong_Attention_class(self.config_data, self.config_mdl, self.config_sim, self.config_arch)
        base_model._training_model(pre_processing_data, filepath, self.name_model, self.type_mdl)

    def prediction(self, model, filepath):
        base_model = Seq2Seq_LSTM_with_Luong_Attention_class(self.config_data, self.config_mdl, self.config_sim, self.config_arch)
        yhat = base_model._prediction_model(pre_processing_data, model, self.type_mdl, filepath)


class Seq2Seq_LSTM_with_Luong_Attention:

    def __init__(self, config_data=None, config_mdl=None, config_sim=None):
        self.config_data = config_data
        self.n_past = config_data['n_past']
        self.n_future = config_data['n_future']
        self.n_inp_ft = config_data['n_inp_ft']
        self.n_out_ft = config_data['n_out_ft']
        # Parameters for model
        self.config_mdl = config_mdl
        self.optimizer = config_mdl['optimizer']
        self.loss = config_mdl['loss']
        self.metrics = config_mdl['metrics']
        self.batch_size = config_mdl['batch_size']  # Batch size for training.
        self.epochs = config_mdl['epochs']  # Number of epochs to train for.
        self.units = config_mdl['units']  # no of lstm units
        self.dropout = config_mdl['dropout']
        # Parameters for simulation
        self.config_sim = config_sim
        self.verbose = config_sim['verbose']
        self.patience = config_sim['patience']
        self.plot_history = config_sim['plt_history']
        self.preliminary = config_sim['preliminary']
        self.name_model = 'Seq2Seq_LSTM_with_Luong_Attention'

    def build_model(self):
        input_train = tkl.Input(shape=(self.n_past, self.n_inp_ft))
        output_train = tkl.Input(shape=(self.n_future, self.n_out_ft))

        encoder_stack_h, encoder_last_h, encoder_last_c = tkl.LSTM(
            self.units,
            activation='elu',
            dropout=0.2,
            recurrent_dropout=0.2,
            return_state=True,
            return_sequences=True,
            kernel_regularizer=tkr.l2(0.01),
            recurrent_regularizer=tkr.l2(0.01),
            bias_regularizer=tkr.l2(0.01)
        )(input_train)
        encoder_last_h = tkl.BatchNormalization(momentum=0.6)(encoder_last_h)
        encoder_last_c = tkl.BatchNormalization(momentum=0.6)(encoder_last_c)
        # Repeat Vector
        decoder_input = tkl.RepeatVector(output_train.shape[1])(encoder_last_h)
        decoder_stack_h = tkl.LSTM(
            self.units,
            activation='elu',
            dropout=0.2,
            recurrent_dropout=0.2,
            return_state=False,
            return_sequences=True,
            kernel_regularizer=tkr.l2(0.01),
            recurrent_regularizer=tkr.l2(0.01),
            bias_regularizer=tkr.l2(0.01)
        )(decoder_input, initial_state=[encoder_last_h, encoder_last_c])
        attention = tkl.dot([decoder_stack_h, encoder_stack_h], axes=[2, 2])
        attention = tkl.Activation('softmax')(attention)
        context = tkl.dot([attention, encoder_stack_h], axes=[2, 1])
        context = tkl.BatchNormalization(momentum=0.6)(context)
        decoder_combined_context = tkl.concatenate([context, decoder_stack_h])
        out = tkl.TimeDistributed(tkl.Dense(output_train.shape[2]))(decoder_combined_context)
        built_model = tkm.Model(inputs=input_train, outputs=out, name='Seq2Seq_LSTM_with_Attention')
        return built_model

    def train_model(
            self,
            filepath: str = None
    ):
        data = pre_processing_data(self.config_data, train=True, valid=True)
        pre_processed = data.transformer_data()
        model = Seq2Seq_LSTM_with_Luong_Attention(self.config_data, self.config_mdl).build_model()
        model.compile(
            optimizer=self.optimizer,
            loss=self.loss,
            metrics=self.metrics
        )
        _mdl_caracteristic(model, self.config_sim, filepath)
        # Training
        history = model.fit(
            pre_processed['train']['X'],
            pre_processed['train']['y'],
            epochs=self.epochs,
            validation_data=(
                pre_processed['valid']['X'],
                pre_processed['valid']['y']
            ),
            batch_size=self.batch_size,
            verbose=self.verbose,
            callbacks=_callbacks(
                filepath,
                weights=True,
                verbose=self.verbose,
                patience=self.patience
            )
        )
        if self.plot_history:
            _learning_curve(history, self.name_model, filepath, self.config_sim['time_init'])
        if self.preliminary:
            data = pre_processing_data(self.config_data, test=True)
            dict_test = data.transformer_data()
            yhat = _process_values_preliminary(
                model,
                dict_test,
                self.config_data,
                self.config_sim,
                self.name_model
            ).get_values()
        return model

    def prediction(
            self,
            model
    ):
        data = pre_processing_data(self.config_data, test=True)
        dict_test = data.transformer_data()
        yhat = _process_values_preliminary(
            model,
            dict_test,
            self.config_data,
            self.config_sim,
            self.name_model
        ).get_values()
        return yhat


class Seq2Seq_ConvLSTM2D:

    def __init__(self, config_data=None, config_mdl=None, config_sim=None):
        self.config_data = config_data
        self.n_past = config_data['n_past']
        self.n_future = config_data['n_future']
        self.n_inp_ft = config_data['n_inp_ft']
        self.n_out_ft = config_data['n_out_ft']
        # Parameters for model
        self.config_mdl = config_mdl
        self.optimizer = config_mdl['optimizer']
        self.loss = config_mdl['loss']
        self.metrics = config_mdl['metrics']
        self.batch_size = config_mdl['batch_size']  # Batch size for training.
        self.epochs = config_mdl['epochs']  # Number of epochs to train for.
        self.units = config_mdl['units']  # no of lstm units
        self.dropout = config_mdl['dropout']
        # Parameters for simulation
        self.config_sim = config_sim
        self.verbose = config_sim['verbose']
        self.patience = config_sim['patience']
        self.plot_history = config_sim['plt_history']
        self.preliminary = config_sim['preliminary']
        self.name_model = 'Seq2Seq_ConvLSTM2D'

    def build_model(self):
        model = tkm.Sequential()
        model.add(tkl.BatchNormalization(name='batch_norm_0', input_shape=(self.n_past, self.n_inp_ft, 1, 1)))
        model.add(tkl.ConvLSTM2D(
            name='conv_lstm_1',
            filters=64,
            kernel_size=(10, 1),
            padding='same',
            return_sequences=True)
        )
        model.add(tkl.Dropout(0.2, name='dropout_1'))
        model.add(tkl.BatchNormalization(name='batch_norm_1'))
        model.add(tkl.ConvLSTM2D(
            name='conv_lstm_2',
            filters=64,
            kernel_size=(5, 1),
            padding='same',
            return_sequences=False)
        )
        model.add(tkl.Dropout(0.1, name='dropout_2'))
        model.add(tkl.BatchNormalization(name='batch_norm_2'))
        model.add(tkl.Flatten())
        # Repeat Vector
        model.add(tkl.RepeatVector(self.n_future))
        #
        if (self.n_inp_ft - self.n_out_ft) == 0:
            aux = 1
        else:
            aux = self.n_inp_ft - self.n_out_ft
        model.add(tkl.Reshape((self.n_future, self.n_out_ft, aux, 64)))
        model.add(tkl.ConvLSTM2D(
            name='conv_lstm_3',
            filters=64,
            kernel_size=(10, 1),
            padding='same',
            return_sequences=True)
        )
        model.add(tkl.Dropout(0.1, name='dropout_3'))
        model.add(tkl.BatchNormalization(name='batch_norm_3'))
        model.add(tkl.ConvLSTM2D(
            name='conv_lstm_4',
            filters=64,
            kernel_size=(5, 1),
            padding='same',
            return_sequences=True)
        )
        model.add(tkl.TimeDistributed(tkl.Dense(units=1, name='dense_1', activation='relu')))
        # model.add(Dense(units=1, name = 'dense_2'))
        return model

    def train_model(
            self,
            filepath: str = None
    ):
        data = pre_processing_data(self.config_data, train=True, valid=True)
        pre_processed = data.transformer_data()
        model = Seq2Seq_ConvLSTM2D(self.config_data, self.config_mdl).build_model()
        model.compile(
            optimizer=self.optimizer,
            loss=self.loss,
            metrics=self.metrics
        )
        _mdl_caracteristic(model, self.config_sim, filepath)
        # Training
        X_train = pre_processed['train']['X']
        y_train = pre_processed['train']['y']
        X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], X_train.shape[2], 1, 1)
        y_train = y_train.reshape(y_train.shape[0], y_train.shape[1], y_train.shape[2], 1, 1)

        X_valid = pre_processed['valid']['X']
        y_valid = pre_processed['valid']['y']
        X_valid = X_valid.reshape(X_valid.shape[0], X_valid.shape[1], X_valid.shape[2], 1, 1)
        y_valid = y_valid.reshape(y_valid.shape[0], y_valid.shape[1], y_valid.shape[2], 1, 1)

        history = model.fit(
            X_train,
            y_train,
            epochs=self.epochs,
            validation_data=(
                X_valid,
                y_valid
            ),
            batch_size=self.batch_size,
            verbose=self.verbose,
            callbacks=_callbacks(filepath, weights=True)
        )
        if self.config_data['plt_history']:
            _learning_curve(history, self.name_model, filepath, self.config_data['time_init'])
        if self.config_data['preliminary']:
            data = pre_processing_data(self.config_data, test=True)
            dict_test = data.transformer_data()
            _values_preliminary_2D(model, dict_test, self.config_data)
        return model

    def prediction(
            self,
            model
    ):
        data = pre_processing_data(self.config_data, test=True)
        dict_test = data.transformer_data()
        yhat = _values_preliminary_2D(model, dict_test, self.config_data)
        return yhat
