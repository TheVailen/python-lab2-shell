import shutil
import time
from pathlib import Path
from typing import List, Optional

from src.helpers import resolve_path
from src.history import UndoRecord
from src.constants import TRASH_DIR


def run(args: List[str]) -> Optional[UndoRecord]:
    """
    Перемещение файла/каталога в корзину (.trash) для возможности отмены.

    :param args: [path1, path2, ...] [--yes (для пропуска подтверждения), -r (для каталогов)]
    :return: UndoRecord для отмены операции.
    :raises FileNotFoundError: если файл не найден.
    """
    if not args:
        raise ValueError("Использование: rm <файл> [опции]")

    recursive = "-r" in args
    force = "--yes" in args

    paths = [arg for arg in args if arg not in ("-r", "--yes")]

    trash_path = Path.home() / TRASH_DIR
    trash_path.mkdir(exist_ok=True)

    for path_str in paths:
        p = resolve_path(path_str)

        if not p.exists():
            raise FileNotFoundError(f"Нет такого файла или каталога: {path_str}")

        if p.is_dir() and not recursive:
            raise ValueError(f"Невозможно удалить каталог без флага -r: {path_str}")

        should_confirm = not force and p.is_dir()

        if should_confirm:
            confirmation = input(f"Удалить директорию {path_str}? (y/n): ")
            if confirmation.lower() != 'y':
                continue

        trash_target = trash_path / f"{p.name}_{int(time.time())}"

        try:
            shutil.move(str(p), str(trash_target))

            print(f"Перемещено в корзину (для отмены): {p.name}")

            return UndoRecord(
                cmd="rm",
                args=args,
                metadata={
                    "original_path": path_str,
                    "trash_path": str(trash_target),
                },
            )
        except Exception as e:
            raise IOError(f"Ошибка при перемещении в корзину: {e}")

    return None
