import os
import platform
import subprocess
import time

import pytest


@pytest.fixture
def linux_wm_local():
    """Start a WM in the background for tests that need a WM.

    This will only run on Linux and in CI (determined by CI env var).

    The window manager start command can be set via env var `WM_START_CMD`
    (default is `herbstluftwm`).
    """
    wm_start_cmd = os.environ.get("WM_START_CMD", "herbstluftwm")
    proc = None
    if platform.system() == "Linux" and os.environ.get("CI"):
        proc = subprocess.Popen([wm_start_cmd])
        time.sleep(1)
        if proc.poll() is not None:
            raise RuntimeError(
                f"window manager '{wm_start_cmd}' process [{proc.pid}] exited, "
                f"return code: {proc.returncode}"
            )

    yield proc

    if proc:
        proc.terminate()
        try:
            proc.wait(timeout=20)
        except subprocess.TimeoutExpired:
            proc.kill()
            raise RuntimeError(f"failed to terminate window manager '{wm_start_cmd}'")
