from __future__ import annotations
import os
from pathlib import Path
from typing import List
from src.logger import log_command
from src.helpers import resolve_path


def run(args: List[str]) -> None:
    """
    Выполнить cd.

    :param args: ожидaется 0 или 1 аргумент; если 0 — перейти в домашний каталог
    :raises FileNotFoundError: если каталог не найден
    """
    arg = args[0] if args else "~"
    try:
        target = resolve_path(arg, base=Path.cwd())
        if not target.exists() or not target.is_dir():
            raise FileNotFoundError(f"No such directory: {arg}")
        os.chdir(target)
        log_command(f"cd {arg}", True)
    except Exception as exc:
        log_command(f"cd {arg}", False, str(exc))
        raise
