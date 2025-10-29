import time
import json
from pathlib import Path
from typing import List, Dict, Any

from src import constants
from src.logger import log_command

class UndoRecord:
    """Хранит метаданные, необходимые для отмены операции."""
    def __init__(self, cmd: str, args: List[str], metadata: Dict[str, Any]):
        self.timestamp = int(time.time())
        self.cmd = cmd
        self.args = args
        self.metadata = metadata

    def to_dict(self) -> Dict:
        """Возвращает словарь для сериализации в JSON."""
        return {
            "timestamp": self.timestamp,
            "cmd": self.cmd,
            "args": self.args,
            "metadata": self.metadata,
        }

def append_history(record: UndoRecord) -> None:
    """Добавить запись истории как JSON-объект, используя Path.home()."""
    p = Path.home() / constants.HISTORY_FILE

    if p.exists():
        try:
            records = json.loads(p.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            records = []
    else:
        records = []

    records.append(record.to_dict())
    p.write_text(json.dumps(records, indent=2), encoding="utf-8")


def read_history(n: int = 50) -> List[Dict]:
    """Прочитать последние n записей (словарей)."""
    p = Path.home() / constants.HISTORY_FILE
    if not p.exists():
        return []

    try:
        records = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []

    return records[-n:]


def run(args: List[str]) -> List[str]:
    """
    Команда history: возвращает последние N записей с номерами.
    Использование: history [N]
    """
    n = 50
    if args:
        try:
            n = int(args[0])
        except ValueError:
            raise ValueError("history ожидает число")

    records = read_history(n)

    output = []
    for i, rec in enumerate(records, 1):
        command_str = f"{rec['cmd']} {' '.join(rec['args'])}"
        output.append(f"{i}. {command_str}")

    log_command(f"history {' '.join(args)}", True)
    return output
