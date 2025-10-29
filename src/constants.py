"""
Константы и настройки для мини-оболочки.

Здесь хранятся названия операторов, имена лог-файлов и другие значения, используемые в проекте.
"""

ALLOWED_OPERATORS = {"+", "-", "*", "/", "//", "%", "**"}

SHELL_LOG: str = "shell.log"

HISTORY_FILE: str = ".history"

MAX_RECURSION_DEPTH: int = 1000

LOG_TIME_FORMAT: str = "%Y-%m-%d %H:%M:%S"

HISTORY_FILE = ".shell_history.json"

TRASH_DIR = ".trash"
