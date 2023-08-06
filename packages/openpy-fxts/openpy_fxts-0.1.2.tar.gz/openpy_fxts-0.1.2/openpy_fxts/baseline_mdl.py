import tensorflow as tf

from openpy_fxts.models.utils import _mdl_caracteristic
from openpy_fxts.models.utils import _callbacks
from openpy_fxts.models.utils import _learning_curve
from openpy_fxts.models.utils import _process_values_preliminary

from openpy_fxts.models.get_architecture import get_architecture_of_model

tkm = tf.keras.models
tkl = tf.keras.layers
tkloss = tf.keras.losses
tko = tf.keras.optimizers
tku = tf.keras.utils


class baseline_mdl:

    def __init__(
            self,
            config_data=None,
            config_fit=None,
            config_sim=None,
            config_arch=None
    ):
        # Parameters for dataset
        self.config_data = config_data
        self.n_past = config_data['n_past']
        self.n_future = config_data['n_future']
        self.n_inp_ft = config_data['n_inp_ft']
        self.n_out_ft = config_data['n_out_ft']
        # Parameters for model
        self.config_mdl = config_fit
        self.optimizer = config_fit['optimizer']
        self.loss = config_fit['loss']
        self.metrics = config_fit['metrics']
        self.batch_size = config_fit['batch_size']  # Batch size for training.
        self.epochs = config_fit['epochs']  # Number of epochs to train for.
        # Parameters for simulation
        self.config_sim = config_sim
        self.verbose = config_sim['verbose']
        self.patience = config_sim['patience']
        self.plot_history = config_sim['plt_history']
        self.preliminary = config_sim['preliminary']
        self.config_arch = config_arch

    def _architecture_model(self, name_mdl, type_mdl):
        model = get_architecture_of_model(
            name_mdl=name_mdl,
            type_mdl=type_mdl,
            n_past=self.n_past,
            n_future=self.n_future,
            n_inp_ft=self.n_inp_ft,
            n_out_ft=self.n_out_ft,
            config_arch=self.config_arch
        )
        return model

    def _training_model(self, data_class, filepath, name_mdl, type_mdl):
        data = data_class(self.config_data, train=True, valid=True)
        pre_processed = data.transformer_data()
        aux = baseline_mdl(self.config_data, self.config_mdl, self.config_sim, self.config_arch)
        model = aux._architecture_model(name_mdl, type_mdl)
        model.compile(optimizer=self.optimizer, loss=self.loss, metrics=self.metrics)
        _mdl_caracteristic(model, self.config_sim, filepath)
        # Training
        history = model.fit(
            x=pre_processed['train']['X'],
            y=pre_processed['train']['y'],
            validation_data=(
                pre_processed['valid']['X'],
                pre_processed['valid']['y']
            ),
            batch_size=self.batch_size,
            epochs=self.epochs,
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
            data = data_class(self.config_data, test=True)
            dict_test = data.transformer_data()
            _process_values_preliminary(
                model,
                dict_test,
                self.config_data,
                self.config_sim,
                self.name_model
            ).get_values(name_mdl, filepath)

    def _prediction_model(
            self,
            data_class,
            model_train,
            type_mdl,
            filepath
    ):
        data = data_class(self.config_data, test=True)
        dict_test = data.transformer_data()
        yhat = _process_values_preliminary(
            model_train,
            dict_test,
            self.config_data,
            self.config_sim,
            self.name_model
        ).get_values(type_mdl, filepath)
        return yhat