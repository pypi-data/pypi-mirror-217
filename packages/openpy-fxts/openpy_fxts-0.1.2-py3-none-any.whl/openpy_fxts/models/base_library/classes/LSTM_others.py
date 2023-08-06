from openpy_fxts.base_tf import tkm, tkl


class lstm2_dense(tkm.Model):

    def __init__(
            self,
            n_future=None,
            n_out_ft=None,
            config=None
    ):
        super(lstm2_dense, self).__init__()
        if config is None:
            config = {
                'lstm': {
                    'units': 256,
                    'activation': 'relu'
                },
                'dropout': 0.3,
                'dense': {
                    'activation': 'linear'
                }
            }

        self.lstm1 = tkl.LSTM(
            units=config['lstm']['units'],
            return_sequences=True
        )
        self.drop1 = tkl.Dropout(config['dropout'])
        self.lstm2 = tkl.LSTM(
            units=config['lstm']['units'],
            activation=config['lstm']['activation']
        )
        self.drop2 = tkl.Dropout(config['dropout'])
        self.dense1 = tkl.Dense(
            n_future * n_out_ft,
            activation=config['dense']['activation']
        )
        self.dense2 = tkl.Reshape((n_future, n_out_ft))

    def call(self, inputs, training=True, **kwargs):
        x = self.lstm1(inputs)
        x = self.drop1(x)
        x = self.lstm2(inputs)
        x = self.drop2(x)
        x = self.dense1(x)
        x = self.dense2(x)
        return x
