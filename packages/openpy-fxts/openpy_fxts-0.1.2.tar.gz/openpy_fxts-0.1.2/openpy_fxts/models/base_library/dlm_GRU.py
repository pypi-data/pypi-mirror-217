from openpy_fxts.baseline_mdl import baseline_mdl
from openpy_fxts.preprocessing.prepare_data import pre_processing_data


class GRU_Dense_class(baseline_mdl):

    def __init__(self, config_data=None, config_fit=None, config_sim=None, config_arch=None):
        super().__init__(config_data, config_fit, config_sim, config_arch)
        self.name_model = 'GRU_Dense'
        self.type_mdl = 'GRU'

    def building(self):
        base_model = GRU_Dense_class(self.config_data, self.config_mdl, self.config_sim, self.config_arch)
        model = base_model._architecture_model(self.name_model, self.type_mdl)
        return model

    def training(self, filepath: str = None):
        base_model = GRU_Dense_class(self.config_data, self.config_mdl, self.config_sim, self.config_arch)
        base_model._training_model(pre_processing_data, filepath, self.name_model, self.type_mdl)

    def prediction(self, model, filepath):
        base_model = GRU_Dense_class(self.config_data, self.config_mdl, self.config_sim, self.config_arch)
        yhat = base_model._prediction_model(pre_processing_data, model, self.type_mdl, filepath)
        return yhat