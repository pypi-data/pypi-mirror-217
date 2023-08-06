import re
from contextlib import contextmanager
import os
import sys
import types
from pathlib import Path
from textwrap import dedent
from typing import TYPE_CHECKING, Any, Callable, Dict, Generator, List, Optional, Set, Tuple, Union

from reloadium.corium.lll11l11111lll11Il1l1 import ll111l1l1lll1l1lIl1l1
from reloadium.lib.lllllll11lll111lIl1l1.l1ll1llll111ll1lIl1l1 import l1lll1llll1ll11lIl1l1, ll11llll111l1l1lIl1l1
from reloadium.corium.l1l1l111l1l1ll1lIl1l1 import ll1111lll1l11111Il1l1
from reloadium.corium.ll111l1111l11lllIl1l1 import ll11ll1111l11111Il1l1

if (TYPE_CHECKING):
    from dataclasses import dataclass, field

    from sqlalchemy.engine.base import Engine, Transaction
    from sqlalchemy.orm.session import Session
else:
    from reloadium.vendored.dataclasses import dataclass, field


__RELOADIUM__ = True


@dataclass(repr=False)
class ll111llll11lll11Il1l1(ll11llll111l1l1lIl1l1):
    l1ll1llll111ll1lIl1l1: "l111l1l1lll111llIl1l1"
    l1l111ll111111l1Il1l1: List["Transaction"] = field(init=False, default_factory=list)

    def l1lllll11ll1ll11Il1l1(l11l1ll1ll1ll111Il1l1) -> None:
        from sqlalchemy.orm.session import _sessions

        super().l1lllll11ll1ll11Il1l1()

        ll1llll11ll11l1lIl1l1 = list(_sessions.values())

        for l1lllll1l111l111Il1l1 in ll1llll11ll11l1lIl1l1:
            if ( not l1lllll1l111l111Il1l1.is_active):
                continue

            ll1l1llll1ll1l11Il1l1 = l1lllll1l111l111Il1l1.begin_nested()
            l11l1ll1ll1ll111Il1l1.l1l111ll111111l1Il1l1.append(ll1l1llll1ll1l11Il1l1)

    def __repr__(l11l1ll1ll1ll111Il1l1) -> str:
        return 'DbMemento'

    def l111l1l11ll1l1llIl1l1(l11l1ll1ll1ll111Il1l1) -> None:
        super().l111l1l11ll1l1llIl1l1()

        while l11l1ll1ll1ll111Il1l1.l1l111ll111111l1Il1l1:
            ll1l1llll1ll1l11Il1l1 = l11l1ll1ll1ll111Il1l1.l1l111ll111111l1Il1l1.pop()
            if (ll1l1llll1ll1l11Il1l1.is_active):
                try:
                    ll1l1llll1ll1l11Il1l1.rollback()
                except :
                    pass

    def ll1111ll1ll1l1l1Il1l1(l11l1ll1ll1ll111Il1l1) -> None:
        super().ll1111ll1ll1l1l1Il1l1()

        while l11l1ll1ll1ll111Il1l1.l1l111ll111111l1Il1l1:
            ll1l1llll1ll1l11Il1l1 = l11l1ll1ll1ll111Il1l1.l1l111ll111111l1Il1l1.pop()
            if (ll1l1llll1ll1l11Il1l1.is_active):
                try:
                    ll1l1llll1ll1l11Il1l1.commit()
                except :
                    pass


