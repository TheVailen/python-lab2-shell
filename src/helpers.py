from __future__ import annotations
import os
from pathlib import Path


def resolve_path(path_str: str, base: Path | None = None) -> Path:
    """
    Преобразует путь (относительный или абсолютный) в объект Path,
    нормализует расширения типа '~' и '..'.

    :param path_str: Входная строка пути.
    :param base: Базовый каталог для относительных путей (по умолчанию — текущая папка).
    :return: Path — абсолютный нормализованный путь.
    """
    if base is None:
        base = Path.cwd()
    p = Path(os.path.expanduser(path_str))
    if not p.is_absolute():
        p = base.joinpath(p)
    return p.resolve()


def ensure_parent_exists(path: Path) -> None:
    """
    Убеждаемся, что родительская директория файла существует.
    """
    parent = path.parent
    if not parent.exists():
        parent.mkdir(parents=True, exist_ok=True)


def safe_remove_guard(path: Path) -> None:
    """
    Блоки-предохранитель для удаления — запрет удаления корня и родительского каталога.
    """
    p_str = str(path)
    if p_str in ("/", "", ".") or p_str.endswith(".."):
        raise PermissionError("Запрещено удалять корневой или родительский каталог.")
