import contextlib
import csv
import io
import pathlib
from dataclasses import dataclass

import click
import sqlalchemy as s
from sqlalchemy.orm import Session, declarative_base
from sqlalchemy.sql import text
from tabulate import tabulate

from psanalyzer.queries import QUERIES

Base = declarative_base()


@dataclass(init=False)
class File(Base):
    __tablename__ = "file"
    id: int = s.Column(s.Integer, primary_key=True, autoincrement=True)
    path: str = s.Column(s.String, unique=True)
    extension: str = s.Column(s.String)
    hash: str = s.Column(s.String(64))  # sha256 of a file
    size_bytes: int = s.Column(s.Integer)


@dataclass(init=False)
class Dir(Base):
    __tablename__ = "dir"
    id: int = s.Column(s.Integer, primary_key=True, autoincrement=True)
    path: str = s.Column(s.String, unique=True)
    hash: str = s.Column(s.String(64))  # sha256 of all containing files
    size_bytes: int = s.Column(s.Integer)  # sum of all sizes of containing files
    files: int = s.Column(s.Integer)  # total number of files in a dir
    dirs: int = s.Column(s.Integer)  # total number of dirs in a dir


def create_engine(output: pathlib.Path, create_tables=True):
    engine = s.create_engine(f"sqlite:///{output}")

    if create_tables:
        Base.metadata.create_all(bind=engine)

    return engine


@contextlib.contextmanager
def get_session(engine, cleanup=False):
    session = Session(engine)
    Base.metadata.create_all(engine)

    try:
        yield session
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

    if cleanup:
        Base.metadata.drop_all(engine)


OUTPUT_FORMATS = ["csv", "human"]


def run_query(session: Session, queryname, format: str) -> None:
    assert format in OUTPUT_FORMATS, format
    assert queryname in QUERIES, queryname
    header, query = QUERIES[queryname]
    stmt = text(query)
    data = session.execute(stmt)
    if format == "csv":
        buf = io.StringIO(newline="")
        w = csv.writer(buf, dialect="excel", lineterminator="\n")
        w.writerow(header)
        w.writerows(data)
        print(buf.getvalue())
    elif format == "human":
        print(tabulate(data, headers=header, maxcolwidths=[64] * len(header)))
    else:
        raise click.UsageError(f"Bad format: {format}")
