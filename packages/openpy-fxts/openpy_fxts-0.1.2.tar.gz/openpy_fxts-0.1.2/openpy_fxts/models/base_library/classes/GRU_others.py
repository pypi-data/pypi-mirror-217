from openpy_fxts.base_tf import tkm, tkl


class gru_dense(tkm.Model):

    def __init__(
            self,
            n_future=None,
            n_out_ft=None,
            config=None
    ):
        super(gru_dense, self).__init__()
        if config is None:
            config = {
                'gru1': {
                    'units': 256,
                    'activation': 'relu'
                },
                'gru2': {
                    'units': 256,
                    'activation': 'relu'
                },
                'dropout': 0.3,
                'dense': {
                    'activation': 'linear'
                }
            }

        self.gru1 = tkl.GRU(
            units=config['gru1']['units'],
            return_sequences=True
        )
        self.drop1 = tkl.Dropout(config['dropout'])
        self.gru2 = tkl.GRU(
            units=config['gru2']['units'],
            activation=config['gru2']['activation']
        )
        self.drop2 = tkl.Dropout(config['dropout'])
        self.dense1 = tkl.Dense(
            n_future * n_out_ft,
            activation=config['dense']['activation']
        )
        self.dense2 = tkl.Reshape((n_future, n_out_ft))

    def call(self, inputs, training=True, **kwargs):
        x = self.gru1(inputs)
        x = self.drop1(x)
        x = self.gru2(inputs)
        x = self.drop2(x)
        x = self.dense1(x)
        x = self.dense2(x)
        return x
