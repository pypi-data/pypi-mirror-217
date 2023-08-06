import tensorflow as tf
# models -> LSTM
from .base_library.classes.LSTM_others import lstm2_dense
# models -> GRU
from .base_library.classes.GRU_others import gru_dense
# models -> Conv1D
from .base_library.classes.Conv1D_others import conv1D_dense
from .base_library.classes.Conv1D_others import conv1D_lstm_dense
from .base_library.classes.Conv1D_others import conv1D_bilstm_dense
from .base_library.classes.Conv1D_others import conv1D_bilstm_attention_dense
# models -> BiLSTM
from .base_library.classes.BiLSTM_others import bilstm_dense
from .base_library.classes.BiLSTM_others import bilstm_conv1d_dense
from .base_library.classes.BiLSTM_others import bilstm_bahdanau_attention_conv1d_dense
from .base_library.classes.BiLSTM_others import bilstm_multihead_attention_conv1d_dense
from .base_library.classes.BiLSTM_others import bilstm_luong_attention_conv1d_dense
# models -> Others
from .base_library.classes.Others import tcn_bilstm
from .base_library.classes.Others import time2vec_bilstm
# models -> Seq2Seq
from .base_library.classes.Seq2Seq.Seq2Seq_hybrid import seq2seq_lstm
from .base_library.classes.Seq2Seq.Seq2Seq_hybrid import seq2seq_lstm2
from .base_library.classes.Seq2Seq.Seq2Seq_hybrid import seq2seq_lstm_batch_drop
from .base_library.classes.Seq2Seq.Seq2Seq_hybrid import seq2seq_bilstm
from .base_library.classes.Seq2Seq.Seq2Seq_hybrid import seq2seq_bilstm2
from .base_library.classes.Seq2Seq.Seq2Seq_hybrid import seq2seq_conv1d_bilstm
from .base_library.classes.Seq2Seq.Seq2Seq_hybrid import seq2seq_multihead_conv1d_bilstm  # Function
from .base_library.classes.Seq2Seq.Seq2Seq_hybrid import seq2seq_bilstm_with_attention  # Function
from .base_library.classes.Seq2Seq.Seq2Seq_hybrid import seq2seq_lstm_with_loung_attention  # Function

tkl = tf.keras.layers
tkm = tf.keras.models


