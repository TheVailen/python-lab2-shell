import os
from typing import List, Optional
from src.helpers import resolve_path
from src.history import UndoRecord


def run(args: List[str]) -> Optional[UndoRecord]:
    """
    Перемещение/переименование файла/каталога.

    :param args: [path_src, path_dst]
    :return: UndoRecord для отмены операции.
    :raises FileNotFoundError: если исходный файл не найден.
    """
    if len(args) != 2:
        raise ValueError("Использование: mv <источник> <цель>")

    path_str_src, path_str_dst = args
    path_src = resolve_path(path_str_src)
    path_dst = resolve_path(path_str_dst)

    if not path_src.exists():
        raise FileNotFoundError(f"Нет такого файла или каталога: {path_str_src}")

    os.rename(path_src, path_dst)

    return UndoRecord(
        cmd="mv",
        args=args,
        metadata={"source": path_str_src, "target": path_str_dst}
    )
