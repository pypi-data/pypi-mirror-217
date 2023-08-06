
from abc import abstractmethod
from dataclasses import dataclass
from typing import Callable, Dict, List

import jax
import jax.numpy as jnp

from numpyro import infer

import arviz as az

from theoval.stats.base import Approximation


@dataclass(frozen=True)
class MCMCResult:
    mcmc_samples: Dict[str, jnp.DeviceArray]


@dataclass
class AbstractExperiment:

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
    @abstractmethod
    def result(samples: Dict[str, jnp.DeviceArray]) -> MCMCResult:
        raise NotImplementedError



class MCMCSampler:

    def __init__(
            self,
            num_warmup: int = 2000,
            num_samples: int = 10000,
            num_chains: int = 5,
            verbose: bool = True,
            random_seed: int = 0xdeadbeef,
    ):
        self.num_warmup = num_warmup
        self.num_samples = num_samples
        self.num_chains = num_chains
        self.verbose = verbose
        self.random_seed = random_seed

    def __call__(self, model_fn):
        sampler = infer.MCMC(
            infer.NUTS(model_fn),
            num_warmup=self.num_warmup,
            num_samples=self.num_samples,
            num_chains=self.num_chains,
            progress_bar=self.verbose,
        )

        sampler.run(jax.random.PRNGKey(self.random_seed))

        samples = sampler.get_samples(group_by_chain=False)

        if self.verbose:
            inf_data = az.from_numpyro(sampler)
            print(az.summary(inf_data, fmt="long"))

        return samples

class MCMCRunner:

    def __init__(
            self,
            num_warmup: int = 2000,
            num_samples: int = 10000,
            num_chains: int = 5,
            verbose: bool = True,
            random_seed: int = 0xdeadbeef,
    ):
        self.sampler = MCMCSampler(
            num_warmup=num_warmup,
            num_samples=num_samples,
            num_chains=num_chains,
            verbose=verbose,
            random_seed=random_seed,
        )

    def run(
            self,
            experiment: AbstractExperiment,
    ) -> MCMCResult:
        return experiment.result(self.sampler(experiment.numpyro()))

    def run_many(
        self,
        experiments: List[AbstractExperiment],  # assume they all have the same subtype
    ) -> MCMCResult:

        result_dict = {}
        for ex in experiments:
            res = self.sampler(ex.numpyro())
            for k, v in res.items():
                if result_dict.get(k) is None:
                    result_dict[k] = []
                result_dict[k].append(v)

        result = {
            k: jnp.concatenate(v)
            for k, v in result_dict.items()
        }

        return experiments[0].result(result)




def approx_from_samples(
    flat_samples: jnp.DeviceArray,
    n_approx: int,
) -> Approximation:
    upper = (jnp.arange(n_approx) + 1.) / n_approx
    mid = (jnp.arange(n_approx) + .5) / n_approx

    counts = jnp.zeros(n_approx, dtype=int)

    for ix, thresh in enumerate(upper):
        counts = counts.at[ix].set((flat_samples < thresh).sum())

    h = jnp.diff(counts, prepend=0)

    return Approximation(
        n_approx=n_approx,
        values=mid,
        probas=h / h.sum(),
    )
