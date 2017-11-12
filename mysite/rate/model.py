import json
import copy
import tensorflow
from os import path
from keras.preprocessing import sequence
from keras.models import load_model, model_from_json, Sequential
from keras.layers import Embedding, Dropout, Conv1D, MaxPooling1D, LSTM, Dense, Activation, BatchNormalization
from typing import List


class KerasModel:
    MODEL = None
    TF_GRAPH = None
    MAXLEN = 0
    BATCH_SIZE = 0

    def __init__(self, model_name):
        dirname = path.join(path.dirname(__file__), 'models')
        if not KerasModel.MODEL or not KerasModel.TF_GRAPH:
            with open(path.join(dirname, model_name+"_configs.json")) as file:
                configs = json.load(file)
            if path.isfile(path.join(dirname, model_name+".hdf5")):
                KerasModel.MODEL = load_model(path.join(dirname, model_name+".hdf5"))
            elif path.isfile(path.join(dirname, model_name+"_arch.json")):
                with open(path.join(dirname, model_name+"_arch.json")) as file:
                    KerasModel.MODEL = model_from_json(file)
                KerasModel.MODEL.load_weights(path.join(dirname, model_name+"_weights.h5"))
            else:
                model = Sequential()
                model.add(Embedding(configs["max_features"], configs["embedding_size"], input_length=configs["maxlen"]))
                model.add(Dropout(0.25))
                model.add(Conv1D(filters=configs["filters"],
                                 kernel_size=configs["kernel_size"],
                                 activation=configs["conv_activation"]))
                model.add(MaxPooling1D(pool_size=configs["pool_size"]))
                model.add(BatchNormalization())
                model.add(Dropout(0.3))
                model.add(LSTM(128, return_sequences=True))
                model.add(BatchNormalization())
                model.add(Dropout(0.3))
                model.add(LSTM(64))
                model.add(BatchNormalization())
                model.add(Dense(1))
                model.add(Activation(configs["activation"]))
                model.load_weights(path.join(dirname, model_name+"_weights.h5"))
                KerasModel.MODEL = model

            KerasModel.TF_GRAPH = tensorflow.get_default_graph()
            KerasModel.MAXLEN = configs["maxlen"]
            KerasModel.BATCH_SIZE = configs["batch_size"]
        self._model = copy.copy(KerasModel.MODEL)
        self._maxlen = KerasModel.MAXLEN
        self._batch_size = KerasModel.BATCH_SIZE

    def predict(self, articles: List[List[int]]) -> List[float]:
        model = self._model
        truncated_articles = []
        for article in articles:
            truncated_articles.append(list(word for word in article if 20 < word < 41000))
        articles = sequence.pad_sequences(truncated_articles, maxlen=self._maxlen)
        with KerasModel.TF_GRAPH.as_default():
            result = model.predict(articles, batch_size=self._batch_size)
        result = list(score**0.5 for score in result)
        return result
