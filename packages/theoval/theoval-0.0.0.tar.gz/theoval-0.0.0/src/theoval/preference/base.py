
from dataclasses import dataclass
from typing import Dict, List, Tuple, Union, Optional

import numpy as np
from multiprocessing import Pool
from scipy.spatial.distance import cosine
from theoval.stats.base import BinomialExperiment, TrinomialExperiment
from theoval.preference.experiment import (
    HumanOnlyExperiment,
    SimpleMixExperiment,
    SimpleFixedMixtureExperiment,
    FullMixExperiment,
    FullFixedMixtureExperiment,
)
from theoval.preference.convert_scalar import CONVERSION_METHOD, conversion


class PreferenceArgs:
    ipath: str
    opath: str
    systems: Union[List, str]
    metrics: Union[List, str]

@dataclass
class ComparisonData:
    system1: str
    system2: str
    human: np.array
    mask: np.array
    metric: Dict[str, np.array]
    cache: Optional[Dict[Tuple[str, str], np.array]] = None
    conversion_methods: Optional[List[str]] = CONVERSION_METHOD.__args__
    parallel: bool = False

    def __post_init__(self):
        if self.cache is None:
            cache = {}
            for metric, scores in self.metric.items():
                if not self.parallel:
                    for method in self.conversion_methods:
                        cache[(metric, method)] = self.convert_metric(
                            metric_name=metric,
                            conversion_method=method,
                        )
                else:
                    items = [(metric, method) for method in self.conversion_methods]
                    with Pool(processes=4) as pool:
                        counter = 0
                        for result in pool.starmap(self.convert_metric, items): #pray that starmap is orderpreserving
                            cache[(metric, items[counter][1])] = result
                            counter += 1

            self.cache = cache

    def __len__(self):
        return self.human.shape[0]

    def __check_lengths(self) -> bool:
        len_h = self.human.shape[0]

        if self.mask.shape[0] != len_h:
            raise ValueError(f"mask length {self.mask.shape[0]} "
                             f"does not match annotation length {len_h}")

        for m, ss in self.metric.items():
            if ss.shape != (len_h, 2):
                raise ValueError(f"length of metric scores {m} "
                                 f"do not match annotation length {len_h}")

        return True

    def __check_values(self) -> bool:
        if not np.isfinite(self.human[self.mask]).all():
            raise ValueError(f"self.human contains inf/nan values "
                             f"that are not masked by self.mask")

        not_1_mask = np.abs(self.human[self.mask]) != 1
        if not (self.human[self.mask][not_1_mask] == 0).all():
            raise ValueError(f"human comparisons self.human "
                             f"contain values that are not in [-1, 0, 1]")

        for m, ss in self.metric.items():
            if not np.isfinite(ss).all():
                raise ValueError(f"scalar values for metric {m} "
                                 f"contain values that are inf/nan")

        return True

    def check_integrity(self) -> bool:
        self.__check_lengths()
        self.__check_values()

        return True

    def flip(self) -> 'ComparisonData':
        return ComparisonData(
            system1=self.system2,
            system2=self.system1,
            human=-self.human,
            mask=self.mask,
            metric={
                m: scores[:, [1, 0]]
                for m, scores in self.metric.items()
            },
            cache={
                key_tup: - ss
                for key_tup, ss in self.cache.items()
            }
        )

    def subsample_human(self, n_human: int, ixs: np.ndarray = None) -> 'ComparisonData':
        assert n_human <= self.mask.sum()

        n_mask = np.zeros_like(self.mask, dtype=bool)
        if ixs is None:
            ixs = np.nonzero(self.mask)[0]
        n_mask[ixs[:n_human]] = True

        result = ComparisonData(
            system1=self.system1,
            system2=self.system2,
            human=self.human,
            mask=n_mask,
            metric=self.metric,
            cache=self.cache,
        )
        result.check_integrity()

        return result

    def oracle_data(self) -> TrinomialExperiment:
        return TrinomialExperiment(
            win=(self.human[self.mask] == 1).sum(),
            draw=(self.human[self.mask] == 0).sum(),
            loss=(self.human[self.mask] == -1).sum(),
        )

    def convert_metric(
        self,
        metric_name: str,
        conversion_method: CONVERSION_METHOD = "naive",
    ) -> np.array:
        if self.cache is not None:
            return self.cache[(metric_name, conversion_method)]
        raw_metric = self.metric[metric_name]
        converter = conversion(conversion_method)
        converter.fit(
            scalars_sys1=raw_metric[self.mask, 0],
            scalars_sys2=raw_metric[self.mask, 1],
            human_comparisons=self.human[self.mask],
        )
        return converter.transform(
            scalars_sys1=raw_metric[:, 0],
            scalars_sys2=raw_metric[:, 1],
        )

    def metric_data(
        self,
        metric_name: str,
        simplified: bool = False,
        conversion_method: CONVERSION_METHOD = "naive",
    ) -> Union[BinomialExperiment, TrinomialExperiment]:
        ss = self.convert_metric(metric_name, conversion_method)
        win = (ss[~self.mask] == 1).sum()
        draw = (ss[~self.mask] == 0).sum()
        loss = (ss[~self.mask] == -1).sum()
        if simplified:
            return BinomialExperiment(
                pos=win,
                tot=win+loss,
            )
        else:
            return TrinomialExperiment(
                win=win,
                draw=draw,
                loss=loss,
            )

    def mixtures(
        self,
        metric_name: str,
        simplified: bool = False,
        conversion_method: CONVERSION_METHOD = "naive",
    ) -> Dict[str, Union[BinomialExperiment, TrinomialExperiment]]:

        ss = self.convert_metric(metric_name, conversion_method)[self.mask]
        hs = self.human[self.mask]

        result = {}
        for n, lbl in [("win", 1), ("draw", 0), ("loss", -1)]:
            sub_mask = hs == lbl

            win = (ss[sub_mask] == 1).sum()
            draw = (ss[sub_mask] == 0).sum()
            loss = (ss[sub_mask] == -1).sum()

            if simplified:
                result[n] = BinomialExperiment(
                    pos=win,
                    tot=win+loss,
                )
            else:
                result[n] = TrinomialExperiment(
                    win=win,
                    draw=draw,
                    loss=loss,
                )

        return result

    def win_mixture(
        self,
        metric_name: str,
        simplified: bool = False,
        conversion_method: CONVERSION_METHOD = "naive",
    ) -> Union[BinomialExperiment, TrinomialExperiment]:
        return self.mixtures(metric_name, simplified, conversion_method)['win']

    def draw_mixture(
            self,
            metric_name: str,
            simplified: bool = False,
            conversion_method: CONVERSION_METHOD = "naive",
    ) -> Union[BinomialExperiment, TrinomialExperiment]:
        return self.mixtures(metric_name, simplified, conversion_method)['draw']

    def loss_mixture(
        self,
        metric_name: str,
        simplified: bool = False,
        conversion_method: CONVERSION_METHOD = "naive",
    ) -> Union[BinomialExperiment, TrinomialExperiment]:
        return self.mixtures(metric_name, simplified, conversion_method)['loss']

    def mu(
        self,
        metric_name: str,
        conversion_method: CONVERSION_METHOD = "naive",
    ) -> np.array:
        mix_data = self.mixtures(
            metric_name=metric_name,
            simplified=False,
            conversion_method=conversion_method,
        )

        mu = np.array([
            mix_data['win'].p(),
            mix_data['draw'].p(),
            mix_data['loss'].p(),
        ]).T

        return mu

    def mu_steady_state(
        self,
        metric_name: str,
        conversion_method: CONVERSION_METHOD = "naive",
    ):
        mu = self.mu(metric_name, conversion_method)

        vals, vs = np.linalg.eig(mu)
        assert np.allclose(float(np.max(vals)), 1.0, atol=1e-6)
        idx = vals.argsort()[::-1]

        v = vs[:, idx[0]]
        v /= v.sum()
        # assert np.allclose(np.imag(v), 0., atol=1e-7)
        return np.real(v)

    def bias_score(
            self,
            metric_name: str,
            conversion_method: CONVERSION_METHOD = "naive"
    ):
        steady_state = self.mu_steady_state(metric_name, conversion_method)
        unbiased_vec = np.array([0.5, -1, 0.5])
        complete_draw = np.array([0.0, 1.0, 0.0])
        complete_loss = np.array([0.0, 0.0, 1.0])
        steady_vector = steady_state - complete_draw
        maximal_vector = complete_loss - complete_draw
        bias_cosine = cosine(unbiased_vec, steady_vector)
        max_cosine = cosine(unbiased_vec, maximal_vector)

        bias_angle = np.degrees(np.arccos(1 - bias_cosine))
        max_angle = np.degrees(np.arccos(1 - max_cosine))
        bias_score = bias_angle/max_angle

        if steady_state[0] > steady_state[2]:
            bias_direction = 1
        elif steady_state[0] < steady_state[2]:
            bias_direction = -1
        else:
            bias_direction = 0

        return bias_score, bias_direction


    def human_only_experiment(self):
        return HumanOnlyExperiment(oracle=self.oracle_data())

    def simple_experiment(
        self,
        metric_name: str,
        conversion_method: CONVERSION_METHOD = "naive",
    ) -> SimpleMixExperiment:
        mixes = self.mixtures(
            metric_name, simplified=True, conversion_method=conversion_method)
        return SimpleMixExperiment(
            win_mix=mixes['win'],
            draw_mix=mixes['draw'],
            loss_mix=mixes['loss'],
            oracle=self.oracle_data(),
            metric=self.metric_data(
                metric_name,
                simplified=True,
                conversion_method=conversion_method,
            ),
        )

    def simple_fixed_experiment(
        self,
        metric_name: str,
        conversion_method: CONVERSION_METHOD = "naive",
    ):
        mixes = self.mixtures(
            metric_name=metric_name,
            simplified=True,
            conversion_method=conversion_method,
        )
        return SimpleFixedMixtureExperiment(
            win_mix=mixes['win'].p_win(),
            draw_mix=mixes['draw'].p_win(),
            loss_mix=mixes['loss'].p_win(),
            oracle=self.oracle_data(),
            metric=self.metric_data(
                metric_name,
                simplified=True,
                conversion_method=conversion_method,
            ),
        )

    def full_experiment(
        self,
        metric_name: str,
        conversion_method: CONVERSION_METHOD = "naive",
    ) -> FullMixExperiment:
        mixes = self.mixtures(
            metric_name,
            simplified=False,
            conversion_method=conversion_method,
        )
        return FullMixExperiment(
            win_mix=mixes['win'],
            draw_mix=mixes['draw'],
            loss_mix=mixes['loss'],
            oracle=self.oracle_data(),
            metric=self.metric_data(
                metric_name,
                simplified=False,
                conversion_method=conversion_method,
            ),
        )

    def full_fixed_experiment(
        self,
        metric_name: str,
        conversion_method: CONVERSION_METHOD = "naive",
    ):
        mixes = self.mixtures(
            metric_name=metric_name,
            simplified=False,
            conversion_method=conversion_method,
        )
        return FullFixedMixtureExperiment(
            win_mix=mixes['win'].p(),
            draw_mix=mixes['draw'].p(),
            loss_mix=mixes['loss'].p(),
            oracle=self.oracle_data(),
            metric=self.metric_data(
                metric_name,
                simplified=False,
                conversion_method=conversion_method,
            ),
        )


    @staticmethod
    def concatenate(data1: 'ComparisonData', data2: 'ComparisonData', metrics: List[str], primary_system: str):
        if not data1.system1 == primary_system:
            data1 = data1.flip()
        if not data2.system1 == primary_system:
            data2 = data2.flip()
        cmask = np.concatenate((data1.mask, data2.mask))
        chuman = np.concatenate((data1.human, data2.human))
        ccache = {}
        for key in data1.cache.keys():
            if key[0] not in metrics:
                continue

            value1 = data1.cache[key]
            value2 = data2.cache[key]
            cvalue = np.concatenate((value1, value2))
            ccache[key] = cvalue
        cmetric = {}
        for key in data1.metric.keys():
            if key[0] not in metrics:
                continue
            value1 = data1.metric[key]
            value2 = data2.metric[key]
            cvalue = np.concatenate((value1, value2), axis=1)
            cmetric[key] = cvalue

        return ComparisonData(
            system1=primary_system,
            system2='all',
            metric=cmetric,
            cache=ccache,
            human=chuman,
            mask=cmask
        )

