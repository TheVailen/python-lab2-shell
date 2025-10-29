from __future__ import annotations

import sys
from typing import List, Optional
from src import (
    ls,
    cd,
    cat,
    cp,
    mv,
    rm,
    zip_utils,
    grep,
    history,
    undo,
)
from src.logger import setup_logger, log_command
from src.history import append_history, UndoRecord


def _dispatch(command_parts: List[str]) -> Optional[object]:
    """
    Выполнить одну команду, переданную списком токенов.
    Возвращает результат команды (если есть) или None.
    """
    if not command_parts:
        return None

    cmd = command_parts[0]
    args = command_parts[1:]

    history_record: Optional[UndoRecord] = None

    result: Optional[object] = None

    if cmd == "ls":
        result = ls.run(args)
    elif cmd == "cd":
        cd.run(args)
    elif cmd == "cat":
        result = cat.run(args)
    elif cmd == "cp":
        history_record = cp.run(args)
    elif cmd == "mv":
        history_record = mv.run(args)
    elif cmd == "rm":
        history_record = rm.run(args)
    elif cmd == "zip":
        zip_utils.create_zip(args)
    elif cmd == "unzip":
        zip_utils.extract_zip(args)
    elif cmd == "tar":
        zip_utils.create_tar(args)
    elif cmd == "untar":
        zip_utils.extract_tar(args)
    elif cmd == "grep":
        grep.run(args)
    elif cmd == "history":
        result = history.run(args)
    elif cmd == "undo":
        undo.run(args)
    else:
        raise ValueError(f"Неизвестная команда: {cmd}")

    if history_record:
        append_history(history_record)

    if cmd not in ("history", "undo"):
        # Сохраняем текстовую историю для всех команд, которые не поддерживают undo
        if not history_record:
            append_history(UndoRecord(cmd, args, {}))

    return result


def _print_result(res: object) -> None:
    """Универсальный вывод результата команды в консоль."""
    if res is None:
        return
    if isinstance(res, list):
        for line in res:
            print(line)
    else:
        print(res)


def main(argv: List[str] | None = None) -> None:
    """Запуск приложения; если argv не указан — режим REPL."""
    setup_logger()
    if argv is None:
        argv = sys.argv[1:]
    if argv:
        # Однократный запуск: python -m src.main ls -1 /tmp
        try:
            res = _dispatch(argv)
            log_command(" ".join(argv), True)
            _print_result(res)
        except Exception as exc:
            log_command(" ".join(argv), False, str(exc))
            print(f"ERROR: {exc}")
        return

    # REPL
    print("Мини-оболочка — введите команду или 'exit' для выхода.")
    while True:
        try:
            line = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not line:
            continue
        if line.lower() in ("exit", "quit"):
            break
        parts = line.split()
        try:
            res = _dispatch(parts)
            _print_result(res)
        except Exception as exc:
            log_command(line, False, str(exc))
            print(f"Ошибка: {exc}")


if __name__ == "__main__":
    main()
