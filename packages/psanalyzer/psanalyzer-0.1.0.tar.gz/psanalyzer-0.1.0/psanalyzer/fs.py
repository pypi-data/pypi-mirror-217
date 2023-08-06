import hashlib
import multiprocessing.pool
import os
import pathlib
from functools import partial

import click
import tqdm

from psanalyzer.database import Dir, File
from psanalyzer.util import get_hash_and_size


def _proc_file(relpath: pathlib.Path):
    assert relpath.exists(), relpath
    hash, size = get_hash_and_size(relpath)

    f = File(
        path=str(relpath),
        extension=relpath.suffix,
        hash=hash,
        size_bytes=size,
    )

    return relpath, f


def _proc_dir(relpath: pathlib.Path, state: dict):
    files = 0
    dirs = 0
    size = 0
    h = hashlib.sha256()
    assert relpath.exists(), relpath
    contains = os.listdir(relpath)
    for fp in sorted(contains):
        p = relpath.joinpath(fp)
        assert p in state, (
            relpath,
            fp,
            p,
            [x for x in state.keys() if str(x).startswith(".git")],
        )
        f = state[p]
        assert isinstance(f, File) or isinstance(f, Dir), f
        if isinstance(f, Dir):
            assert f.hash, f  # hash must not be empty/None
            dirs += 1
            files += f.files
        else:
            files += 1

        h.update(f.hash.encode("ascii"))
        size += f.size_bytes

    d = Dir(
        path=str(relpath),
        size_bytes=size,
        hash=h.hexdigest(),
        files=files,
        dirs=dirs,
    )
    return relpath, d


def iter_files(root: pathlib.Path):
    pool = multiprocessing.pool.ThreadPool()

    state = {}
    allfiles = set()
    alldirs = set()

    # first, walk over entire repo
    for path, dirs, files in os.walk(root, topdown=True):
        allfiles.update([pathlib.Path(path).joinpath(x).resolve(True).relative_to(root) for x in files])
        alldirs.update([pathlib.Path(path).joinpath(x).resolve(True).relative_to(root) for x in dirs])

    WIDTH = 20
    click.echo("Total files found".rjust(WIDTH) + f": {len(allfiles)}")
    click.echo("Total dirs found".rjust(WIDTH) + f": {len(alldirs)}")

    for p, f in tqdm.tqdm(
        pool.imap_unordered(_proc_file, allfiles),
        desc="Processing files".rjust(WIDTH),
        total=len(allfiles),
        unit="files",
    ):
        assert isinstance(f, File), f
        assert isinstance(p, pathlib.Path), p
        state[p] = f
        yield f

    for p, d in tqdm.tqdm(
        # sort paths, as we need to calculate hash of children to calculate parents
        map(partial(_proc_dir, state=state), sorted(alldirs)[::-1]),
        desc="Processing dirs".rjust(WIDTH),
        total=len(alldirs),
        unit="dirs",
    ):
        assert isinstance(d, Dir), d
        assert isinstance(p, pathlib.Path), p
        state[p] = d
        yield d
