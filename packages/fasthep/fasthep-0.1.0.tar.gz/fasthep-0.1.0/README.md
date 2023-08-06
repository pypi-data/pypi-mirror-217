# fasthep

[![Actions Status][actions-badge]][actions-link]
[![Documentation Status][rtd-badge]][rtd-link]

[![PyPI version][pypi-version]][pypi-link]
[![PyPI platforms][pypi-platforms]][pypi-link]

[![GitHub Discussion][github-discussions-badge]][github-discussions-link]
[![Gitter][gitter-badge]][gitter-link]

FAST-HEP provides tools for analysis of high-energy physics data. It is designed
to be used in conjunction [SciKit-HEP](https://scikit-hep.org/) packages such as
[uproot](https://github.com/scikit-hep/uproot5) and
[awkward-array](https://github.com/scikit-hep/awkward) and more. On the data
processing side it leverages [Numba](https://numba.pydata.org/) and
[Cupy](https://cupy.dev/) to provide fast and efficient implementations of
common analysis tasks. For distributed computing, Dask is used as the primary
backend.

## Installation

The meta-package `fasthep` can be installed via `pip` or `conda`:

```bash
pip install fasthep
```

by default, this will install only the core packages such as the FAST-HEP CLI
and logging packages. To install the full package, including the optional
dependencies, use:

```bash
pip install fasthep[full]
```

You can also cherry-picker the optional dependencies you want to install:

```bash
pip install fasthep[plotting, carpenter, validate]
```

<!-- prettier-ignore-start -->
[actions-badge]:            https://github.com/FAST-HEP/fasthep/workflows/CI/badge.svg
[actions-link]:             https://github.com/FAST-HEP/fasthep/actions
[github-discussions-badge]: https://img.shields.io/static/v1?label=Discussions&message=Ask&color=blue&logo=github
[github-discussions-link]:  https://github.com/orgs/FAST-HEP/discussions
[gitter-badge]:             https://badges.gitter.im/FAST-HEP/community.svg
[gitter-link]:              https://gitter.im/FAST-HEP/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge
[pypi-link]:                https://pypi.org/project/fasthep/
[pypi-platforms]:           https://img.shields.io/pypi/pyversions/fasthep
[pypi-version]:             https://img.shields.io/pypi/v/fasthep
[rtd-badge]:                https://readthedocs.org/projects/fasthep/badge/?version=latest
[rtd-link]:                 https://fasthep.readthedocs.io/en/latest/?badge=latest

<!-- prettier-ignore-end -->
