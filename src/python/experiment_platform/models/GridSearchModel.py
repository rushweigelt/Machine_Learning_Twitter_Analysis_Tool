import mlflow
from sklearn.model_selection import GridSearchCV, cross_validate

from .SklearnModel import SklearnModel, SCORING_FUNCS
from experiment_platform import PARALLELISM


class SklearnGridSearchCV(SklearnModel):
    def __init__(self, model, param_grid, name, cv=5, refit=SCORING_FUNCS):
        self.child_model = model
        self.param_grid = param_grid
        self.cv = cv
        self.name = name
        self.refit = refit
        self.__update_model()

    def scores(self, X, y, scoring=SCORING_FUNCS, cv=5):
        self.cv = cv
        self.refit = scoring
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
        self.model = GridSearchCV(
            self.child_model,
            self.param_grid,
            scoring=SCORING_FUNCS,
            refit="precision",
            cv=self.cv,
            n_jobs=PARALLELISM,
        )
