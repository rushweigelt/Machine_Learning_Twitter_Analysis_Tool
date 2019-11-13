import mlflow.sklearn
from sklearn.model_selection import cross_val_score

from Models import BaseModel

class SklearnModel(BaseModel):
    def __init__(self, **kwargs,):
        super(**kwargs)

    def train(self, X, y):
        self.model.fit(X, y)
    
    def predict(self, X):
        self.model.predict(X)
    
    def score(self, X, y):
        return cross_val_score(self.model, X, y, scoring='precision')

    def save(self):
        mlflow.sklearn.log_model(self.model)
    
    @staticmethod
    def load(uri):
        model = SklearnModel()
        model.model = mlflow.sklearn.load_model(uri)
        return model