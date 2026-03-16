"""
Data enrichment module for the cleaning pipeline.

Handles augmentation of the dataset with external data and derived features:
  - Adding county numbers (Fylkesnr) based on municipality lookup
  - Categorizing income levels into quantile-based groups
  - Generating unique sequential identifiers for respondents

The module runs after validation and deduplication, adding 
value to the cleaned dataset before final export
"""


import pandas as pd
import logging
from typing import Optional
from .config import (
  MUNICIPALITY_COL, COUNTY_FILE_COUNTY_COL, 
  COUNTY_FILE_MUNICIPALITY_COL, INCOME_COL
)


def add_county_number(
    df: pd.DataFrame, 
    county_df: Optional[pd.DataFrame] = None
    ) -> pd.DataFrame:
  """
  Enriches data by adding Fylkesnr (county number) based on Kommunenr (municipality number) lookup

  Maps municipality numbers from the input DataFrame to county numbers using a reference table.
  If the reference table is missing or a municipality is not found,
  the resulting value will be NaN.

  Args:
    df: Input DataFrame to enrich 
    county_df: Optional reference DataFrame containing:
                - COUNTY_FILE_MUNICIPALITY_COL (Kommunenr)
                - COUNTY_FILE_COUNTY_COL (Fylkesnr) 
  
  Returns:
    DataFrame with new 'fylkesnummer' column added
    If county_df is None or Missing, the column is not added

  Args:
    df: The data to enrich
    county_df: Reference DataFrame with Kommunenr and Fylkesnr columns

  Returns:
    DataFrame with new Fylkesnr column
  """
  df = df.copy()

  if county_df is None:
    logging.warning("County reference table is None. Skipping county enrichment")
    return df
  
  if MUNICIPALITY_COL not in df.columns:
    logging.warning(f"Column '{MUNICIPALITY_COL}' not found. Skipping county enrichment")
    return df
  
  # Create a mapping dictionary: Kommunenr -> Fylkesnr
  # set_index creates a Series indexed by municipality number
  # to_dict() converts it to a fast lookup dictionary
  try:
    county_mapping = county_df.set_index(COUNTY_FILE_MUNICIPALITY_COL)[COUNTY_FILE_COUNTY_COL].to_dict()
  except KeyError as e:
    logging.error(f"Reference table missing required column: {e}")
    return df

  # Map the municipality numbers to county numbers
  # Unmatched values become NaN automatically
  df["fylkesnummer"] = df[MUNICIPALITY_COL].map(county_mapping)

  # Log how many mappings succeeded vs failed
  matched = df["fylkesnummer"].notna().sum()
  total = len(df)
  logging.info(f"County enrichment: {matched}/{total} rows mapped successfully.")

  return df


def add_income_level(df: pd.DataFrame) -> pd.DataFrame:
  """
  Enriches data by adding an income level category ('lav', 'middels', 'høy').

  Splits the income distribution into three equal-sized groups (quantiles):
  - 'lav':      Bottom 33 %
  - 'middels':  Middle 33 %
  - 'høy':      top 33 %

  Args:
    df: Input DataFrame to enrich (must contain INCOME_COL)

  Returns:
    DataFrame with new 'inntektsnivå' column added
    If income data is insufficient or has no variance, the column may contain NaN
  """
  df = df.copy()

  if INCOME_COL not in df.columns:
    logging.warning(f"Column {INCOME_COL} missing. Skipping income enrichment")
    return df
  
  try:
    # pd.qcut divides data into n equal-sized buckets
    # q = 3 means 3 quantiles (0-33%, 33-66%, 66-100%)
    # duplicates='drop' handles cases where many values are identical
    df["inntektsnivå"] = pd.qcut(
      df[INCOME_COL], 
      q=3, 
      labels=["lav", "middels", "høy"], 
      duplicates="drop"
    )

    # Check if we ended up with fewer than 3 groups
    unique_groups = df["inntektsnivå"].nunique()
    if unique_groups < 3:
      logging.warning(
        f"Income distribution lacks variance: only {unique_groups} unique groups "
        "created. Consider reviewing the data."
      )
  except ValueError as e:
    logging.error(f"Failed to create income levels due to insufficient variance: {e}")
    df["inntektsnivå"] = pd.NA

  return df    


def add_unique_id(
    df: pd.DataFrame, 
    id_column: str = "respondent_id"
) -> pd.DataFrame:
  """
  Adds a unique sequential identifier to each row.

  Generates a simple integer ID (1, 2, 3, ...) for each row in the DataFrame.

  Args:
    df: Input DataFrame to enrich
    id_column: Name of the new ID column (default: "respondent_id")
  
  Returns:
    DataFrame with new unique ID column added.
  """
  df = df.copy()

  # Generate sequential IDs starting from 1
  df[id_column] = range(1, len(df) + 1)
  
  return df
