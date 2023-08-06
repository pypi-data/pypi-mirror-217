
from typing import Literal

import numpy as np
from sklearn.metrics import roc_curve


ConversionMethod = Literal["max_sum", "min_diff"]

def threshold(
    human: np.array,
    scalar: np.array,
    method: ConversionMethod
) -> np.array:
    fpr, tpr, thresholds = roc_curve(
        y_true=human,
        y_score=scalar,
    )
    rhos = tpr
    etas = 1. - fpr

    if method == "max_sum":
        selected = (rhos + etas).argmax()
    elif method == "min_diff":
        selected = np.abs(rhos - etas).argmin()
    else:
        raise ValueError(
            f"unknown conversion method {method},"
            f"use one of [{ConversionMethod.__args__}]"
        )

    return thresholds[selected]
