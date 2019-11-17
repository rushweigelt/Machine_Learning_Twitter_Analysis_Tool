from .GaussianNBModel import GaussianNBModel
from .KNeighborsModel import KNeighborsModel
from .GridSearchModel import GridSearchModel

model_types = [GaussianNBModel, KNeighborsModel]

custom_models = [
    GridSearchModel(child_model=KNeighborsModel, param_grid={'n_neighbors': [2, 5]}),
]