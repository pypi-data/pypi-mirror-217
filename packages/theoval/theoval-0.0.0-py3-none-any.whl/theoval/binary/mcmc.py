
from dataclasses import dataclass

import jax.numpy as jnp

from theoval.stats.base import Approximation
from theoval.stats.mcmc import MCMCResult, approx_from_samples


@dataclass(frozen=True)
class BinaryMCMCResult(MCMCResult):

    def approximation(self, n_approx: int = 2000) -> Approximation:
        return approx_from_samples(
            flat_samples=self.mcmc_samples['alpha'],
            n_approx=n_approx,
        )

    def mean(self) -> float:
        return jnp.mean(self.mcmc_samples['alpha']).item()

    def var(self) -> float:
        return jnp.var(self.mcmc_samples['alpha']).item()

    def std(self) -> float:
        return jnp.std(self.mcmc_samples['alpha']).item()
