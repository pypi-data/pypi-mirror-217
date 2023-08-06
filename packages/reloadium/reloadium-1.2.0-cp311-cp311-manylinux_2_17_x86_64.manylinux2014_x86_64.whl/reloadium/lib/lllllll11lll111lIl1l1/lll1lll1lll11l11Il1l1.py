from contextlib import contextmanager
from pathlib import Path
import types
from typing import TYPE_CHECKING, Any, Dict, Generator, List, Tuple, Type

from reloadium.lib.environ import env
from reloadium.corium.lll11l11111lll11Il1l1 import ll111l1l1lll1l1lIl1l1
from reloadium.lib.lllllll11lll111lIl1l1.l1lll1lll11l11l1Il1l1 import l11l1ll1l1ll11llIl1l1
from reloadium.corium.l11l11ll111l11llIl1l1 import llll111111111111Il1l1, lll11l11lll1ll1lIl1l1, l11111l1l11111l1Il1l1, l1ll1l111l1l1111Il1l1
from reloadium.corium.l1l1l1l1llllllllIl1l1 import l11l111l1111l11lIl1l1
from reloadium.corium.ll111l1111l11lllIl1l1 import ll11ll1111l11111Il1l1

if (TYPE_CHECKING):
    from dataclasses import dataclass
else:
    from reloadium.vendored.dataclasses import dataclass


__RELOADIUM__ = True


@dataclass(**l1ll1l111l1l1111Il1l1)
class l1ll11ll1lll111lIl1l1(l11111l1l11111l1Il1l1):
    l11l11llll1l111lIl1l1 = 'FlaskApp'

    @classmethod
    def l1l1l1111lllllllIl1l1(ll11l11ll11l11llIl1l1, ll111ll11111l1llIl1l1: l11l111l1111l11lIl1l1.l11l111llll111llIl1l1, ll11l1l111l1lll1Il1l1: Any, l1llll11ll1lll1lIl1l1: llll111111111111Il1l1) -> bool:
        import flask

        if (isinstance(ll11l1l111l1lll1Il1l1, flask.Flask)):
            return True

        return False

    def ll111llll11l111lIl1l1(l11l1ll1ll1ll111Il1l1) -> bool:
        return True

    @classmethod
    def l1llll1l11ll11l1Il1l1(ll11l11ll11l11llIl1l1) -> int:
        return (super().l1llll1l11ll11l1Il1l1() + 10)


@dataclass(**l1ll1l111l1l1111Il1l1)
class llll1l111ll1ll1lIl1l1(l11111l1l11111l1Il1l1):
    l11l11llll1l111lIl1l1 = 'Request'

    @classmethod
    def l1l1l1111lllllllIl1l1(ll11l11ll11l11llIl1l1, ll111ll11111l1llIl1l1: l11l111l1111l11lIl1l1.l11l111llll111llIl1l1, ll11l1l111l1lll1Il1l1: Any, l1llll11ll1lll1lIl1l1: llll111111111111Il1l1) -> bool:
        if (repr(ll11l1l111l1lll1Il1l1) == '<LocalProxy unbound>'):
            return True

        return False

    def ll111llll11l111lIl1l1(l11l1ll1ll1ll111Il1l1) -> bool:
        return True

    @classmethod
    def l1llll1l11ll11l1Il1l1(ll11l11ll11l11llIl1l1) -> int:

        return int(10000000000.0)


