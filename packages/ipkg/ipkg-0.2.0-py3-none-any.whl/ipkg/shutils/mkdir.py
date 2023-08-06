from pathlib import Path

from ipkg import logging


def mkdir(path: Path) -> None:
    if not path.exists():
        path.mkdir(parents=True)
        logging.log(level=logging.CREATE, msg=f"directory '{path}'")
