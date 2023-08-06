# This file is placed in the Public Domain.


"error"


import io
import traceback


from opr.handler import Errors


def err(event):
    "show errors"
    nmr = 0
    for exc in Errors.errors:
        stream = io.StringIO(
                             traceback.print_exception(
                                                       type(exc),
                                                       exc,
                                                       exc.__traceback__
                                                      )
                            )
        for line in stream.readlines():
            event.reply(line)
            nmr += 1
    if not nmr:
        event.reply("no error")
