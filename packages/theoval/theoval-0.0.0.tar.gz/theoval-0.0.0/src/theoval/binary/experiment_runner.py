import json

import numpyro

from tqdm import tqdm

from theoval.stats.mcmc import MCMCRunner
from theoval.binary.data_loader import create_binary_dataset
from theoval.binary.base import BinaryArgs


def run_experiment(args: BinaryArgs):
    binary_dataset = create_binary_dataset(args.ipath)
    numpyro.set_host_device_count(8)

    runner = MCMCRunner(verbose=False)

    if args.systems is None or args.systems == 'all' or len(args.systems) == 0:
        systems = binary_dataset.systems()
    else:
        systems = args.systems

    if args.metrics is None or args.metrics == 'all' or len(args.metrics) == 0:
        metrics = binary_dataset.metrics()
    else:
        metrics = args.metrics

    mu = {
        s: {}
        for s in systems
    }
    sigma = {
        s: {}
        for s in systems
    }

    for s in tqdm(systems):
        data = binary_dataset[s]
        human_res = runner.run(data.oracle_only_experiment())
        mu[s]['Human'] = human_res.mean()
        sigma[s]['Human'] = human_res.std()

        for m in tqdm(metrics):
            if m not in data.metric.keys():
                continue
            m_res = runner.run(data.full_model(metric_name=m))
            mu[s][m] = m_res.mean()
            sigma[s][m] = m_res.std()

    with open(args.opath, 'wt', encoding='utf-8') as ofile:
        odict = {
            'mu': mu,
            'sigma': sigma,
        }

        json.dump(odict, ofile)
