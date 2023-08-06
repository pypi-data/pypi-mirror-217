import asyncio
from contextlib import contextmanager
import os
from pathlib import Path
import sys
import types
from typing import TYPE_CHECKING, Any, Callable, Dict, Generator, List, Optional, Tuple, Type

from reloadium.corium.l1lll111l111l111Il1l1 import ll1lll1l11ll11llIl1l1
from reloadium.lib.environ import env
from reloadium.corium.lll11l11111lll11Il1l1 import ll111l1l1lll1l1lIl1l1
from reloadium.lib.lllllll11lll111lIl1l1.l1ll1llll111ll1lIl1l1 import ll11llll111l1l1lIl1l1, l1l1lllll1111l1lIl1l1
from reloadium.lib.lllllll11lll111lIl1l1.l1lll1lll11l11l1Il1l1 import l11l1ll1l1ll11llIl1l1
from reloadium.corium.l11l11ll111l11llIl1l1 import l111l1l11l1lll11Il1l1, llll111111111111Il1l1, lll11l11lll1ll1lIl1l1, l11111l1l11111l1Il1l1, l1ll1l111l1l1111Il1l1
from reloadium.corium.l1l1l111l1l1ll1lIl1l1 import ll1111lll1l11111Il1l1, ll1lllllll1l1111Il1l1
from reloadium.corium.l1l1l1l1llllllllIl1l1 import l11l111l1111l11lIl1l1
from reloadium.corium.ll111l1111l11lllIl1l1 import ll11ll1111l11111Il1l1

if (TYPE_CHECKING):
    from dataclasses import dataclass, field

    from django.db import transaction
    from django.db.transaction import Atomic
else:
    from reloadium.vendored.dataclasses import dataclass, field


__RELOADIUM__ = True


@dataclass(**l1ll1l111l1l1111Il1l1)
class l1l1l11l111ll1l1Il1l1(l11111l1l11111l1Il1l1):
    l11l11llll1l111lIl1l1 = 'Field'

    @classmethod
    def l1l1l1111lllllllIl1l1(ll11l11ll11l11llIl1l1, ll111ll11111l1llIl1l1: l11l111l1111l11lIl1l1.l11l111llll111llIl1l1, ll11l1l111l1lll1Il1l1: Any, l1llll11ll1lll1lIl1l1: llll111111111111Il1l1) -> bool:
        from django.db.models.fields import Field

        if ((hasattr(ll11l1l111l1lll1Il1l1, 'field') and isinstance(ll11l1l111l1lll1Il1l1.field, Field))):
            return True

        return False

    def l11111lll11ll1l1Il1l1(l11l1ll1ll1ll111Il1l1, lll11l1lll1l11l1Il1l1: lll11l11lll1ll1lIl1l1) -> bool:
        return True

    @classmethod
    def l1llll1l11ll11l1Il1l1(ll11l11ll11l11llIl1l1) -> int:
        return 200


@dataclass(repr=False)
class ll111llll11lll11Il1l1(ll11llll111l1l1lIl1l1):
    ll1ll111l11ll1llIl1l1: "Atomic" = field(init=False)

    l111l11llll111llIl1l1: bool = field(init=False, default=False)

    def l1lllll11ll1ll11Il1l1(l11l1ll1ll1ll111Il1l1) -> None:
        super().l1lllll11ll1ll11Il1l1()
        from django.db import transaction

        l11l1ll1ll1ll111Il1l1.ll1ll111l11ll1llIl1l1 = transaction.atomic()
        l11l1ll1ll1ll111Il1l1.ll1ll111l11ll1llIl1l1.__enter__()

    def l111l1l11ll1l1llIl1l1(l11l1ll1ll1ll111Il1l1) -> None:
        super().l111l1l11ll1l1llIl1l1()
        if (l11l1ll1ll1ll111Il1l1.l111l11llll111llIl1l1):
            return 

        l11l1ll1ll1ll111Il1l1.l111l11llll111llIl1l1 = True
        from django.db import transaction

        transaction.set_rollback(True)
        l11l1ll1ll1ll111Il1l1.ll1ll111l11ll1llIl1l1.__exit__(None, None, None)

    def ll1111ll1ll1l1l1Il1l1(l11l1ll1ll1ll111Il1l1) -> None:
        super().ll1111ll1ll1l1l1Il1l1()

        if (l11l1ll1ll1ll111Il1l1.l111l11llll111llIl1l1):
            return 

        l11l1ll1ll1ll111Il1l1.l111l11llll111llIl1l1 = True
        l11l1ll1ll1ll111Il1l1.ll1ll111l11ll1llIl1l1.__exit__(None, None, None)

    def __repr__(l11l1ll1ll1ll111Il1l1) -> str:
        return 'DbMemento'


