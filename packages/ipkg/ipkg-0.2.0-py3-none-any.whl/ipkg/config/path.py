from pathlib import Path

CACHE: Path = Path.home() / ".cache"
CONFIG: Path = Path.home() / ".config"
PREFIX: Path = Path.home() / ".local"

BIN: Path = PREFIX / "bin"
OPT: Path = PREFIX / "opt"
SHARE: Path = PREFIX / "share"

APPLICATIONS: Path = SHARE / "applications"
ICONS: Path = SHARE / "icons"
