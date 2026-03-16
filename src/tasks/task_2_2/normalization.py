"""
Data normalization module for the cleaning pipeline.

Handles normalizaton of data formats including:
  - String normalization (lowercase, whitespace trimming)
  - Date parsing with multiple format support
  - Email standardization

The module runs early in the pipeline to ensure consistent data formats
before data validation.
"""


import pandas as pd
import datetime as dt
from typing import Any
from .config import FIRST_NAME_COL, LAST_NAME_COL, EMAIL_COL, DOB_COL


# Date formats to try when parsing dates
DATE_FORMATS = [
    "%Y-%m-%d",      # 1980-01-01 
    "%d.%m.%Y",      # 15.02.1985 
    "%Y/%m/%d",      # 1985/02/15
    "%Y.%m.%d",      # 1995.04.25
    "%d-%m-%Y",      # 15-02-1985
    "%m/%d/%Y",      # 02/15/1985 
    "%d/%m/%Y",      # 15/02/1985 
]


def parse_date_flexible(date_value: Any) -> dt.datetime | None:
  """
  Attempts to parse a date string using multiple format strategies.

  Tries common date formats in sequence, falling back to pandas' flexible
  parser if all explicit formats fail. 

  Args:
    date_value: Input value (string, datetime, or NaT) to parse
  
  Returns:
    datetime.datetime object if parsing succeeds, pd.NaT otherwise
  """
  # Handle missing or empty values
  if pd.isna(date_value) or date_value == "":
    return pd.NaT
  
  date_str = str(date_value).strip()

  # Try pre defined date formats sequentially
  for fmt in DATE_FORMATS:
    try:
      return dt.datetime.strptime(date_str, fmt)
    except ValueError:
      continue

  #Fallback: Try pandas flexible datetime parser (handles edge cases)
  try:
    return pd.to_datetime(date_str, dayfirst=True, errors='raise')
  except (ValueError, TypeError):
    return pd.NaT
  

def normalize_data(df: pd.DataFrame) -> pd.DataFrame:
  """
  Normalizes data formats in the DataFrame.

  Performs the following standardizations:
  - Converts name and email columns to lowercase with trimmed whitespace
  - Parses date columns to datetime objects (invalid dates become NaT)

  Args:
    df: Input DataFrame to normalize

  Returns:
    DataFrame with normalized formats

  Note:
    Date columns will be datetime64[ns] dtype after normalization.
  """
  df = df.copy()

  # Normalize string columns (name and email)
  for col in [FIRST_NAME_COL, LAST_NAME_COL, EMAIL_COL]:
    if col in df.columns:
      df[col] = df[col].astype(str).str.lower().str.strip()
  
  # Parse date column to datetime objects
  if DOB_COL in df.columns:
    df[DOB_COL] = df[DOB_COL].apply(parse_date_flexible)

  return df
  