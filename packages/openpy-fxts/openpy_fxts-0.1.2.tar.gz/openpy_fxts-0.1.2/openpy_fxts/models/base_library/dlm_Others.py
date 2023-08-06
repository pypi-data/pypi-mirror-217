from openpy_fxts.baseline_mdl import baseline_mdl
from openpy_fxts.preprocessing.prepare_data import pre_processing_data

class TCN_BiLSTM_class(baseline_mdl):

    def __init__(self, config_data=None, config_fit=None, config_sim=None, config_arch=None):
        super().__init__(config_data, config_fit, config_sim, config_arch)
        self.name_model = 'TCN_BiLSTM'
        self.type_mdl = 'Others'

    def building(self):
        base_model = TCN_BiLSTM_class(self.config_data, self.config_mdl, self.config_sim, self.config_arch)
        model = base_model._architecture_model(self.name_model, self.type_mdl)
        return model

    def training(self, filepath: str = None):
        base_model = TCN_BiLSTM_class(self.config_data, self.config_mdl, self.config_sim, self.config_arch)
        base_model._training_model(pre_processing_data, filepath, self.name_model, self.type_mdl)

    def prediction(self, model, filepath):
        base_model = TCN_BiLSTM_class(self.config_data, self.config_mdl, self.config_sim, self.config_arch)
        yhat = base_model._prediction_model(pre_processing_data, model, self.type_mdl, filepath)
        return yhat


class Time2Vec_BiLSTM_class(baseline_mdl):

    def __init__(self, config_data=None, config_fit=None, config_sim=None, config_arch=None):
        super().__init__(config_data, config_fit, config_sim, config_arch)
        self.name_model = 'Time2Vec_BiLSTM'
        self.type_mdl = 'Others'

    def building(self):
        base_model = Time2Vec_BiLSTM_class(self.config_data, self.config_mdl, self.config_sim, self.config_arch)
        model = base_model._architecture_model(self.name_model, self.type_mdl)
        return model

    def training(self, filepath: str = None):
        base_model = Time2Vec_BiLSTM_class(self.config_data, self.config_mdl, self.config_sim, self.config_arch)
        base_model._training_model(pre_processing_data, filepath, self.name_model, self.type_mdl)

    def prediction(self, model, filepath):
        base_model = Time2Vec_BiLSTM_class(self.config_data, self.config_mdl, self.config_sim, self.config_arch)
        yhat = base_model._prediction_model(pre_processing_data, model, self.type_mdl, filepath)
        return yhat


class Time2Vec_BiLSTM:

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
        self.name_model = 'Time2Vec_BiLSTM'

    def build_model(self):
        inp = tkl.Input(shape=(self.n_past, self.n_inp_ft))
        x = Time2Vec(self.units)(inp)
        x = tkl.Bidirectional(
            tkl.LSTM(
                (self.n_future * self.n_out_ft),
                activation='tanh',
                return_sequences=False
            )
        )(x)
        x = tkl.Dense((self.n_future * self.n_out_ft), activation='linear')(x)
        x = tkl.Reshape((self.n_future, self.n_out_ft))(x)
        model = tkm.Model(inp, x)
        return model

    def train_model(
            self,
            filepath
    ):
        data = pre_processing_data(self.config_data, train=True, valid=True)
        pre_processed = data.transformer_data()
        model = Time2Vec_BiLSTM(self.config_data, self.config_mdl, self.config_sim).build_model()
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
        yhat = _values_preliminary(model, dict_test, self.config_data)
        return yhat
