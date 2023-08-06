from __future__ import annotations
from typing import TypeAlias
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
    new_config = {k: v for k, v in locals().items() if v is not None}
    create_hpc_config_file_if_required()
    current_config = get_hpc_config()
    updated_config = {**current_config, **new_config}
    save_hpc_config(updated_config)
