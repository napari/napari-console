from napari_console import QtConsole


def test_console():
    console = QtConsole()
    assert console is not None
