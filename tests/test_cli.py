import pytest

from letter_metter.cli import main


@pytest.fixture
def text_file(tmp_path):
    path = tmp_path / "sample.txt"
    path.write_text(
        "En un lugar de la Mancha, de cuyo nombre no quiero acordarme", encoding="utf-8"
    )
    return path


def test_prints_full_report(text_file, capsys):
    assert main([str(text_file), "--kpm", "15"]) == 0
    out = capsys.readouterr().out
    for expected in (
        "Valid keystrokes: 48",
        "Distance QWERTY:",
        "Distance Eye Sense:",
        "Saved distance:",
        "Baseline of 15.0 KPM",
        "Extrapolated to",
        "Total time saved:",
    ):
        assert expected in out
    assert out.isascii(), "report must be printable on any console encoding"


def test_accepts_utf8_bom(tmp_path, capsys):
    path = tmp_path / "bom.txt"
    path.write_bytes("﻿hola".encode())
    assert main([str(path)]) == 0
    assert "Valid keystrokes: 4" in capsys.readouterr().out


def test_missing_file_exits_with_error(tmp_path, capsys):
    assert main([str(tmp_path / "missing.txt")]) == 1
    assert "file not found" in capsys.readouterr().err


@pytest.mark.parametrize("args", [["--kpm", "0"], ["--eye-scale", "-1"]])
def test_invalid_numbers_exit_with_error(text_file, capsys, args):
    assert main([str(text_file), *args]) == 1
    assert "Error" in capsys.readouterr().err


def test_too_short_text_exits_with_error(tmp_path, capsys):
    path = tmp_path / "short.txt"
    path.write_text("a", encoding="utf-8")
    assert main([str(path)]) == 1
    assert "Not enough" in capsys.readouterr().err
