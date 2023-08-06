import sys

from reloadium.corium.ll111l1111l11lllIl1l1.l111111lllll1l1lIl1l1 import l1l11l11l1l1llllIl1l1

__RELOADIUM__ = True

l1l11l11l1l1llllIl1l1()


try:
    import _pytest.assertion.rewrite
except ImportError:
    class llllll11l1l111l1Il1l1:
        pass

    _pytest = lambda :None  # type: ignore
    sys.modules['_pytest'] = _pytest

    _pytest.assertion = lambda :None  # type: ignore
    sys.modules['_pytest.assertion'] = _pytest.assertion

    _pytest.assertion.rewrite = lambda :None  # type: ignore
    _pytest.assertion.rewrite.AssertionRewritingHook = llllll11l1l111l1Il1l1  # type: ignore
    sys.modules['_pytest.assertion.rewrite'] = _pytest.assertion.rewrite
