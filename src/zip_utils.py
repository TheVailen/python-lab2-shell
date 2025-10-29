from __future__ import annotations

import shutil
import zipfile
import tarfile
from pathlib import Path
from typing import List
from src.logger import log_command
from src.helpers import resolve_path


def create_zip(args: List[str]) -> None:
    if len(args) != 2:
        raise ValueError("Использование: zip <folder> <archive.zip>")
    src_str, dst_str = args
    try:
        src = resolve_path(src_str)
        if not src.exists() or not src.is_dir():
            raise FileNotFoundError(f"No such directory: {src_str}")
        dst = Path(dst_str)
        # shutil.make_archive требует имя без .zip
        base = str(dst.with_suffix(""))
        shutil.make_archive(base, "zip", root_dir=str(src))
        log_command(f"zip {src_str} {dst_str}", True)
    except Exception as exc:
        log_command(f"zip {src_str} {dst_str}", False, str(exc))
        raise


def extract_zip(args: List[str]) -> None:
    if len(args) != 1:
        raise ValueError("Использование: unzip <archive.zip>")
    archive = args[0]
    try:
        with zipfile.ZipFile(archive, "r") as zf:
            zf.extractall()
        log_command(f"unzip {archive}", True)
    except Exception as exc:
        log_command(f"unzip {archive}", False, str(exc))
        raise


def create_tar(args: List[str]) -> None:
    if len(args) != 2:
        raise ValueError("Использование: tar <folder> <archive.tar.gz>")
    src_str, dst_str = args
    try:
        src = resolve_path(src_str)
        if not src.exists() or not src.is_dir():
            raise FileNotFoundError(f"No such directory: {src_str}")
        with tarfile.open(dst_str, "w:gz") as tar:
            tar.add(str(src), arcname=".")
        log_command(f"tar {src_str} {dst_str}", True)
    except Exception as exc:
        log_command(f"tar {src_str} {dst_str}", False, str(exc))
        raise


def extract_tar(args: List[str]) -> None:
    if len(args) != 1:
        raise ValueError("Использование: untar <archive.tar.gz>")
    archive = args[0]
    try:
        with tarfile.open(archive, "r:gz") as tar:
            tar.extractall()
        log_command(f"untar {archive}", True)
    except Exception as exc:
        log_command(f"untar {archive}", False, str(exc))
        raise
