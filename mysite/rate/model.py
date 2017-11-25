from multiprocessing.connection import Client, Listener
from typing import List


class KerasModel:
    def __init__(self):
        print('start listening on localhost:6000')
        self.listener = Listener(address=('localhost', 6000))

    def __del__(self):
        self.listener.close()

    def predict(self, articles: List[List[int]]):
        client = Client(address=('localhost', 6001))
        client.send(articles)
        client.close()
        result = self.listener.accept().recv()
        return result
