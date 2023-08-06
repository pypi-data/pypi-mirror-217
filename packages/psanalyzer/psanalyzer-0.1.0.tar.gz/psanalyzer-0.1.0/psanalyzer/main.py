import pathlib
import sys

import click

from psanalyzer.database import OUTPUT_FORMATS, create_engine, get_session, run_query
from psanalyzer.fs import iter_files
from psanalyzer.queries import QUERIES

DEFAULT_DB_PATH = pathlib.Path("psanalyzer.sqlite3")


@click.command(help="Create sqlite3 database from a git project workspace")
@click.option(
    "--db",
    show_default=True,
    default=DEFAULT_DB_PATH,
    type=click.Path(file_okay=True, dir_okay=False, writable=True, path_type=pathlib.Path),
    help="Path to output sqlite3 database",
)
@click.option(
    "-f",
    "--force",
    is_flag=True,
    show_default=True,
    default=False,
    type=bool,
    help="Overwrite output database if exists",
)
def build(db: pathlib.Path, force: bool) -> None:
    if db.exists():
        if force:
            click.echo(f"Output file {db} exists, overwriting it...")
            try:
                db.unlink()
            except PermissionError as e:
                raise click.FileError(db, e) from e
        else:
            raise click.UsageError(f"Output file {db} exists, provide -f/--force to overwrite")

    engine = create_engine(db, True)
    with get_session(engine) as session:
        session.add_all(iter_files(pathlib.Path.cwd()))
        session.commit()

    click.echo(
        f"""\
Success! Now run queries:
{pathlib.Path(sys.argv[0]).name} query duplicates --format csv > output.csv
"""
    )


@click.command(help="Run query against database created with `build` command")
@click.argument("name", type=click.Choice(list(QUERIES.keys())))
@click.option("--format", type=click.Choice(OUTPUT_FORMATS), default="human")
@click.option(
    "--db",
    default=DEFAULT_DB_PATH,
    type=click.Path(file_okay=True, dir_okay=False, readable=True, path_type=pathlib.Path),
    help="Database build with `build` command",
)
def query(name: str, format: str, db: pathlib.Path):
    engine = create_engine(db, False)
    with get_session(engine, False) as session:
        run_query(session, name, format)


@click.group(
    help="This tool turns a project folder into sqlite3 database, and "
    "runs queries against it to extract useful info."
)
def main() -> None:
    pass


main.add_command(build)
main.add_command(query)

if __name__ == "__main__":
    main()
