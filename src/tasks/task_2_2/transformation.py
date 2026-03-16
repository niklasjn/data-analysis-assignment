import pandas as pd
import datetime as dt
from .config import FIRST_NAME_COL, LAST_NAME_COL, DOB_COL, MUNCIPALITY_COL, DATA_PATH, TARGET_COLUMNS
import logging

def merge_names(df: pd.DataFrame) -> pd.DataFrame:
  """Merge first and last name into Full_Name, drop originals"""
  df = df.copy()
  df["fullt_navn"] = (
    df[FIRST_NAME_COL].str.title() + " " + df[LAST_NAME_COL].str.title()
  )
  df = df.drop(columns=[FIRST_NAME_COL, LAST_NAME_COL])
  return df

def format_dates(df: pd.DataFrame) -> pd.DataFrame:
  """
  Converts datetime objects to a consistent string format (YYYY-MM-DD)
  """
  df = df.copy()
  if DOB_COL in df.columns:
    df[DOB_COL] = df[DOB_COL].dt.datetime.strftime("%Y-%m-%d")
  return df

def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
  """
  Standardizes column names to lowercase with underscores as separators,
  and reorders columns to a predefined schema

  Args:
    df: The data to transform
  
  Returns:
    DataFrame with standardized column names and order
  """
  df = df.copy()
  df[DOB_COL] = df[DOB_COL].dt.strftime("%Y-%m-%d")
  df = df.rename(columns=TARGET_COLUMNS)
  available_columns = [col for col in TARGET_COLUMNS.values() if col in df.columns]
  df = df[available_columns]
  return df


