# This file is placed in the Public Domain.


"modules"


import os

import opr.modules


def mod(event):
    "show list of available modules"
    path = opr.modules.__path__[0]
    modlist = [x[:-3] for x in os.listdir(path) if x.endswith(".py") and x != "__init__.py"]
    mods = ",".join(sorted(modlist))
    event.reply(mods)
