import json

import numpyro

from tqdm import tqdm

from theoval.stats.mcmc import MCMCRunner
from theoval.preference.data_loader import create_preference_dataset
from theoval.preference.base import PreferenceArgs
from itertools import combinations


def run_experiment(args: PreferenceArgs):

    preference_dataset = create_preference_dataset(args.ipath, conversion_methods=['naive'])
    numpyro.set_host_device_count(8)

    runner = MCMCRunner(verbose=False)

    if args.systems is None or args.systems == 'all' or len(args.systems) == 0:
        systems = preference_dataset.sys
    else:
        systems = args.systems

    if args.metrics is None or args.metrics == 'all' or len(args.metrics) == 0:
        metrics = preference_dataset.ms
    else:
        metrics = args.metrics

    sys_pairs = list(combinations(systems, r=2))

    sys_pair_keys = [f'{s1}-{s2}' for s1, s2, in sys_pairs]

    p_true = {
        s: {}
        for s in sys_pair_keys
    }
    comparisons = {
        s: {}
        for s in sys_pair_keys
    }
    p_vals = {
        s: {}
        for s in sys_pair_keys
    }

    for s1, s2 in tqdm(list(combinations(systems, r=2))):
        data = preference_dataset[(s1, s2)]
        human_res = runner.run(data.human_only_experiment())
        hum_p_true = human_res.expected_p_true().tolist()
        hum_comparison = int(human_res.comparison())
        hum_p_val = float(human_res.p_win_proba_larger())

        sys_pair_key = f'{s1}-{s2}'

        p_true[sys_pair_key]['Human'] = hum_p_true
        comparisons[sys_pair_key]['Human'] = hum_comparison
        p_vals[sys_pair_key]['Human'] = hum_p_val

        for m in tqdm(metrics):
            if m not in data.metric.keys():
                continue
            m_res = runner.run(data.full_experiment(metric_name=m))
            met_p_true = m_res.expected_p_true().tolist()
            met_comparison = int(m_res.comparison())
            met_p_val = float(m_res.p_win_proba_larger())

            p_true[sys_pair_key][m] = met_p_true
            comparisons[sys_pair_key][m] = met_comparison
            p_vals[sys_pair_key][m] = met_p_val

    with open(args.opath, 'wt', encoding='utf-8') as ofile:
        odict = {
            'p_true': p_true,
            'comparisons': comparisons,
            'p_vals': p_vals,
        }

        json.dump(odict, ofile)