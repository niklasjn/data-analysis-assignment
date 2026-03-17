"""
Configuration module for task 2.2: Data cleaning pipeline.

Defines constants used across the pipeline:
- Column name mappings (source names)
- Target output schema (standardized snake-case names in preferred order)
- File paths for input, output and logging

The module aims at centralizing all configuration to ensure consistency
and make future updates easier.
"""


from pathlib import Path


# -----------------------------------------------------------------------------
# Column names (source data)
# -----------------------------------------------------------------------------
FIRST_NAME_COL = "Fornavn"
LAST_NAME_COL = "Etternavn"
EMAIL_COL = "E-post"
DOB_COL = "Fødselsdato"
ADDRESS_COL = "Adresse"
INCOME_COL = "INNTEKT"
MUNICIPALITY_COL = "Komm.Nr. (fra 2024)"
COMMENT_COL = "Intern kommentar"

# Reference file column names
COUNTY_FILE_MUNICIPALITY_COL = "Kommunenr"
COUNTY_FILE_COUNTY_COL = "Fylkesnr"

# -----------------------------------------------------------------------------
# Validation and deduplication configuration
# -----------------------------------------------------------------------------

#Fields used to identify potential person duplicates
PERSON_DUPLICATE_FIELDS = [FIRST_NAME_COL, LAST_NAME_COL, DOB_COL]

# Expected columns in the input data (used for schema validation)
EXPECTED_COLUMNS = [
  FIRST_NAME_COL, LAST_NAME_COL, EMAIL_COL, DOB_COL, ADDRESS_COL,
  INCOME_COL, MUNICIPALITY_COL, COMMENT_COL
]

# -----------------------------------------------------------------------------
# Output schema (Target column names)
# -----------------------------------------------------------------------------

# Mapping from source column names to standardized output names (snake_case)
# The order of the target columns decides the order of the output columns
TARGET_COLUMNS = {
    "Respondent_ID": "respondent_id",
    "Full_Name": "fullt_navn",
    "E-post": "epost",
    "Fødselsdato": "fødselsdato",
    "Adresse": "adresse",
    "INNTEKT": "inntekt",
    "Inntektsnivå": "inntektsnivå",
    "Kommunenr (fra 2024)": "kommunenr",
    "Fylkesnr": "fylkesnr"
}

# -----------------------------------------------------------------------------
# File paths
# -----------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent.parent

DATA_PATH = PROJECT_ROOT / 'data' / 'raw'
LOG_PATH = PROJECT_ROOT / 'data' / 'logs'
PROCESSED_PATH = PROJECT_ROOT / 'data' / 'processed'

# Ensure directories exist
for path in [DATA_PATH, LOG_PATH, PROCESSED_PATH]:
  path.mkdir(parents=True, exist_ok=True)
