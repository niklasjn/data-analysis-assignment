import re
import pandas as pd
import logging
import datetime as dt
from .config import FIRST_NAME_COL, LAST_NAME_COL, EMAIL_COL, DOB_COL, ADDRESS_COL, INCOME_COL, MUNCIPALITY_COL, COMMENT_COL, EXPECTED_COLUMNS, COUNTY_FILE_MUNCIPALITY_COL

REGEX_VALIDATION_RULES = [
  {
    "column": FIRST_NAME_COL,
    "pattern": r'^[A-Za-zæøåÆØÅ][A-Za-zæøåÆØÅ\s\-\'\.]*$',
    "error_msg": "Invalid first name format"
  },
  {
    "column": LAST_NAME_COL,
    "pattern": r'^[A-Za-zæøåÆØÅ][A-Za-zæøåÆØÅ\s\-\'\.]*$',
    "error_msg": "Invalid last name format"
  },
  {
    "column": EMAIL_COL,
    "pattern": r'^[A-Za-zæøåÆØÅ0-9._%+-]+@[A-Za-zæøåÆØÅ0-9.-]+\.[a-zA-Z]{2,}$',
    "error_msg": "Invalid email format"
  }
]

  
def apply_validation_rules(df, county_df = None):
  """
  Applies validation rules to the DF

  Returns: (valid_mask, invalid_df)
  """
  valid_mask = pd.Series(True, index=df.index)
  invalid_reasons = pd.Series("", index=df.index)

  # Check for unexpected columns with data and flag for inspection
  unexpected_cols = [col for col in df.columns if col not in EXPECTED_COLUMNS]
  if unexpected_cols:
    for col in unexpected_cols:
      has_data = df[col].astype(str).str.strip().str.len() > 0
      valid_mask &= ~has_data
      invalid_indices = df.index[has_data]
      invalid_reasons.loc[invalid_indices] = f"Unexpected column '{col}' contains data. Requires manual review"

  # Check for internal comments added to rows and flag for inspection
  if COMMENT_COL in df.columns:
    has_comment = df[COMMENT_COL].astype(str).str.strip().str.len() > 0
    valid_mask &= ~has_comment
    invalid_indices = df.index[has_comment]
    invalid_reasons.loc[invalid_indices] = "Internal comment detected. Requires manual review"

  # Apply regex rules
  for rule in REGEX_VALIDATION_RULES:
    col = rule["column"]
    pattern = re.compile(rule["pattern"])
    msg = rule["error_msg"]

    if col not in df.columns:
      raise ValueError(f"Rule for column '{col}' failed: Column not found in DataFrame")

    # Create mask for this specific rule    
    col_mask = df[col].astype(str).str.match(pattern)

    # Update global valid mask 
    valid_mask &= col_mask

    #Record reasons for invalid rows if they failed this rule
    invalid_indices = df.index[~col_mask]
    invalid_reasons.loc[invalid_indices] = msg

  # Address with custom logic more robust than regex in this use case
  if ADDRESS_COL in df.columns:
    has_digit = df["Adresse"].astype(str).str.contains(r'\d', regex=True, na=False)
    not_empty = df["Adresse"].astype(str).str.strip().str.len() > 0
    address_mask = has_digit & not_empty
    valid_mask &= address_mask
    invalid_indices = df.index[~address_mask]
    invalid_reasons.loc[invalid_indices] = "Address missing or is invalid"
  
  # DOB must be parseable as a date and not in the future
  if DOB_COL in df.columns:
    is_valid_date = ~pd.isna(df[DOB_COL])
    is_not_future = df[DOB_COL] <= pd.Timestamp.now()
    date_mask = is_valid_date & is_not_future
    valid_mask &= date_mask
    invalid_indices = df.index[~date_mask]
    invalid_reasons.loc[invalid_indices] = "Invalid or future birth date"
  
  # Income must be number > 0
  if INCOME_COL in df.columns:
    income_numeric = pd.to_numeric(df[INCOME_COL], errors="coerce")
    income_mask = income_numeric.notna() & (income_numeric > 0)
    valid_mask &= income_mask
    invalid_indices = df.index[~income_mask]
    invalid_reasons.loc[invalid_indices] = "Income must be a number > 0"
  
  # Muncipality number validation with reference check
  if MUNCIPALITY_COL in df.columns:
    muncipality_numeric = pd.to_numeric(df[MUNCIPALITY_COL], errors='coerce')
    numeric_mask = muncipality_numeric.notna() & (muncipality_numeric > 0)
    
    if county_df is not None:
      valid_muncipalities = set(county_df[COUNTY_FILE_MUNCIPALITY_COL].unique())
      exists_in_reference = df[MUNCIPALITY_COL].isin(valid_muncipalities)
      muncipality_mask = numeric_mask & exists_in_reference
      invalid_numeric = df.index[~numeric_mask]
      invalid_reference = df.index[~exists_in_reference & numeric_mask]
      invalid_reasons.loc[invalid_numeric] = "Muncipality number must be a number > 0"
      invalid_reasons.loc[invalid_reference] = "Muncipality number not found in reference table"
    else:
      muncipality_mask = numeric_mask
      invalid_indices = df.index[~muncipality_mask]
      invalid_reasons.loc[invalid_indices] = "Muncipality number must be a number > 0"

    valid_mask &= muncipality_mask
  
  #Filter invalid rows
  invalid_df = df[~valid_mask].copy()
  invalid_df['removal_reason'] = invalid_reasons[~valid_mask]
  invalid_df["original_index"] = invalid_df.index

  return valid_mask, invalid_df
