import logging
from pathlib import Path
from threading import Thread
import time
from typing import TYPE_CHECKING, List, Optional

from reloadium.corium import ll111l1111l11lllIl1l1
from reloadium.lib.lllllll11lll111lIl1l1.l1ll1llll111ll1lIl1l1 import l1lll1llll1ll11lIl1l1
from reloadium.corium.l1lll111l111l111Il1l1 import ll1lll1l11ll11llIl1l1
from reloadium.corium.l111lllll111ll11Il1l1 import l11lll1ll1l1l111Il1l1
from reloadium.corium.l11l11ll111l11llIl1l1 import l111l1l11l1lll11Il1l1
from reloadium.corium.l1l11111ll11llllIl1l1 import l1l11111ll11llllIl1l1

if (TYPE_CHECKING):
    from dataclasses import dataclass, field

    from reloadium.vendored.websocket_server import WebsocketServer
else:
    from reloadium.vendored.dataclasses import dataclass, field


__RELOADIUM__ = True

__all__ = ['l111l111111l111lIl1l1']



l1lll1ll11ll11l1Il1l1 = '\n<!--{info}-->\n<script type="text/javascript">\n   // <![CDATA[  <-- For SVG support\n     function refreshCSS() {\n        var sheets = [].slice.call(document.getElementsByTagName("link"));\n        var head = document.getElementsByTagName("head")[0];\n        for (var i = 0; i < sheets.length; ++i) {\n           var elem = sheets[i];\n           var parent = elem.parentElement || head;\n           parent.removeChild(elem);\n           var rel = elem.rel;\n           if (elem.href && typeof rel != "string" || rel.length === 0 || rel.toLowerCase() === "stylesheet") {\n              var url = elem.href.replace(/(&|\\?)_cacheOverride=\\d+/, \'\');\n              elem.href = url + (url.indexOf(\'?\') >= 0 ? \'&\' : \'?\') + \'_cacheOverride=\' + (new Date().valueOf());\n           }\n           parent.appendChild(elem);\n        }\n     }\n     let protocol = window.location.protocol === \'http:\' ? \'ws://\' : \'wss://\';\n     let address = protocol + "{address}:{port}";\n     let socket = undefined;\n     let lost_connection = false;\n\n     function connect() {\n        socket = new WebSocket(address);\n         socket.onmessage = function (msg) {\n            if (msg.data === \'reload\') window.location.href = window.location.href;\n            else if (msg.data === \'refreshcss\') refreshCSS();\n         };\n     }\n\n     function checkConnection() {\n        if ( socket.readyState === socket.CLOSED ) {\n            lost_connection = true;\n            connect();\n        }\n     }\n\n     connect();\n     setInterval(checkConnection, 500)\n\n   // ]]>\n</script>\n'














































@dataclass
class l111l111111l111lIl1l1:
    l11lll11ll1ll1l1Il1l1: str
    ll1ll111l11111l1Il1l1: int
    ll1ll11llllll1llIl1l1: l11lll1ll1l1l111Il1l1

    l11l111l1ll11111Il1l1: Optional["WebsocketServer"] = field(init=False, default=None)
    ll11l1l1l1lll1llIl1l1: str = field(init=False, default='')

    ll11ll111ll11ll1Il1l1 = 'Reloadium page reloader'

    def l1l1ll1llllllll1Il1l1(l11l1ll1ll1ll111Il1l1) -> None:
        from reloadium.vendored.websocket_server import WebsocketServer

        l11l1ll1ll1ll111Il1l1.ll1ll11llllll1llIl1l1.ll11ll111ll11ll1Il1l1(''.join(['Starting reload websocket server on port ', '{:{}}'.format(l11l1ll1ll1ll111Il1l1.ll1ll111l11111l1Il1l1, '')]))

        l11l1ll1ll1ll111Il1l1.l11l111l1ll11111Il1l1 = WebsocketServer(host=l11l1ll1ll1ll111Il1l1.l11lll11ll1ll1l1Il1l1, port=l11l1ll1ll1ll111Il1l1.ll1ll111l11111l1Il1l1, loglevel=logging.CRITICAL)
        l11l1ll1ll1ll111Il1l1.l11l111l1ll11111Il1l1.run_forever(threaded=True)

        l11l1ll1ll1ll111Il1l1.ll11l1l1l1lll1llIl1l1 = l1lll1ll11ll11l1Il1l1

        l11l1ll1ll1ll111Il1l1.ll11l1l1l1lll1llIl1l1 = l11l1ll1ll1ll111Il1l1.ll11l1l1l1lll1llIl1l1.replace('{info}', str(l11l1ll1ll1ll111Il1l1.ll11ll111ll11ll1Il1l1))
        l11l1ll1ll1ll111Il1l1.ll11l1l1l1lll1llIl1l1 = l11l1ll1ll1ll111Il1l1.ll11l1l1l1lll1llIl1l1.replace('{port}', str(l11l1ll1ll1ll111Il1l1.ll1ll111l11111l1Il1l1))
        l11l1ll1ll1ll111Il1l1.ll11l1l1l1lll1llIl1l1 = l11l1ll1ll1ll111Il1l1.ll11l1l1l1lll1llIl1l1.replace('{address}', l11l1ll1ll1ll111Il1l1.l11lll11ll1ll1l1Il1l1)

    def l111111l11l11ll1Il1l1(l11l1ll1ll1ll111Il1l1, ll111ll1111111l1Il1l1: str) -> str:
        llll1lll1l11llllIl1l1 = ll111ll1111111l1Il1l1.find('<head>')
        if (llll1lll1l11llllIl1l1 ==  - 1):
            llll1lll1l11llllIl1l1 = 0
        l1l1lll111l11111Il1l1 = ((ll111ll1111111l1Il1l1[:llll1lll1l11llllIl1l1] + l11l1ll1ll1ll111Il1l1.ll11l1l1l1lll1llIl1l1) + ll111ll1111111l1Il1l1[llll1lll1l11llllIl1l1:])
        return l1l1lll111l11111Il1l1

    def ll1l1ll1l1111111Il1l1(l11l1ll1ll1ll111Il1l1) -> None:
        try:
            l11l1ll1ll1ll111Il1l1.l1l1ll1llllllll1Il1l1()
        except Exception as l11l1llllll1l11lIl1l1:
            l11l1ll1ll1ll111Il1l1.ll1ll11llllll1llIl1l1.l1ll11ll11ll1l11Il1l1('Could not start server')

    def l1l1lllll1111111Il1l1(l11l1ll1ll1ll111Il1l1) -> None:
        if ( not l11l1ll1ll1ll111Il1l1.l11l111l1ll11111Il1l1):
            return 

        l11l1ll1ll1ll111Il1l1.ll1ll11llllll1llIl1l1.ll11ll111ll11ll1Il1l1('Reloading page')
        l11l1ll1ll1ll111Il1l1.l11l111l1ll11111Il1l1.send_message_to_all('reload')
        l1l11111ll11llllIl1l1.llll1ll1llllllllIl1l1()

    def ll1l11l1lll11l1lIl1l1(l11l1ll1ll1ll111Il1l1, l111ll11ll11l111Il1l1: float) -> None:
        def ll1ll111lll1llllIl1l1() -> None:
            time.sleep(l111ll11ll11l111Il1l1)
            l11l1ll1ll1ll111Il1l1.l1l1lllll1111111Il1l1()

        Thread(target=ll1ll111lll1llllIl1l1, daemon=True, name=ll111l1111l11lllIl1l1.ll1111lll11lll1lIl1l1.ll1l1ll1ll11llllIl1l1('page-reloader')).start()


