from typing import List
from src.helpers import resolve_path

def run(args: List[str]) -> List[str]:
    """
    Поиск по шаблону в файлах.

    :param args: [шаблон, файл1, файл2, ...] [-i (опционально, без учета регистра)]
    :return: Список строк, содержащих совпадение.
    """
    if len(args) < 2:
        raise ValueError("Использование: grep [опции] <шаблон> <файл1> [файл2...]")

    ignore_case = "-i" in args

    effective_args = [arg for arg in args if arg != "-i"]

    if len(effective_args) < 2:
        raise ValueError("Использование: grep [опции] <шаблон> <файл1> [файл2...]")

    pattern = effective_args[0]
    file_paths = effective_args[1:]

    results: List[str] = []

    for path_str in file_paths:
        p = resolve_path(path_str)

        if not p.exists() or p.is_dir():
            results.append(f"Ошибка: {path_str}: Нет такого файла или каталога")
            continue

        try:
            content = p.read_text(encoding="utf-8")

            search_pattern = pattern

            if ignore_case:
                search_pattern = pattern.lower()

            for i, line in enumerate(content.splitlines(), 1):
                line_to_search = line
                if ignore_case:
                    line_to_search = line.lower()

                if search_pattern in line_to_search:
                    results.append(f"{path_str}:{i}:{line}")

        except Exception as e:
            results.append(f"Ошибка при чтении {path_str}: {e}")

    return results
