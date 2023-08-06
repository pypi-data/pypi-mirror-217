
from abc import abstractmethod
from dataclasses import dataclass
from typing import Optional, Union, Dict, Callable

import jax.numpy as jnp

import numpyro
from numpyro import distributions as dist

from theoval.stats.base import (
    BinomialExperiment,
    TrinomialExperiment,
    simulate_binomial,
    simulate_trinomial,
)
from theoval.stats.mcmc import AbstractExperiment
from theoval.preference.est_mcmc import ComparisonMCMCResult


@dataclass
class AbstractComparisonExperiment(AbstractExperiment):

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
    def result(samples: Dict[str, jnp.DeviceArray]) -> ComparisonMCMCResult:
        return ComparisonMCMCResult(mcmc_samples=samples)



@dataclass
class SimpleMixExperiment(AbstractComparisonExperiment):
    win_mix: BinomialExperiment
    draw_mix: BinomialExperiment
    loss_mix: BinomialExperiment
    oracle: TrinomialExperiment
    metric: BinomialExperiment

    def json(self) -> dict:
        return {
            "win_mix": self.win_mix.json(),
            "draw_mix": self.draw_mix.json(),
            "loss_mix": self.loss_mix.json(),
            "oracle": self.oracle.json(),
            "metric": self.metric.json(),
        }

    @staticmethod
    def from_json(d: dict) -> 'SimpleMixExperiment':
        return SimpleMixExperiment(
            win_mix=BinomialExperiment.from_json(d['win_mix']),
            draw_mix=BinomialExperiment.from_json(d['draw_mix']),
            loss_mix=BinomialExperiment.from_json(d['loss_mix']),
            oracle=TrinomialExperiment.from_json(d['oracle']),
            metric=BinomialExperiment.from_json(d['metric']),
        )

    def numpyro(self):
        def model_fn():
            win_mix = numpyro.sample(
                "win_mix",
                dist.Beta(
                    self.win_mix.pos + 1,
                    self.win_mix.tot - self.win_mix.pos + 1,
                ),
            )
            draw_mix = numpyro.sample(
                "draw_mix",
                dist.Beta(
                    self.draw_mix.pos + 1,
                    self.draw_mix.tot - self.draw_mix.pos + 1,
                ),
            )
            loss_mix = numpyro.sample(
                "loss_mix",
                dist.Beta(
                    self.loss_mix.pos + 1,
                    self.loss_mix.tot - self.loss_mix.pos + 1,
                ),
            )

            dirichlet_params = jnp.array([
                self.oracle.win + 1,
                self.oracle.draw + 1,
                self.oracle.loss + 1,
            ])
            ps = numpyro.sample(
                "p_true",
                dist.Dirichlet(dirichlet_params)
            )

            p_win_obs = numpyro.deterministic(
                "p_win_obs",
                jnp.array([win_mix, draw_mix, loss_mix]) @ ps
            )

            with numpyro.plate("data", 1):
                numpyro.sample(
                    "obs",
                    dist.Binomial(
                        total_count=self.metric.tot,
                        probs=p_win_obs,
                    ),
                    obs=self.metric.pos,
                )

        return model_fn


@dataclass
class SimpleFixedMixtureExperiment(AbstractComparisonExperiment):
    win_mix: float
    draw_mix: float
    loss_mix: float
    oracle: TrinomialExperiment
    metric: BinomialExperiment

    def json(self) -> dict:
        return {
            "win_mix": self.win_mix,
            "draw_mix": self.draw_mix,
            "loss_mix": self.loss_mix,
            "oracle": self.oracle.json(),
            "metric": self.metric.json(),
        }

    @staticmethod
    def from_json(d: dict) -> 'SimpleFixedMixtureExperiment':
        return SimpleFixedMixtureExperiment(
            win_mix=d['win_mix'],
            draw_mix=d['draw_mix'],
            loss_mix=d['loss_mix'],
            oracle=TrinomialExperiment.from_json(d['oracle']),
            metric=BinomialExperiment.from_json(d['metric']),
        )

    def numpyro(self):
        def model_fn():
            dirichlet_params = jnp.array([
                self.oracle.win + 1,
                self.oracle.draw + 1,
                self.oracle.loss + 1,
                ])
            ps = numpyro.sample(
                "p_true",
                dist.Dirichlet(dirichlet_params)
            )

            p_win_obs = numpyro.deterministic(
                "p_win_obs",
                jnp.array([self.win_mix, self.draw_mix, self.loss_mix]) @ ps
            )

            with numpyro.plate("data", 1):
                numpyro.sample(
                    "obs",
                    dist.Binomial(
                        total_count=self.metric.tot,
                        probs=p_win_obs,
                    ),
                    obs=self.metric.pos,
                )

        return model_fn


