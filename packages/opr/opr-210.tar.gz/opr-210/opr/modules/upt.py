# This file is placed in the Public Domain.


"show uptime"


import time


from opr.utility import elapsed


STARTTIME = time.time()


def upt(event):
    "show uptime"
    event.reply(elapsed(time.time()-STARTTIME))
