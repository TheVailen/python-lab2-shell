"""
Команда ls — отображение списка файлов и каталогов.

Поддерживает:
 - аргумент path (относительный/абсолютный);
 - опцию -l (подробный вывод: имя, размер, дата изменения, права доступа).
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import List
from src.logger import log_command
from src.helpers import resolve_path


def _format_long(entry: Path) -> str:
    """
    Форматирует строку подробного вывода для файла/каталога.

    :param entry: путь к файлу или каталогу
    :return: строка вида "<имя>\t<размер>\t<дата>\t<права>"
    """
    stat = entry.stat()
    size = f"{stat.st_size} bytes"
    mtime = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
    mode = oct(stat.st_mode)[-3:]
    return f"{entry.name}\t{size}\t{mtime}\t{mode}"


def run(args: List[str]) -> List[str]:
    """
    Выполняет команду ls.

    :param args: список аргументов команды (например: ['-l', '/tmp'])
    :return: список строк — результат выполнения
    """
    path = "."
    long_format = False

    # парсим аргументы
    for a in args:
        if a == "-l":
            long_format = True
        else:
            path = a

    try:
        p = resolve_path(path)
        if not p.exists():
            raise FileNotFoundError(f"No such file or directory: {path}")

        # сортировка: сначала каталоги, потом файлы
        items = sorted(p.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower()))
        lines: List[str] = []

        for entry in items:
            lines.append(_format_long(entry) if long_format else entry.name)

        log_command(f"ls {' '.join(args)}", True)
        return lines

    except Exception as exc:
        log_command(f"ls {' '.join(args)}", False, str(exc))
        raise