@dataclass
class FullMixExperiment(AbstractComparisonExperiment):
    win_mix: TrinomialExperiment
    draw_mix: TrinomialExperiment
    loss_mix: TrinomialExperiment
    oracle: TrinomialExperiment
    metric: TrinomialExperiment

    def json(self) -> dict:
        return {
            "win_mix": self.win_mix.json(),
            "draw_mix": self.draw_mix.json(),
            "loss_mix": self.loss_mix.json(),
            "oracle": self.oracle.json(),
            "metric": self.metric.json(),
        }

    @staticmethod
    def from_json(d: dict) -> 'FullMixExperiment':
        return FullMixExperiment(
            win_mix=TrinomialExperiment.from_json(d['win_mix']),
            draw_mix=TrinomialExperiment.from_json(d['draw_mix']),
            loss_mix=TrinomialExperiment.from_json(d['loss_mix']),
            oracle=TrinomialExperiment.from_json(d['oracle']),
            metric=TrinomialExperiment.from_json(d['metric']),
        )

    def numpyro(self):
        def model_fn():
            win_mix = numpyro.sample(
                "win_mix",
                dist.Dirichlet(jnp.array([
                    self.win_mix.win + 1,
                    self.win_mix.draw + 1,
                    self.win_mix.loss + 1,
                ])),
            )
            draw_mix = numpyro.sample(
                "draw_mix",
                dist.Dirichlet(jnp.array([
                    self.draw_mix.win + 1,
                    self.draw_mix.draw + 1,
                    self.draw_mix.loss + 1,
                ])),
            )
            loss_mix = numpyro.sample(
                "loss_mix",
                dist.Dirichlet(jnp.array([
                    self.loss_mix.win + 1,
                    self.loss_mix.draw + 1,
                    self.loss_mix.loss + 1,
                ])),
            )

            ps = numpyro.sample(
                "p_true",
                dist.Dirichlet(jnp.array([
                    self.oracle.win + 1,
                    self.oracle.draw + 1,
                    self.oracle.loss + 1,
                ])),
            )

            mixture_mat = jnp.array([
                win_mix,
                draw_mix,
                loss_mix,
            ]).T

            p_win_obs = numpyro.deterministic(
                "p_win_obs",
                mixture_mat @ ps
            )

            my_obs = jnp.array([
                self.metric.win,
                self.metric.draw,
                self.metric.loss,
            ])

            with numpyro.plate("data", 1):
                numpyro.sample(
                    "obs",
                    dist.Multinomial(
                        total_count=my_obs.sum(),
                        probs=p_win_obs,
                    ),
                    obs=my_obs,
                )

        return model_fn


@dataclass
class FullFixedMixtureExperiment(AbstractComparisonExperiment):
    win_mix: jnp.array
    draw_mix: jnp.array
    loss_mix: jnp.array
    oracle: TrinomialExperiment
    metric: TrinomialExperiment

    def json(self) -> dict:
        return {
            "win_mix": self.win_mix.tolist(),
            "draw_mix": self.draw_mix.tolist(),
            "loss_mix": self.loss_mix.tolist(),
            "oracle": self.oracle.json(),
            "metric": self.metric.json(),
        }

    @staticmethod
    def from_json(d: dict) -> 'FullFixedMixtureExperiment':
        return FullFixedMixtureExperiment(
            win_mix=jnp.array(d['win_mix']),
            draw_mix=jnp.array(d['draw_mix']),
            loss_mix=jnp.array(d['loss_mix']),
            oracle=TrinomialExperiment.from_json(d['oracle']),
            metric=TrinomialExperiment.from_json(d['metric']),
        )

    def numpyro(self):
        def model_fn():
            ps = numpyro.sample(
                "p_true",
                dist.Dirichlet(jnp.array([
                    self.oracle.win + 1,
                    self.oracle.draw + 1,
                    self.oracle.loss + 1,
                    ])),
            )

            mixture_mat = jnp.array([
                self.win_mix,
                self.draw_mix,
                self.loss_mix,
            ]).T

            p_win_obs = numpyro.deterministic(
                "p_win_obs",
                mixture_mat @ ps
            )

            my_obs = jnp.array([
                self.metric.win,
                self.metric.draw,
                self.metric.loss,
            ])

            with numpyro.plate("data", 1):
                numpyro.sample(
                    "obs",
                    dist.Multinomial(
                        total_count=my_obs.sum(),
                        probs=p_win_obs,
                    ),
                    obs=my_obs,
                )

        return model_fn


