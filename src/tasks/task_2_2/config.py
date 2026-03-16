from pathlib import Path

# Columns
FIRST_NAME_COL = "Fornavn"
LAST_NAME_COL = "Etternavn"
EMAIL_COL = "E-post"
DOB_COL = "Fødselsdato"
ADDRESS_COL = "Adresse"
INCOME_COL = "INNTEKT"
MUNCIPALITY_COL = "Komm.Nr. (fra 2024)"
COMMENT_COL = "Intern kommentar"
COUNTY_FILE_MUNCIPALITY_COL = "Kommunenr"
COUNTY_FILE_COUNTY_COL = "Fylkesnr"
PERSON_DUPLICATE_FIELDS = [FIRST_NAME_COL, LAST_NAME_COL, DOB_COL]
EXPECTED_COLUMNS = [
  FIRST_NAME_COL, LAST_NAME_COL, EMAIL_COL, DOB_COL, ADDRESS_COL,
  INCOME_COL, MUNCIPALITY_COL, COMMENT_COL
]
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

# Path handling
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent.parent
DATA_PATH = PROJECT_ROOT / 'data' / 'raw'
LOG_PATH = PROJECT_ROOT / 'data' / 'logs'
LOG_PATH.mkdir(parents=True, exist_ok=True)
PROCESSED_PATH = PROJECT_ROOT / 'data' / 'processed'
PROCESSED_PATH.mkdir(parents=True, exist_ok=True)
