import shutil
from pathlib import Path
from typing import Dict, List
from src.history import read_history
from src.helpers import resolve_path


def undo_cp(metadata: Dict) -> None:
    """Отменяет cp: удаляет скопированный целевой файл/каталог."""
    target_path = resolve_path(metadata["target"])

    if target_path.exists():
        if target_path.is_dir():
            shutil.rmtree(target_path)
        else:
            target_path.unlink()
        print(f"UNDO: Удален скопированный объект: {target_path}")
    else:
        print(f"UNDO: Целевой объект {target_path} не существует, отмена не требуется.")


def undo_mv(metadata: Dict) -> None:
    """Отменяет mv: перемещает объект обратно в исходное место."""
    source_path = resolve_path(metadata["source"])
    target_path = resolve_path(metadata["target"])

    if target_path.exists():
        if source_path.exists():
             raise FileExistsError(f"UNDO Ошибка: Исходный путь {source_path} занят. Отмена невозможна.")

        target_path.rename(source_path)
        print(f"UNDO: Объект {target_path} возвращен в {source_path}")
    else:
        print(f"UNDO: Объект {target_path} не существует, отмена невозможна.")


def undo_rm(metadata: Dict) -> None:
    """Отменяет rm: восстанавливает объект из .trash."""
    trash_path_str = metadata["trash_path"]
    original_path_str = metadata["original_path"]

    trash_path = Path(trash_path_str)
    original_path = resolve_path(original_path_str)

    if trash_path.exists():
        if not original_path.exists():
            trash_path.rename(original_path)
            print(f"UNDO: Объект {original_path} восстановлен из корзины.")
        else:
            print(f"UNDO Ошибка: Исходный путь {original_path} занят, восстановление невозможно.")
    else:
        print(f"UNDO Ошибка: Объект не найден в корзине ({trash_path}).")


def run(args: List[str]) -> None:
    """Выполнить отмену последней обратимой команды."""
    records = read_history(n=1)
    if not records:
        print("UNDO: История команд пуста.")
        return

    last_record = records[-1]
    cmd = last_record['cmd']
    metadata = last_record['metadata']

    undo_actions = {
        "cp": undo_cp,
        "mv": undo_mv,
        "rm": undo_rm,
    }

    if cmd in undo_actions:
        print(f"Выполняется отмена: {cmd} {' '.join(last_record['args'])}")
        undo_actions[cmd](metadata)
    else:
        print(f"UNDO: Команда '{cmd}' не поддерживает отмену.")
