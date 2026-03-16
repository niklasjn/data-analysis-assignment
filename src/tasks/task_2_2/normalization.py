import pandas as pd
import datetime as dt
from .config import FIRST_NAME_COL, LAST_NAME_COL, EMAIL_COL, DOB_COL, ADDRESS_COL

def parse_date_flexible(date_value):
  """
  Attempts to parse a date string using multiple format strategies.
  Returns a datetime object or pd.NaT if all attempts fail.
  """
  if pd.isna(date_value) or date_value == "":
    return pd.NaT
  date_str = str(date_value).strip()
  formats = [
      "%Y-%m-%d",      # 1980-01-01 
      "%d.%m.%Y",      # 15.02.1985 
      "%Y/%m/%d",      # 1985/02/15
      "%Y.%m.%d",      # 1995.04.25
      "%d-%m-%Y",      # 15-02-1985
      "%m/%d/%Y",      # 02/15/1985 
      "%d/%m/%Y",      # 15/02/1985 
  ]
  # Try Python datetime parser
  for fmt in formats:
    try:
      return dt.datetime.strptime(date_str, fmt)
    except ValueError:
      continue
  #Fallback: Try pandas flexible datetime parser
  try:
    return pd.to_datetime(date_str, dayfirst=True, errors='raise')
  except:
    return pd.NaT

def normalize_data(df: pd.DataFrame) -> pd.DataFrame:
  df = df.copy()
  for col in [FIRST_NAME_COL, LAST_NAME_COL, EMAIL_COL, DOB_COL]:
    if col in df.columns:
      df[col] = df[col].astype(str).str.lower().str.strip()
  
  if DOB_COL in df.columns:
    df[DOB_COL] = df[DOB_COL].apply(parse_date_flexible)

  return df
  