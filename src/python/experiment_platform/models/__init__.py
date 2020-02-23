from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC

from .SklearnModel import SklearnModel
from .GridSearchModel import SklearnGridSearchCV


custom_models = [
    SklearnModel(model=GaussianNB()),
    SklearnModel(model=KNeighborsClassifier()),
    SklearnModel(model=AdaBoostClassifier()),
    SklearnModel(model=RandomForestClassifier()),
    SklearnGridSearchCV(
        model=KNeighborsClassifier(),
        param_grid={"n_neighbors": range(2, 10)},
        name="GridSearchKNeighbors",
    ),
    SklearnGridSearchCV(
        model=RandomForestClassifier(),
        param_grid={"n_estimators": [5, 10, 100, 200, 500]},
        name="GridSearchRandomForest",
    ),
    SklearnGridSearchCV(
        model=AdaBoostClassifier(),
        param_grid={
            "n_estimators": [20, 50, 100, 200],
            "learning_rate": [0.1, 0.5, 0.75, 1],
        },
        name="GridSearchAdaBoost",
    ),
]