@dataclass(repr=False)
class ll1l1ll11l11l11lIl1l1(l1l1lllll1111l1lIl1l1):
    ll1ll111l11ll1llIl1l1: "Atomic" = field(init=False)

    l111l11llll111llIl1l1: bool = field(init=False, default=False)

    async def l1lllll11ll1ll11Il1l1(l11l1ll1ll1ll111Il1l1) -> None:
        await super().l1lllll11ll1ll11Il1l1()
        from django.db import transaction
        from asgiref.sync import sync_to_async

        l11l1ll1ll1ll111Il1l1.ll1ll111l11ll1llIl1l1 = transaction.atomic()


        with ll1lll1l11ll11llIl1l1.l111ll1lllll1ll1Il1l1.l1l1l1lllll111llIl1l1.l1l1l11l111l1l11Il1l1(False):
            await sync_to_async(l11l1ll1ll1ll111Il1l1.ll1ll111l11ll1llIl1l1.__enter__)()

    async def l111l1l11ll1l1llIl1l1(l11l1ll1ll1ll111Il1l1) -> None:
        from asgiref.sync import sync_to_async

        await super().l111l1l11ll1l1llIl1l1()
        if (l11l1ll1ll1ll111Il1l1.l111l11llll111llIl1l1):
            return 

        l11l1ll1ll1ll111Il1l1.l111l11llll111llIl1l1 = True
        from django.db import transaction

        def llll1lllll11l1llIl1l1() -> None:
            transaction.set_rollback(True)
            l11l1ll1ll1ll111Il1l1.ll1ll111l11ll1llIl1l1.__exit__(None, None, None)
        with ll1lll1l11ll11llIl1l1.l111ll1lllll1ll1Il1l1.l1l1l1lllll111llIl1l1.l1l1l11l111l1l11Il1l1(False):
            await sync_to_async(llll1lllll11l1llIl1l1)()

    async def ll1111ll1ll1l1l1Il1l1(l11l1ll1ll1ll111Il1l1) -> None:
        from asgiref.sync import sync_to_async

        await super().ll1111ll1ll1l1l1Il1l1()

        if (l11l1ll1ll1ll111Il1l1.l111l11llll111llIl1l1):
            return 

        l11l1ll1ll1ll111Il1l1.l111l11llll111llIl1l1 = True
        with ll1lll1l11ll11llIl1l1.l111ll1lllll1ll1Il1l1.l1l1l1lllll111llIl1l1.l1l1l11l111l1l11Il1l1(False):
            await sync_to_async(l11l1ll1ll1ll111Il1l1.ll1ll111l11ll1llIl1l1.__exit__)(None, None, None)

    def __repr__(l11l1ll1ll1ll111Il1l1) -> str:
        return 'AsyncDbMemento'


