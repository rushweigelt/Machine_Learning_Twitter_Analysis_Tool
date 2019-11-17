import mlflow.sklearn
from sklearn.model_selection import cross_val_score

from .BaseModel import BaseModel

class SklearnModel(BaseModel):
    def fit(self, X, y):
        self.model.fit(X, y)
    
    def predict(self, X):
        return self.model.predict(X)
    
    def score(self, X, y):
        return self.scores(X, y)['precision']

    def scores(self, X, y):
        scoring_funcs = ['precision', 'roc_auc', 'accuracy']
        scores = {}
        for sf in scoring_funcs:
            raw_scores = cross_val_score(self.model, X, y, scoring=sf, cv=5)
            scores[sf] = raw_scores.mean()
        return scores

    def save(self, uri):
        mlflow.sklearn.log_model(self.model, artifact_path=uri)
    
    def get_params(self, deep=True):
        return self.model.get_params()

    def set_params(self, **params):
        self.model.set_params(**params)
        return self
    
    @staticmethod
    def load(uri):
        model = SklearnModel()
        model.model = mlflow.sklearn.load_model(uri)
        return model