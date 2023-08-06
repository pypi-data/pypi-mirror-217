from pathlib import Path
import sys
import threading
from types import CodeType, FrameType, ModuleType
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Set, cast

from reloadium.corium import l1llll11l1ll11llIl1l1, lll11l11111lll11Il1l1, public, l1l11111ll11llllIl1l1, ll111l1111l11lllIl1l1
from reloadium.corium.l111ll111lll11llIl1l1 import l1llll1ll1llll11Il1l1, l1l11ll111ll11l1Il1l1
from reloadium.corium.lll11l11111lll11Il1l1 import lll11ll11l1l11l1Il1l1, ll111l1l1lll1l1lIl1l1, l111l11llll11l11Il1l1
from reloadium.corium.l1lll111l111l111Il1l1 import ll1lll1l11ll11llIl1l1
from reloadium.corium.l111lllll111ll11Il1l1 import l111lllll111ll11Il1l1
from reloadium.corium.lll1111111l1l1llIl1l1 import l11111llll1l1l11Il1l1
from reloadium.corium.l1l1l111l1l1ll1lIl1l1 import ll1111lll1l11111Il1l1, ll1lllllll1l1111Il1l1

if (TYPE_CHECKING):
    from dataclasses import dataclass, field
else:
    from reloadium.vendored.dataclasses import dataclass, field


__RELOADIUM__ = True

__all__ = ['ll1l111lllllllllIl1l1', 'lll1l11l11111lllIl1l1', 'll11111111ll1ll1Il1l1']


ll1ll11llllll1llIl1l1 = l111lllll111ll11Il1l1.l1l11l1l1l11l1l1Il1l1(__name__)


class ll1l111lllllllllIl1l1:
    @classmethod
    def l1111l11l1llll1lIl1l1(l11l1ll1ll1ll111Il1l1) -> Optional[FrameType]:
        l1l111111l1lll11Il1l1: FrameType = sys._getframe(2)
        l1l1lll111l11111Il1l1 = next(ll111l1111l11lllIl1l1.l1l111111l1lll11Il1l1.l1llll111ll1111lIl1l1(l1l111111l1lll11Il1l1))
        return l1l1lll111l11111Il1l1


class lll1l11l11111lllIl1l1(ll1l111lllllllllIl1l1):
    @classmethod
    def llll11l1l1l111l1Il1l1(ll11l11ll11l11llIl1l1, l1l111l1111l1lllIl1l1: List[Any], ll11111111ll11llIl1l1: Dict[str, Any], ll111lll111l1111Il1l1: List[ll1111lll1l11111Il1l1]) -> Any:  # type: ignore
        with ll111l1l1lll1l1lIl1l1():
            assert ll1lll1l11ll11llIl1l1.l111ll1lllll1ll1Il1l1.l111l1ll1lllllllIl1l1
            l1l111111l1lll11Il1l1 = ll1lll1l11ll11llIl1l1.l111ll1lllll1ll1Il1l1.l111l1ll1lllllllIl1l1.l1lll11l1l1l11l1Il1l1.ll11ll1l1l1ll1llIl1l1()
            l1l111111l1lll11Il1l1.ll1l1l1lll1ll1l1Il1l1()

            l1111lll1ll1111lIl1l1 = ll1lll1l11ll11llIl1l1.l111ll1lllll1ll1Il1l1.ll11l1111l11l1llIl1l1.lllll1l1l1l111l1Il1l1(l1l111111l1lll11Il1l1.lllll11l111111l1Il1l1, l1l111111l1lll11Il1l1.l11l11111l1l11l1Il1l1.llll1111ll111l1lIl1l1())
            assert l1111lll1ll1111lIl1l1
            l1ll1l1111l11l1lIl1l1 = ll11l11ll11l11llIl1l1.l1111l11l1llll1lIl1l1()

            for lllll1l1l1ll1111Il1l1 in ll111lll111l1111Il1l1:
                lllll1l1l1ll1111Il1l1.l111l1l11ll1l1llIl1l1()

            for lllll1l1l1ll1111Il1l1 in ll111lll111l1111Il1l1:
                lllll1l1l1ll1111Il1l1.ll1111ll1ll1l1l1Il1l1()


        l1l1lll111l11111Il1l1 = l1111lll1ll1111lIl1l1(*l1l111l1111l1lllIl1l1, **ll11111111ll11llIl1l1);        l1l111111l1lll11Il1l1.ll1111lll11lll1lIl1l1.additional_info.pydev_step_stop = l1ll1l1111l11l1lIl1l1  # type: ignore

        return l1l1lll111l11111Il1l1

    @classmethod
    async def ll111l1l1l1l1111Il1l1(ll11l11ll11l11llIl1l1, l1l111l1111l1lllIl1l1: List[Any], ll11111111ll11llIl1l1: Dict[str, Any], ll111lll111l1111Il1l1: List[ll1lllllll1l1111Il1l1]) -> Any:  # type: ignore
        with ll111l1l1lll1l1lIl1l1():
            assert ll1lll1l11ll11llIl1l1.l111ll1lllll1ll1Il1l1.l111l1ll1lllllllIl1l1
            l1l111111l1lll11Il1l1 = ll1lll1l11ll11llIl1l1.l111ll1lllll1ll1Il1l1.l111l1ll1lllllllIl1l1.l1lll11l1l1l11l1Il1l1.ll11ll1l1l1ll1llIl1l1()
            l1l111111l1lll11Il1l1.ll1l1l1lll1ll1l1Il1l1()

            l1111lll1ll1111lIl1l1 = ll1lll1l11ll11llIl1l1.l111ll1lllll1ll1Il1l1.ll11l1111l11l1llIl1l1.lllll1l1l1l111l1Il1l1(l1l111111l1lll11Il1l1.lllll11l111111l1Il1l1, l1l111111l1lll11Il1l1.l11l11111l1l11l1Il1l1.llll1111ll111l1lIl1l1())
            assert l1111lll1ll1111lIl1l1
            l1ll1l1111l11l1lIl1l1 = ll11l11ll11l11llIl1l1.l1111l11l1llll1lIl1l1()

            for lllll1l1l1ll1111Il1l1 in ll111lll111l1111Il1l1:
                await lllll1l1l1ll1111Il1l1.l111l1l11ll1l1llIl1l1()

            for lllll1l1l1ll1111Il1l1 in ll111lll111l1111Il1l1:
                await lllll1l1l1ll1111Il1l1.ll1111ll1ll1l1l1Il1l1()


        l1l1lll111l11111Il1l1 = await l1111lll1ll1111lIl1l1(*l1l111l1111l1lllIl1l1, **ll11111111ll11llIl1l1);        l1l111111l1lll11Il1l1.ll1111lll11lll1lIl1l1.additional_info.pydev_step_stop = l1ll1l1111l11l1lIl1l1  # type: ignore

        return l1l1lll111l11111Il1l1


