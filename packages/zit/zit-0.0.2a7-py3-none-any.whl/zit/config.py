import logging
import os
from pathlib import Path

from rich.logging import RichHandler

ZITRC_FILE = Path(os.path.expanduser("~/.zitrc"))
REGISTRY_ENDPOINT = "http://localhost:6000/api/formula"
WS_PUBLISH_ENDPOINT = "ws://localhost:6000/api/formula/publish"
WS_INSTALL_ENDPOINT = "ws://localhost:6000/api/formula/install"
AUTH_PUBLIC_ENDPOINT = "http://localhost:8080/api/auth/public"


logging.basicConfig(level="INFO", format="%(message)s", handlers=[RichHandler(rich_tracebacks=True)])
logger = logging.getLogger(__name__)
