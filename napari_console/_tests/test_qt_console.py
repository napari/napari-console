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


def test_console_focus_proxy(qtbot, make_test_viewer):
    """Test setting/clearing focus on a QtConsole sets/clears focus on the underlying QTextEdit"""
    viewer = make_test_viewer()

    # setFocus does nothing if the widget is not shown
    console = viewer.window._qt_viewer.console
    with qtbot.waitExposed(console):
        viewer.show()
        viewer.window._qt_viewer.toggle_console_visibility()

    console.clearFocus()

    assert (
        not console._control.hasFocus()
    ), "underlying QTextEdit widget should not have focus after clearing"

    console.setFocus()

    # timeout (in ms) avoids flaky tests since setting focus takes time
    def control_has_focus():
        assert (
            console._control.hasFocus()
        ), "underlying QTextEdit widget never received focus"

    qtbot.waitUntil(control_has_focus)


def test_console_pass_variable(make_test_viewer, monkeypatch):
    monkeypatch.setattr("napari_console.qt_console._PREF_LIST", ["napari.", "in_n_out."])
    variable1 = True
    variable2 = "sample text"

    viewer = make_test_viewer()
    console = viewer.window._qt_viewer.console
    assert console.shell.user_ns['variable1'] == variable1
    assert console.shell.user_ns['variable2'] == variable2

    assert "mock" in console.shell.user_ns


def test_console_disable_pass_variable(make_test_viewer, monkeypatch):
    monkeypatch.setattr("napari_console.qt_console._PREF_LIST", ["napari.", "in_n_out."])
    monkeypatch.setitem(globals(), "NAPARI_EMBED", True)
    variable3 = True

    viewer = make_test_viewer()
    console = viewer.window._qt_viewer.console
    assert locals()['variable3'] == variable3
    assert "variable3" not in console.shell.user_ns
