import pytest
import sys

from napari import Viewer


def pytest_addoption(parser):
    """Add napari specific command line options.

    --show-viewer
        Show viewers during tests, they are hidden by default. Showing viewers
        decreases test speed by around 20%.

    Notes
    -----
    Due to the placement of this conftest.py file, you must specifically name
    the napari folder such as "pytest napari --show-viewer"
    """
    parser.addoption(
        "--show-viewer",
        action="store_true",
        default=False,
        help="don't show viewer during tests",
    )


@pytest.fixture
def qtbot(qtbot):
    """A modified qtbot fixture that makes sure no widgets have been leaked."""
    from qtpy.QtWidgets import QApplication

    initial = QApplication.topLevelWidgets()
    prior_exception = getattr(sys, 'last_value', None)

    yield qtbot

    # if an exception was raised during the test, we should just quit now and
    # skip looking for leaked widgets.
    if getattr(sys, 'last_value', None) is not prior_exception:
        return

    QApplication.processEvents()
    leaks = set(QApplication.topLevelWidgets()).difference(initial)
    # still not sure how to clean up some of the remaining vispy
    # vispy.app.backends._qt.CanvasBackendDesktop widgets...
    if any([n.__class__.__name__ != 'CanvasBackendDesktop' for n in leaks]):
        raise AssertionError(f'Widgets leaked!: {leaks}')
    if leaks:
        warnings.warn(f'Widgets leaked!: {leaks}')


@pytest.fixture(scope="function")
def make_test_viewer(qtbot, request):
    viewers: List[Viewer] = []

    def actual_factory(*model_args, viewer_class=Viewer, **model_kwargs):
        model_kwargs['show'] = model_kwargs.pop(
            'show', request.config.getoption("--show-viewer")
        )
        viewer = viewer_class(*model_args, **model_kwargs)
        viewers.append(viewer)
        return viewer

    yield actual_factory

    for viewer in viewers:
        viewer.close()