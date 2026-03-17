from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent.parent
DATA_PATH = PROJECT_ROOT / 'data' / 'raw'

CODEBOOK_START_HEADER_ROW = 43
VARIABLE_NAME_COL = "Variabelnavn 2025"
QUESTION_TEXT_COL = "Spørsmålstekst"
LEARN_OUTCOME_PREFIX = "laerutb_"
