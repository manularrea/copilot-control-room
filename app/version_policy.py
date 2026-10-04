"""Training exercise only: never installs or downloads packages."""
import json
from pathlib import Path


def allowed(manifest):
    data = json.loads(Path(manifest).read_text(encoding='utf-8'))
    return data['components']['faro-csv-parser']['version'] == '1.0.1'
