
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple, Union

import numpy as np

from theoval.stats.base import BinomialExperiment
from theoval.binary.convert_scalar import ConversionMethod, threshold
from theoval.binary.experiment import (
    FullModelExperiment,
    FixedRhoEtaExperiment,
    DirectExperiment,
)


class BinaryArgs:
    ipath: str
    opath: str
    systems: Union[List, str]
    metrics: Union[List, str]

@dataclass
class BinaryData:
    system: str
    human: np.array
    mask: np.array
    metric: Dict[str, np.array]
    cache: Optional[Dict[Tuple[str, str], np.array]] = None

    def __post_init__(self):
        if self.cache is None:
            cache = {}
            for m, ss in self.metric.items():
                for method in ConversionMethod.__args__:
                    cache[(m, method)] = self.convert_metric(
                        metric_name=m,
                        method=method,
                    )

            self.cache = cache

    def __len__(self) -> int:
        return self.human.shape[0]

    def __check_lengths(self) -> bool:
        len_h = len(self)

        if self.human.shape != (len_h,):
            raise ValueError(
                f"expecting 1-D dimensional array as human ratings")

        if self.mask.shape != (len_h,):
            raise ValueError(
                f"mask array needs to have same shape as human ratings array")

        for m, ss in self.metric.items():
            if ss.shape != (len_h,):
                raise ValueError(f"shape of metric ratings {m} do not math"
                                 f"human shape of human ratings {(len_h,)}")

        return True

    def __check_values(self) -> bool:
        if not np.isfinite(self.human[self.mask]).all():
            raise ValueError(f"self.human contains inf/nan values "
                             f"that are not masked by self.mask")

        if not ((self.human == 0) | (self.human == 1))[self.mask].all():
            raise ValueError(f"human ratings in self.human contain "
                             f"values not in [0, 1]")

        if not (self.human[~self.mask] == 255).all():
            raise ValueError(f"masked out ratings contain values different from "
                             f"the canary value 255")

        for m, ss in self.metric.items():
            if not np.isfinite(ss).all():
                raise ValueError(f"scalar values for metric {m}"
                                 f"containt inf/nan values")

        return True

    def check_integrity(self) -> bool:
        self.__check_lengths()
        self.__check_values()
        return True

    def convert_metric(
        self,
        metric_name: str,
        method: ConversionMethod = "min_diff",
    ):
        if self.cache is not None:
            return self.cache[(metric_name, method)]
        scalar = self.metric[metric_name]
        thresh = threshold(
            human=self.human[self.mask],
            scalar=scalar[self.mask],
            method=method,
        )
        return scalar >= thresh

    def oracle_data(self) -> BinomialExperiment:
        return BinomialExperiment(
            pos=self.human[self.mask].sum(),
            tot=self.mask.sum(),
        )

    def metric_data(
        self,
        metric_name: str,
        conversion_method: ConversionMethod = "min_diff",
    ) -> BinomialExperiment:
        ss = self.convert_metric(
            metric_name=metric_name, method=conversion_method)
        return BinomialExperiment(
            pos=ss.sum(),
            tot=len(ss),
        )

    def mixture_params(
        self,
        metric_name: str,
        conversion_method: ConversionMethod = "min_diff",
    ) -> Dict[str, BinomialExperiment]:
        ss = self.convert_metric(
            metric_name=metric_name, method=conversion_method)[self.mask]
        hs = self.human[self.mask]

        true_pos_mask = (hs == 1)
        rho = BinomialExperiment(
            pos=(ss[true_pos_mask] == 1).sum(),
            tot=true_pos_mask.sum(),
        )

        true_neg_mask = (hs == 0)
        eta = BinomialExperiment(
            pos=(ss[true_neg_mask] == 0).sum(),
            tot=true_neg_mask.sum(),
        )

        return {
            "rho": rho,
            "eta": eta,
        }

    def rho_data(
        self,
        metric_name: str,
        conversion_method: ConversionMethod = "min_diff",
    ) -> BinomialExperiment:
        return self.mixture_params(
            metric_name=metric_name, conversion_method=conversion_method,
        )["rho"]

    def eta_data(
        self,
        metric_name: str,
        conversion_method: ConversionMethod = "min_diff",
    ) -> BinomialExperiment:
        return self.mixture_params(
            metric_name=metric_name, conversion_method=conversion_method,
        )["eta"]

    def full_model(
        self,
        metric_name: str,
        conversion_method: ConversionMethod = "min_diff",
    ) -> FullModelExperiment:
        mix = self.mixture_params(
            metric_name=metric_name,
            conversion_method=conversion_method,
        )
        return FullModelExperiment(
            rho=mix["rho"],
            eta=mix["eta"],
            oracle=self.oracle_data(),
            metric=self.metric_data(
                metric_name=metric_name,
                conversion_method=conversion_method,
            )
        )

    def fixed_rho_eta_model(
        self,
        metric_name: str,
        conversion_method: ConversionMethod = "min_diff",
    ) -> FixedRhoEtaExperiment:
        mix = self.mixture_params(
            metric_name=metric_name,
            conversion_method=conversion_method,
        )
        return FixedRhoEtaExperiment(
            rho=mix["rho"].p_win(),
            eta=mix["eta"].p_win(),
            oracle=self.oracle_data(),
            metric=self.metric_data(
                metric_name=metric_name,
                conversion_method=conversion_method,
            )
        )

    def oracle_only_experiment(self) -> DirectExperiment:
        return DirectExperiment(
            binom=self.oracle_data(),
        )

    def naive_metric_experiment(
        self,
        metric_name: str,
        conversion_method: ConversionMethod = "min_diff",
    ) -> DirectExperiment:
        return DirectExperiment(
            binom=self.metric_data(
                metric_name=metric_name, conversion_method=conversion_method),
        )

    def concatenate(self, other: 'BinaryData') -> 'BinaryData':
        system = f"{self.system}__{other.system}"
        human = np.concatenate([self.human, other.human])
        mask = np.concatenate([self.mask, other.mask])
        metrics = {}

        metric_names = set(self.metric.keys()).union(other.metric.keys())
        for m in metric_names:
            ss1 = self.metric.get(m)
            ss2 = other.metric.get(m)
            if ss1 is not None and ss2 is not None:
                metrics[m] = np.concatenate([ss1, ss2])

        return BinaryData(
            system=system,
            human=human,
            mask=mask,
            metric=metrics,
        )

    def subsample_human(
        self,
        n_human: int,
        rng: Optional[Union[np.random.Generator, int]] = None,
    ) -> 'BinaryData':
        assert n_human <= self.mask.sum()

        new_mask = np.zeros_like(self.mask, dtype=bool)
        new_human = np.ones_like(self.mask, dtype=int) * 255
        ixs = np.nonzero(self.mask)[0]

        if rng is not None:
            if type(rng) is int:
                rng = np.random.default_rng(rng)
            rng.shuffle(ixs)

        new_mask[ixs[:n_human]] = True
        new_human[ixs[:n_human]] = self.human[ixs[:n_human]]

        result = BinaryData(
            system=self.system,
            human=new_human,
            mask=new_mask,
            metric=self.metric,
        )
        result.check_integrity()
        return result


