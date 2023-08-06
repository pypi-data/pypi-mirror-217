# This file is placed in the Public Domain.


"thread"


import threading
import time


from opr.objects import Object, update
from opr.utility import elapsed


STARTTIME = time.time()


def thr(event):
    "show list of running threads"
    result = []
    for thread in sorted(threading.enumerate(), key=lambda x: x.getName()):
        if str(thread).startswith('<_'):
            continue
        obj = Object()
        update(obj, vars(thread))
        if getattr(obj, 'sleep', None):
            uptime = obj.sleep - int(time.time() - obj.state.latest)
        elif getattr(obj, 'starttime', None):
            uptime = int(time.time() - obj.starttime)
        else:
            uptime = int(time.time() - STARTTIME)
        result.append((uptime, thread.name))
    res = []
    for uptime, txt in sorted(result, key=lambda x: x[1]):
        lap = elapsed(uptime)
        res.append(f'{txt}/{lap}')
    if res:
        event.reply(' '.join(res))
    else:
        event.reply('no threads')
