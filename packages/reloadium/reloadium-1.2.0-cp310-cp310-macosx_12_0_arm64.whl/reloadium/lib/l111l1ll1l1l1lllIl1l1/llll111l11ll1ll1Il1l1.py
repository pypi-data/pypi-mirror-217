import sys

__RELOADIUM__ = True


def lllll11l11111l1lIl1l1(llll11l111l1llllIl1l1, ll1l1l11ll1l1l1lIl1l1):
    from reloadium.lib.environ import env
    from pathlib import Path
    from multiprocessing import util, spawn
    from multiprocessing.context import reduction, set_spawning_popen
    import io
    import os

    env.sub_process += 1
    env.save_to_os_environ()

    def l11l111ll111l111Il1l1(*llll1l11l1llll1lIl1l1):

        for lll111111ll1111lIl1l1 in llll1l11l1llll1lIl1l1:
            os.close(lll111111ll1111lIl1l1)

    if (sys.version_info > (3, 8, )):
        from multiprocessing import resource_tracker as tracker 
    else:
        from multiprocessing import semaphore_tracker as tracker 

    lll11l1ll1l1l1llIl1l1 = tracker.getfd()
    llll11l111l1llllIl1l1._fds.append(lll11l1ll1l1l1llIl1l1)
    l1ll111lll11ll1lIl1l1 = spawn.get_preparation_data(ll1l1l11ll1l1l1lIl1l1._name)
    lllll1ll111111llIl1l1 = io.BytesIO()
    set_spawning_popen(llll11l111l1llllIl1l1)

    try:
        reduction.dump(l1ll111lll11ll1lIl1l1, lllll1ll111111llIl1l1)
        reduction.dump(ll1l1l11ll1l1l1lIl1l1, lllll1ll111111llIl1l1)
    finally:
        set_spawning_popen(None)

    ll1l1llllll1llllIl1l1llll111ll1l1111lIl1l1l1lll1111ll111llIl1l1l11l11l11llllll1Il1l1 = None
    try:
        (ll1l1llllll1llllIl1l1, llll111ll1l1111lIl1l1, ) = os.pipe()
        (l1lll1111ll111llIl1l1, l11l11l11llllll1Il1l1, ) = os.pipe()
        ll1l11ll11ll1lllIl1l1 = spawn.get_command_line(tracker_fd=lll11l1ll1l1l1llIl1l1, pipe_handle=l1lll1111ll111llIl1l1)


        lll1ll11ll1ll11lIl1l1 = str(Path(l1ll111lll11ll1lIl1l1['sys_argv'][0]).absolute())
        ll1l11ll11ll1lllIl1l1 = [ll1l11ll11ll1lllIl1l1[0], '-B', '-m', 'reloadium_launcher', 'spawn_process', str(lll11l1ll1l1l1llIl1l1), 
str(l1lll1111ll111llIl1l1), lll1ll11ll1ll11lIl1l1]
        llll11l111l1llllIl1l1._fds.extend([l1lll1111ll111llIl1l1, llll111ll1l1111lIl1l1])
        llll11l111l1llllIl1l1.pid = util.spawnv_passfds(spawn.get_executable(), 
ll1l11ll11ll1lllIl1l1, llll11l111l1llllIl1l1._fds)
        llll11l111l1llllIl1l1.sentinel = ll1l1llllll1llllIl1l1
        with open(l11l11l11llllll1Il1l1, 'wb', closefd=False) as l1l1l11lllll111lIl1l1:
            l1l1l11lllll111lIl1l1.write(lllll1ll111111llIl1l1.getbuffer())
    finally:
        l1ll11l111l1ll11Il1l1 = []
        for lll111111ll1111lIl1l1 in (ll1l1llllll1llllIl1l1, l11l11l11llllll1Il1l1, ):
            if (lll111111ll1111lIl1l1 is not None):
                l1ll11l111l1ll11Il1l1.append(lll111111ll1111lIl1l1)
        llll11l111l1llllIl1l1.finalizer = util.Finalize(llll11l111l1llllIl1l1, l11l111ll111l111Il1l1, l1ll11l111l1ll11Il1l1)

        for lll111111ll1111lIl1l1 in (l1lll1111ll111llIl1l1, llll111ll1l1111lIl1l1, ):
            if (lll111111ll1111lIl1l1 is not None):
                os.close(lll111111ll1111lIl1l1)