class BinaryDataset:

    def __init__(self, data: List[BinaryData]):
        for d in data:
            d.check_integrity()

        self.sys = {d.system for d in data}
        self.ms = {
            m
            for d in data
            for m in d.metric.keys()
        }
        self.store = {
            d.system: d
            for d in data
        }

    def systems(self) -> List[str]:
        return sorted(self.sys)

    def metrics(self) -> List[str]:
        return sorted(self.ms)

    def concatenate_for_metric(
        self,
        metric_name: str
    ) -> BinaryData:
        data = [
            d
            for d in self.store.values()
            if metric_name in d.metric.keys()
        ]
        data = sorted(data, key=lambda d: d.system)

        systems = []
        masks = []
        humans = []
        metrics = []

        for d in data:
            systems.append(d.system)
            masks.append(d.mask)
            humans.append(d.human)
            metrics.append(d.metric[metric_name])

        res = BinaryData(
            system="__".join(systems),
            human=np.concatenate(humans),
            mask=np.concatenate(masks),
            metric={metric_name: np.concatenate(metrics)}
        )
        res.check_integrity()

        return res

    def __getitem__(self, item: str) -> BinaryData:
        if item not in self.sys:
            raise ValueError(f"unknown system {item}")
        return self.store[item]

    def subsample_human(
        self,
        n_human: int,
        rng: Optional[Union[int, np.random.Generator]] = None,
    ) -> 'BinaryDataset':
        if type(rng) is int:
            rng = np.random.default_rng(rng)
        return BinaryDataset(
            [d.subsample_human(n_human, rng) for d in self.store.values()])
