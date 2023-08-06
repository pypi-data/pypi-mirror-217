import json
from typing import *
import numpy as np
from collections import defaultdict
from theoval.preference.base import ComparisonData, ComparisonDataset, CONVERSION_METHOD


def _load_data_from_path(
        path: str
) -> List[Dict]:
    samples = []
    with open(path, 'rt', encoding='utf-8') as ifile:
        for line in ifile:
            idict = json.loads(line)
            samples.append(idict)
    return samples


def _load_system_ratings(samples: List[Dict]):
    system_to_metric_to_idx_to_rating = defaultdict(lambda: defaultdict(lambda: {}))
    for sample in samples:
        idx = sample['sample_id']
        metric_name = sample['metric_name']
        metric_score0 = sample['metric_score0']
        metric_score1 = sample['metric_score1']
        system_name0 = sample['system_name0']
        system_name1 = sample['system_name1']

        system_to_metric_to_idx_to_rating[(system_name0, system_name1)][metric_name][idx] = (
        metric_score0, metric_score1)

    system_to_mratings = {}
    for system, metric_to_idx_to_rating in system_to_metric_to_idx_to_rating.items():
        metric_to_scores = {}
        for metric, idx_to_mrating in metric_to_idx_to_rating.items():
            max_idx = max(idx_to_mrating.keys())
            metric_scores = 255 * np.ones(shape=(max_idx + 1, 2), dtype=float)
            for idx, mrating in idx_to_mrating.items():
                metric_scores[idx][0] = mrating[0]
                metric_scores[idx][1] = mrating[1]
            metric_to_scores[metric] = metric_scores
        system_to_mratings[system] = metric_to_scores
    return system_to_mratings


def _load_human_data(samples: List[Dict]):
    system_to_idx_to_hrating = defaultdict(lambda: {})
    for sample in samples:
        idx = sample['sample_id']
        human_rating = sample.get('human_rating')
        system_name0 = sample['system_name0']
        system_name1 = sample['system_name1']
        system_to_idx_to_hrating[(system_name0, system_name1)][idx] = human_rating

    system_to_hrating = {}
    for system, idx_to_hrating in system_to_idx_to_hrating.items():
        max_idx = max(idx_to_hrating.keys())
        human_scores = 255 * np.ones(shape=(max_idx + 1,), dtype=int)
        for idx, hrating in idx_to_hrating.items():
            if hrating in {-1, 0, 1}:
                human_scores[idx] = hrating
            else:
                human_scores[idx] = 255

        mask = np.where(human_scores == 255, False, True)
        system_to_hrating[system] = (human_scores, mask)

    return system_to_hrating


def _create_preference_dataset(
        samples: List[Dict],
        conversion_methods: List[str] = CONVERSION_METHOD.__args__
):

    human_scores = _load_human_data(samples)
    metric_scores = _load_system_ratings(samples)
    preference_data = []
    for (system0, system1), human in human_scores.items():
        metrics_to_scores = metric_scores[(system0, system1)]

        data = ComparisonData(
            human=human[0],
            system1=system0,
            system2=system1,
            mask=human[1],
            metric=metrics_to_scores,
            conversion_methods=conversion_methods
        )

        data.check_integrity()
        preference_data.append(data)
    return ComparisonDataset(preference_data)


def create_preference_dataset(path, conversion_methods=CONVERSION_METHOD.__args__):
    samples = _load_data_from_path(path)
    preference_dataset = _create_preference_dataset(samples, conversion_methods=conversion_methods)
    return preference_dataset