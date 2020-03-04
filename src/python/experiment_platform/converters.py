"""
Collection of functions to handle data cleanup and conversion
"""
import numpy as np
from sklearn import preprocessing

# TODO: include Alex's feature engineering (different file?)


def dates_to_floats(X, y):
    """
    Convert datetimes to floats of seconds since epoch
    """
    dates = X.select_dtypes(
        include=["datetime64", "datetime64[ns]", "datetime64[ns, UTC]"]
    )
    for col in dates.columns:
        X[col] = X[col].astype(int) / 10 ** 9
    return X, y


def binarize_y(X, y):
    """
    Binarizes labels
    """
    if y.dtype == object:
        lb = preprocessing.LabelBinarizer()
        y = lb.fit_transform(y).ravel()
    return X, y


def replace_nan(X, y):
    """
    Replace NaNs in float columns in place with 0s
    """
    floats = X.select_dtypes(include=["float32", "float64"])
    for col in floats.columns:
        X[col] = X[col].replace(np.nan, 0)
    return X, y


def drop_objects(X, y):
    """
    Drop all object type columns
    """
    return X.select_dtypes(exclude=["object"]), y


ALL_CONVERTERS = [
    dates_to_floats,
    replace_nan,
    binarize_y,
    drop_objects,
]
