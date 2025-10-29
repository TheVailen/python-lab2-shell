from __future__ import annotations
from typing import List
from src.logger import log_command
from src.helpers import resolve_path


def run(args: List[str]) -> str:
    """
    Возвращение содержимого файла в виде строки. В случае ошибки логируется и выбрасывается исключение.

    :param args: [path_to_file]
    :return: содержимое файла
    """
    if not args:
        raise ValueError("Использование: cat <file>")
    path_str = args[0]
    try:
        p = resolve_path(path_str)
        if not p.exists():
            raise FileNotFoundError(f"No such file: {path_str}")
        if p.is_dir():
            raise IsADirectoryError(f"Is a directory: {path_str}")
        content = p.read_text(encoding="utf-8")
        log_command(f"cat {path_str}", True)
        return content
    except Exception as exc:
        log_command(f"cat {path_str}", False, str(exc))
        raise
