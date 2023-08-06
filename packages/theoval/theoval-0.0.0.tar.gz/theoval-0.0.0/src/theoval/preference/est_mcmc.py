
from dataclasses import dataclass

import jax.numpy as jnp

from theoval.stats.mcmc import MCMCResult


@dataclass(frozen=True)
class ComparisonMCMCResult(MCMCResult):

    def p_win_proba_larger(self) -> float:
        p = self.mcmc_samples['p_true']
        return (p[:, 0] > p[:, 2]).mean()

    def expected_p_true(self) -> jnp.array:
        return jnp.mean(self.mcmc_samples['p_true'], axis=0)

    def comparison(self, gamma: float = 0.05) -> int:
        p = self.p_win_proba_larger()
        if p > (1. - gamma / 2):
            return 1
        elif p < gamma / 2:
            return -1
        else:
            return 0
