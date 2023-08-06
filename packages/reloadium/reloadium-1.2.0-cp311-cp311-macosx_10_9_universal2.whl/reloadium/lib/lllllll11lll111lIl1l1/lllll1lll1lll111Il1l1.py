import sys
from contextlib import contextmanager
from pathlib import Path
import types
from typing import TYPE_CHECKING, Any, Dict, Generator, List, Tuple, Type

from reloadium.corium.ll111l1111l11lllIl1l1 import ll11ll1111l11111Il1l1
from reloadium.lib.environ import env
from reloadium.corium.lll11l11111lll11Il1l1 import ll111l1l1lll1l1lIl1l1
from reloadium.lib.lllllll11lll111lIl1l1.l1lll1lll11l11l1Il1l1 import l11l1ll1l1ll11llIl1l1
from reloadium.corium.l11l11ll111l11llIl1l1 import llll111111111111Il1l1, lll11l11lll1ll1lIl1l1, l11111l1l11111l1Il1l1, l1ll1l111l1l1111Il1l1

if (TYPE_CHECKING):
    from dataclasses import dataclass
else:
    from reloadium.vendored.dataclasses import dataclass


__RELOADIUM__ = True


@dataclass
class lll11111ll1l1l1lIl1l1(l11l1ll1l1ll11llIl1l1):
    ll11111l11ll1l11Il1l1 = 'FastApi'

    ll11ll11l111l1llIl1l1 = 'uvicorn'

    @contextmanager
    def l1l1lll111lll1l1Il1l1(l11l1ll1ll1ll111Il1l1) -> Generator[None, None, None]:
        yield 

    def ll1ll11ll111l1l1Il1l1(l11l1ll1ll1ll111Il1l1) -> List[Type[lll11l11lll1ll1lIl1l1]]:
        return []

    def l1l1l11l11llllllIl1l1(l11l1ll1ll1ll111Il1l1, l11ll1l11ll1l111Il1l1: types.ModuleType) -> None:
        if (l11l1ll1ll1ll111Il1l1.ll1l111l1l1l1111Il1l1(l11ll1l11ll1l111Il1l1, l11l1ll1ll1ll111Il1l1.ll11ll11l111l1llIl1l1)):
            l11l1ll1ll1ll111Il1l1.l111llll11l1llllIl1l1()

    @classmethod
    def l11111111l1l1ll1Il1l1(ll11l11ll11l11llIl1l1, l1lll1ll11ll1l11Il1l1: types.ModuleType) -> bool:
        l1l1lll111l11111Il1l1 = super().l11111111l1l1ll1Il1l1(l1lll1ll11ll1l11Il1l1)
        l1l1lll111l11111Il1l1 |= l1lll1ll11ll1l11Il1l1.__name__ == ll11l11ll11l11llIl1l1.ll11ll11l111l1llIl1l1
        return l1l1lll111l11111Il1l1

    def l111llll11l1llllIl1l1(l11l1ll1ll1ll111Il1l1) -> None:
        l11l1111ll11ll1lIl1l1 = '--reload'
        if (l11l1111ll11ll1lIl1l1 in sys.argv):
            sys.argv.remove('--reload')