class ComparisonDataset:

    def __init__(self, comparisons: List[ComparisonData]):
        for c in comparisons:
            c.check_integrity()

        self.sys = {
                c.system1 for c in comparisons
            }.union({
                c.system2 for c in comparisons
            })

        self.ms = {
            metric
            for c in comparisons
            for metric in c.metric.keys()
        }

        self.store = {
            (c.system1, c.system2): c
            for c in comparisons
        }
        for c in comparisons:
            self.store[(c.system2, c.system1)]: c.flip()

        self.human_shuffle_idx = None

    def subsample_human(self, n_human: int, use_shuffled_idx:bool = False) -> 'ComparisonDataset':
        all_sys = self.systems()
        return ComparisonDataset([
            syspair_store.subsample_human(n_human, self.human_shuffle_idx if use_shuffled_idx and self.human_shuffle_idx is not None else None)
            for syspair_store in self.store.values()
        ])

    def shuffle_human(self):
        all_sys = self.systems()
        s1, s2 = all_sys[0], all_sys[2]
        old_mask = self.store[(s1, s2)].mask
        ixs = np.nonzero(old_mask)[0]
        np.random.shuffle(ixs)
        self.human_shuffle_idx = ixs

    def systems(self) -> List[str]:
        return sorted(self.sys)

    def metrics(self) -> List[str]:
        return sorted(self.ms)

    def __getitem__(self, item: Tuple[str, str]) -> ComparisonData:
        s1, s2 = item
        if s1 not in self.sys:
            raise ValueError(f"unknown system {s1} in lookup {item}")
        if s2 not in self.sys:
            raise ValueError(f"unknown system {s2} in lookup {item}")

        result = self.store.get((s1, s2))
        if result is None:
            result = self.store.get((s2, s1))
            if result is None:
                raise KeyError(f"no comparison data for {item}")
            else:
                return result.flip()
        else:
            return result