@dataclass
class ll1l111ll11l1l11Il1l1(l11l1ll1l1ll11llIl1l1):
    ll11111l11ll1l11Il1l1 = 'Django'

    lll111l1ll111lllIl1l1: Optional[int] = field(init=False)
    lllll11l11ll111lIl1l1: Optional[Callable[..., Any]] = field(init=False, default=None)

    def __post_init__(l11l1ll1ll1ll111Il1l1) -> None:
        super().__post_init__()
        l11l1ll1ll1ll111Il1l1.lll111l1ll111lllIl1l1 = None

    def ll1ll11ll111l1l1Il1l1(l11l1ll1ll1ll111Il1l1) -> List[Type[lll11l11lll1ll1lIl1l1]]:
        return [l1l1l11l111ll1l1Il1l1]

    def ll1l111ll1llll1lIl1l1(l11l1ll1ll1ll111Il1l1) -> None:
        super().ll1l111ll1llll1lIl1l1()
        if ('runserver' in sys.argv):
            sys.argv.append('--noreload')

    def l1l1l11l11llllllIl1l1(l11l1ll1ll1ll111Il1l1, l1lll1ll11ll1l11Il1l1: types.ModuleType) -> None:
        if (l11l1ll1ll1ll111Il1l1.ll1l111l1l1l1111Il1l1(l1lll1ll11ll1l11Il1l1, 'django.core.management.commands.runserver')):
            l11l1ll1ll1ll111Il1l1.l11l1l1l1lllll11Il1l1()
            l11l1ll1ll1ll111Il1l1.ll1ll1l1l1111l11Il1l1()

    def l111l11l11l111l1Il1l1(l11l1ll1ll1ll111Il1l1, ll1l111l111l1lllIl1l1: str, ll1l111l1ll111l1Il1l1: bool) -> Optional["ll1111lll1l11111Il1l1"]:
        if ( not os.environ.get('DJANGO_SETTINGS_MODULE')):
            return None

        if (ll1l111l1ll111l1Il1l1):
            return None
        else:
            l1l1lll111l11111Il1l1 = ll111llll11lll11Il1l1(ll1l111l111l1lllIl1l1=ll1l111l111l1lllIl1l1, l1ll1llll111ll1lIl1l1=l11l1ll1ll1ll111Il1l1)
            l1l1lll111l11111Il1l1.l1lllll11ll1ll11Il1l1()

        return l1l1lll111l11111Il1l1

    async def l1l1111l1lllllllIl1l1(l11l1ll1ll1ll111Il1l1, ll1l111l111l1lllIl1l1: str) -> Optional["ll1lllllll1l1111Il1l1"]:
        if ( not os.environ.get('DJANGO_SETTINGS_MODULE')):
            return None

        l1l1lll111l11111Il1l1 = ll1l1ll11l11l11lIl1l1(ll1l111l111l1lllIl1l1=ll1l111l111l1lllIl1l1, l1ll1llll111ll1lIl1l1=l11l1ll1ll1ll111Il1l1)
        await l1l1lll111l11111Il1l1.l1lllll11ll1ll11Il1l1()
        return l1l1lll111l11111Il1l1

    def l11l1l1l1lllll11Il1l1(l11l1ll1ll1ll111Il1l1) -> None:
        import django.core.management.commands.runserver

        l11l1ll111lllll1Il1l1 = django.core.management.commands.runserver.Command.handle

        def llll1l1111l1lll1Il1l1(*l1l111l1111l1lllIl1l1: Any, **l1lll1l11ll1llllIl1l1: Any) -> Any:
            with ll111l1l1lll1l1lIl1l1():
                ll1ll111l11111l1Il1l1 = l1lll1l11ll1llllIl1l1.get('addrport')
                if ( not ll1ll111l11111l1Il1l1):
                    ll1ll111l11111l1Il1l1 = django.core.management.commands.runserver.Command.default_port

                ll1ll111l11111l1Il1l1 = ll1ll111l11111l1Il1l1.split(':')[ - 1]
                ll1ll111l11111l1Il1l1 = int(ll1ll111l11111l1Il1l1)
                l11l1ll1ll1ll111Il1l1.lll111l1ll111lllIl1l1 = ll1ll111l11111l1Il1l1

            return l11l1ll111lllll1Il1l1(*l1l111l1111l1lllIl1l1, **l1lll1l11ll1llllIl1l1)

        ll11ll1111l11111Il1l1.l11ll11l11lll111Il1l1(django.core.management.commands.runserver.Command, 'handle', llll1l1111l1lll1Il1l1)

    def ll1ll1l1l1111l11Il1l1(l11l1ll1ll1ll111Il1l1) -> None:
        import django.core.management.commands.runserver

        l11l1ll111lllll1Il1l1 = django.core.management.commands.runserver.Command.get_handler

        def llll1l1111l1lll1Il1l1(*l1l111l1111l1lllIl1l1: Any, **l1lll1l11ll1llllIl1l1: Any) -> Any:
            with ll111l1l1lll1l1lIl1l1():
                assert l11l1ll1ll1ll111Il1l1.lll111l1ll111lllIl1l1
                l11l1ll1ll1ll111Il1l1.l1lll1ll11ll11l1Il1l1 = l11l1ll1ll1ll111Il1l1.l111l11l1ll1ll1lIl1l1(l11l1ll1ll1ll111Il1l1.lll111l1ll111lllIl1l1)
                if (env.page_reload_on_start):
                    l11l1ll1ll1ll111Il1l1.l1lll1ll11ll11l1Il1l1.ll1l11l1lll11l1lIl1l1(2.0)

            return l11l1ll111lllll1Il1l1(*l1l111l1111l1lllIl1l1, **l1lll1l11ll1llllIl1l1)

        ll11ll1111l11111Il1l1.l11ll11l11lll111Il1l1(django.core.management.commands.runserver.Command, 'get_handler', llll1l1111l1lll1Il1l1)

    def lll111ll1111ll1lIl1l1(l11l1ll1ll1ll111Il1l1) -> None:
        super().lll111ll1111ll1lIl1l1()

        import django.core.handlers.base

        l11l1ll111lllll1Il1l1 = django.core.handlers.base.BaseHandler.get_response

        def llll1l1111l1lll1Il1l1(l1l11ll1l111ll11Il1l1: Any, ll1111lll111lll1Il1l1: Any) -> Any:
            l11ll111l1ll1l1lIl1l1 = l11l1ll111lllll1Il1l1(l1l11ll1l111ll11Il1l1, ll1111lll111lll1Il1l1)

            if ( not l11l1ll1ll1ll111Il1l1.l1lll1ll11ll11l1Il1l1):
                return l11ll111l1ll1l1lIl1l1

            l111111l1llllll1Il1l1 = l11ll111l1ll1l1lIl1l1.get('content-type')

            if (( not l111111l1llllll1Il1l1 or 'text/html' not in l111111l1llllll1Il1l1)):
                return l11ll111l1ll1l1lIl1l1

            l111l11ll11l1lllIl1l1 = l11ll111l1ll1l1lIl1l1.content

            if (isinstance(l111l11ll11l1lllIl1l1, bytes)):
                l111l11ll11l1lllIl1l1 = l111l11ll11l1lllIl1l1.decode('utf-8')

            l11lll1l1ll1111lIl1l1 = l11l1ll1ll1ll111Il1l1.l1lll1ll11ll11l1Il1l1.l111111l11l11ll1Il1l1(l111l11ll11l1lllIl1l1)

            l11ll111l1ll1l1lIl1l1.content = l11lll1l1ll1111lIl1l1.encode('utf-8')
            l11ll111l1ll1l1lIl1l1['content-length'] = str(len(l11ll111l1ll1l1lIl1l1.content)).encode('ascii')
            return l11ll111l1ll1l1lIl1l1

        django.core.handlers.base.BaseHandler.get_response = llll1l1111l1lll1Il1l1  # type: ignore

    def l11llll1111l1lllIl1l1(l11l1ll1ll1ll111Il1l1, lll1ll1l1l1l1ll1Il1l1: Path) -> None:
        super().l11llll1111l1lllIl1l1(lll1ll1l1l1l1ll1Il1l1)

        from django.apps.registry import Apps

        l11l1ll1ll1ll111Il1l1.lllll11l11ll111lIl1l1 = Apps.register_model

        def ll1l11l111l1l1l1Il1l1(*l1l111l1111l1lllIl1l1: Any, **ll11111111ll11llIl1l1: Any) -> Any:
            pass

        Apps.register_model = ll1l11l111l1l1l1Il1l1

    def lllll1lll11ll111Il1l1(l11l1ll1ll1ll111Il1l1, lll1ll1l1l1l1ll1Il1l1: Path, l1111l1ll111lll1Il1l1: List[l111l1l11l1lll11Il1l1]) -> None:
        super().lllll1lll11ll111Il1l1(lll1ll1l1l1l1ll1Il1l1, l1111l1ll111lll1Il1l1)

        if ( not l11l1ll1ll1ll111Il1l1.lllll11l11ll111lIl1l1):
            return 

        from django.apps.registry import Apps

        Apps.register_model = l11l1ll1ll1ll111Il1l1.lllll11l11ll111lIl1l1
