# from __future__ import annotations
# from typing import Any, Sequence
# import argparse
# from .main import schedule


# def parse_args() -> argparse.Namespace:
#     parser = argparse.ArgumentParser('Test CLI')
#     parser.add_argument('--working_dir', type=str, default='.')
#     parser.add_argument('--jobs_dir', type=str, default='jobs')
#     parser.add_argument('--partition', type=str, default='publicgpu')
#     parser.add_argument('--account', type=str, default='miv')
#     parser.add_argument('--node', type=int, default=1)
#     parser.add_argument('--task', type=int, default=1)
#     parser.add_argument('--cpu', type=int, default=1)
#     parser.add_argument('--gpu', type=int, default=1)
#     parser.add_argument('--ram', type=int, default=16)
#     parser.add_argument('--constraint', type=str,
#                         default='gpua100|gpurtx6000|gpurtx5000|gpuv100')
#     parser.add_argument('--modules', type=list[str], nargs='+',
#                         default=['python/Anaconda3-2019',
#                                  'cuda/cuda-11.8',
#                                  'gcc/gcc-11'])
#     parser.add_argument('--commands', type=list[str], nargs='+',
#                         default=[
#                             'source /usr/local/Anaconda/Anaconda3-2019.07/etc/profile.d/conda.sh',
#                             'conda deactivate',
#                             'conda activate torch2cu118'])
#     parser.add_argument('--file', type=str)
#     parser.add_argument('--function', type=str)
#     parser.add_argument('--args', type=dict[Any: Any])
#     parser.add_argument('--name', type=str)
#     parser.add_argument('--schedule', type=dict[str: Sequence[Any]])
#     args = parser.parse_args()
#     return args


# def main() -> None:
#     schedule(**vars(parse_args()))
