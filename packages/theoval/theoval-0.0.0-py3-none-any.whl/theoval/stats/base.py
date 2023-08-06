
from dataclasses import dataclass
from typing import Optional

import numpy as np
from numpy.random import Generator
import scipy.stats as stats

from matplotlib import pyplot as plt


@dataclass
class BinomialExperiment:
    pos: int
    tot: int

    def json(self) -> dict:
        return {
            'pos': self.pos,
            'tot': self.tot,
        }

    @staticmethod
    def from_json(d: dict) -> 'BinomialExperiment':
        return BinomialExperiment(**d)

    def p_win(self) -> float:
        return self.pos / self.tot


@dataclass
class TrinomialExperiment:
    win: int
    draw: int
    loss: int

    def json(self) -> dict:
        return {
            'win': self.win,
            'draw': self.draw,
            'loss': self.loss,
        }

    @staticmethod
    def from_json(d: dict) -> 'TrinomialExperiment':
        return TrinomialExperiment(**d)

    def n(self) -> int:
        return self.win + self.draw + self.loss

    def p(self) -> np.array:
        n = self.n()
        if n == 0:
            return np.zeros(3)
        else:
            return np.array([self.win, self.draw, self.loss]) / self.n()

    def p_win_proba_larger(self) -> float:
        z = (self.win - self.loss) / np.sqrt(self.win + self.loss)
        p = stats.norm.cdf(z, loc=0., scale=1.)
        return p


@dataclass
class Approximation:
    n_approx: int
    values: np.array
    probas: np.array

    def json(self) -> dict:
        return {
            "n_approx": self.n_approx,
            "values": list(self.values),
            "probas": list(self.probas),
        }

    @staticmethod
    def from_json(d: dict) -> 'Approximation':
        return Approximation(
            n_approx=d['n_approx'],
            values=np.array(d['values']),
            probas=np.array(d['probas']),
        )

    def mean(self) -> float:
        return self.probas @ self.values

    def var(self) -> float:
        m = self.mean()
        sq = (self.values * self.values) @ self.probas
        return sq - (m*m)

    def stdev(self) -> float:
        return np.sqrt(self.var())

    def epsilon(self, gamma: float):
        stdev = np.sqrt(2*self.var())
        _, eps = stats.norm.interval(1. - gamma, loc=0., scale=stdev)
        return eps

    def plot(self, name: str, ax: Optional[plt.Axes] = None):
        xs = np.arange(self.n_approx) / self.n_approx
        width = 1. / self.n_approx

        if ax is not None:
            ax.bar(x=xs, height=self.probas, width=width, label=name, alpha=.6)
        else:
            plt.bar(x=xs, height=self.probas, width=width, label=name, alpha=.6)


def approximate_uniform(n_approx: int) -> Approximation:
    return Approximation(
        n_approx=n_approx,
        values=(np.arange(n_approx) + .5) / n_approx,
        probas=np.ones(n_approx) / n_approx
    )


def approximate_beta(beta_a: float, beta_b: float, n_approx: int) -> Approximation:
    lower = np.arange(n_approx) / n_approx
    upper = (np.arange(n_approx) + 1.) / n_approx
    mid = (np.arange(n_approx) + .5) / n_approx

    beta = stats.beta(a=beta_a, b=beta_b)

    return Approximation(
        n_approx=n_approx,
        values=mid,
        probas=beta.cdf(upper) - beta.cdf(lower)
    )


def compare(bigger: Approximation, smaller: Approximation) -> float:
    if bigger.n_approx != smaller.n_approx:
        raise ValueError(
            f"need both inputs to have the same approximation granularity,"
            f" got {bigger.n_approx} and {smaller.n_approx}")

    acc = 0.
    for i in range(smaller.n_approx):
        for j in range(i+1, bigger.n_approx):
            acc += smaller.probas[i]*bigger.probas[j]

    return acc


def kl_divergence(
    p: Approximation,
    q: Approximation,
    smooth: float = 1e-8,
) -> float:
    assert p.n_approx == q.n_approx
    assert np.allclose(p.values, q.values)

    return p.probas @ (np.log(p.probas + smooth) - np.log(q.probas + smooth))


def simulate_binomial(
    p_win: float,
    n_trials: int,
    rng: Optional[Generator] = None,
) -> BinomialExperiment:
    if rng is None:
        n_pos = int(round(p_win*n_trials))
    else:
        n_pos = rng.binomial(n=n_trials, p=p_win)
    return BinomialExperiment(
        pos=n_pos,
        tot=n_trials,
    )


def simulate_trinomial(
    p: np.array,
    n_trials: int,
    rng: Optional[Generator] = None,
) -> TrinomialExperiment:
    assert np.allclose(p.sum(), 1.)
    assert p.shape[-1] == 3

    if rng is None:
        p_win = p[0]
        p_loss = p[2]
        # this assumes that we will run a lot of
        # experiments where p_draw >> p_win, p_loss
        # alternative would be to fudge n_trials (would be off by 1 sometimes)
        n_win = int(round(p_win * n_trials))
        n_loss = int(round(p_loss * n_trials))
        n_draw = n_trials - n_win - n_loss
    else:
        ns = rng.multinomial(n=n_trials, pvals=p)
        n_win = ns[0]
        n_draw = ns[1]
        n_loss = ns[2]

    return TrinomialExperiment(
        win=n_win,
        draw=n_draw,
        loss=n_loss,
    )
