import pandas as pd
from pathlib import Path

import logging

# Path handling
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent.parent
DATA_PATH = PROJECT_ROOT / 'data' / 'raw'
LOG_PATH = PROJECT_ROOT / 'data' / 'logs'
LOG_PATH.mkdir(parents=True, exist_ok=True)

# Configure logging
logging.basicConfig(
  filename= LOG_PATH / 'processing.log',
  level=logging.INFO,
  format='%(asctime)s - %(levelname)s - %(message)s'
)





# Column names
FIRST_NAME_COL = "Fornavn"
LAST_NAME_COL = "Etternavn"
EMAIL_COL = "E-post"

df = pd.read_excel(DATA_PATH / "fiktiv_kontaktinformasjon.xlsx", sheet_name="Sheet1")
df.columns = df.columns.str.strip()

# Masks
valid_name_mask = (
    df[FIRST_NAME_COL].astype(str).str.match(LEGAL_NAME_PATTERN)
) & (
    df[LAST_NAME_COL].astype(str).str.match(LEGAL_NAME_PATTERN)
)
valid_email_mask = (
  df[EMAIL_COL].astype(str).str.match(LEGAL_EMAIL_PATTERN)
)
valid_mask = valid_name_mask & valid_email_mask

# Log removed rows before filtering
invalid_rows_names = df[~valid_name_mask]
n_removed_names = len(invalid_rows_names)
logging.info(f"Name validation: {n_removed_names} rows removed")
invalid_rows_emails = df[~valid_email_mask]
n_removed_emails = len(invalid_rows_emails)
logging.info(f"Email validation: {n_removed_emails} rows removed")


if n_removed_names > 0:
  invalid_rows_names.to_excel(LOG_PATH / "removed_rows_names.xlsx", index=False)
  logging.info(f"Removed rows saved to {LOG_PATH} / 'removed_rows_names.xlsx'")
if n_removed_emails > 0:
  invalid_rows_emails.to_excel(LOG_PATH / "removed_rows_emails.xlsx", index=False)
  logging.info(f"Removed rows saved to {LOG_PATH} / 'removed_rows_emails.xlsx'")


# Filter on name
df = df[valid_name_mask]
#Filter on email
df = df[valid_email_mask]



