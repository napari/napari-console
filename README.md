# napari-console (WIP, under active development)

[![License](https://img.shields.io/pypi/l/napari-console.svg?color=green)](https://github.com/napari/napari-console/raw/master/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/napari-console.svg?color=green)](https://pypi.org/project/napari-console)
[![Python Version](https://img.shields.io/pypi/pyversions/napari-console.svg?color=green)](https://python.org)
[![tests](https://github.com/napari/napari-console/workflows/tests/badge.svg)](https://github.com/napari/napari-console/actions)
[![codecov](https://codecov.io/gh/napari/napari-console/branch/main/graph/badge.svg)](https://codecov.io/gh/napari/napari-console)

A plugin that adds a console to napari

----------------------------------

This [napari] plugin was generated with [Cookiecutter] using with [@napari]'s [cookiecutter-napari-plugin] template.

<!--
Don't miss the full getting started guide to set up your new package:
https://github.com/napari/cookiecutter-napari-plugin#getting-started

and review the napari docs for plugin developers:
https://napari.org/docs/plugins/index.html
-->

## Capturing variables

Since napari-console 0.0.9 the napari-console try to determine the variables that are defined in place where 
napari viewer is created and pass them to the console. 
Technically it looks for a first frame of stacktrace which is not in `napari_console`, `napari` and `in_n_out` modules.
Then it looks for the variables in the frame's `f_locals` and `f_globals` and passes them to the console.

If you create napari viewer in your own application and want to disable this behavior you can create
`NAPARI_EMBED` global variable before creating the viewer.


## Installation

You can install `napari-console` via [pip]:

    pip install napari-console

## Contributing

Contributions are very welcome. Tests can be run with [tox], please ensure
the coverage at least stays the same before you submit a pull request.

## License

Distributed under the terms of the [BSD-3] license,
"napari-console" is free and open source software

## Issues

If you encounter any problems, please [file an issue] along with a detailed description.

[napari]: https://github.com/napari/napari
[Cookiecutter]: https://github.com/audreyr/cookiecutter
[@napari]: https://github.com/napari
[MIT]: http://opensource.org/licenses/MIT
[BSD-3]: http://opensource.org/licenses/BSD-3-Clause
[GNU GPL v3.0]: http://www.gnu.org/licenses/gpl-3.0.txt
[GNU LGPL v3.0]: http://www.gnu.org/licenses/lgpl-3.0.txt
[Apache Software License 2.0]: http://www.apache.org/licenses/LICENSE-2.0
[Mozilla Public License 2.0]: https://www.mozilla.org/media/MPL/2.0/index.txt
[cookiecutter-napari-plugin]: https://github.com/napari/cookiecutter-napari-plugin
[file an issue]: https://github.com/sofroniewn/napari-console/issues
[napari]: https://github.com/napari/napari
[tox]: https://tox.readthedocs.io/en/latest/
[pip]: https://pypi.org/project/pip/
[PyPI]: https://pypi.org/
