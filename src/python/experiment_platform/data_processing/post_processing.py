"""
Collection of post-processing functions to clean up data after feature-engineering
but before it's passed to the model.
"""


def dates_to_floats(X, y):
    """
    Convert datetimes and timedeltas to floats of seconds since epoch
    """
    dates = X.select_dtypes(
        include=[
            "datetime64",
            "datetime64[ns]",
            "datetime64[ns, UTC]",
            "timedelta64[ns]",
        ]
    )
    for col in dates.columns:
        X[col] = X[col].astype(int) / 10 ** 9
    return X, y


def drop_objects(X, y):
    """
    Drop all object type columns
    """
    return X.select_dtypes(exclude=["object"]), y


ALL_POSTPROCESSING = [
    dates_to_floats,
    drop_objects,
]
