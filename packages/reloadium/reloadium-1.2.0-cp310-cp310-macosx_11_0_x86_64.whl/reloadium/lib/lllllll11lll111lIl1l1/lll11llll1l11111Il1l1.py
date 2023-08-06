from pathlib import Path
import types
from typing import TYPE_CHECKING, Any, List

from reloadium.lib.lllllll11lll111lIl1l1.l1ll1llll111ll1lIl1l1 import l1lll1llll1ll11lIl1l1
from reloadium.corium.l11l11ll111l11llIl1l1 import l111l1l11l1lll11Il1l1
from reloadium.corium.ll111l1111l11lllIl1l1 import ll11ll1111l11111Il1l1

if (TYPE_CHECKING):
    from dataclasses import dataclass, field
else:
    from reloadium.vendored.dataclasses import dataclass, field


__RELOADIUM__ = True


@dataclass
class ll1l111ll111lll1Il1l1(l1lll1llll1ll11lIl1l1):
    ll11111l11ll1l11Il1l1 = 'PyGame'

    l1lll11ll1l1llllIl1l1: bool = field(init=False, default=False)

    def l1l1l11l11llllllIl1l1(l11l1ll1ll1ll111Il1l1, l11ll1l11ll1l111Il1l1: types.ModuleType) -> None:
        if (l11l1ll1ll1ll111Il1l1.ll1l111l1l1l1111Il1l1(l11ll1l11ll1l111Il1l1, 'pygame.base')):
            l11l1ll1ll1ll111Il1l1.l1ll111l1l11l111Il1l1()

    def l1ll111l1l11l111Il1l1(l11l1ll1ll1ll111Il1l1) -> None:
        import pygame.display

        l1lll1ll111l111lIl1l1 = pygame.display.update

        def ll111ll1l1l1ll1lIl1l1(*l1l111l1111l1lllIl1l1: Any, **ll11111111ll11llIl1l1: Any) -> None:
            if (l11l1ll1ll1ll111Il1l1.l1lll11ll1l1llllIl1l1):
                ll11ll1111l11111Il1l1.l11llll1llll111lIl1l1(0.1)
                return None
            else:
                return l1lll1ll111l111lIl1l1(*l1l111l1111l1lllIl1l1, **ll11111111ll11llIl1l1)

        pygame.display.update = ll111ll1l1l1ll1lIl1l1

    def l11llll1111l1lllIl1l1(l11l1ll1ll1ll111Il1l1, lll1ll1l1l1l1ll1Il1l1: Path) -> None:
        l11l1ll1ll1ll111Il1l1.l1lll11ll1l1llllIl1l1 = True

    def lllll1lll11ll111Il1l1(l11l1ll1ll1ll111Il1l1, lll1ll1l1l1l1ll1Il1l1: Path, l1111l1ll111lll1Il1l1: List[l111l1l11l1lll11Il1l1]) -> None:
        l11l1ll1ll1ll111Il1l1.l1lll11ll1l1llllIl1l1 = False

    def l1l1ll111l1l111lIl1l1(l11l1ll1ll1ll111Il1l1, llll1l111ll11lllIl1l1: Exception) -> None:
        l11l1ll1ll1ll111Il1l1.l1lll11ll1l1llllIl1l1 = False
