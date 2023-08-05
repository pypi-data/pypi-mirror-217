from __future__ import annotations

from stability_matrix_tools.models.settings import env
from stability_matrix_tools.utils.progress import RichProgressListener
from stability_matrix_tools.utils.uploader import Uploader

from pathlib import Path
from urllib.parse import urljoin
from typing import Annotated, TypeVar, Callable, ParamSpec, Any

import typer
from typer import Option

T = TypeVar("T")
P = ParamSpec("P")

ConfirmType = Annotated[bool, Option("--yes", "-y", help="Confirm action")]

app = typer.Typer()


def assert_exists(*target: T, msg: str) -> T:
    """Assert that objects are truthy."""
    if not all(target):
        typer.echo(f"❌  {msg}")
        raise SystemExit(1)
    return target


def attempt(func: Callable[[P], T], *args: Any) -> T:
    try:
        return func(*args)
    except Exception as e:
        if env.verbose:
            raise
        else:
            typer.echo(f"❌  Error: {e}")
            raise SystemExit(1)


@app.command()
def upload(file_path: Path, b2_path: str, confirm: ConfirmType = False):
    """Upload a file to a B2 bucket."""

    file = file_path.resolve()
    assert_exists(file, msg=f"File {file_path} does not exist.")

    uploader = Uploader(
        api_id=env.b2_api_id,
        api_key=env.b2_api_key,
        bucket_name=env.b2_bucket_name,
    )

    with RichProgressListener("Uploading...", transient=True) as pbar:
        uploader.upload(str(file), b2_path, pbar)

    result = urljoin(env.cdn_root, b2_path)
    typer.echo(f"✅  Uploaded at: {result!r}")


@app.command()
def delete(b2_path: str):
    """Delete a file from the B2 bucket."""
    uploader = Uploader(
        api_id=env.b2_api_id,
        api_key=env.b2_api_key,
        bucket_name=env.b2_bucket_name,
    )

    typer.echo(f"Deleting {b2_path}...")

    file = attempt(uploader.find_file, b2_path)
    assert_exists(file, msg="File not found in B2 bucket")

    uploader.delete_file(file)

    typer.echo(f"🗑️  Deleted {b2_path!r}")

