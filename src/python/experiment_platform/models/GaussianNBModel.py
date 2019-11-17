from sklearn.naive_bayes import GaussianNB

from .SklearnModel import SklearnModel

class GaussianNBModel(SklearnModel):
    def __init__(self):
        self.model = GaussianNB()
        self.params = self.get_params()
