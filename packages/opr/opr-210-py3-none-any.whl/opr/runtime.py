# This file is placed in the Public Domain.


"runtime"


# IMPORTS


import io
import os
import readline
import sys
import termios
import time
import traceback


from opr.handler import Commands, Errors, Event, Handler
from opr.loggers import Logging
from opr.objects import Default, update
from opr.persist import Persist
from opr.threads import launch
from opr.utility import spl


import opr.modules


# DEFINES


DATE = time.ctime(time.time()).replace("  ", " ")
NAME = __file__.split(os.sep)[-2]
STARTTIME = time.time()


Persist.workdir = os.path.expanduser("~/.{NAME}")


Cfg = Default()
Cfg.debug = False
Cfg.mod = "cmd,mod,thr,upt"
Cfg.verbose = False


readline.redisplay()


# CLASSES


class CLI(Handler):

    "command line interface"

    def announce(self, txt):
        "annouce text"

    def raw(self, txt):
        "print text"
        print(txt)


class Console(CLI):

    "cli in a loop"

    def handle(self, evt):
        "wait for events"
        CLI.handle(self, evt)
        evt.wait()

    def poll(self):
        "echo prompt"
        return self.event(input("> "))


# UTILITY


def banner():
    "print banner"
    print(f"{NAME.upper()} started {DATE}")
    sys.stdout.flush()


def command(cli, txt) -> Event:
    "run a command on a cli"
    evt = cli.event(txt)
    Commands.handle(evt)
    evt.ready()
    return evt


def daemon():
    "fork to the background"
    pid = os.fork()
    if pid:
        os.setsid()
        os.umask(0)
        with open('/dev/null', 'r', encoding="utf-8") as sis:
            os.dup2(sis.fileno(), sys.stdin.fileno())
        with open('/dev/null', 'a+', encoding="utf-8") as sos:
            os.dup2(sos.fileno(), sys.stdout.fileno())
        with open('/dev/null', 'a+', encoding="utf-8") as ses:
            os.dup2(ses.fileno(), sys.stderr.fileno())


def parse_cli(txt) -> Cfg:
    "parse commad line interface"
    evt = Event()
    evt.parse(txt)
    update(Cfg, evt, False)
    Cfg.mod += evt.mods
    return Cfg


def scanstr(pkg, mods, init=None, doall=False, wait=False) -> None:
    "scan a package for list of modules"
    res = []
    path = pkg.__path__[0]
    if doall:
        modlist = [x[:-3] for x in os.listdir(path) if x.endswith(".py") and x != "__init__.py"]
        mods = ",".join(sorted(modlist))
    threads = []
    for modname in spl(mods):
        module = getattr(pkg, modname, None)
        if module:
            if not init:
                Commands.scan(module)
        if init and "start" in dir(module):
            threads.append(launch(module.start))
        res.append(module)
    if wait:
        for thread in threads:
            thread.join()
    return res


def waiter(clear=True):
    "poll for errors"
    got = []
    for ex in Errors.errors:
        stream = io.StringIO(
                             traceback.print_exception(
                                                       type(ex),
                                                       ex,
                                                       ex.__traceback__
                                                      )
                            )
        for line in stream.readlines():
            Logging.debug(line)
        got.append(ex)
    if clear:
        for exc in got:
            Errors.errors.remove(exc)



def wrap(func):
    "wrap function"
    fds = sys.stdin.fileno()
    gotterm = True
    try:
        old = termios.tcgetattr(fds)
    except termios.error:
        gotterm = False
    try:
        func()
    except (EOFError, KeyboardInterrupt):
        print("")
    finally:
        if gotterm:
            termios.tcsetattr(fds, termios.TCSADRAIN, old)
        waiter()


def main():
    "main program function"
    parse_cli(' '.join(sys.argv[1:]))
    if "v" in Cfg.opts and "d" not in Cfg.opts:
        Logging.verbose = True
        Logging.raw = print
    dowait = False
    scanstr(opr.modules, Cfg.mod)
    if Cfg.txt:
        cli = CLI()
        command(cli, Cfg.otxt)
    elif 'd' in Cfg.opts:
        daemon()
        dowait = True
    if "c" in Cfg.opts:
        dowait = True
    if dowait:
        banner()
        if 'c' in Cfg.opts and "d" not in Cfg.opts:
            csl = Console()
            csl.start()
        scanstr(opr.modules, Cfg.mod, True, wait=True)
        while 1:
            time.sleep(1.0)
            waiter()


if __name__ == "__main__":
    wrap(main)
