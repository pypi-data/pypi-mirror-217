# This file is placed in the Public Domain.


"fleet"


from opr.handler import Bus
from opr.objects import kind, prt


def flt(event):
    "show listeners"
    try:
        index = int(event.args[0])
        event.reply(prt(Bus.objs[index]))
        return
    except (KeyError, TypeError, IndexError, ValueError):
        pass
    event.reply(' | '.join([kind(obj) for obj in Bus.objs]))
