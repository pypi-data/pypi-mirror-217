import platform
from pathlib import Path

from ipkg.config.path import OPT
from ipkg.shutils.download import download_cache
from ipkg.shutils.run import run
from ipkg.utils.pkg import get_name


def get_install_url() -> str:
    system: str = platform.system()
    machine: str = platform.machine()
    return (
        f"https://repo.anaconda.com/miniconda/Miniconda3-latest-{system}-{machine}.sh"
    )


def main() -> None:
    name: str = get_name(__name__)
    install_script: Path = download_cache(
        url=get_install_url(),
        pkg_name=name,
        filename="install.sh",
    )
    run(["bash", install_script, "-b", "-f", "-p", OPT / name])
