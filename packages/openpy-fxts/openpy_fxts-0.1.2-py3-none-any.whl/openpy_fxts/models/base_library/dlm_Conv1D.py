from openpy_fxts.preprocessing.prepare_data import pre_processing_data
from openpy_fxts.baseline_mdl import baseline_mdl


class Conv1D_Dense_class(baseline_mdl):

    def __init__(self, config_data=None, config_fit=None, config_sim=None, config_arch=None):
        super().__init__(config_data, config_fit, config_sim, config_arch)
        self.name_model = 'Conv1D_Dense'
        self.type_mdl = 'Conv1D'

    def building(self):
        base_model = Conv1D_Dense_class(self.config_data, self.config_mdl, self.config_sim, self.config_arch)
        model = base_model._architecture_model(self.name_model, self.type_mdl)
        return model

    def training(self, filepath: str = None):
        base_model = Conv1D_Dense_class(self.config_data, self.config_mdl, self.config_sim, self.config_arch)
        base_model._training_model(pre_processing_data, filepath, self.name_model, self.type_mdl)

    def prediction(self, model, filepath):
        base_model = Conv1D_Dense_class(self.config_data, self.config_mdl, self.config_sim, self.config_arch)
        yhat = base_model._prediction_model(pre_processing_data, model, self.type_mdl, filepath)
        return yhat


class Conv1D_LSTM_class(baseline_mdl):

    def __init__(self, config_data=None, config_fit=None, config_sim=None, config_arch=None):
        super().__init__(config_data, config_fit, config_sim, config_arch)
        self.name_model = 'Conv1D_LSTM'
        self.type_mdl = 'Conv1D'

    def building(self):
        base_model = Conv1D_LSTM_class(self.config_data, self.config_mdl, self.config_sim, self.config_arch)
        model = base_model._architecture_model(self.name_model, self.type_mdl)
        return model

    def training(self, filepath: str = None):
        base_model = Conv1D_LSTM_class(self.config_data, self.config_mdl, self.config_sim, self.config_arch)
        base_model._training_model(pre_processing_data, filepath, self.name_model, self.type_mdl)

    def prediction(self, model, filepath):
        base_model = Conv1D_LSTM_class(self.config_data, self.config_mdl, self.config_sim, self.config_arch)
        yhat = base_model._prediction_model(pre_processing_data, model, self.type_mdl, filepath)
        return yhat


class Conv1D_BiLSTM_class(baseline_mdl):

    def __init__(self, config_data=None, config_fit=None, config_sim=None, config_arch=None):
        super().__init__(config_data, config_fit, config_sim, config_arch)
        self.name_model = 'Conv1D_BiLSTM'
        self.type_mdl = 'Conv1D'

    def building(self):
        base_model = Conv1D_BiLSTM_class(self.config_data, self.config_mdl, self.config_sim, self.config_arch)
        model = base_model._architecture_model(self.name_model, self.type_mdl)
        return model

    def training(self, filepath: str = None):
        base_model = Conv1D_BiLSTM_class(self.config_data, self.config_mdl, self.config_sim, self.config_arch)
        base_model._training_model(pre_processing_data, filepath, self.name_model, self.type_mdl)

    def prediction(self, model, filepath):
        base_model = Conv1D_BiLSTM_class(self.config_data, self.config_mdl, self.config_sim, self.config_arch)
        yhat = base_model._prediction_model(pre_processing_data, model, self.type_mdl, filepath)
        return yhat


class Conv1D_BiLSTM_Attention_class(baseline_mdl):

    def __init__(self, config_data=None, config_fit=None, config_sim=None, config_arch=None):
        super().__init__(config_data, config_fit, config_sim, config_arch)
        self.name_model = 'Conv1D_BiLSTM_Attention'
        self.type_mdl = 'Conv1D'

    def building(self):
        base_model = Conv1D_BiLSTM_Attention_class(self.config_data, self.config_mdl, self.config_sim, self.config_arch)
        model = base_model._architecture_model(self.name_model, self.type_mdl)
        return model

    def training(self, filepath: str = None):
        base_model = Conv1D_BiLSTM_Attention_class(self.config_data, self.config_mdl, self.config_sim, self.config_arch)
        base_model._training_model(pre_processing_data, filepath, self.name_model, self.type_mdl)

    def prediction(self, model, filepath):
        base_model = Conv1D_BiLSTM_Attention_class(self.config_data, self.config_mdl, self.config_sim, self.config_arch)
        yhat = base_model._prediction_model(pre_processing_data, model, self.type_mdl, filepath)
        return yhat

