from unittest import mock

from IPython.terminal.interactiveshell import TerminalInteractiveShell

import pytest
from napari_console import QtConsole


@pytest.fixture
def make_test_viewer(qtbot, request):
    from napari import Viewer
    viewers = []

    def actual_factory(*model_args, viewer_class=Viewer, **model_kwargs):
        model_kwargs.setdefault('show', False)
        viewer = viewer_class(*model_args, **model_kwargs)
        viewers.append(viewer)
        return viewer

    yield actual_factory

    for viewer in viewers:
        viewer.close() 


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
