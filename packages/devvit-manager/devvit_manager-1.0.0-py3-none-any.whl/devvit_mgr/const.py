"""Devvit Manager Constants."""
from pathlib import Path

__version__ = "1.0.0"

DEVVIT_CLIENT_ID = "Bep8X2RRjuoyuxkKsKxFuQ"
DEVVIT_COPY_PASTE_CLIENT_ID = "TWTsqXa53CexlrYGBWaesQ"
DEVVIT_MGR_PATH = Path("~/.devvit-mgr").expanduser()
DEVVIT_PATH = Path("~/.devvit").expanduser()
PROFILES_FILE = DEVVIT_MGR_PATH / "profiles.json"
TOKEN_PATH = DEVVIT_PATH / "token"
