import shutil
from typing import List, Optional

from src.helpers import resolve_path
from src.history import UndoRecord


def run(args: List[str]) -> Optional[UndoRecord]:
    """
    Копирование файла/каталога.

    :param args: [path_src, path_dst] [-r (опционально, для рекурсивного копирования)]
    :return: UndoRecord для отмены операции.
    :raises FileNotFoundError: если исходный файл не найден.
    :raises FileExistsError: если целевой файл уже существует.
    """
    if len(args) < 2:
        raise ValueError("Использование: cp [опции] <источник> <цель>")

    recursive = "-r" in args

    effective_args = [arg for arg in args if arg != "-r"]

    if len(effective_args) != 2:
        raise ValueError("Использование: cp [опции] <источник> <цель>")

    path_str_src, path_str_dst = effective_args
    path_src = resolve_path(path_str_src)
    path_dst = resolve_path(path_str_dst)

    if not path_src.exists():
        raise FileNotFoundError(f"Нет такого файла или каталога: {path_str_src}")

    if path_src.is_dir():
        if not recursive:
            raise ValueError(f"Невозможно скопировать каталог без флага -r: {path_str_src}")

        # Копирование каталога (рекурсивное)
        if path_dst.exists():
            raise FileExistsError(f"Каталог уже существует: {path_str_dst}")
        shutil.copytree(path_src, path_dst)
    else:
        # Копирование файла
        shutil.copy2(path_src, path_dst)

    return UndoRecord(
        cmd="cp",
        args=args,
        metadata={"source": path_str_src, "target": path_str_dst}
    )
