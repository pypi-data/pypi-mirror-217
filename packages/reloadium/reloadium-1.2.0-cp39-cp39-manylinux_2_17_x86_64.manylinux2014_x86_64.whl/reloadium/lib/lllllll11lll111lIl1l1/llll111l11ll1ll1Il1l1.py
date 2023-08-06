import types
from typing import TYPE_CHECKING, Any, Callable, Dict, Generator, List, Optional, Tuple, Type, Union, cast

from reloadium.lib.lllllll11lll111lIl1l1.l1ll1llll111ll1lIl1l1 import l1lll1llll1ll11lIl1l1
from reloadium.lib import l111l1ll1l1l1lllIl1l1

if (TYPE_CHECKING):
    from dataclasses import dataclass, field
else:
    from reloadium.vendored.dataclasses import dataclass, field


__RELOADIUM__ = True


@dataclass
class l1l11l1111ll11llIl1l1(l1lll1llll1ll11lIl1l1):
    ll11111l11ll1l11Il1l1 = 'Multiprocessing'

    def __post_init__(l11l1ll1ll1ll111Il1l1) -> None:
        super().__post_init__()

    def l1l1l11l11llllllIl1l1(l11l1ll1ll1ll111Il1l1, l1lll1ll11ll1l11Il1l1: types.ModuleType) -> None:
        if (l11l1ll1ll1ll111Il1l1.ll1l111l1l1l1111Il1l1(l1lll1ll11ll1l11Il1l1, 'multiprocessing.popen_spawn_posix')):
            l11l1ll1ll1ll111Il1l1.l11l1l1l1l11ll11Il1l1(l1lll1ll11ll1l11Il1l1)

        if (l11l1ll1ll1ll111Il1l1.ll1l111l1l1l1111Il1l1(l1lll1ll11ll1l11Il1l1, 'multiprocessing.popen_spawn_win32')):
            l11l1ll1ll1ll111Il1l1.l11llll1lll11l1lIl1l1(l1lll1ll11ll1l11Il1l1)

    def l11l1l1l1l11ll11Il1l1(l11l1ll1ll1ll111Il1l1, l1lll1ll11ll1l11Il1l1: types.ModuleType) -> None:
        import multiprocessing.popen_spawn_posix
        multiprocessing.popen_spawn_posix.Popen._launch = l111l1ll1l1l1lllIl1l1.llll111l11ll1ll1Il1l1.lllll11l11111l1lIl1l1  # type: ignore

    def l11llll1lll11l1lIl1l1(l11l1ll1ll1ll111Il1l1, l1lll1ll11ll1l11Il1l1: types.ModuleType) -> None:
        import multiprocessing.popen_spawn_win32
        multiprocessing.popen_spawn_win32.Popen.__init__ = l111l1ll1l1l1lllIl1l1.llll111l11ll1ll1Il1l1.__init__  # type: ignore
