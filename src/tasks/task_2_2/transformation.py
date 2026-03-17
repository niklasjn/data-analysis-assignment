"""
Data transformation module for for task 2.2: Cleaning pipeline.

Handles structural changes to the DataFrame including:
  - Merging name columns into full names
  - Standardizing column names and order
  - Formatting dates for final output
"""


import pandas as pd
import datetime as dt
from .config import FIRST_NAME_COL, LAST_NAME_COL, DOB_COL, TARGET_COLUMNS


def merge_names(df: pd.DataFrame) -> pd.DataFrame:
  """
  Merges first and last name columns into a signle full name column.

  Combines the first and last name columns with a space separator,
  applies title case formatting, and removes the original columns.

  Args:
    df: Input DataFrame with FIRST_NAME_COL and LAST_NAME_COL columns

  Returns:
    DataFrame with a new "full_name" column and original name columns removed
  """
  df = df.copy()

  # Combine names with title case formatting for consistency
  df["fullt_navn"] = (
    df[FIRST_NAME_COL].str.title() + " " + df[LAST_NAME_COL].str.title()
  )

  # Remove original name columns
  df = df.drop(columns=[FIRST_NAME_COL, LAST_NAME_COL])

  return df


def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
  """
  Standardizes column names and orders them according to the target schema.

  Performs the following transformations:
    - Formats date columns to YYYY-MM-DD string format
    - Renames columns to lowercase with underscores (snake_case)
    - Reorders columns to match the predefined TARGET_COLUMNS schema

  Args:
    - df: Input DataFrame with columns to standardize
  
  Returns:
    - DataFrame with standardizeed column names and order
  """
  df = df.copy()

  # Format date column to string (removes time component for clean export)
  if DOB_COL in df.columns:
    df[DOB_COL] = df[DOB_COL].dt.strftime("%Y-%m-%d")
  
  # Rename columns to standardized snake_case from TARGET_COLUMNS schema
  df = df.rename(columns=TARGET_COLUMNS)

  # Reorder columns and keep only those that exist in the DataFrame
  available_columns = [col for col in TARGET_COLUMNS.values() if col in df.columns]
  df = df[available_columns]

  return df


