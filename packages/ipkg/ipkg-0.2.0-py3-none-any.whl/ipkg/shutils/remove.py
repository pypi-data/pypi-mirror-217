import os
import shutil
from pathlib import Path

from ipkg import logging


def remove(path: Path) -> None:
    if not path.exists():
        return
    if path.is_dir():
        shutil.rmtree(path)
        logging.log(level=logging.REMOVE, msg=f"directory '{path}'")
    elif path.is_file():
        os.remove(path)
        logging.log(level=logging.REMOVE, msg=f"'{path}'")
    else:
        raise ValueError(f"Unknown path type: '{path}'")
    if not os.listdir(path.parent):
        remove(path.parent)
