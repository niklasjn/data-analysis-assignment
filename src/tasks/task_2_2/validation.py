"""
Data validation module for for task 2.2: Cleaning pipeline.

Handles data quality checks including:
  - Regex pattern matching for names and emails
  - Date validation (parseability and future date checks)
  - Numeric validation for income and municipality numbers
  - Referential integrity checks against external reference tables
  - Detection of unexpected columns and internal comments

Module runs after normalization and before deduplication,
ensuring only valid data proceeds through the pipeline
"""


import re
import pandas as pd
from typing import Optional, Tuple
from .config import (
  FIRST_NAME_COL, LAST_NAME_COL, EMAIL_COL, DOB_COL, 
  ADDRESS_COL, INCOME_COL, MUNICIPALITY_COL, COMMENT_COL, 
  EXPECTED_COLUMNS, COUNTY_FILE_MUNICIPALITY_COL
)


# Validation rules for regex pattern matching (column name, pattern, error message)
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

  
def apply_validation_rules(
    df: pd.DataFrame,
    county_df: Optional[pd.DataFrame] = None
) -> Tuple[pd.Series, pd.DataFrame]:
  """
  Applies validation rules to the DataFrame.

  Performs the following checks:
    - Unexpected columns with data (flags for manual review)
    - Internal comments in designated column (falgs for manual review)
    - Regex pattern matching for names and emails
    - Address validation (must contain house number)
    - Date validation (parseable and not in future)
    - Numeric validation for income and municipality numbers
    - Referential integrity for municipality numbers (if reference table is provided)

  Args:
    df: Input DataFrame to validate
    county_df: Optional reference DataFrame with valid municipality number
               (contains columns COUNTY_FILE_MUNICIPALITY_COL, COUNTY_FILE_COUNTY_COL)

  Returns:
    Tuple containing:
      - valid_mask: Boolean Series indicating which rows pass all validation rules
      - invalid_df: DataFrame containing rows that failed validation, with
                    'removal_reason' and 'original_index' columns
  
  Note:
    Rows flagged for manual remove will (and must) have "Requires manual review" in 
    their removal_reason.
  """
  valid_mask = pd.Series(True, index=df.index)
  invalid_reasons = pd.Series("", index=df.index)

  # Check for unexpected columns with data and flag for manual review
  unexpected_cols = [col for col in df.columns if col not in EXPECTED_COLUMNS]
  if unexpected_cols:
    for col in unexpected_cols:
      has_data = df[col].astype(str).str.strip().str.len() > 0
      valid_mask &= ~has_data
      invalid_indices = df.index[has_data]
      invalid_reasons.loc[invalid_indices] = (
        f"Unexpected column '{col}' contains data. Requires manual review"
      )

  # Check for internal comments added to rows and flag for manual review
  if COMMENT_COL in df.columns:
    has_comment = df[COMMENT_COL].astype(str).str.strip().str.len() > 0
    valid_mask &= ~has_comment
    invalid_indices = df.index[has_comment]
    invalid_reasons.loc[invalid_indices] = (
      f"Internal comment detected. Requires manual review"
      )

  # Apply regex rules for names and email
  for rule in REGEX_VALIDATION_RULES:
    col = rule["column"]
    pattern = re.compile(rule["pattern"])
    msg = rule["error_msg"]

    if col not in df.columns:
      raise ValueError(f"Rule for column '{col}' failed: Column not found in DataFrame")

    col_mask = df[col].astype(str).str.match(pattern)
    valid_mask &= col_mask

    invalid_indices = df.index[~col_mask]
    invalid_reasons.loc[invalid_indices] = msg

  # Address validation. Must be non empty and contain house number
  if ADDRESS_COL in df.columns:
    has_digit = df["Adresse"].astype(str).str.contains(r'\d', regex=True, na=False)
    not_empty = df["Adresse"].astype(str).str.strip().str.len() > 0
    address_mask = has_digit & not_empty
    valid_mask &= address_mask
    invalid_indices = df.index[~address_mask]
    invalid_reasons.loc[invalid_indices] = "Address missing or is invalid"
  
  # Date validation. Must be parseable and not in future
  if DOB_COL in df.columns:
    is_valid_date = ~pd.isna(df[DOB_COL])
    is_not_future = df[DOB_COL] <= pd.Timestamp.now()
    date_mask = is_valid_date & is_not_future
    valid_mask &= date_mask
    invalid_indices = df.index[~date_mask]
    invalid_reasons.loc[invalid_indices] = "Invalid or future birth date"
  
  # Income validation. Must be numeric and > 0
  if INCOME_COL in df.columns:
    income_numeric = pd.to_numeric(df[INCOME_COL], errors="coerce")
    income_mask = income_numeric.notna() & (income_numeric > 0)
    valid_mask &= income_mask
    invalid_indices = df.index[~income_mask]
    invalid_reasons.loc[invalid_indices] = "Income must be a number > 0"
  
  # Municipality validation. Numeric check + optional referential integrity
  if MUNICIPALITY_COL in df.columns:
    municipality_numeric = pd.to_numeric(df[MUNICIPALITY_COL], errors='coerce')
    numeric_mask = municipality_numeric.notna() & (municipality_numeric > 0)
    
    if county_df is not None:
      # Check against reference table
      valid_municipalities = set(county_df[COUNTY_FILE_MUNICIPALITY_COL].unique())
      exists_in_reference = df[MUNICIPALITY_COL].isin(valid_municipalities)
      municipality_mask = numeric_mask & exists_in_reference
      # Track specific failure reasons
      invalid_numeric = df.index[~numeric_mask]
      invalid_reference = df.index[~exists_in_reference & numeric_mask]
      invalid_reasons.loc[invalid_numeric] = (
        "Municipality number must be a number > 0"
      )
      invalid_reasons.loc[invalid_reference] = (
        "Municipality number not found in reference table"
      )
    else:
      # Fallback: only numeric check
      municipality_mask = numeric_mask
      invalid_indices = df.index[~municipality_mask]
      invalid_reasons.loc[invalid_indices] = (
        "Municipality number must be a number > 0"
      )

    valid_mask &= municipality_mask
  
  # Create invalid DataFrame with metadata
  invalid_df = df[~valid_mask].copy()
  invalid_df['removal_reason'] = invalid_reasons[~valid_mask]
  invalid_df["original_index"] = invalid_df.index

  return valid_mask, invalid_df
