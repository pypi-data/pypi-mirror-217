# TESSTI - The Easiest SLURM Scheduler There Is

Tessti has been made to be the simplest SLURM scheduler possible. <br>
It does not offer much but it works, and is extremely easy to use.


## Getting Started

Suppose you run locally a function `f` in a script named `script.py` in a folder `/some/path/` with some arguments. <br>
The end of the `script.py` may look like this:
```python
if __name__ == '__main__':
    f(arg1=value1, arg2=value2)
```

You want to schedule many executions of this script with different values for arguments `arg1` and `arg2`. <br>
You will be able to run something like:

```
$ tessti schedule --file some/path/script.py --function f --args arg1=value1,arg2=value2 --schedule arg1=[value3, value4],arg2=[value5, value6]
```

The `--args` flag defines the default parameters, whereas the `--schedule` flag defines all the runs to be requested to SLURM.


## Comprehensive overview

`tessti` relies on (toml) config files. It will creates one config file per job to run, plus two special config files, one acting as a template to generate the job configs, and one for the schedule itself.

Each config is composed of two parts:
1. the SLURM config, where ressources are requested, and general environment is set up.
2. the script config, required to execute a single job.

The SLURM config can be set globally, so that it doesn't need to be specified for every schedule.

Hence, tessti exposes three commands:
1. `tessti set-config`: allows to update the global SLURM configuration. <br>
2. `tessti get-config`: displays the current SLURM configuration.
3. `tessti schedule`: requests SLURM jobs based on the SLURM and script configs. SLURM config can also be modified here for this schedule only.

(Technically, there is a fourth command `run`. This is the one called by SLURM jobs. You are not really supposed to use it but of course you can if you want to).


For each of these three commands, you can run `tessti command --help` to see the parameters.
For the sake of completeness, they are written bellow as well.


### The SLURM configuration

- `jobs_dir: str`: relative or absolute path of the directory in which the SLURM inputs and outputs files will be placed. <br>
*Defaults to 'jobs'*. 
- `partition: str`: HPC partition to use. <br>
*Defaults to 'publigpu'*. 
- `account: str`: HPC account to use. <br>
*Defaults to 'miv'*.
- `node: int`: number of node(s). <br>
*Defaults to 1*.
- `task: int`: number of task(s) per node. <br>
- `cpu: int`: CPU cores per task. <br>
*Defaults to 1*.
- `gpu: int`: GPU per node. <br>
*Defaults to 1*.
- `ram: int`: RAM memory in Go. <br>
*Defaults to 16*.
- `constraint: str`: Any constraint for the nodes requested. <br>
*Defaults to `'gpua100|gpurtx6000|gpurtx5000|gpuv100'`.*
- `modules: list[str]`: Modules that must the loaded before starting a job. <br>
*Defaults to `['python/Anaconda3-2019', 'cuda/cuda-11.8', 'gcc/gcc-11']`.*
- `commands: list[str]`: Any command that must be executed before starting a job.
*Defaults to `['source /usr/local/Anaconda/Anaconda3-2019.07/etc/profile.d/conda.sh', 'conda deactivate', 'conda activate torch2cu118']`*.

**WARNING**: when providing list of strings in argument, **do not use spaces between list elements**.

### The schedule parameters


- Job parameters:
    - `file: str`: relative or absolute path to the file each job must execute. The '.py' extension is not required.
    - `function: str`: name of the function within `file.py` that each job must execute.
    - `args: dict[Any: Any]`: Base args of the function within `file.py` that each job must execute. For each job, exactly one of these args will be overwritten.
- Scheduler parameters:
    - `name: str`: base name for the whole schedule. Created jobs will be named alike `name_arg=value.job`.
    - `schedule: dict[str: Sequence[Any]]`: Sequence of values for each arg that must be set in a separated job.

**WARNING**: when providing list of strings in argument, **do not use spaces between list elements**.

## Some examples

The relevant code can be found in the [example](example/) folder.

The file `script.py` contains a function `add` with the following signature:
```python
add(a: int, b: int) -> int:
```

First, let's set up the global SLURM config, which will be the base for all subsequent schedules.

```
$ tessti set-config --account some_account_name --cpu 2 --gpu 4 --commands ['command1','command2']
```

**WARNING**: when providing list of strings in argument, **do not use spaces between list elements**.


We can then check the current configuration with
```
$ tessti get-config
```

Now let's schedule some jobs. We also change some SLURM configuration parameters on the fly for this schedule only.

```
$ tessti schedule --file example/script.py --function add --args a=0,b=0 --schedule a=[1,2],b=[3,4] --cpu 4
```

**WARNING**: when providing list of parameters with `--args` and `--schedule`, **do not use spaces between list elements**.


This schedule sets the defaults values for the `add()` function both to 0 through the `args` keyword argument. <br>
It schedules four jobs: <br>
    - one with `a=1, b=0` (first scheduled value for `a`, default value for `b`). <br>
    - one with `a=2, b=0` (second scheduled value for `a`, default value for `b`). <br>
    - one with `a=0, b=4` (default value for `a`, first scheduled values for `b`). <br>
    - one with `a=0, b=5` (default value for `a`, second scheduled value `b`). <br>


You can see the generated files in a folder within the directory containing the file to be executed, named after the `--jobs_dir` flag.

You can check in the generated `schedule.toml` file that the SLURM config was indeed updated and that the global config (as returned by `tessti get-config`) was **not updated. 


## Using the schedule function

If you prefer not to use the tessti CLI, you are free to create a python script that directly uses tessti's schedule function. <br>
Please refer to the example in `example/schedule.py`.