from ML import validated
from ML.Connectors import Connector

class MockConnector(Connector):
    @validated
    def retrieve(self):
        return [1, 2, 3, 4, 5]
