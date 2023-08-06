from ipkg.config.path import APPLICATIONS, BIN, ICONS, SHARE
from ipkg.shutils.remove import remove
from ipkg.utils.pkg import get_name


def main() -> None:
    name: str = get_name(__name__)
    remove(APPLICATIONS / f"{name}.desktop")
    remove(BIN / name)
    remove(ICONS / "hicolor" / "48x48" / "apps" / f"{name}.png")
    remove(ICONS / "hicolor" / "scalable" / "apps" / f"{name}.svg")
    remove(SHARE / name)
