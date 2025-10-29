import os
from pathlib import Path
import pytest
from src.ls import run as ls_command
from src.cd import run as cd_command
from src.cat import run as cat_command
from src.cp import run as cp_command
from src.mv import run as mv_command
from src.rm import run as rm_command
from src.grep import run as grep_command
from src.zip_utils import create_zip as zip_folder
from src.zip_utils import extract_zip as unzip_archive


@pytest.fixture
def temp_dir(tmp_path):
    """Создаёт временную рабочую директорию для тестов."""
    cwd = os.getcwd()
    os.chdir(tmp_path)
    yield tmp_path
    os.chdir(cwd)


def test_ls_basic(temp_dir, capsys):
    (temp_dir / "file.txt").write_text("hello")
    (temp_dir / "folder").mkdir()

    result = ls_command(["."])
    print('\n'.join(result))
    out = capsys.readouterr().out

    assert "file.txt" in out
    assert "folder" in out


def test_ls_long_format(temp_dir, capsys):
    (temp_dir / "file.txt").write_text("hello")

    result = ls_command(["-l", "."])
    print('\n'.join(result))
    out = capsys.readouterr().out

    assert "file.txt" in out
    assert "bytes" in out


def test_cd_success(temp_dir):
    (temp_dir / "folder").mkdir()
    cd_command(["folder"])
    assert Path(os.getcwd()).name == "folder"


def test_cd_fail(temp_dir, capsys):
    with pytest.raises(FileNotFoundError):
        cd_command(["no_such_folder"])
    pass


def test_cat_success(temp_dir, capsys):
    (temp_dir / "a.txt").write_text("hello")
    content = cat_command(["a.txt"])
    assert content.strip() == "hello"


def test_cat_file_not_found(temp_dir, capsys):
    with pytest.raises(FileNotFoundError):
        cat_command(["missing.txt"])
    pass


def test_cp_file(temp_dir):
    (temp_dir / "a.txt").write_text("hello")
    cp_command(["a.txt", "b.txt"])
    assert (temp_dir / "b.txt").read_text() == "hello"


def test_mv_rename(temp_dir):
    (temp_dir / "a.txt").write_text("hello")
    mv_command(["a.txt", "c.txt"])
    assert (temp_dir / "c.txt").exists()
    assert not (temp_dir / "a.txt").exists()


def test_rm_file(temp_dir):
    (temp_dir / "a.txt").write_text("delete me")
    rm_command(["a.txt", "--yes"])
    assert not (temp_dir / "a.txt").exists()


def test_grep_search(temp_dir, capsys):
    (temp_dir / "a.txt").write_text("hello world", encoding="utf-8")
    results = grep_command(["hello", str(temp_dir / "a.txt")])
    expected_line = f"{temp_dir / 'a.txt'}:1:hello world"
    assert len(results) == 1
    assert expected_line == results[0]


def test_zip_unzip(temp_dir):
    (temp_dir / "folder").mkdir()
    (temp_dir / "folder/file.txt").write_text("data")

    zip_folder(["folder", "archive.zip"])
    assert Path("archive.zip").exists()

    unzip_archive(["archive.zip"])
    assert (temp_dir / "folder/file.txt").exists()
