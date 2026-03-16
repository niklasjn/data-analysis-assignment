import pandas as pd
import logging
from .config import MUNCIPALITY_COL, COUNTY_FILE_COUNTY_COL, COUNTY_FILE_MUNCIPALITY_COL, INCOME_COL

def add_county_number(df: pd.DataFrame, county_df: pd.DataFrame) -> pd.DataFrame:
  """
  Adds Fylkesnr (county number) column based on Kommunenr (muncipality number) lookup.

  Args:
    df: The data to enrich
    county_df: Reference DataFrame with Kommunenr and Fylkesnr columns

  Returns:
    DataFrame with new Fylkesnr column
  """
  df = df.copy()
  if county_df is not None and MUNCIPALITY_COL in df.columns:
    # Create a mapping dictionary: Kommunenr -> Fylkesnr
    county_mapping = county_df.set_index(COUNTY_FILE_MUNCIPALITY_COL)[COUNTY_FILE_COUNTY_COL].to_dict()
    # Map the muncipality numbers to county numbers
    df["fylkesnummer"] = df[MUNCIPALITY_COL].map(county_mapping)
  return df

def add_income_level(df: pd.DataFrame) -> pd.DataFrame:
  """
  Adds characterization of income level (lav/middels/høy) based on 
  quantiles of the income distribution

  Args:
    df: The data to enrich
  
  Returns:
    DataFrame with new income level column
  """
  df = df.copy()
  if INCOME_COL not in df.columns:
    logging.warning(f"Column {INCOME_COL} missing. Skipping income enrichment")
    return df
  try:
    # Assume data is clean from validation, but handle edge cases
    df["inntektsnivå"] = pd.qcut(df[INCOME_COL], q=3, labels=["lav", "middels", "høy"], duplicates="drop")
    if df["inntektsnivå"].nunique() < 3:
      logging.warning("Income distribution lacks variance for 3 groups")
  except ValueError as e:
    logging.error(f"Cannot create income levels: {e}")
    df["inntektsnivå"] = pd.NA
  return df    

def add_unique_id(df: pd.DataFrame, id_column: str = "respondent_id") -> pd.DataFrame:
  """
  Adds a unique sequential identifier to each row

  Args:
    df: The data to enrich
    id_column: Name of the new ID column

  Returns:
    DataFrame with new unique ID column
  """
  df = df.copy()
  df[id_column] = range(1, len(df) + 1)
  return df
