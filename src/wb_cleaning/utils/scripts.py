'''
Module containing common functions used across the scripts.
'''
from pathlib import Path
import logging
import subprocess
import os
import sys
import hashlib
import json
import yaml
from dask.distributed import Client, LocalCluster
# export DASK_DISTRIBUTED__SCHEDULER__ALLOWED_FAILURES=210
# export DASK_DISTRIBUTED__COMM__TIMEOUTS__CONNECT=60
# export DASK_DISTRIBUTED__COMM__RETRY__COUNT=20


def configure_logger(log_level):
    '''
    Configures how the logger output is formatted.
    '''
    logging.basicConfig(stream=sys.stdout,
                        level=log_level,
                        datefmt='%Y-%m-%d %H:%M:%S',
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def load_config(config_path: Path, config_root: str, logger=None) -> dict:
    '''
    Function to load a yaml config file and returns a dictionary version of the config.
    '''
    if logger is not None:
        logger.info(f'Load config file {config_path}...')
    with open(config_path) as cfg_file:
        config = yaml.safe_load(cfg_file)
        config = config[config_root]

    if logger is not None:
        logger.info(config)

    return config


def generate_model_hash(config: dict) -> str:
    '''
    Computes an md5 hash of a config which can be used as a unique identifier.

    NOTE: Changing the hashing algorithm below will essentially reset any stateful
    processes that use ids based on this method. Example, cleaning configurations with the
    same values will appear on the database simply because the algorithm for computing the
    unique id is using this.
    '''
    # return hashlib.md5(json.dumps(config, sort_keys=True).encode('utf-8')).hexdigest()
    return hashlib.md5(''.join(sorted(json.dumps(config))).encode('utf-8')).hexdigest()


def create_get_directory(parent: Path, child: str) -> Path:
    '''
    A helper function that automatically creates a directory if it doesn't exist.
    '''
    path = parent / child
    if not path.exists():
        path.mkdir(parents=True)

    return path


def create_dask_cluster(logger=None, n_workers=None, return_cluster=False):
    '''
    This function creates a local dask cluster.
    '''
    if n_workers is not None:
        n_workers = int(n_workers)

    if logger:
        logger.info('Creating dask client...')
    cluster = LocalCluster(n_workers=max(1, os.cpu_count() - 4) if n_workers is None else n_workers, dashboard_address=':8887',
                           threads_per_worker=1, processes=True, memory_limit=0)
    client = Client(cluster)
    if logger:
        logger.info(client)
        logger.info(client.dashboard_link)

    if not return_cluster:
        return client
    else:
        return cluster, client


def checkpoint_log(logger, timer=None, message=''):
    '''
    Given a contexttimer instance, this logs a message with elapsed time since the timer was created.
    '''
    elapsed_time = timer.elapsed / 60 if timer else None
    if logger:
        logger.info('Time elapsed now in minutes: %s %s',
                    elapsed_time, message)
    else:
        print(f'Time elapsed now in minutes: {elapsed_time} {message}')


def get_cleaned_corpus_id(cleaned_docs_dir):
    '''
    This gets a unique id that is based on the content of the files in the given directory.
    There is an assumption that the files being checked are under sub-directories.
    '''
    cleaned_corpus_id = subprocess.check_output("md5sum " + cleaned_docs_dir.resolve().__str__(
    ) + "/*/*.txt | awk '{print $1}' | md5sum | awk '{print $1}'", shell=True)

    # The previous command returns a binary value like this: `b'07591edc636a73eafe9bea6eb2aaf3a6\n'` so we convert to str.
    cleaned_corpus_id = cleaned_corpus_id.strip().decode('utf-8')

    return cleaned_corpus_id
