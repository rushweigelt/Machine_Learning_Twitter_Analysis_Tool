from sklearn.neighbors import KNeighborsClassifier

from .SklearnModel import SklearnModel

class KNeighborsModel(SklearnModel):
    def __init__(self, **kwargs):
        self.model = KNeighborsClassifier(**kwargs)
        self.params = self.get_params()
