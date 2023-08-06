from pathlib import Path

from ipkg.config.path import CACHE, PREFIX
from ipkg.shutils.download import download_cache
from ipkg.shutils.extract import extract
from ipkg.shutils.run import run
from ipkg.utils.github import get_latest_release
from ipkg.utils.pkg import get_name


def main() -> None:
    name: str = get_name(__name__)
    url: str = get_latest_release("aristocratos/btop")
    output: Path = download_cache(url=url, pkg_name=name)
    extract(filepath=output, output=CACHE / name)
    run(["make", f"--directory={CACHE / name / name}", "install", f"PREFIX={PREFIX}"])
