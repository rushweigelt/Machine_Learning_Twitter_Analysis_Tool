"""
Collection of functions to cleanup data before feature engineering
"""
import numpy as np
from sklearn.preprocessing import LabelBinarizer


def replace_nan(X, y):
    """
    Replace NaNs in float columns in place with 0s
    """
    floats = X.select_dtypes(include=["float32", "float64"])
    for col in floats.columns:
        X[col] = X[col].replace(np.nan, 0)
    return X, y


def binarize_y(X, y):
    """
    Binarizes labels
    """
    if y.dtype == object:
        lb = LabelBinarizer()
        y = lb.fit_transform(y).ravel()
    return X, y


ALL_PREPROCESSING = [replace_nan, binarize_y]
