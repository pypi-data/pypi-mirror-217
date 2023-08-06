import platform
from collections.abc import Sequence

from github import Github
from github.GitRelease import GitRelease
from github.GitReleaseAsset import GitReleaseAsset
from github.Repository import Repository


def get_latest_release(full_name_or_id: int | str) -> str:
    github: Github = Github()
    repo: Repository = github.get_repo(full_name_or_id)
    release: GitRelease = repo.get_latest_release()
    assets: Sequence[GitReleaseAsset] = release.assets
    system: str = platform.system().lower()
    assets = list(filter(lambda asset: system in asset.name.lower(), assets))
    machine: str = platform.machine().lower()
    assets = list(filter(lambda asset: machine in asset.name.lower(), assets))
    assert len(assets) == 1
    return assets[0].browser_download_url
