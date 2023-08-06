"""Command-line interface."""
import click, argparse
from theoval.binary.base import BinaryArgs
from theoval.preference.base import PreferenceArgs
from theoval.binary.experiment_runner import run_experiment as run_binary_experiment
from theoval.preference.experiment_runner import run_experiment as run_preference_experiment


def get_args(etype, input_data, output_path, metrics, systems):

    if etype == 'binary':
        oargs = BinaryArgs()
        oargs.ipath = input_data
        oargs.opath = output_path
        oargs.metrics = metrics
        oargs.systems = systems
    else:
        oargs = PreferenceArgs()
        oargs.ipath = input_data
        oargs.opath = output_path
        oargs.metrics = metrics
        oargs.systems = systems

    return oargs


@click.command()
@click.version_option()
@click.option('-e', '--etype', required=True, type=click.Choice(['binary', 'preference']))
@click.option('-i', '--input_data', required=True)
@click.option('-o', '--output_path', required=True)
@click.option('-m', '--metrics', default=None, multiple=True)
@click.option('-s', '--systems', default=None, multiple=True)
def main(
     etype,
     input_data,
     output_path,
     metrics,
     systems,
) -> None:
    args = get_args(etype, input_data, output_path, metrics, systems)
    if etype == 'binary':
        run_binary_experiment(args)
    elif etype == 'preference':
        run_preference_experiment(args)


@click.command()
@click.version_option()
@click.option('-i', '--input_data', required=True)
@click.option('-o', '--output_path', required=True)
@click.option('-m', '--metrics', default=None, multiple=True)
@click.option('-s', '--systems', default=None, multiple=True)
def binary(
     input_data,
     output_path,
     metrics,
     systems,
) -> None:
    args = get_args('binary', input_data, output_path, metrics, systems)
    run_binary_experiment(args)



@click.command()
@click.version_option()
@click.option('-i', '--input_data', required=True)
@click.option('-o', '--output_path', required=True)
@click.option('-m', '--metrics', default=None, multiple=True)
@click.option('-s', '--systems', default=None, multiple=True)
def preference(
     input_data,
     output_path,
     metrics,
     systems,
) -> None:
    args = get_args('preference', input_data, output_path, metrics, systems)
    run_preference_experiment(args)


if __name__ == "__main__":
    main(prog_name="theoval")  # pragma: no cover
