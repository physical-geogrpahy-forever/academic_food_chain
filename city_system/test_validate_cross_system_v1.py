import subprocess
import sys
from pathlib import Path


def test_cross_system_validator_exits_zero():
    script = Path(__file__).resolve().parent / "validate_cross_system_v1.py"
    result = subprocess.run([sys.executable, str(script)], capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + "\n" + result.stderr
    assert "CROSS_SYSTEM_STATIC_QA: PASS" in result.stdout
