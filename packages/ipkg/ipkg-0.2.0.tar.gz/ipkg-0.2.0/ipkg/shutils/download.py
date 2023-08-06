from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional
from urllib.parse import ParseResult, urlparse

import requests
import tenacity
from httpie.core import main as https

from ipkg import NAME, logging
from ipkg.config.path import CACHE

from .mkdir import mkdir

logger: logging.Logger = logging.get_logger(__name__)


@tenacity.retry(
    stop=tenacity.stop_after_attempt(4),
    wait=tenacity.wait_random_exponential(),
    before_sleep=tenacity.before_sleep_log(logger=logger, log_level=logging.ERROR),
    reraise=True,
)
def _download(url: str, output: Path) -> None:
    https(
        args=[
            "https",
            "--body",
            f"--output={output}",
            "--download",
            url,
        ]
    )


def download(
    url: str,
    output: Path,
    *,
    cache_ttl: timedelta = timedelta(),
) -> None:
    if not output.parent.exists():
        mkdir(output.parent)
    if output.exists():
        if datetime.now() - datetime.fromtimestamp(output.stat().st_mtime) < cache_ttl:
            response: requests.Response = requests.get(url=url, stream=True)
            if output.stat().st_size == int(response.headers.get("Content-Length", -1)):
                logging.log(level=logging.DOWNLOAD, msg=f"cached '{output}' <- {url}")
                return
    logging.log(level=logging.DOWNLOAD, msg=f"'{output}' <- {url}")
    _download(url=url, output=output)
    return


def download_cache(
    url: str,
    pkg_name: str,
    filename: Optional[str] = None,
    *,
    cache_ttl: timedelta = timedelta(days=1),
) -> Path:
    if not filename:
        parse_result: ParseResult = urlparse(url)
        url_path: Path = Path(parse_result.path)
        filename = url_path.name
    output: Path = CACHE / NAME / pkg_name / filename
    download(url=url, output=output, cache_ttl=cache_ttl)
    return output
