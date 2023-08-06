from __future__ import annotations
from typing import TypeAlias, Any, Sequence
import toml
from pathlib import Path
from prettytable import PrettyTable


ConfigHPC: TypeAlias = dict[str: int | str | list[str]]
CONFIG_PATH = Path(__file__).resolve().parent / '.config.toml'


def create_hpc_config_file_if_required() -> None:
    if CONFIG_PATH.exists():
        return
    f = open(CONFIG_PATH, 'w')
    f.close()


def save_hpc_config(config: ConfigHPC) -> None:
    with open(CONFIG_PATH, 'w') as file:
        toml.dump(config, file)


def get_hpc_config() -> ConfigHPC:
    return toml.load(CONFIG_PATH) if CONFIG_PATH.exists() else dict()


def pretty_print_hpc_config(max_width: int = 40) -> None:
    config = get_hpc_config()
    table = PrettyTable(["Key", "Value"], max_width=max_width)
    for k, v in config.items():
        table.add_row([k, v])
    table.title = 'HPC Configuration'
    print(table)


def set_hpc_config(
    jobs_dir: str = None,
    partition: str = None,
    account: str = None,
    node: int = None,
    task: int = None,
    cpu: int = None,
    gpu: int = None,
    ram: int = None,
    constraint: str = None,
    modules: list[str] = None,
    commands: list[str] = None,
) -> None:
    params = parse(**locals())
    new_config = {k: v for k, v in params.items() if v is not None}
    create_hpc_config_file_if_required()
    current_config = get_hpc_config()
    updated_config = {**current_config, **new_config}
    save_hpc_config(updated_config)


def resolve_config(**kwargs: ConfigHPC) -> ConfigHPC:
    """ Update a copy of the global SLURM config with given parameters for a single schedule. """
    current_slurm_config = get_hpc_config()
    for k in current_slurm_config.keys():
        if kwargs[k] is not None:
            current_slurm_config[k] = kwargs[k]
    return current_slurm_config


def create_configs(
    *,
    # ___________________________________ SLURM #
    jobs_dir: str,
    partition: str,
    account: str,
    node: int,
    task: int,
    cpu: int,
    gpu: int,
    ram: int,
    constraint: str,
    modules: list[str],
    commands: list[str],
    # _____________________________________ JOB #
    file: str,
    function: str,
    args: dict[Any: Any],
    # ________________________________ SCHEDULE #
    name: str,
    schedule: dict[str: Sequence[Any]],
) -> Path:
    # path handling
    path = Path(file)
    working_dir = path.resolve().parent
    file = path.stem
    # slurm config
    slurm_config = resolve_config(**locals())
    slurm_config['name'] = name
    # template config
    template_config = dict()
    template_config['run'] = dict(working_dir=str(working_dir), file=file, function=function)
    template_config['args'] = args
    template_config_file = (working_dir / 'template').with_suffix('.toml')
    with open(template_config_file, 'w') as config_file:
        toml.dump(template_config, config_file)
    # schedule config
    schedule_config = dict()
    schedule_config['slurm'] = slurm_config
    schedule_config['parameters'] = dict()
    for key, values in schedule.items():
        schedule_config['parameters'][key] = values
    schedule_config_file = (working_dir / 'schedule').with_suffix('.toml')
    with open(schedule_config_file, 'w') as config_file:
        toml.dump(schedule_config, config_file)
    return schedule_config_file


def parse(**kwargs: ConfigHPC) -> ConfigHPC:
    """ Handle string to list of strings or dict[str: Any]. """
    for k, v in kwargs.items():
        if k in ('modules', 'commands') and isinstance(v, str):
            kwargs[k] = v[1:-1].split(',')
        if k in ('args', 'schedule'):
            kwargs[k] = eval(f'dict({kwargs[k]})')
    return kwargs
