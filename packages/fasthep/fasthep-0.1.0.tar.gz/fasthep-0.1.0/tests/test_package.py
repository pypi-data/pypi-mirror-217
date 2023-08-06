from __future__ import annotations

import fasthep as m


def test_version():
    assert m.__version__


def test_import_carpenter():
    import fast_carpenter as fc

    assert fc.__version__


def test_import_curator():
    import fast_curator as fc

    assert fc.__version__


def test_import_flow():
    import fast_flow as ff

    assert ff.__version__


def test_import_plotter():
    import fast_plotter as fp

    assert fp.__version__


def test_import_validate():
    import skvalidate

    assert skvalidate.__version__
