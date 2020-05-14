"""
Collection of functions for data cleanup, feature engineering, and postprocessing
"""
from .feature_engineering import ALL_FEATURES
from .pre_processing import ALL_PREPROCESSING
from .post_processing import ALL_POSTPROCESSING


def process_all(X, y):
    """
    Run all preprocessing, feature engineering, and postprocessing functions
    on input data, and returns the result.
    """
    for func in ALL_PREPROCESSING:
        X, y = func(X, y)

    for feature_col, feature in ALL_FEATURES.items():
        feature_func = feature[0]
        input_cols = feature[1]
        cols = map(lambda c: X[c], input_cols)
        X[feature_col] = feature_func(*cols)

    for func in ALL_POSTPROCESSING:
        X, y = func(X, y)

    return X, y
