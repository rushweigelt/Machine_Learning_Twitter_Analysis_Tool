"""
Contains wrapper classes for Sklearn models, so that they can easily be
trained with MLFlow and existing Datasets.
"""
import mlflow.sklearn
from sklearn.model_selection import GridSearchCV, cross_validate

from experiment_platform import PARALLELISM
from experiment_platform.models import BaseModel


class SklearnModel(BaseModel):
    """
    Wrapper for simple Sklearn models
    """

    def __init__(self, model, name=None):
        self.model = model
        self.name = name if name else type(model).__name__

    def fit(self, X, y):
        self.model.fit(X, y)

    def predict(self, X):
        return self.model.predict(X)

    def score(self, X, y):
        return self.model.score(X, y)

    def scores(self, X, y, scoring, cv=5):
        raw_scores = cross_validate(
            self.model, X, y, scoring=scoring, cv=cv, n_jobs=PARALLELISM
        )
        scores = {key: score.mean() for key, score in raw_scores.items()}
        return scores

    def save(self, artifact_path):
        mlflow.sklearn.log_model(self.model, artifact_path=artifact_path)

    def get_params(self):
        """
        Returns the model's configured parameters
        """
        return self.model.get_params()

    @staticmethod
    def load(uri, name):
        sklearn_model = mlflow.sklearn.load_model(uri)
        model = SklearnModel(model=sklearn_model, name=name)
        return model


class SklearnGridSearchCV(SklearnModel):
    """
    Wrapper for GridSearch Sklearn models. Due to their complexity,
    these hyper-models require their own special handling.
    """

    def __init__(self, model, param_grid, name=None, scoring=None, refit=None, cv=5):
        self.child_model = model
        self.param_grid = param_grid
        self.cv = cv
        if name:
            self.name = name
        else:
            self.name = "GridSearch" + type(model).__name__
        self.scoring = scoring
        if refit:
            self.refit = refit
        elif scoring:
            self.refit = scoring[0]
        else:
            self.refit = True
        self.__update_model()

    def scores(self, X, y, scoring, cv=5, refit=None):
        # pylint: disable=arguments-differ
        self.cv = cv
        self.scoring = scoring
        if refit:
            self.refit = refit
        elif self.scoring:
            self.refit = self.scoring[0]
        self.__update_model()

        self.model.fit(X, y)
        scores = cross_validate(
            self.model.best_estimator_, X, y, scoring=scoring, cv=cv, n_jobs=PARALLELISM
        )
        scores = {key: score.mean() for key, score in scores.items()}
        params = {
            f"best_param_{key}": val
            for key, val in self.model.best_estimator_.get_params().items()
        }
        mlflow.log_params(params)
        return scores

    def __update_model(self):
        """
        Re-creates the model. Should be called after changing any
        instance variables.
        """
        self.model = GridSearchCV(
            self.child_model,
            self.param_grid,
            scoring=self.scoring,
            refit=self.refit,
            cv=self.cv,
            n_jobs=PARALLELISM,
        )
