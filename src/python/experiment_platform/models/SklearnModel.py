import mlflow.sklearn
from sklearn.model_selection import cross_validate

from .BaseModel import BaseModel
from experiment_platform import PARALLELISM

SCORING_FUNCS = ["precision", "roc_auc", "accuracy"]


class SklearnModel(BaseModel):
    def __init__(self, model, name=None):
        self.model = model
        self.name = name if name else type(model).__name__

    def fit(self, X, y):
        self.model.fit(X, y)

    def predict(self, X):
        return self.model.predict(X)

    def score(self, X, y):
        return self.model.score(X, y)

    def scores(self, X, y, scoring=SCORING_FUNCS, cv=5):
        raw_scores = cross_validate(
            self.model, X, y, scoring=scoring, cv=cv, n_jobs=PARALLELISM
        )
        scores = {key: score.mean() for key, score in raw_scores.items()}
        return scores

    def save(self, **kwargs):
        mlflow.sklearn.log_model(self.model, **kwargs)

    def get_params(self, deep=True):
        return self.model.get_params()

    def set_params(self, **params):
        self.model.set_params(**params)
        return self

    @staticmethod
    def load(uri, name):
        sklearn_model = mlflow.sklearn.load_model(uri)
        model = SklearnModel(model=sklearn_model, name=name)
        return model