@dataclass
class l11l1ll1l1ll11llIl1l1(l1lll1llll1ll11lIl1l1):
    l1lll1ll11ll11l1Il1l1: Optional[l111l111111l111lIl1l1] = field(init=False, default=None)

    l11lll1llll11lllIl1l1 = '127.0.0.1'
    l111lll1lllll1l1Il1l1 = 4512

    def ll1l111ll1llll1lIl1l1(l11l1ll1ll1ll111Il1l1) -> None:
        ll1lll1l11ll11llIl1l1.l111ll1lllll1ll1Il1l1.ll11l1111l1l111lIl1l1.l11lll11llll1111Il1l1('html')

    def lllll1lll11ll111Il1l1(l11l1ll1ll1ll111Il1l1, lll1ll1l1l1l1ll1Il1l1: Path, l1111l1ll111lll1Il1l1: List[l111l1l11l1lll11Il1l1]) -> None:
        if ( not l11l1ll1ll1ll111Il1l1.l1lll1ll11ll11l1Il1l1):
            return 

        from reloadium.corium.l111l1ll1lllllllIl1l1.l1ll111lll1111llIl1l1 import l111ll11111lll11Il1l1

        if ( not any((isinstance(ll1lllllllllll11Il1l1, l111ll11111lll11Il1l1) for ll1lllllllllll11Il1l1 in l1111l1ll111lll1Il1l1))):
            if (l11l1ll1ll1ll111Il1l1.l1lll1ll11ll11l1Il1l1):
                l11l1ll1ll1ll111Il1l1.l1lll1ll11ll11l1Il1l1.l1l1lllll1111111Il1l1()

    def l1l11l1llll111l1Il1l1(l11l1ll1ll1ll111Il1l1, lll1ll1l1l1l1ll1Il1l1: Path) -> None:
        if ( not l11l1ll1ll1ll111Il1l1.l1lll1ll11ll11l1Il1l1):
            return 
        l11l1ll1ll1ll111Il1l1.l1lll1ll11ll11l1Il1l1.l1l1lllll1111111Il1l1()

    def l111l11l1ll1ll1lIl1l1(l11l1ll1ll1ll111Il1l1, ll1ll111l11111l1Il1l1: int) -> l111l111111l111lIl1l1:
        while True:
            l1lll1l11llll1l1Il1l1 = (ll1ll111l11111l1Il1l1 + l11l1ll1ll1ll111Il1l1.l111lll1lllll1l1Il1l1)
            try:
                l1l1lll111l11111Il1l1 = l111l111111l111lIl1l1(l11lll11ll1ll1l1Il1l1=l11l1ll1ll1ll111Il1l1.l11lll1llll11lllIl1l1, ll1ll111l11111l1Il1l1=l1lll1l11llll1l1Il1l1, ll1ll11llllll1llIl1l1=l11l1ll1ll1ll111Il1l1.ll111llllll1l1l1Il1l1)
                l1l1lll111l11111Il1l1.ll1l1ll1l1111111Il1l1()
                l11l1ll1ll1ll111Il1l1.lll111ll1111ll1lIl1l1()
                break
            except OSError:
                l11l1ll1ll1ll111Il1l1.ll111llllll1l1l1Il1l1.ll11ll111ll11ll1Il1l1(''.join(["Couldn't create page reloader on ", '{:{}}'.format(l1lll1l11llll1l1Il1l1, ''), ' port']))
                l11l1ll1ll1ll111Il1l1.l111lll1lllll1l1Il1l1 += 1

        return l1l1lll111l11111Il1l1

    def lll111ll1111ll1lIl1l1(l11l1ll1ll1ll111Il1l1) -> None:
        l11l1ll1ll1ll111Il1l1.ll111llllll1l1l1Il1l1.ll11ll111ll11ll1Il1l1('Injecting page reloader')
