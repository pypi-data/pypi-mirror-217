
from dataclasses import dataclass
from abc import abstractmethod
from typing import Callable, Dict, Optional, List, Union

import numpyro
from numpyro import distributions as dist
import jax.numpy as jnp
import numpy as np

from theoval.stats.base import BinomialExperiment, simulate_binomial
from theoval.stats.mcmc import AbstractExperiment, MCMCResult
from theoval.binary.mcmc import BinaryMCMCResult


class AbstractBinaryExperiment(AbstractExperiment):

    @abstractmethod
    def json(self) -> dict:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def from_json(d: dict) -> 'AbstractExperiment':
        raise NotImplementedError

    @abstractmethod
    def numpyro(self) -> Callable[[], None]:
        raise NotImplementedError

    @staticmethod
    def result(samples: Dict[str, jnp.DeviceArray]) -> MCMCResult:
        return BinaryMCMCResult(mcmc_samples=samples)

@dataclass
class FullModelExperiment(AbstractBinaryExperiment):
    rho: BinomialExperiment
    eta: BinomialExperiment
    oracle: BinomialExperiment
    metric: BinomialExperiment

    def json(self) -> dict:
        return {
            "rho": self.rho.json(),
            "eta": self.eta.json(),
            "oracle": self.oracle.json(),
            "metric": self.metric.json(),
        }

    @staticmethod
    def from_json(d: dict) -> 'FullModelExperiment':
        return FullModelExperiment(
            rho=BinomialExperiment.from_json(d['rho']),
            eta=BinomialExperiment.from_json(d['eta']),
            oracle=BinomialExperiment.from_json(d['oracle']),
            metric=BinomialExperiment.from_json(d['metric']),
        )

    def numpyro(self) -> Callable[[], None]:
        def model_fn():
            rho = numpyro.sample(
                "rho",
                dist.Beta(self.rho.pos + 1, self.rho.tot - self.rho.pos + 1),
            )
            eta = numpyro.sample(
                "eta",
                dist.Beta(self.eta.pos + 1, self.eta.tot - self.eta.pos + 1),
            )
            alpha = numpyro.sample(
                "alpha",
                dist.Beta(
                    self.oracle.pos + 1, self.oracle.tot - self.oracle.pos + 1),
            )

            alpha_obs = numpyro.deterministic(
                "alpha_obs",
                alpha*(rho + eta - 1.) + (1. - eta),
            )

            with numpyro.plate("data", 1):
                numpyro.sample(
                    "obs",
                    dist.Binomial(total_count=self.metric.tot, probs=alpha_obs),
                    obs=self.metric.pos,
                )

        return model_fn


@dataclass
class FixedRhoEtaExperiment(AbstractBinaryExperiment):
    rho: float
    eta: float
    oracle: BinomialExperiment
    metric: BinomialExperiment

    def json(self) -> dict:
        return {
            "rho": self.rho,
            "eta": self.eta,
            "oracle": self.oracle.json(),
            "metric": self.metric.json(),
        }

    @staticmethod
    def from_json(d: dict) -> 'FixedRhoEtaExperiment':
        return FixedRhoEtaExperiment(
            rho=d['rho'],
            eta=d['eta'],
            oracle=BinomialExperiment.from_json(d['oracle']),
            metric=BinomialExperiment.from_json(d['metric']),
        )

    def numpyro(self) -> Callable[[], None]:

        def model_fn():
            alpha = numpyro.sample(
                "alpha",
                dist.Beta(
                    self.oracle.pos + 1, self.oracle.tot - self.oracle.pos + 1),
            )

            alpha_obs = numpyro.deterministic(
                "alpha_obs",
                alpha*(self.rho + self.eta - 1.) + (1. - self.eta),
            )

            with numpyro.plate("data", 1):
                numpyro.sample(
                    "obs",
                    dist.Binomial(total_count=self.metric.tot, probs=alpha_obs),
                    obs=self.metric.pos,
                )

        return model_fn


@dataclass
class DirectExperiment(AbstractBinaryExperiment):
    binom: BinomialExperiment

    def json(self) -> dict:
        return {
            "binom": self.binom.json(),
        }

    @staticmethod
    def from_json(d: dict) -> 'AbstractExperiment':
        return DirectExperiment(
            binom=BinomialExperiment.from_json(d['binom']),
        )

    def numpyro(self) -> Callable[[], None]:

        def model_fn():
            alpha = numpyro.sample(
                "alpha",
                dist.Beta(1, 1),
            )

            with numpyro.plate("data", 1):
                numpyro.sample(
                    "obs",
                    dist.Binomial(total_count=self.binom.tot, probs=alpha),
                    obs=self.binom.pos,
                )

        return model_fn


def simulate_full(
    rho: float,
    eta: float,
    alpha: float,
    n_oracle: int,
    n_metric: int,
    rng: Optional[np.random.Generator],
) -> FullModelExperiment:
    sim_oracle = simulate_binomial(p_win=alpha, n_trials=n_oracle, rng=rng)
    sim_rho = simulate_binomial(p_win=rho, n_trials=sim_oracle.pos, rng=rng)
    sim_eta = simulate_binomial(
        p_win=eta, n_trials=sim_oracle.tot - sim_oracle.pos, rng=rng)

    a_obs = alpha * (rho + eta - 1.) + (1. - eta)
    sim_metric = simulate_binomial(p_win=a_obs, n_trials=n_metric, rng=rng)

    return  FullModelExperiment(
        rho=sim_rho,
        eta=sim_eta,
        oracle=sim_oracle,
        metric=sim_metric,
    )

def simulate_full_many(
    n: int,
    rho: float,
    eta: float,
    alpha: float,
    n_oracle: int,
    n_metric: int,
    rng: Union[np.random.Generator, int],  # this only makes sense if we really sample
) -> List[FullModelExperiment]:
    if type(rng) is int:
        rng = np.random.default_rng(rng)
    return [
        simulate_full(
            rho=rho,
            eta=eta,
            alpha=alpha,
            n_oracle=n_oracle,
            n_metric=n_metric,
            rng=rng,
        )
        for _ in range(n)
    ]


def simulate_oracle_many(
    n: int,
    alpha: float,
    n_oracle: int,
    rng: Union[np.random.Generator, int],
) -> List[DirectExperiment]:
    if type(rng) is int:
        rng = np.random.default_rng(rng)
    return [
        DirectExperiment(
            binom=simulate_binomial(p_win=alpha, n_trials=n_oracle, rng=rng)
        )
        for _ in range(n)
    ]
