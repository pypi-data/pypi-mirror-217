from typing import Any, ClassVar, List, Optional, Type

from reloadium.corium.l1l1l1l1llllllllIl1l1 import l11l111l1111l11lIl1l1

try:
    import pandas as pd 
except ImportError:
    pass

from typing import TYPE_CHECKING

from reloadium.corium.l11l11ll111l11llIl1l1 import llll111111111111Il1l1, lll11l11lll1ll1lIl1l1, l11111l1l11111l1Il1l1, l1ll1l111l1l1111Il1l1

if (TYPE_CHECKING):
    from dataclasses import dataclass
else:
    from reloadium.vendored.dataclasses import dataclass, field

from reloadium.lib.lllllll11lll111lIl1l1.l1ll1llll111ll1lIl1l1 import l1lll1llll1ll11lIl1l1


__RELOADIUM__ = True


@dataclass(**l1ll1l111l1l1111Il1l1)
class lllllll1l111lll1Il1l1(l11111l1l11111l1Il1l1):
    l11l11llll1l111lIl1l1 = 'Dataframe'

    @classmethod
    def l1l1l1111lllllllIl1l1(ll11l11ll11l11llIl1l1, ll111ll11111l1llIl1l1: l11l111l1111l11lIl1l1.l11l111llll111llIl1l1, ll11l1l111l1lll1Il1l1: Any, l1llll11ll1lll1lIl1l1: llll111111111111Il1l1) -> bool:
        if (type(ll11l1l111l1lll1Il1l1) is pd.DataFrame):
            return True

        return False

    def l11111lll11ll1l1Il1l1(l11l1ll1ll1ll111Il1l1, lll11l1lll1l11l1Il1l1: lll11l11lll1ll1lIl1l1) -> bool:
        return l11l1ll1ll1ll111Il1l1.ll11l1l111l1lll1Il1l1.equals(lll11l1lll1l11l1Il1l1.ll11l1l111l1lll1Il1l1)

    @classmethod
    def l1llll1l11ll11l1Il1l1(ll11l11ll11l11llIl1l1) -> int:
        return 200


@dataclass(**l1ll1l111l1l1111Il1l1)
class l1ll1ll1lll1l11lIl1l1(l11111l1l11111l1Il1l1):
    l11l11llll1l111lIl1l1 = 'Series'

    @classmethod
    def l1l1l1111lllllllIl1l1(ll11l11ll11l11llIl1l1, ll111ll11111l1llIl1l1: l11l111l1111l11lIl1l1.l11l111llll111llIl1l1, ll11l1l111l1lll1Il1l1: Any, l1llll11ll1lll1lIl1l1: llll111111111111Il1l1) -> bool:
        if (type(ll11l1l111l1lll1Il1l1) is pd.Series):
            return True

        return False

    def l11111lll11ll1l1Il1l1(l11l1ll1ll1ll111Il1l1, lll11l1lll1l11l1Il1l1: lll11l11lll1ll1lIl1l1) -> bool:
        return l11l1ll1ll1ll111Il1l1.ll11l1l111l1lll1Il1l1.equals(lll11l1lll1l11l1Il1l1.ll11l1l111l1lll1Il1l1)

    @classmethod
    def l1llll1l11ll11l1Il1l1(ll11l11ll11l11llIl1l1) -> int:
        return 200


@dataclass
class ll111ll111llll1lIl1l1(l1lll1llll1ll11lIl1l1):
    ll11111l11ll1l11Il1l1 = 'Pandas'

    def ll1ll11ll111l1l1Il1l1(l11l1ll1ll1ll111Il1l1) -> List[Type["lll11l11lll1ll1lIl1l1"]]:
        return [lllllll1l111lll1Il1l1, l1ll1ll1lll1l11lIl1l1]
