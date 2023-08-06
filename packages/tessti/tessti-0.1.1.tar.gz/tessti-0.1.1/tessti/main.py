from __future__ import annotations
from typing import Any, Sequence
import toml
import fire
from pathlib import Path
from .scheduler import HPCScheduler
from .config import parse, create_configs, set_hpc_config, pretty_print_hpc_config


def run(config_path: str | Path) -> None:
    import os
    config = toml.load(config_path)
    working_dir = Path(config['run']['working_dir']).resolve()
    os.chdir(working_dir)
    print(80 * '-')
    print(os.getcwd())
    print(80 * '-')
    file, function, args = config['run']['file'], config['run']['function'], config['args']
    exec(f"from {file} import {function}")
    eval(f"{function}(**{args})")


def schedule(
    *,
    # ___________________________ SLURM
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
    # _____________________________ JOB
    file: str,
    function: str,
    args: dict[Any: Any],
    # ________________________ SCHEDULE
    name: str,
    schedule: dict[str: Sequence[Any]],
) -> None:
    schedule_config_file = create_configs(**parse(**locals()))
    HPCScheduler(config_path=schedule_config_file).run()


def cli() -> None:
    fire.Fire({'run': run,
               'schedule': schedule,
               'set-config': set_hpc_config,
               'get-config': pretty_print_hpc_config})