@dataclass
class l11l111l1llll111Il1l1(l11l1ll1l1ll11llIl1l1):
    ll11111l11ll1l11Il1l1 = 'Flask'

    @contextmanager
    def l1l1lll111lll1l1Il1l1(l11l1ll1ll1ll111Il1l1) -> Generator[None, None, None]:




        from flask import Flask as FlaskLib 

        def l1ll1l111l111l1lIl1l1(*l1l111l1111l1lllIl1l1: Any, **ll11111111ll11llIl1l1: Any) -> Any:
            def ll1l11l1l11111llIl1l1(l1l1l11lllll111lIl1l1: Any) -> Any:
                return l1l1l11lllll111lIl1l1

            return ll1l11l1l11111llIl1l1

        lllll1l111l1lll1Il1l1 = FlaskLib.route
        FlaskLib.route = l1ll1l111l111l1lIl1l1  # type: ignore

        try:
            yield 
        finally:
            FlaskLib.route = lllll1l111l1lll1Il1l1  # type: ignore

    def ll1ll11ll111l1l1Il1l1(l11l1ll1ll1ll111Il1l1) -> List[Type[lll11l11lll1ll1lIl1l1]]:
        return [l1ll11ll1lll111lIl1l1, llll1l111ll1ll1lIl1l1]

    def l1l1l11l11llllllIl1l1(l11l1ll1ll1ll111Il1l1, l11ll1l11ll1l111Il1l1: types.ModuleType) -> None:
        if (l11l1ll1ll1ll111Il1l1.ll1l111l1l1l1111Il1l1(l11ll1l11ll1l111Il1l1, 'flask.app')):
            l11l1ll1ll1ll111Il1l1.l1lll1l11l1l1l11Il1l1()
            l11l1ll1ll1ll111Il1l1.lllll1llll11ll11Il1l1()
            l11l1ll1ll1ll111Il1l1.ll111111ll1ll1llIl1l1()

        if (l11l1ll1ll1ll111Il1l1.ll1l111l1l1l1111Il1l1(l11ll1l11ll1l111Il1l1, 'flask.cli')):
            l11l1ll1ll1ll111Il1l1.ll11l11l111111llIl1l1()

    def l1lll1l11l1l1l11Il1l1(l11l1ll1ll1ll111Il1l1) -> None:
        try:
            import werkzeug.serving
            import flask.cli
        except ImportError:
            return 

        l11l1ll111lllll1Il1l1 = werkzeug.serving.run_simple

        def llll1l1111l1lll1Il1l1(*l1l111l1111l1lllIl1l1: Any, **ll11111111ll11llIl1l1: Any) -> Any:
            with ll111l1l1lll1l1lIl1l1():
                ll1ll111l11111l1Il1l1 = ll11111111ll11llIl1l1.get('port')
                if ( not ll1ll111l11111l1Il1l1):
                    ll1ll111l11111l1Il1l1 = l1l111l1111l1lllIl1l1[1]

                l11l1ll1ll1ll111Il1l1.l1lll1ll11ll11l1Il1l1 = l11l1ll1ll1ll111Il1l1.l111l11l1ll1ll1lIl1l1(ll1ll111l11111l1Il1l1)
                if (env.page_reload_on_start):
                    l11l1ll1ll1ll111Il1l1.l1lll1ll11ll11l1Il1l1.ll1l11l1lll11l1lIl1l1(1.0)
            l11l1ll111lllll1Il1l1(*l1l111l1111l1lllIl1l1, **ll11111111ll11llIl1l1)

        ll11ll1111l11111Il1l1.l11ll11l11lll111Il1l1(werkzeug.serving, 'run_simple', llll1l1111l1lll1Il1l1)
        ll11ll1111l11111Il1l1.l11ll11l11lll111Il1l1(flask.cli, 'run_simple', llll1l1111l1lll1Il1l1)

    def ll111111ll1ll1llIl1l1(l11l1ll1ll1ll111Il1l1) -> None:
        try:
            import flask
        except ImportError:
            return 

        l11l1ll111lllll1Il1l1 = flask.app.Flask.__init__

        def llll1l1111l1lll1Il1l1(llll11l111l1llllIl1l1: Any, *l1l111l1111l1lllIl1l1: Any, **ll11111111ll11llIl1l1: Any) -> Any:
            l11l1ll111lllll1Il1l1(llll11l111l1llllIl1l1, *l1l111l1111l1lllIl1l1, **ll11111111ll11llIl1l1)
            with ll111l1l1lll1l1lIl1l1():
                llll11l111l1llllIl1l1.config['TEMPLATES_AUTO_RELOAD'] = True

        ll11ll1111l11111Il1l1.l11ll11l11lll111Il1l1(flask.app.Flask, '__init__', llll1l1111l1lll1Il1l1)

    def lllll1llll11ll11Il1l1(l11l1ll1ll1ll111Il1l1) -> None:
        try:
            import waitress  # type: ignore
        except ImportError:
            return 

        l11l1ll111lllll1Il1l1 = waitress.serve


        def llll1l1111l1lll1Il1l1(*l1l111l1111l1lllIl1l1: Any, **ll11111111ll11llIl1l1: Any) -> Any:
            with ll111l1l1lll1l1lIl1l1():
                ll1ll111l11111l1Il1l1 = ll11111111ll11llIl1l1.get('port')
                if ( not ll1ll111l11111l1Il1l1):
                    ll1ll111l11111l1Il1l1 = int(l1l111l1111l1lllIl1l1[1])

                ll1ll111l11111l1Il1l1 = int(ll1ll111l11111l1Il1l1)

                l11l1ll1ll1ll111Il1l1.l1lll1ll11ll11l1Il1l1 = l11l1ll1ll1ll111Il1l1.l111l11l1ll1ll1lIl1l1(ll1ll111l11111l1Il1l1)
                if (env.page_reload_on_start):
                    l11l1ll1ll1ll111Il1l1.l1lll1ll11ll11l1Il1l1.ll1l11l1lll11l1lIl1l1(1.0)

            l11l1ll111lllll1Il1l1(*l1l111l1111l1lllIl1l1, **ll11111111ll11llIl1l1)

        ll11ll1111l11111Il1l1.l11ll11l11lll111Il1l1(waitress, 'serve', llll1l1111l1lll1Il1l1)

    def ll11l11l111111llIl1l1(l11l1ll1ll1ll111Il1l1) -> None:
        try:
            from flask import cli
        except ImportError:
            return 

        lllllllllllllll1Il1l1 = Path(cli.__file__).read_text(encoding='utf-8')
        lllllllllllllll1Il1l1 = lllllllllllllll1Il1l1.replace('.tb_next', '.tb_next.tb_next')

        exec(lllllllllllllll1Il1l1, cli.__dict__)

    def lll111ll1111ll1lIl1l1(l11l1ll1ll1ll111Il1l1) -> None:
        super().lll111ll1111ll1lIl1l1()
        import flask.app

        l11l1ll111lllll1Il1l1 = flask.app.Flask.dispatch_request

        def llll1l1111l1lll1Il1l1(*l1l111l1111l1lllIl1l1: Any, **ll11111111ll11llIl1l1: Any) -> Any:
            l11ll111l1ll1l1lIl1l1 = l11l1ll111lllll1Il1l1(*l1l111l1111l1lllIl1l1, **ll11111111ll11llIl1l1)

            if ( not l11l1ll1ll1ll111Il1l1.l1lll1ll11ll11l1Il1l1):
                return l11ll111l1ll1l1lIl1l1

            if (isinstance(l11ll111l1ll1l1lIl1l1, str)):
                l1l1lll111l11111Il1l1 = l11l1ll1ll1ll111Il1l1.l1lll1ll11ll11l1Il1l1.l111111l11l11ll1Il1l1(l11ll111l1ll1l1lIl1l1)
                return l1l1lll111l11111Il1l1
            elif ((isinstance(l11ll111l1ll1l1lIl1l1, flask.app.Response) and 'text/html' in l11ll111l1ll1l1lIl1l1.content_type)):
                l11ll111l1ll1l1lIl1l1.data = l11l1ll1ll1ll111Il1l1.l1lll1ll11ll11l1Il1l1.l111111l11l11ll1Il1l1(l11ll111l1ll1l1lIl1l1.data.decode('utf-8')).encode('utf-8')
                return l11ll111l1ll1l1lIl1l1
            else:
                return l11ll111l1ll1l1lIl1l1

        flask.app.Flask.dispatch_request = llll1l1111l1lll1Il1l1  # type: ignore
