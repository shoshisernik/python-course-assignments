# Import the program file under test: PCR extension time calculator_cmdline_copy.py
from importlib.util import spec_from_file_location, module_from_spec
from pathlib import Path
import sys
import pytest

# Load the target file from the same folder as this test
_test_path = Path(__file__).resolve().parent / "PCR extension time calculator_cmdline_copy.py"
if not _test_path.exists():
    # fallback to day02 if you accidentally placed it there
    _test_path = Path(__file__).resolve().parent.parent / "day02" / "PCR extension time calculator_cmdline_copy.py"
spec = spec_from_file_location("pcr_cmdline_copy", str(_test_path))
module = module_from_spec(spec)
spec.loader.exec_module(module)


def test_calculate_extension_time_seconds_and_minutes(capsys):
    module.calculate_extension_time(2.0, 150.0)
    out = capsys.readouterr().out
    assert "Extension time: 75.00 seconds" in out
    assert "Or: 1 minutes and 15.00 seconds" in out


def test_calculate_extension_time_only_seconds_when_less_than_minute(capsys):
    module.calculate_extension_time(2.0, 50.0)
    out = capsys.readouterr().out
    assert "Extension time: 25.00 seconds" in out
    assert "Or:" not in out


def test_calculate_extension_time_zero_rate_reports_error(capsys):
    module.calculate_extension_time(0, 100.0)
    out = capsys.readouterr().out
    assert "Error: Enzyme rate cannot be zero" in out


def test_main_parses_args_and_prints(capsys, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["prog", "2.0", "150.0"])
    module.main()
    out = capsys.readouterr().out
    assert "Extension time: 75.00 seconds" in out