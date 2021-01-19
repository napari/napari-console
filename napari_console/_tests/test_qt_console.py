from unittest import mock

from IPython.terminal.interactiveshell import TerminalInteractiveShell

from napari_console import QtConsole
from napari import Viewer


def test_console(qtbot, make_test_viewer):
    """Test creating the console."""
    viewer = make_test_viewer()
    console = QtConsole(viewer)
    qtbot.addWidget(console)
    assert console.kernel_client is not None
    assert console.viewer is viewer


def test_ipython_console(qtbot, make_test_viewer):
    """Test mock-creating a console from within ipython."""

    def mock_get_ipython():
        return TerminalInteractiveShell()

    with mock.patch(
        'napari_console.qt_console.get_ipython',
        side_effect=mock_get_ipython,
    ):
        viewer = make_test_viewer()
        console = QtConsole(viewer)
        qtbot.addWidget(console)
        assert console.kernel_client is None