def __init__(llll11l111l1llllIl1l1, ll1l1l11ll1l1l1lIl1l1):
    from reloadium.lib.environ import env
    from multiprocessing import util, spawn
    from multiprocessing.context import reduction, set_spawning_popen
    from multiprocessing.popen_spawn_win32 import TERMINATE, WINEXE, WINSERVICE, WINENV, _path_eq
    from pathlib import Path
    import os
    import msvcrt
    import sys
    import _winapi

    env.sub_process += 1
    env.save_to_os_environ()

    if (sys.version_info > (3, 8, )):
        from multiprocessing import resource_tracker as tracker 
        from multiprocessing.popen_spawn_win32 import _close_handles
    else:
        from multiprocessing import semaphore_tracker as tracker 
        _close_handles = _winapi.CloseHandle

    l1ll111lll11ll1lIl1l1 = spawn.get_preparation_data(ll1l1l11ll1l1l1lIl1l1._name)







    (l11l1ll11l111l11Il1l1, l11llll1l1l11l1lIl1l1, ) = _winapi.CreatePipe(None, 0)
    l1l11l11ll1l111lIl1l1 = msvcrt.open_osfhandle(l11llll1l1l11l1lIl1l1, 0)
    l11llll11ll111llIl1l1 = spawn.get_executable()
    lll1ll11ll1ll11lIl1l1 = str(Path(l1ll111lll11ll1lIl1l1['sys_argv'][0]).absolute())
    ll1l11ll11ll1lllIl1l1 = ' '.join([l11llll11ll111llIl1l1, '-B', '-m', 'reloadium_launcher', 'spawn_process', str(os.getpid()), 
str(l11l1ll11l111l11Il1l1), lll1ll11ll1ll11lIl1l1])



    if ((WINENV and _path_eq(l11llll11ll111llIl1l1, sys.executable))):
        l11llll11ll111llIl1l1 = sys._base_executable
        env = os.environ.copy()
        env['__PYVENV_LAUNCHER__'] = sys.executable
    else:
        env = None

    with open(l1l11l11ll1l111lIl1l1, 'wb', closefd=True) as ll1llll11ll11111Il1l1:

        try:
            (lll1l1l1l1111111Il1l1, l1l1111ll1l1l11lIl1l1, ll1l1llllll1ll1lIl1l1, llllllll11lllll1Il1l1, ) = _winapi.CreateProcess(l11llll11ll111llIl1l1, ll1l11ll11ll1lllIl1l1, None, None, False, 0, env, None, None)


            _winapi.CloseHandle(l1l1111ll1l1l11lIl1l1)
        except :
            _winapi.CloseHandle(l11l1ll11l111l11Il1l1)
            raise 


        llll11l111l1llllIl1l1.pid = ll1l1llllll1ll1lIl1l1
        llll11l111l1llllIl1l1.returncode = None
        llll11l111l1llllIl1l1._handle = lll1l1l1l1111111Il1l1
        llll11l111l1llllIl1l1.sentinel = int(lll1l1l1l1111111Il1l1)
        if (sys.version_info > (3, 8, )):
            llll11l111l1llllIl1l1.finalizer = util.Finalize(llll11l111l1llllIl1l1, _close_handles, (llll11l111l1llllIl1l1.sentinel, int(l11l1ll11l111l11Il1l1), 
))
        else:
            llll11l111l1llllIl1l1.finalizer = util.Finalize(llll11l111l1llllIl1l1, _close_handles, (llll11l111l1llllIl1l1.sentinel, ))



        set_spawning_popen(llll11l111l1llllIl1l1)
        try:
            reduction.dump(l1ll111lll11ll1lIl1l1, ll1llll11ll11111Il1l1)
            reduction.dump(ll1l1l11ll1l1l1lIl1l1, ll1llll11ll11111Il1l1)
        finally:
            set_spawning_popen(None)