@dataclass
class l111l1l1lll111llIl1l1(l1lll1llll1ll11lIl1l1):
    ll11111l11ll1l11Il1l1 = 'Sqlalchemy'

    ll1l1ll11lll11llIl1l1: List["Engine"] = field(init=False, default_factory=list)
    ll1llll11ll11l1lIl1l1: Set["Session"] = field(init=False, default_factory=set)
    lll111l1lll11l11Il1l1: Tuple[int, ...] = field(init=False)

    def l1l1l11l11llllllIl1l1(l11l1ll1ll1ll111Il1l1, l1lll1ll11ll1l11Il1l1: types.ModuleType) -> None:
        if (l11l1ll1ll1ll111Il1l1.ll1l111l1l1l1111Il1l1(l1lll1ll11ll1l11Il1l1, 'sqlalchemy')):
            l11l1ll1ll1ll111Il1l1.llllll1lllllll11Il1l1(l1lll1ll11ll1l11Il1l1)

        if (l11l1ll1ll1ll111Il1l1.ll1l111l1l1l1111Il1l1(l1lll1ll11ll1l11Il1l1, 'sqlalchemy.engine.base')):
            l11l1ll1ll1ll111Il1l1.l11l11l1l1111l1lIl1l1(l1lll1ll11ll1l11Il1l1)

    def llllll1lllllll11Il1l1(l11l1ll1ll1ll111Il1l1, l1lll1ll11ll1l11Il1l1: Any) -> None:
        l111l11ll11l1lllIl1l1 = Path(l1lll1ll11ll1l11Il1l1.__file__).read_text(encoding='utf-8')
        __version__ = re.findall('__version__\\s*?=\\s*?"(.*?)"', l111l11ll11l1lllIl1l1)[0]

        ll1ll1l1111l1111Il1l1 = [int(lllll1lll11l1ll1Il1l1) for lllll1lll11l1ll1Il1l1 in __version__.split('.')]
        l11l1ll1ll1ll111Il1l1.lll111l1lll11l11Il1l1 = tuple(ll1ll1l1111l1111Il1l1)

    def l111l11l11l111l1Il1l1(l11l1ll1ll1ll111Il1l1, ll1l111l111l1lllIl1l1: str, ll1l111l1ll111l1Il1l1: bool) -> Optional["ll1111lll1l11111Il1l1"]:
        l1l1lll111l11111Il1l1 = ll111llll11lll11Il1l1(ll1l111l111l1lllIl1l1=ll1l111l111l1lllIl1l1, l1ll1llll111ll1lIl1l1=l11l1ll1ll1ll111Il1l1)
        l1l1lll111l11111Il1l1.l1lllll11ll1ll11Il1l1()
        return l1l1lll111l11111Il1l1

    def l11l11l1l1111l1lIl1l1(l11l1ll1ll1ll111Il1l1, l1lll1ll11ll1l11Il1l1: Any) -> None:
        l1lll111llllll1lIl1l1 = locals().copy()

        l1lll111llllll1lIl1l1.update({'original': l1lll1ll11ll1l11Il1l1.Engine.__init__, 'reloader_code': ll111l1l1lll1l1lIl1l1, 'engines': l11l1ll1ll1ll111Il1l1.ll1l1ll11lll11llIl1l1})





        l1ll11l1l1llllllIl1l1 = dedent('\n            def patched(\n                    self2: Any,\n                    pool: Any,\n                    dialect: Any,\n                    url: Any,\n                    logging_name: Any = None,\n                    echo: Any = None,\n                    proxy: Any = None,\n                    execution_options: Any = None,\n                    hide_parameters: Any = None,\n            ) -> Any:\n                original(self2,\n                         pool,\n                         dialect,\n                         url,\n                         logging_name,\n                         echo,\n                         proxy,\n                         execution_options,\n                         hide_parameters\n                         )\n                with reloader_code():\n                    engines.append(self2)')
























        ll1lllll11ll1lllIl1l1 = dedent('\n            def patched(\n                    self2: Any,\n                    pool: Any,\n                    dialect: Any,\n                    url: Any,\n                    logging_name: Any = None,\n                    echo: Any = None,\n                    query_cache_size: Any = 500,\n                    execution_options: Any = None,\n                    hide_parameters: Any = False,\n            ) -> Any:\n                original(self2,\n                         pool,\n                         dialect,\n                         url,\n                         logging_name,\n                         echo,\n                         query_cache_size,\n                         execution_options,\n                         hide_parameters)\n                with reloader_code():\n                    engines.append(self2)\n        ')
























        if (l11l1ll1ll1ll111Il1l1.lll111l1lll11l11Il1l1 <= (1, 3, 24, )):
            exec(l1ll11l1l1llllllIl1l1, {**globals(), **l1lll111llllll1lIl1l1}, l1lll111llllll1lIl1l1)
        else:
            exec(ll1lllll11ll1lllIl1l1, {**globals(), **l1lll111llllll1lIl1l1}, l1lll111llllll1lIl1l1)

        ll11ll1111l11111Il1l1.l11ll11l11lll111Il1l1(l1lll1ll11ll1l11Il1l1.Engine, '__init__', l1lll111llllll1lIl1l1['patched'])
