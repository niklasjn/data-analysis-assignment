from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent.parent
DATA_PATH = PROJECT_ROOT / 'data' / 'raw'
