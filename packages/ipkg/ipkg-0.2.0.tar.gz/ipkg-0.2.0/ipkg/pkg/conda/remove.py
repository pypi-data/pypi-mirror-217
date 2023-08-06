from ipkg.config.path import OPT
from ipkg.shutils.remove import remove
from ipkg.utils.pkg import get_name


def main() -> None:
    name: str = get_name(__name__)
    remove(OPT / name)
