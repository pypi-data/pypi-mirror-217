import shutil
from pathlib import Path

from ipkg import logging


def _unpack_tarfile(filename, extract_dir):
    """Unpack tar/tar.gz/tar.bz2/tar.xz `filename` to `extract_dir`"""
    import tarfile  # late import for breaking circular dependency

    try:
        tarobj = tarfile.open(filename)
    except tarfile.TarError:
        raise shutil.ReadError(
            "%s is not a compressed or uncompressed tar file" % filename
        )
    try:
        tarobj.extractall(extract_dir)
    finally:
        tarobj.close()


shutil.unregister_unpack_format("bztar")
shutil.register_unpack_format(
    name="bztar",
    extensions=[".tar.bz2", ".tbz2", ".tbz"],
    function=_unpack_tarfile,
    description="bzip2'ed tar-file",
)


def extract(filepath: Path, output: Path) -> None:
    logging.log(level=logging.EXTRACT, msg=f"'{filepath}' -> '{output}'")
    shutil.unpack_archive(filename=filepath, extract_dir=output)
