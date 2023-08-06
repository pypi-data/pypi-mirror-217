import datetime
import enum

import numpy as np
import pandas as pd
from numbers import Integral, Real


def pandas_isnull(obj):
    """
    Helper function to check if an object is null, even if it's a pandas object.
    """
    try:
        return pd.isnull(obj) is True  # prevents issues with pandas arrays treating this as an array
    except ValueError:
        return False


def sanitize(obj, n_digits=5):  # pylint: disable=R0911, R0912
    """
    Sanitizes obj into something json-encodable, and rounds floats to n_digits
    Args:
        obj: Object to sanitize
        n_digits: number of digits to round floats to

    Returns:
        Sanitized version of object.
    """
    if obj is None:
        return "NA"
    if pandas_isnull(obj):
        return "NA"
    if isinstance(obj, Integral):
        return int(obj)
    if isinstance(obj, Real):
        if obj == float("inf"):
            return "inf"
        if obj == float("-inf"):
            return "-inf"
        return round(float(obj), ndigits=n_digits)
    if isinstance(obj, enum.Enum):
        return sanitize(obj.value, n_digits=n_digits)
    if isinstance(obj, np.ndarray):
        return sanitize(obj.tolist(), n_digits=n_digits)
    if isinstance(obj, (bool, bytes, str, int, float)):
        return obj
    if isinstance(obj, list):
        return [sanitize(sub_obj, n_digits=n_digits) for sub_obj in obj]
    if isinstance(obj, tuple):
        return tuple(sanitize(sub_obj, n_digits=n_digits) for sub_obj in obj)
    if isinstance(obj, set):
        return {sanitize(sub_obj, n_digits=n_digits) for sub_obj in obj}
    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()
    if isinstance(obj, dict):
        obj_dict = obj
        return {sanitize(key, n_digits=n_digits): sanitize(val, n_digits=n_digits) for key, val in obj_dict.items()}
    raise ValueError(f"Sanitizing value {obj} of type {type(obj)} is not supported. Add code to this function "
                     f"to support sanitization if necessary.")
