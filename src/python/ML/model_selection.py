class ModelRanking:
    def __init__(self, pipelines):
        self.pipelines = pipelines
        self.is_fit = False

    def fit(self, X, y):
        for (preprocessing, models) in self.pipelines:
            transformed_X = preprocessing.fit_transform(X)
            for model in models:
                model.fit(transformed_X, y)
        self.is_fit = True

    def score(self, X, y):
        if not self.is_fit:
            raise RuntimeError("Tried to score models before fitting to training data")
        scores_and_models = []
        for (preprocessing, models) in self.pipelines:
            transformed_X = preprocessing.transform(X)
            for model in models:
                scores_and_models.append((model.score(transformed_X, y), model))
        return sorted(scores_and_models, reverse=True)