def get_architecture_of_model(
        name_mdl,
        type_mdl,
        n_past,
        n_future,
        n_inp_ft,
        n_out_ft,
        config_arch
):
    input_layer = tkl.Input(shape=(n_past, n_inp_ft))
    if type_mdl == 'LSTM':
        # models -> LSTM
        if name_mdl == 'LSTM2_Dense':
            x = lstm2_dense(n_future, n_out_ft, config_arch)(input_layer)
            model = tkm.Model(inputs=input_layer, outputs=x)
            return model
    if type_mdl == 'GRU':
        # models -> GRU
        if name_mdl == 'GRU_Dense':
            x = gru_dense(n_future, n_out_ft, config_arch)(input_layer)
            model = tkm.Model(inputs=input_layer, outputs=x)
            return model
    if type_mdl == 'Conv1D':
        # models -> Conv1D
        if name_mdl == 'Conv1D_Dense':
            x = conv1D_dense(n_future, n_out_ft, config_arch)(input_layer)
            model = tkm.Model(inputs=input_layer, outputs=x)
            return model
        if name_mdl == 'Conv1D_LSTM':
            x = conv1D_lstm_dense(n_future, n_out_ft, config_arch)(input_layer)
            model = tkm.Model(inputs=input_layer, outputs=x)
            return model
        if name_mdl == 'Conv1D_BiLSTM':
            x = conv1D_bilstm_dense(n_future, n_out_ft, config_arch)(input_layer)
            model = tkm.Model(inputs=input_layer, outputs=x)
            return model
        if name_mdl == 'Conv1D_BiLSTM_Attention':
            x = conv1D_bilstm_attention_dense(n_future, n_out_ft, config_arch)(input_layer)
            model = tkm.Model(inputs=[input_layer], outputs=x)
            return model
    if type_mdl == 'BiLSTM':
        # models -> BiLSTM
        if name_mdl == 'BiLSTM_Dense':
            x = bilstm_dense(n_future, n_out_ft, config_arch)(input_layer)
            model = tkm.Model(inputs=[input_layer], outputs=x)
            return model
        if name_mdl == 'BiLSTM_Conv1D':
            x = bilstm_conv1d_dense(n_future, n_out_ft, config_arch)(input_layer)
            model = tkm.Model(inputs=[input_layer], outputs=x)
            return model
        if name_mdl == 'BiLSTM_Bahdanau_Attention_Conv1D':
            x = bilstm_bahdanau_attention_conv1d_dense(n_future, n_out_ft, config_arch)(input_layer)
            model = tkm.Model(inputs=input_layer, outputs=x)
            return model
        if name_mdl == 'BiLSTM_MultiHeadAttention_Conv1D':
            x = bilstm_multihead_attention_conv1d_dense(n_future, n_out_ft, config_arch)(input_layer)
            model = tkm.Model(inputs=input_layer, outputs=x)
            return model
        if name_mdl == 'BiLSTM_Luong_Attention_Conv1D':
            x = bilstm_luong_attention_conv1d_dense(n_future, n_out_ft, config_arch)(input_layer)
            model = tkm.Model(inputs=input_layer, outputs=x)
            return model
    if type_mdl == 'Others':
        # models -> Others
        if name_mdl == 'TCN_BiLSTM':
            x = tcn_bilstm(n_future, n_out_ft, config_arch)(input_layer)
            model = tkm.Model(inputs=input_layer, outputs=x)
            return model
        if name_mdl == 'Time2Vec_BiLSTM':
            x = time2vec_bilstm(n_future, n_out_ft, config_arch)(input_layer)
            model = tkm.Model(inputs=input_layer, outputs=x)
            return model
    if type_mdl == 'Seq2Seq':
        if name_mdl == 'Seq2Seq_LSTM':
            x = seq2seq_lstm(n_future, n_out_ft, config_arch)(input_layer)
            model = tkm.Model(inputs=input_layer, outputs=x)
            return model
        if name_mdl == 'Seq2Seq_LSTM2':
            x = seq2seq_lstm2(n_future, n_out_ft, config_arch)(input_layer)
            model = tkm.Model(inputs=input_layer, outputs=x)
            return model
        if name_mdl == 'Seq2Seq_LSTM_Batch_Drop':
            x = seq2seq_lstm_batch_drop(n_future, n_out_ft, config_arch)(input_layer)
            model = tkm.Model(inputs=input_layer, outputs=x)
            return model
        if name_mdl == 'Seq2Seq_BiLSTM':
            x = seq2seq_bilstm(n_future, n_out_ft, config_arch)(input_layer)
            model = tkm.Model(inputs=input_layer, outputs=x)
            return model
        if name_mdl == 'Seq2Seq_BiLSTM2':
            x = seq2seq_bilstm2(n_future, n_out_ft, config_arch)(input_layer)
            model = tkm.Model(inputs=input_layer, outputs=x)
            return model
        if name_mdl == 'Seq2Seq_Conv1D_BiLSTM':
            x = seq2seq_conv1d_bilstm(n_future, n_out_ft, config_arch)(input_layer)
            model = tkm.Model(inputs=input_layer, outputs=x)
            return model
        if name_mdl == 'Seq2Seq_Multi_Head_Conv1D_BiLSTM':
            model = seq2seq_multihead_conv1d_bilstm(n_past, n_inp_ft, n_future, n_out_ft)
            return model
        if name_mdl == 'Seq2Seq_BiLSTM_with_Attention':
            model = seq2seq_bilstm_with_attention(n_past, n_inp_ft, n_future, n_out_ft)
            return model
        if name_mdl == 'Seq2Seq_LSTM_with_Luong_Attention':
            model = seq2seq_lstm_with_loung_attention(n_past, n_inp_ft, n_future, n_out_ft)
            return model













