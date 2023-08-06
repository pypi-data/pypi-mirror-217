import datetime
import hashlib
import os
import pathlib
import time
from contextlib import contextmanager

import click


@contextmanager
def chdir(path: pathlib.Path):
    old = os.getcwd()
    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(old)


def get_hash_and_size(path: pathlib.Path):
    assert path.exists(), path

    h = hashlib.sha256()
    size = 0
    with open(path, "rb") as r:
        while True:
            data = r.read(40960)  # read 10 pages
            if not data:
                break
            h.update(data)
            size += len(data)
    return h.hexdigest(), size


@contextmanager
def log_time(msg):
    start_time = time.time()
    try:
        yield
    finally:
        end_time = time.time()
        execution_time = end_time - start_time
        duration = datetime.timedelta(seconds=execution_time)
        click.echo(f"{msg} finished in {duration}")
