"""Small local configuration loader for development.

In AWS Lambda, configure the same values as Lambda environment variables.
"""

import os
from pathlib import Path


def _load_dotenv():
    """Load simple KEY=VALUE entries from a local .env file if present."""
    for env_path in (Path(__file__).with_name('.env'), Path.cwd() / '.env'):
        if not env_path.exists():
            continue

        for line in env_path.read_text(encoding='utf-8').splitlines():
            line = line.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue
            key, value = line.split('=', 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"\''))


_load_dotenv()


def get_env(name, default=None):
    return os.getenv(name, default)