@dataclass
class HumanOnlyExperiment(AbstractComparisonExperiment):
    oracle: TrinomialExperiment

    def json(self) -> dict:
        return {'oracle': self.oracle.json()}

    @staticmethod
    def from_json(d: dict) -> 'HumanOnlyExperiment':
        return HumanOnlyExperiment(
            oracle=TrinomialExperiment.from_json(d['oracle']),
        )

    def numpyro(self):
        def model_fn():
            numpyro.sample(
                "p_true",
                dist.Dirichlet(jnp.array([
                    self.oracle.win + 1,
                    self.oracle.draw + 1,
                    self.oracle.loss + 1,
                    ])),
            )

        return model_fn


def simulate_simple(
    p_true: jnp.array,
    win_mix: float,
    draw_mix: float,
    loss_mix: float,
    n_oracle: int,
    n_metric: int,
    n_mix_estimation: Optional[int] = None,
) -> Union[SimpleMixExperiment, SimpleFixedMixtureExperiment]:
    assert jnp.allclose(p_true.sum(), 1.)

    oracle = simulate_trinomial(p_true, n_oracle)

    p_win_obs = jnp.array([win_mix, draw_mix, loss_mix]) @ p_true
    metric = simulate_binomial(p_win_obs, n_metric)

    if n_mix_estimation is None:
        return SimpleFixedMixtureExperiment(
            win_mix=win_mix,
            draw_mix=draw_mix,
            loss_mix=loss_mix,
            oracle=oracle,
            metric=metric,
        )
    else:
        # when estimating mixtures we condition on the true underlying win/draw/loss
        # oracle meaning win_mix, draw_mix, loss_mix are estimated on a sub-sample
        # of n_mix_estimation according to p_true
        condition_split = simulate_trinomial(p_true, n_mix_estimation)
        return SimpleMixExperiment(
            win_mix=simulate_binomial(win_mix, condition_split.win),
            draw_mix=simulate_binomial(draw_mix, condition_split.draw),
            loss_mix=simulate_binomial(loss_mix, condition_split.loss),
            oracle=oracle,
            metric=metric,
        )


def simulate_full(
    p_true: jnp.array,
    win_mix: jnp.array,
    draw_mix: jnp.array,
    loss_mix: jnp.array,
    n_oracle: int,
    n_metric: int,
    n_mix_estimation: Optional[int] = None,
) -> Union[FullMixExperiment, FullFixedMixtureExperiment]:
    assert jnp.allclose(p_true.sum(), 1.)
    assert jnp.allclose(win_mix.sum(), 1.)
    assert jnp.allclose(draw_mix.sum(), 1.)
    assert jnp.allclose(loss_mix.sum(), 1.)

    oracle = simulate_trinomial(p_true, n_oracle)

    mix_mat = jnp.array([
        win_mix,
        draw_mix,
        loss_mix,
    ]).T
    p_obs = mix_mat @ p_true
    metric = simulate_trinomial(p_obs, n_metric)

    if n_mix_estimation is None:
        return FullFixedMixtureExperiment(
            win_mix=win_mix,
            draw_mix=draw_mix,
            loss_mix=loss_mix,
            oracle=oracle,
            metric=metric,
        )
    else:
        # when estimating mixtures we condition on the true underlying win/draw/loss
        # oracle meaning win_mix, draw_mix, loss_mix are estimated on a sub-sample
        # of n_mix_estimation according to p_true
        condition_split = simulate_trinomial(p_true, n_mix_estimation)
        return FullMixExperiment(
            win_mix=simulate_trinomial(win_mix, condition_split.win),
            draw_mix=simulate_trinomial(draw_mix, condition_split.draw),
            loss_mix=simulate_trinomial(loss_mix, condition_split.loss),
            oracle=oracle,
            metric=metric,
        )


def simulate_human_only(
    p_true: jnp.array,
    n_oracle: int,
) -> HumanOnlyExperiment:
    oracle = simulate_trinomial(p_true, n_oracle)
    return HumanOnlyExperiment(oracle)
