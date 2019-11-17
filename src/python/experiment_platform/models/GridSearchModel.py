import mlflow
from sklearn.model_selection import GridSearchCV

from .SklearnModel import SklearnModel

class GridSearchModel(SklearnModel):
    def __init__(self, child_model=None, param_grid=None):
        self.child_model = self.create_child_model(child_model)
        self.model = GridSearchCV(self.child_model, param_grid, cv=5)
        self.params = self.get_params()
    
    def create_child_model(self, child_model):
        class GridSearchChildModel(child_model):
            def __init__(self, **kwargs):
                self.model = child_model(**kwargs)
                self.active_run = None

            def fit(self, X, y):
                self.active_run = mlflow.start_run(nested=True)
                mlflow.set_tag('model', child_model.__name__)
                mlflow.log_params(self.get_params())
                super().fit(X, y)
            
            def score(self, X, y):
                metrics = self.scores(X, y)
                mlflow.log_metrics(metrics)
                mlflow.end_run()
                return metrics['precision']

        return GridSearchChildModel()
