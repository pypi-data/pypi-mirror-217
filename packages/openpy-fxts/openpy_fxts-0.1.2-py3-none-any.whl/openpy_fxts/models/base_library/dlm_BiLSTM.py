from openpy_fxts.baseline_mdl import baseline_mdl
from openpy_fxts.preprocessing.prepare_data import pre_processing_data

from openpy_fxts.models.utils import _callbacks, _learning_curve
from openpy_fxts.models.utils import _values_preliminary, _values_preliminary_mdn
from openpy_fxts.models.utils import _mdl_caracteristic, _process_values_preliminary
from openpy_fxts.models.base_library.classes.Attention_class import SeqSelfAttention
from mdn import MDN, get_mixture_loss_func
import tensorflow as tf

tkm = tf.keras.models
tkl = tf.keras.layers
tkloss = tf.keras.losses
tko = tf.keras.optimizers
tku = tf.keras.utils
tkr = tf.keras.regularizers


class BiLSTM_Dense_class(baseline_mdl):

    def __init__(self, config_data=None, config_fit=None, config_sim=None, config_arch=None):
        super().__init__(config_data, config_fit, config_sim, config_arch)
        self.name_model = 'BiLSTM_Dense'
        self.type_mdl = 'BiLSTM'

    def building(self):
        base_model = BiLSTM_Dense_class(self.config_data, self.config_mdl, self.config_sim, self.config_arch)
        model = base_model._architecture_model(self.name_model, self.type_mdl)
        return model

    def training(self, filepath: str = None):
        base_model = BiLSTM_Dense_class(self.config_data, self.config_mdl, self.config_sim, self.config_arch)
        base_model._training_model(pre_processing_data, filepath, self.name_model, self.type_mdl)

    def prediction(self, model, filepath):
        base_model = BiLSTM_Dense_class(self.config_data, self.config_mdl, self.config_sim, self.config_arch)
        yhat = base_model._prediction_model(pre_processing_data, model, self.type_mdl, filepath)
        return yhat


class BiLSTM_Conv1D_class(baseline_mdl):

    def __init__(self, config_data=None, config_fit=None, config_sim=None, config_arch=None):
        super().__init__(config_data, config_fit, config_sim, config_arch)
        self.name_model = 'BiLSTM_Conv1D'
        self.type_mdl = 'BiLSTM'

    def building(self):
        base_model = BiLSTM_Conv1D_class(self.config_data, self.config_mdl, self.config_sim, self.config_arch)
        model = base_model._architecture_model(self.name_model, self.type_mdl)
        return model

    def training(self, filepath: str = None):
        base_model = BiLSTM_Conv1D_class(self.config_data, self.config_mdl, self.config_sim, self.config_arch)
        base_model._training_model(pre_processing_data, filepath, self.name_model, self.type_mdl)

    def prediction(self, model, filepath):
        base_model = BiLSTM_Conv1D_class(self.config_data, self.config_mdl, self.config_sim, self.config_arch)
        yhat = base_model._prediction_model(pre_processing_data, model, self.type_mdl, filepath)
        return yhat


class BiLSTM_Bahdanau_Attention_Conv1D_class(baseline_mdl):

    def __init__(self, config_data=None, config_fit=None, config_sim=None, config_arch=None):
        super().__init__(config_data, config_fit, config_sim, config_arch)
        self.name_model = 'BiLSTM_Bahdanau_Attention_Conv1D'
        self.type_mdl = 'BiLSTM'

    def building(self):
        base_model = BiLSTM_Bahdanau_Attention_Conv1D_class(
            self.config_data, self.config_mdl, self.config_sim, self.config_arch
        )
        model = base_model._architecture_model(self.name_model, self.type_mdl)
        return model

    def training(self, filepath: str = None):
        base_model = BiLSTM_Bahdanau_Attention_Conv1D_class(
            self.config_data, self.config_mdl, self.config_sim, self.config_arch
        )
        base_model._training_model(pre_processing_data, filepath, self.name_model, self.type_mdl)

    def prediction(self, model, filepath):
        base_model = BiLSTM_Bahdanau_Attention_Conv1D_class(
            self.config_data, self.config_mdl, self.config_sim, self.config_arch
        )
        yhat = base_model._prediction_model(pre_processing_data, model, self.type_mdl, filepath)
        return yhat


class BiLSTM_MultiHeadAttention_Conv1D_class(baseline_mdl):

    def __init__(self, config_data=None, config_fit=None, config_sim=None, config_arch=None):
        super().__init__(config_data, config_fit, config_sim, config_arch)
        self.name_model = 'BiLSTM_MultiHeadAttention_Conv1D'
        self.type_mdl = 'BiLSTM'

    def building(self):
        base_model = BiLSTM_MultiHeadAttention_Conv1D_class(
            self.config_data, self.config_mdl, self.config_sim, self.config_arch
        )
        model = base_model._architecture_model(self.name_model, self.type_mdl)
        return model

    def training(self, filepath: str = None):
        base_model = BiLSTM_MultiHeadAttention_Conv1D_class(
            self.config_data, self.config_mdl, self.config_sim, self.config_arch
        )
        base_model._training_model(pre_processing_data, filepath, self.name_model, self.type_mdl)

    def prediction(self, model, filepath):
        base_model = BiLSTM_MultiHeadAttention_Conv1D_class(
            self.config_data, self.config_mdl, self.config_sim, self.config_arch
        )
        yhat = base_model._prediction_model(pre_processing_data, model, self.type_mdl, filepath)
        return yhat


