import json
import numpy as np
from typing import List, Dict
from collections import defaultdict
from theoval.binary.base import BinaryDataset, BinaryData


def _load_data_from_path(
        path: str
) -> List[Dict]:
    samples = []
    with open(path, 'rt', encoding='utf-8') as ifile:
        for line in ifile:
            idict = json.loads(line)
            samples.append(idict)
    return samples


def _load_human_data(samples: List[Dict]):
    system_to_idx_to_hrating = defaultdict(lambda : {})
    for sample in samples:
        idx = sample['sample_id']
        human_rating = sample.get('human_rating')
        system_name = sample['system_name']
        system_to_idx_to_hrating[system_name][idx] = human_rating

    system_to_hrating = {}
    for system, idx_to_hrating in system_to_idx_to_hrating.items():
        max_idx = max(idx_to_hrating.keys())
        human_scores = 255 * np.ones(shape=(max_idx + 1, ), dtype=int)
        for idx, hrating in idx_to_hrating.items():
            if hrating in {0, 1}:
                human_scores[idx] = hrating
            else:
                human_scores[idx] = 255

        mask = np.where(human_scores == 255, False, True)
        system_to_hrating[system] = (human_scores, mask)

    return system_to_hrating


def _load_system_ratings(samples: List[Dict]):
    system_to_metric_to_idx_to_rating = defaultdict(lambda : defaultdict(lambda :{}))
    for sample in samples:
        idx = sample['sample_id']
        metric_name = sample['metric_name']
        metric_score = sample['metric_score']
        system_name = sample['system_name']

        system_to_metric_to_idx_to_rating[system_name][metric_name][idx] = metric_score

    system_to_mratings = {}
    for system, metric_to_idx_to_rating in system_to_metric_to_idx_to_rating.items():
        metric_to_scores = {}
        for metric, idx_to_mrating in metric_to_idx_to_rating.items():
            max_idx = max(idx_to_mrating.keys())
            metric_scores = 255 * np.ones(shape=(max_idx + 1, ), dtype=float)
            for idx, mrating in idx_to_mrating.items():
                metric_scores[idx] = mrating
            metric_to_scores[metric] = metric_scores
        system_to_mratings[system] = metric_to_scores
    return system_to_mratings


def create_binary_dataset(path):
    samples = _load_data_from_path(path)
    binary_dataset = _create_binary_dataset(samples)
    return binary_dataset


def _create_binary_dataset(samples: List[Dict]) -> BinaryDataset:
    human_scores = _load_human_data(samples)
    metric_scores = _load_system_ratings(samples)

    binary_data = []
    for system, human in human_scores.items():
        metrics_to_scores = metric_scores[system]

        data = BinaryData(
            system=system,
            human=human[0],
            mask=human[1],
            metric=metrics_to_scores
        )
        data.check_integrity()
        binary_data.append(data)

    return BinaryDataset(data=binary_data)

