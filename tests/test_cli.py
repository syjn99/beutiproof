import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def test_module_help_explains_scaffold_status():
    result = subprocess.run(
        [sys.executable, "-m", "beutiproof", "--help"],
        cwd=ROOT,
        env={**os.environ, "PYTHONPATH": str(ROOT / "src")},
        capture_output=True,
        text=True,
        check=False,
        timeout=30,
    )
    assert result.returncode == 0, result.stderr
    assert "scaffold" in result.stdout.lower()
    assert "check" in result.stdout
    assert "suggest" in result.stdout


def test_console_version_matches_installed_distribution():
    from importlib.metadata import version

    result = subprocess.run(
        [str(Path(sys.executable).with_name("beautiproof")), "--version"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
        timeout=30,
    )
    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == f"beautiproof {version('beutiproof')}"


def test_check_reports_unavailable_analysis_as_json():
    import json

    result = subprocess.run(
        [sys.executable, "-m", "beutiproof", "check", ".", "--format", "json"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
        timeout=30,
    )
    assert result.returncode == 2
    assert result.stdout.strip(), result.stderr
    payload = json.loads(result.stdout)
    assert payload["schema_version"] == "0.1.0"
    assert payload["status"] == "unsupported"
    assert payload["stage"] == "scaffold"
    assert payload["analysis_available"] is False
    assert payload["error"]["code"] == "not_implemented"
    assert "findings" not in payload


def test_suggest_reports_unavailable_refactoring_for_a_provider():
    import json

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "beutiproof",
            "suggest",
            ".",
            "--file",
            "Example.lean",
            "--theorem",
            "demo",
            "--provider",
            "configured",
            "--format",
            "json",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
        timeout=30,
    )
    assert result.returncode == 2
    assert result.stdout.strip(), result.stderr
    payload = json.loads(result.stdout)
    assert payload["error"]["code"] == "not_implemented"
    assert "Refactoring" in payload["error"]["message"]
    assert "patch" not in payload


@pytest.mark.parametrize(
    ("arguments", "expected_message"),
    [
        ([], "usage:"),
        (["unknown"], "invalid choice"),
        (["check"], "required"),
        (["check", ".", "--format", "xml"], "invalid choice"),
        (["check", "."], "Project analysis is not implemented"),
        (["suggest", "."], "Refactoring is not implemented"),
    ],
)
def test_incomplete_or_unavailable_commands_exit_two(arguments, expected_message):
    result = subprocess.run(
        [sys.executable, "-m", "beutiproof", *arguments],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
        timeout=30,
    )
    assert result.returncode == 2
    assert expected_message in result.stdout + result.stderr


@pytest.mark.parametrize("command", ["check", "suggest"])
def test_reserved_commands_leave_target_project_untouched(tmp_path, command):
    original = b"This is deliberately not executable Lean source.\n"
    project_file = tmp_path / "lakefile.lean"
    project_file.write_bytes(original)
    result = subprocess.run(
        [sys.executable, "-m", "beutiproof", command, str(tmp_path), "--format", "json"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
        timeout=30,
    )
    assert result.returncode == 2
    assert project_file.read_bytes() == original
    assert sorted(path.name for path in tmp_path.iterdir()) == ["lakefile.lean"]
