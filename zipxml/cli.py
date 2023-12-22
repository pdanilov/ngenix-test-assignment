from pathlib import Path

import typer

from zipxml.archive import ArchiveArgs, run_archive
from zipxml.parse import run_parse

app = typer.Typer()


@app.command()
def archive(out_dir: str, zip_num: int = 50, xml_num: int = 100, id_len: int = 32, object_name_len: int = 10):
    p_out = Path(out_dir)
    if not p_out.is_dir():
        p_out.mkdir()

    args = ArchiveArgs(zip_num, xml_num, id_len, object_name_len)
    run_archive(p_out, args)


@app.command()
def parse(in_dir: str, out_dir: str):
    p_in, p_out = map(Path, [in_dir, out_dir])
    if not p_in.is_dir():
        raise ValueError("provided argumant 'in_dir' is not a directory")
    if not p_out.is_dir():
        p_out.mkdir()

    run_parse(p_in, p_out)


if __name__ == "__main__":
    app()
