import logging
from logging import CRITICAL, DEBUG, ERROR, INFO, NOTSET, WARNING, Logger, log
from typing import Optional

from rich.console import Console
from rich.logging import RichHandler
from rich.style import Style
from rich.theme import Theme


def add_level_name(level_name: str, level: int = INFO) -> int:
    while level in logging.getLevelNamesMapping().values():
        level += 1
    logging.addLevelName(levelName=level_name, level=level)
    return level


COPY: int = add_level_name(level_name="COPY")
CREATE: int = add_level_name(level_name="CREATE")
DOWNLOAD: int = add_level_name(level_name="DOWNLOAD")
EXTRACT: int = add_level_name(level_name="EXTRACT")
REMOVE: int = add_level_name(level_name="REMOVE")
RUN: int = add_level_name(level_name="RUN")

logging.basicConfig(
    format="%(message)s",
    datefmt="[%Y-%m-%dT%H:%M:%S]",
    level=INFO,
    handlers=[
        RichHandler(
            console=Console(
                theme=Theme(
                    styles={
                        "logging.level.copy": Style(bold=True),
                        "logging.level.create": Style(bold=True),
                        "logging.level.download": Style(bold=True),
                        "logging.level.extract": Style(bold=True),
                        "logging.level.remove": Style(bold=True),
                        "logging.level.run": Style(bold=True),
                    }
                )
            )
        )
    ],
)


def get_logger(name: Optional[str] = None) -> Logger:
    return logging.getLogger(name)