class ll11111111ll1ll1Il1l1(ll1l111lllllllllIl1l1):
    @classmethod
    def llll11l1l1l111l1Il1l1(ll11l11ll11l11llIl1l1) -> Optional[ModuleType]:  # type: ignore
        with ll111l1l1lll1l1lIl1l1():
            assert ll1lll1l11ll11llIl1l1.l111ll1lllll1ll1Il1l1.l111l1ll1lllllllIl1l1
            l1l111111l1lll11Il1l1 = ll1lll1l11ll11llIl1l1.l111ll1lllll1ll1Il1l1.l111l1ll1lllllllIl1l1.l1lll11l1l1l11l1Il1l1.ll11ll1l1l1ll1llIl1l1()

            lll1ll11ll1ll11lIl1l1 = Path(l1l111111l1lll11Il1l1.ll11l1l111l1lll1Il1l1.f_globals['__spec__'].origin).absolute()
            ll1ll1lll111l111Il1l1 = l1l111111l1lll11Il1l1.ll11l1l111l1lll1Il1l1.f_globals['__name__']
            l1l111111l1lll11Il1l1.ll1l1l1lll1ll1l1Il1l1()
            l1ll11l1l11ll1l1Il1l1 = ll1lll1l11ll11llIl1l1.l111ll1lllll1ll1Il1l1.l1l111l1ll1lll11Il1l1.llll1l1l11l1ll1lIl1l1(lll1ll11ll1ll11lIl1l1)

            if ( not l1ll11l1l11ll1l1Il1l1):
                ll1ll11llllll1llIl1l1.l1ll1llll11l11llIl1l1('Could not retrieve src.', lll11111l11111l1Il1l1={'file': l11111llll1l1l11Il1l1.lll1ll1l1l1l1ll1Il1l1(lll1ll11ll1ll11lIl1l1), 
'fullname': l11111llll1l1l11Il1l1.ll1ll1lll111l111Il1l1(ll1ll1lll111l111Il1l1)})

            assert l1ll11l1l11ll1l1Il1l1

        try:
            l1ll11l1l11ll1l1Il1l1.l1l11llllll1l1llIl1l1()
            l1ll11l1l11ll1l1Il1l1.ll1lllllll111ll1Il1l1(ll11ll1l1ll11l11Il1l1=False)
            l1ll11l1l11ll1l1Il1l1.l11ll111lllll111Il1l1(ll11ll1l1ll11l11Il1l1=False)
        except lll11ll11l1l11l1Il1l1 as l11l1llllll1l11lIl1l1:
            l1l111111l1lll11Il1l1.l1ll11lll1l111llIl1l1(l11l1llllll1l11lIl1l1)
            return None

        import importlib.util

        l1lll1llllll11l1Il1l1 = l1l111111l1lll11Il1l1.ll11l1l111l1lll1Il1l1.f_locals['__spec__']
        l1lll1ll11ll1l11Il1l1 = importlib.util.module_from_spec(l1lll1llllll11l1Il1l1)

        l1ll11l1l11ll1l1Il1l1.ll11l111ll1lll11Il1l1(l1lll1ll11ll1l11Il1l1)
        return l1lll1ll11ll1l11Il1l1


l1l11ll111ll11l1Il1l1.ll11ll1l11l1l1llIl1l1(l1llll1ll1llll11Il1l1.lllll1l1111111llIl1l1, lll1l11l11111lllIl1l1.llll11l1l1l111l1Il1l1)
l1l11ll111ll11l1Il1l1.ll11ll1l11l1l1llIl1l1(l1llll1ll1llll11Il1l1.ll1lllll1l1l11l1Il1l1, lll1l11l11111lllIl1l1.ll111l1l1l1l1111Il1l1)
l1l11ll111ll11l1Il1l1.ll11ll1l11l1l1llIl1l1(l1llll1ll1llll11Il1l1.l111l1111l1l111lIl1l1, ll11111111ll1ll1Il1l1.llll11l1l1l111l1Il1l1)
