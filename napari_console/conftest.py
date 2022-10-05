import os
import platform
import subprocess
import time

import pytest


@pytest.fixture
def linux_wm():
    """Start a WM in the background for tests that need a WM.

    This will only run on Linux and in CI (determined by CI env var).
    """
    wm = os.environ.get("WM", "herbstluftwm")
    proc = None
    if platform.system() == "Linux" and os.environ.get("CI"):
        proc = subprocess.Popen([wm])
        time.sleep(1)

    yield proc

    if proc:
        proc.terminate()
        try:
            proc.wait(timeout=20)
        except subprocess.TimeoutExpired:
            proc.kill()
            raise subprocess.SubprocessError(f"failed to terminate window manager '{wm}'")
