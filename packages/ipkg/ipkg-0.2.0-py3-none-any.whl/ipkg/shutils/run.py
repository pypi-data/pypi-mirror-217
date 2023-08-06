import shlex
import subprocess

from ipkg import logging


def run(args: list, check: bool = True) -> None:
    args = list(map(str, args))
    logging.log(level=logging.RUN, msg=shlex.join(args))
    subprocess.run(args=args, check=check)
