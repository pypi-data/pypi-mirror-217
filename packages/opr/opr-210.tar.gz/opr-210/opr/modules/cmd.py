# This file is placed in the Public Domain.


"command"


from opr.handler import Commands
from opr.objects import keys


def cmd(event):
    "show list of commands"
    event.reply(','.join(sorted(keys(Commands.cmds))))
