from napari_plugin_engine import napari_hook_implementation
from .qt_console import QtConsole


@napari_hook_implementation
def napari_experimental_provide_dock_widget():
    return (QtConsole, {'area': 'bottom'})
