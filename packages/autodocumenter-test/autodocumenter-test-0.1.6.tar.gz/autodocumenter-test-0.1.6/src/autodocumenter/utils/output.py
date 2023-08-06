# copied from: https://github.com/psf/black/blob/main/src/black/output.py
import tempfile
from typing import Any, Optional
from click import echo, style


def _out(message: Optional[str] = None, nl: bool = True, **styles: Any) -> None:
    if message is not None:
        if "bold" not in styles:
            styles["bold"] = True
        message = style(message, **styles)
    echo(message, nl=nl, err=True)


def _err(message: Optional[str] = None, nl: bool = True, **styles: Any) -> None:
    if message is not None:
        if "fg" not in styles:
            styles["fg"] = "red"
        message = style(message, **styles)
    echo(message, nl=nl, err=True)


def out(message: Optional[str] = None, nl: bool = True, **styles: Any) -> None:
    _out(message, nl=nl, **styles)


def err(message: Optional[str] = None, nl: bool = True, **styles: Any) -> None:
    _err(message, nl=nl, **styles)


def dump_to_file(*output: str, ensure_final_newline: bool = True) -> str:
    """Dump `output` to a temporary file. Return path to the file."""
    with tempfile.NamedTemporaryFile(
        mode="w", prefix="blk_", suffix=".log", delete=False, encoding="utf8"
    ) as f:
        for lines in output:
            f.write(lines)
            if ensure_final_newline and lines and lines[-1] != "\n":
                f.write("\n")
    return f.name
