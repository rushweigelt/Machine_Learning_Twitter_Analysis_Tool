import mlflow
from sklearn.model_selection import GridSearchCV, cross_validate

from .SklearnModel import SklearnModel, SCORING_FUNCS


class SklearnGridSearchCV(SklearnModel):
    def __init__(self, model, param_grid, name):
        self.child_model = model
        self.model = GridSearchCV(
            self.child_model, param_grid, scoring=SCORING_FUNCS, refit="precision", cv=3
        )
        self.name = name

    def scores(self, X, y):
        self.model.fit(X, y)
        scores = cross_validate(
            self.model.best_estimator_, X, y, scoring=SCORING_FUNCS, cv=3
        )
        scores = {key: score.mean() for key, score in scores.items()}
        params = {
            f"best_param_{key}": val
            for key, val in self.model.best_estimator_.get_params().items()
        }
        mlflow.log_params(params)
        return scores