class BiLSTM_Luong_Attention_Conv1D_class(baseline_mdl):

    def __init__(self, config_data=None, config_fit=None, config_sim=None, config_arch=None):
        super().__init__(config_data, config_fit, config_sim, config_arch)
        self.name_model = 'BiLSTM_Luong_Attention_Conv1D'
        self.type_mdl = 'BiLSTM'

    def building(self):
        base_model = BiLSTM_Luong_Attention_Conv1D_class(
            self.config_data, self.config_mdl, self.config_sim, self.config_arch
        )
        model = base_model._architecture_model(self.name_model, self.type_mdl)
        return model

    def training(self, filepath: str = None):
        base_model = BiLSTM_Luong_Attention_Conv1D_class(
            self.config_data, self.config_mdl, self.config_sim, self.config_arch
        )
        base_model._training_model(pre_processing_data, filepath, self.name_model, self.type_mdl)

    def prediction(self, model, filepath):
        base_model = BiLSTM_Luong_Attention_Conv1D_class(
            self.config_data, self.config_mdl, self.config_sim, self.config_arch
        )
        yhat = base_model._prediction_model(pre_processing_data, model, self.type_mdl, filepath)
        return yhat

class BiLSTM_MDN:

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
        self.n_mixtures = 5
        self.name_model = 'BiLSTM_MDN'

    def build_model(self):

        inputs = tkl.Input(shape=(self.n_past, self.n_inp_ft))
        x = tkl.Bidirectional(
            tkl.LSTM(
                units=self.n_inp_ft,
                return_sequences=False,
                kernel_initializer='normal',
                activation='tanh'
            )
        )(inputs)  # , padding = 'same'
        dense = tkl.Dense(self.units, activation='tanh')(x)
        output = MDN(self.n_future * self.n_out_ft, self.n_mixtures)(dense)
        model = tkm.Model(inputs=[inputs], outputs=output)
        return model

    def train_model(
            self,
            filepath: str = None
    ):
        data = pre_processing_data(self.config_data, train=True, valid=True)
        pre_processed = data.transformer_data()
        model = BiLSTM_MDN(self.config_data, self.config_mdl, self.config_sim).build_model()
        # opt = tf.keras.optimizers.Adam(learning_rate=0.001, beta_1=0.9, beta_2=0.999, amsgrad=True)
        opt = tf.keras.optimizers.Adam(learning_rate=0.0001)
        model.compile(
            optimizer=self.optimizer,
            loss=get_mixture_loss_func(self.n_future * self.n_out_ft, self.n_mixtures),
            metrics=self.metrics
        )
        if self.config_data['view_summary']:
            model.summary()
        if self.config_data['plt_model']:
            if filepath is None:
                tku.plot_model(model, show_shapes=True)
            else:
                tku.plot_model(model, to_file=filepath, show_shapes=True, show_layer_names=True)

        # Training
        X_train = pre_processed['train']['X']
        y_train = pre_processed['train']['y']
        # X_train = X_train.reshape(X_train.shape[0], self.n_past * self.n_inp_ft)
        y_train = y_train.reshape(y_train.shape[0], self.n_future * self.n_out_ft)

        X_valid = pre_processed['valid']['X']
        y_valid = pre_processed['valid']['y']
        # X_valid = X_valid.reshape(X_valid.shape[0], self.n_past * self.n_inp_ft)
        y_valid = y_valid.reshape(y_valid.shape[0], self.n_future * self.n_out_ft)

        history = model.fit(
            X_train,
            y_train,
            epochs=self.epochs,
            validation_data=(
                X_valid,
                y_valid
            ),
            batch_size=self.batch_size,
            verbose=1,
            callbacks=_callbacks(filepath, weights=True)
        )
        if self.config_data['plt_history']:
            _learning_curve(history, self.name_model, filepath, self.config_data['time_init'])
        if self.config_data['preliminary']:
            data = pre_processing_data(self.config_data, test=True)
            dict_test = data.transformer_data()
            _values_preliminary_mdn(model, dict_test, self.config_data)
        return model

    def prediction(
            self,
            model
    ):
        data = pre_processing_data(self.config_data, test=True)
        dict_test = data.transformer_data()
        yhat = _values_preliminary_mdn(
            model,
            dict_test,
            self.config_data,
            output_dim=(self.n_future * self.n_out_ft),
            n_mixtures=self.n_mixtures
        )
        return yhat
