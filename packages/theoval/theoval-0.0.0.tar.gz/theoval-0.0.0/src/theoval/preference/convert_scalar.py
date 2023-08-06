
from abc import abstractmethod
from typing import Literal, Callable

import numpy as np

from sklearn.metrics import accuracy_score, confusion_matrix


CONVERSION_METHOD = Literal[
    "naive",
    "thresh_max_acc",
    "thresh_max_diag",
    "thresh_symm",
]


class Conversion:

    @abstractmethod
    def fit(
        self,
        scalars_sys1: np.array,
        scalars_sys2: np.array,
        human_comparisons: np.array,
    ) -> 'Conversion':
        raise NotImplemented

    @abstractmethod
    def transform(
        self,
        scalars_sys1: np.array,
        scalars_sys2: np.array,
    ) -> np.array:
        raise NotImplemented

    def fit_transform(
        self,
        scalars_sys1: np.array,
        scalars_sys2: np.array,
        human_comparisons: np.array
    ) -> np.array:
        self.fit(scalars_sys1, scalars_sys2, human_comparisons)
        return self.transform(scalars_sys1, scalars_sys2)


def conversion(method: CONVERSION_METHOD = "naive") -> Conversion:
    if method == "naive":
        return NaiveConversion()
    elif method == "thresh_max_acc":
        return ThresholdConversion(score_fn=accuracy_scoring)
    elif method == "thresh_max_diag":
        return ThresholdConversion(score_fn=max_diag)
    elif method == "thresh_symm":
        return ThresholdConversion(score_fn=symmetry_scoring)
    else:
        raise ValueError


class NaiveConversion(Conversion):

    def __init__(self):
        super().__init__()

    def fit(
        self,
        scalars_sys1: np.array,
        scalars_sys2: np.array,
        human_comparisons: np.array,
    ):
        return self

    def transform(
        self,
        scalars_sys1,
        scalars_sys2,
    ) -> np.array:
        return np.sign(scalars_sys1 - scalars_sys2).astype(int)


class FixedThresholdConversion(Conversion):

    def __init__(
        self,
        th_lo: float,
        th_hi: float,
    ):
        super().__init__()
        self.th_lo = th_lo
        self.th_hi = th_hi

    def fit(
        self,
        scalars_sys1: np.array,
        scalars_sys2: np.array,
        human_comparisons: np.array,
    ) -> 'Conversion':
        return self

    def transform(
        self,
        scalars_sys1: np.array,
        scalars_sys2: np.array,
    ) -> np.array:
        return apply_thresholds(
            scores=scalars_sys1 - scalars_sys2,
            th_lo=self.th_lo,
            th_hi=self.th_hi,
        )


class ThresholdConversion(Conversion):

    def __init__(
        self,
        score_fn: Callable[[np.array, np.array], float],
    ):
        super().__init__()
        self.score_fn = score_fn
        self.th_lo = None
        self.th_hi = None

    def fit(
        self,
        scalars_sys1: np.array,
        scalars_sys2: np.array,
        human_comparisons: np.array,
    ) -> 'Conversion':

        scores = scalars_sys1 - scalars_sys2
        candidates = np.unique(scores)

        best_lo = None
        best_hi = None
        best_loss = np.inf

        for ix_lo, th_lo in enumerate(candidates):
            for th_hi in candidates[ix_lo:]:
                cand_pred = apply_thresholds(
                    scores=scores,
                    th_lo=th_lo,
                    th_hi=th_hi,
                )
                s = self.score_fn(human_comparisons, cand_pred)
                if s < best_loss:
                    best_lo = th_lo
                    best_hi = th_hi
                    best_loss = s

        self.th_lo = best_lo
        self.th_hi = best_hi

        return self

    def transform(
        self,
        scalars_sys1: np.array,
        scalars_sys2: np.array,
    ) -> np.array:
        return apply_thresholds(
            scores=scalars_sys1 - scalars_sys2,
            th_lo=self.th_lo,
            th_hi=self.th_hi,
        )


def apply_thresholds(
    scores: np.array,
    th_lo: float,
    th_hi: float,
) -> np.array:
    result = np.zeros_like(scores).astype(int)
    result[scores >= th_hi] = 1
    result[scores <= th_lo] = -1
    return result


def mu(
    y_true: np.array,
    y_pred: np.array,
) -> np.array:
    return confusion_matrix(
        y_true=y_true,
        y_pred=y_pred,
        normalize="true",
        labels=[1, 0, -1],
    ).T


def accuracy_scoring(
    y_true: np.array,
    y_pred: np.array,
) -> float:
    return - accuracy_score(y_true, y_pred)


def max_diag(
    y_true: np.array,
    y_pred: np.array,
) -> float:
    m = mu(y_true, y_pred)
    return - (m[0, 0] + m[1, 1] + m[2, 2])


def symmetry_scoring(
    y_true: np.array,
    y_pred: np.array,
) -> float:
    m = mu(y_true, y_pred)
    return np.abs(m - m.T).sum()
