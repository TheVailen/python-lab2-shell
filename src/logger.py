from __future__ import annotations

import logging
from typing import Optional
from src import constants

_logger = logging.getLogger("mini_shell")


def setup_logger() -> None:
    """
    Настроить логгер для записи в файл constants.SHELL_LOG.
    Вызывать в начале программы.
    """
    handler = logging.FileHandler(constants.SHELL_LOG, encoding="utf-8")
    formatter = logging.Formatter("[%(asctime)s] %(message)s", datefmt=constants.LOG_TIME_FORMAT)
    handler.setFormatter(formatter)

    _logger.setLevel(logging.INFO)
    if not _logger.handlers:
        _logger.addHandler(handler)


def log_command(command: str, success: bool = True, error_message: Optional[str] = None) -> None:
    """
    Записать в лог команду и её результат.

    :param command: Текст введённой команды.
    :param success: Флаг успеха.
    :param error_message: Текст ошибки, если success == False.
    """
    if success:
        _logger.info(command)
    else:
        _logger.error(f"ERROR: {error_message} — {command}")
