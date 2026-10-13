import json
import shutil
import subprocess
from pathlib import Path

import pytest

LEAN_ROOT = Path(__file__).resolve().parents[1] / "lean"


@pytest.mark.lean
def test_lean_executable_emits_only_scaffold_status():
    if shutil.which("lake") is None:
        pytest.skip("Install the pinned Lean toolchain to run the Lean smoke test.")
    build = subprocess.run(
        ["lake", "build"],
        cwd=LEAN_ROOT,
        capture_output=True,
        text=True,
        check=False,
        timeout=180,
    )
    assert build.returncode == 0, build.stdout + build.stderr
    result = subprocess.run(
        ["lake", "exe", "beutiproof-status"],
        cwd=LEAN_ROOT,
        capture_output=True,
        text=True,
        check=False,
        timeout=30,
    )
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout) == {
        "schema_version": "0.1.0",
        "status": "scaffold",
        "analysis_available": False,
    }
