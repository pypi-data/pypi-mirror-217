from datetime import datetime
from pathlib import Path

import typer
from . import AsyncBasePath
from . import AsyncFluidPath
from . import AsyncPathy

app: typer.Typer = typer.Typer(help="AsyncPathy command line interface.")


@app.command()
async def cp(from_location: str, to_location: str) -> None:
    """
    Copy a blob or folder of blobs from one bucket to another.
    """
    from_path: AsyncFluidPath = AsyncPathy.fluid(from_location)
    if not await from_path.exists():
        raise ValueError(
            f"from_path is not an existing Path or AsyncPathy: {from_path}"
        )
    to_path: AsyncFluidPath = AsyncPathy.fluid(to_location)
    if await from_path.is_dir():
        await to_path.mkdir(parents=True, exist_ok=True)
        for blob in [blob async for blob in from_path.rglob("*")]:
            if not await blob.is_file():
                continue
            to_blob = to_path / str(blob.relative_to(from_path))
            await to_blob.write_bytes(await blob.read_bytes())
    elif from_path.is_file():
        # Copy prefix from the source if the to_path has none.
        #
        # e.g. "cp ./file.txt gs://bucket-name/" writes "gs://bucket-name/file.txt"
        sep: str = to_path._flavour.sep  # type:ignore
        if isinstance(to_path, AsyncPathy) and to_location.endswith(sep):
            to_path = to_path / from_path

        await to_path.parent.mkdir(parents=True, exist_ok=True)
        await to_path.write_bytes(await from_path.read_bytes())


@app.command()
async def mv(from_location: str, to_location: str) -> None:
    """
    Move a blob or folder of blobs from one path to another.
    """
    from_path: AsyncFluidPath = AsyncPathy.fluid(from_location)
    to_path: AsyncFluidPath = AsyncPathy.fluid(to_location)

    if from_path.is_file():
        # Copy prefix from the source if the to_path has none.
        #
        # e.g. "cp ./file.txt gs://bucket-name/" writes "gs://bucket-name/file.txt"
        sep: str = to_path._flavour.sep  # type:ignore
        if isinstance(to_path, AsyncPathy) and to_location.endswith(sep):
            to_path = to_path / from_path
        await to_path.parent.mkdir(parents=True, exist_ok=True)
        await to_path.write_bytes(await from_path.read_bytes())
        await from_path.unlink()

    if from_path.is_dir():
        await to_path.mkdir(parents=True, exist_ok=True)
        to_unlink: list[AsyncPathy | AsyncBasePath | Path] = []
        for blob in [blob async for blob in from_path.rglob("*")]:
            if not blob.is_file():
                continue
            to_blob = to_path / str(blob.relative_to(from_path))
            await to_blob.write_bytes(await blob.read_bytes())
            to_unlink.append(blob)
        for unlink in to_unlink:
            await unlink.unlink()
        if await from_path.is_dir():
            await from_path.rmdir()


@app.command()
async def rm(
    location: str,
    recursive: bool = typer.Option(
        False, "--recursive", "-r", help="Recursively remove files and folders."
    ),
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Print removed files and folders."
    ),
) -> None:
    """
    Remove a blob or folder of blobs from a given location.
    """
    path: AsyncFluidPath = AsyncPathy.fluid(location)
    if not await path.exists():
        typer.echo(f"rm: {path}: No such file or directory")
        raise typer.Exit(1)

    if await path.is_dir():
        if not recursive:
            typer.echo(f"rm: {path}: is a directory")
            raise typer.Exit(1)
        selector = path.rglob("*") if recursive else path.glob("*")
        to_unlink = [b async for b in selector if b.is_file()]
        for blob in to_unlink:
            if verbose:
                typer.echo(str(blob))
            await blob.unlink()
        if await path.exists():
            if verbose:
                typer.echo(str(path))
            await path.rmdir()
    elif await path.is_file():
        if verbose:
            typer.echo(str(path))
        await path.unlink()


@app.command()
async def ls(
    location: str,
    long: bool = typer.Option(
        False,
        "--long",
        "-l",
        help="Print long style entries with updated time and size shown.",
    ),
) -> None:
    """
    List the blobs that exist at a given location.
    """
    path: AsyncFluidPath = AsyncPathy.fluid(location)
    if not await path.exists() or await path.is_file():
        typer.echo(f"ls: {path}: No such file or directory")
        raise typer.Exit(1)
    now = datetime.now()
    async for blob_stat in path.ls():
        print_name = str(path / blob_stat.name)
        if not long:
            typer.echo(print_name)
            continue
        time_str = ""
        if blob_stat.last_modified is not None:
            then = datetime.fromtimestamp(blob_stat.last_modified)
            if now.year != then.year:
                time_str = "%d %b, %Y"
            else:
                time_str = "%d %b, %H:%M"
            time_str = then.strftime(time_str)
        typer.echo(f"{blob_stat.size:10}{time_str:15}{print_name:10}")


if __name__ == "__main__":
    app()

__all__ = ()
