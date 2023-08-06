# This file is placed in the Public Domain.


"status"


from opr.handler import Bus
from opr.objects import prt


def sts(event):
    "print status"
    nmr = 0
    for bot in Bus.objs:
        if 'state' in dir(bot):
            event.reply(prt(bot.state, skip='lastline'))
            nmr += 1
    if nmr:
        event.reply("no status")
