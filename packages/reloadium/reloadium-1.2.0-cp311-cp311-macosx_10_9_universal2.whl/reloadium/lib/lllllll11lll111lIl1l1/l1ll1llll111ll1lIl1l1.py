from abc import ABC
from contextlib import contextmanager
from pathlib import Path
import sys
import types
from typing import TYPE_CHECKING, Any, ClassVar, Dict, Generator, List, Optional, Tuple, Type

from reloadium.corium.l111lllll111ll11Il1l1 import l11lll1ll1l1l111Il1l1, l111lllll111ll11Il1l1
from reloadium.corium.l11l11ll111l11llIl1l1 import l111l1l11l1lll11Il1l1, lll11l11lll1ll1lIl1l1
from reloadium.corium.l1l1l111l1l1ll1lIl1l1 import ll1111lll1l11111Il1l1, ll1lllllll1l1111Il1l1

if (TYPE_CHECKING):
    from dataclasses import dataclass, field

    from reloadium.lib.lllllll11lll111lIl1l1.l1l11l11lllll1llIl1l1 import lllll1l11ll1l1l1Il1l1
else:
    from reloadium.vendored.dataclasses import dataclass, field


__RELOADIUM__ = True


@dataclass
class l1lll1llll1ll11lIl1l1:
    l1l11l11lllll1llIl1l1: "lllll1l11ll1l1l1Il1l1"

    ll11111l11ll1l11Il1l1: ClassVar[str] = NotImplemented
    l11ll1ll111ll111Il1l1: bool = field(init=False, default=False)

    ll111llllll1l1l1Il1l1: l11lll1ll1l1l111Il1l1 = field(init=False)

    def __post_init__(l11l1ll1ll1ll111Il1l1) -> None:
        l11l1ll1ll1ll111Il1l1.ll111llllll1l1l1Il1l1 = l111lllll111ll11Il1l1.l1l11l1l1l11l1l1Il1l1(l11l1ll1ll1ll111Il1l1.ll11111l11ll1l11Il1l1)
        l11l1ll1ll1ll111Il1l1.ll111llllll1l1l1Il1l1.ll11ll111ll11ll1Il1l1('Creating extension')
        l11l1ll1ll1ll111Il1l1.l1l11l11lllll1llIl1l1.l111ll1lllll1ll1Il1l1.l11lll1ll1l1111lIl1l1.l1lll11lll1ll1llIl1l1(l11l1ll1ll1ll111Il1l1.ll11lll1l1l111l1Il1l1())

    def ll11lll1l1l111l1Il1l1(l11l1ll1ll1ll111Il1l1) -> List[Type[lll11l11lll1ll1lIl1l1]]:
        l1l1lll111l11111Il1l1 = []
        l11l11ll111l11llIl1l1 = l11l1ll1ll1ll111Il1l1.ll1ll11ll111l1l1Il1l1()
        for l1l1l111ll11ll1lIl1l1 in l11l11ll111l11llIl1l1:
            l1l1l111ll11ll1lIl1l1.l111l1l1l11lllllIl1l1 = l11l1ll1ll1ll111Il1l1.ll11111l11ll1l11Il1l1

        l1l1lll111l11111Il1l1.extend(l11l11ll111l11llIl1l1)
        return l1l1lll111l11111Il1l1

    def l11l111lll11l1llIl1l1(l11l1ll1ll1ll111Il1l1) -> None:
        l11l1ll1ll1ll111Il1l1.l11ll1ll111ll111Il1l1 = True

    def l1l1l11l11llllllIl1l1(l11l1ll1ll1ll111Il1l1, l1lll1ll11ll1l11Il1l1: types.ModuleType) -> None:
        pass

    @classmethod
    def l11111111l1l1ll1Il1l1(ll11l11ll11l11llIl1l1, l1lll1ll11ll1l11Il1l1: types.ModuleType) -> bool:
        if ( not hasattr(l1lll1ll11ll1l11Il1l1, '__name__')):
            return False

        l1l1lll111l11111Il1l1 = l1lll1ll11ll1l11Il1l1.__name__.split('.')[0].lower() == ll11l11ll11l11llIl1l1.ll11111l11ll1l11Il1l1.lower()
        return l1l1lll111l11111Il1l1

    @contextmanager
    def l1l1lll111lll1l1Il1l1(l11l1ll1ll1ll111Il1l1) -> Generator[None, None, None]:
        yield 

    def ll1l111ll1llll1lIl1l1(l11l1ll1ll1ll111Il1l1) -> None:
        pass

    def l1l1ll111l1l111lIl1l1(l11l1ll1ll1ll111Il1l1, llll1l111ll11lllIl1l1: Exception) -> None:
        pass

    def l111l11l11l111l1Il1l1(l11l1ll1ll1ll111Il1l1, ll1l111l111l1lllIl1l1: str, ll1l111l1ll111l1Il1l1: bool) -> Optional[ll1111lll1l11111Il1l1]:
        return None

    async def l1l1111l1lllllllIl1l1(l11l1ll1ll1ll111Il1l1, ll1l111l111l1lllIl1l1: str) -> Optional[ll1lllllll1l1111Il1l1]:
        return None

    def lll1ll11lll1l1llIl1l1(l11l1ll1ll1ll111Il1l1, ll1l111l111l1lllIl1l1: str) -> Optional[ll1111lll1l11111Il1l1]:
        return None

    async def l111ll1l1l1lllllIl1l1(l11l1ll1ll1ll111Il1l1, ll1l111l111l1lllIl1l1: str) -> Optional[ll1lllllll1l1111Il1l1]:
        return None

    def l1l11l1llll111l1Il1l1(l11l1ll1ll1ll111Il1l1, lll1ll1l1l1l1ll1Il1l1: Path) -> None:
        pass

    def l11llll1111l1lllIl1l1(l11l1ll1ll1ll111Il1l1, lll1ll1l1l1l1ll1Il1l1: Path) -> None:
        pass

    def lllll1lll11ll111Il1l1(l11l1ll1ll1ll111Il1l1, lll1ll1l1l1l1ll1Il1l1: Path, l1111l1ll111lll1Il1l1: List[l111l1l11l1lll11Il1l1]) -> None:
        pass

    def __eq__(l11l1ll1ll1ll111Il1l1, l111l1l1l1l1llllIl1l1: Any) -> bool:
        return id(l111l1l1l1l1llllIl1l1) == id(l11l1ll1ll1ll111Il1l1)

    def ll1ll11ll111l1l1Il1l1(l11l1ll1ll1ll111Il1l1) -> List[Type[lll11l11lll1ll1lIl1l1]]:
        return []

    def ll1l111l1l1l1111Il1l1(l11l1ll1ll1ll111Il1l1, l1lll1ll11ll1l11Il1l1: types.ModuleType, ll1l111l111l1lllIl1l1: str) -> bool:
        l1l1lll111l11111Il1l1 = (hasattr(l1lll1ll11ll1l11Il1l1, '__name__') and l1lll1ll11ll1l11Il1l1.__name__ == ll1l111l111l1lllIl1l1)
        return l1l1lll111l11111Il1l1


@dataclass(repr=False)
class ll11llll111l1l1lIl1l1(ll1111lll1l11111Il1l1):
    l1ll1llll111ll1lIl1l1: l1lll1llll1ll11lIl1l1

    def __repr__(l11l1ll1ll1ll111Il1l1) -> str:
        return 'ExtensionMemento'


@dataclass(repr=False)
class l1l1lllll1111l1lIl1l1(ll1lllllll1l1111Il1l1):
    l1ll1llll111ll1lIl1l1: l1lll1llll1ll11lIl1l1

    def __repr__(l11l1ll1ll1ll111Il1l1) -> str:
        return 'AsyncExtensionMemento'
