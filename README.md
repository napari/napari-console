# napari-console

[![License](https://img.shields.io/pypi/l/napari-console.svg?color=green)](https://github.com/napari/napari-console/raw/master/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/napari-console.svg?color=green)](https://pypi.org/project/napari-console)
[![Python Version](https://img.shields.io/pypi/pyversions/napari-console.svg?color=green)](https://python.org)
[![tests](https://github.com/napari/napari-console/workflows/tests/badge.svg)](https://github.com/napari/napari-console/actions)
[![codecov](https://codecov.io/gh/napari/napari-console/branch/main/graph/badge.svg)](https://codecov.io/gh/napari/napari-console)

A plugin that adds a console to [napari]. This plugin is maintained by the [@napari] team.

`napari-console` adds an interactive console based on IPython to `napari`. The napari UI contains a
[console button](https://napari.org/dev/getting_started/viewer.html#console-button) to display the
console. This button is enabled if you launch napari from the command line, a script, or use the
napari bundled app.

![napari-console in napari UI](https://github.com/napari/docs/blob/main/docs/_static/images/console.png)

## License

Distributed under the terms of the [BSD-3] license,
"napari-console" is free and open source software

## Issues

If you encounter any problems, please file an issue along with a detailed description.

## Contributing

Contributions are very welcome. Tests can be run with [tox]. Please ensure
test coverage results remain the same or higher than before you submit a pull request.

## Installation

You can install `napari-console` via [pip]:

    pip install napari-console

## Local variables and napari-console

In napari-console 0.0.8 and earlier, the console `locals()` namespace only
contained a reference to the napari viewer that enclosed the console.

Since version 0.0.9, it instead contains everything in the enclosing frame that
called napari. That is, if your Python code is:

```python
import napari
import numpy as np
from scipy import ndimage as ndi

image = np.random.random((500, 500))
labels = ndi.label(image > 0.7)[0]

viewer, image_layer = napari.imshow(image)
labels_layer = viewer.add_labels(labels)

napari.run()
```

Then the napari console will have the variables `np`, `napari`, `ndi`, `image`,
`labels`, `viewer`, `image_layer`, and `labels_layer` in its namespace.

This is implemented by inspecting the Python stack when the console is first
instantiated, finding the first frame that is outside of the `napari_console`,
`napari`, and `in_n_out` modules, and passing the variables in the frame's
`f_locals` and `f_globals` to the console namespace.

If you want to disable this behavior (for example, because you are embedding
napari and the console within some larger application), add
`NAPARI_EMBED=1` to your environment variables before instantiating the
console.

[napari]: https://github.com/napari/napari
[@napari]: https://github.com/napari
[BSD-3]: http://opensource.org/licenses/BSD-3-Clause
[napari]: https://github.com/napari/napari
[tox]: https://tox.readthedocs.io/en/latest/
[pip]: https://pypi.org/project/pip/
