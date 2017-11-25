from keras.models import load_model
from keras.preprocessing import sequence
from multiprocessing.connection import Client, Listener
from os import path
from datetime import datetime


def main():
    print('loading models...')
    models = path.join(path.dirname(__file__), 'rate', 'models', '')
    print('loading fasttext...')
    fasttext = load_model(models + 'fasttext.hdf5')
    print('loading cnn_lstm...')
    cnn_lstm = load_model(models + 'cnn_lstm.hdf5')
    print('loading cnn_2lstm...')
    cnn_2lstm = load_model(models + 'cnn_2lstm.hdf5')

    print('start listening on localhost:6001')
    listener = Listener(address=('localhost', 6001))

    while True:
        articles = listener.accept().recv()
        st = datetime.now()
        print(st, 'received one object, type:', type(articles), ' len:', len(articles))
        print('start padding articles')
        articles = sequence.pad_sequences(articles, maxlen=1000)
        print('start predicting scores')
        ft_rst = list(score**0.5 for score in fasttext.predict(articles))
        cl_rst = list(score**0.5 for score in cnn_lstm.predict(articles))
        c2l_rst = list(score**0.5 for score in cnn_2lstm.predict(articles))
        result = {
            'fasttext': ft_rst,
            'cnn_lstm': cl_rst,
            'cnn_2lstm': c2l_rst
        }
        print('create socket on localhost:6000')
        client = Client(address=('localhost', 6000))
        print('sending result to localhost:6000')
        client.send(result)
        client.close()
        print('spend', datetime.now() - st)


if __name__ == '__main__':
    main()
