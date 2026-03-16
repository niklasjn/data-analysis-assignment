import pandas as pd
import logging
from .config import EMAIL_COL, PERSON_DUPLICATE_FIELDS, FIRST_NAME_COL, LAST_NAME_COL, DOB_COL

def handle_duplicate_emails(df: pd.DataFrame):
  """
  Identifies duplicate emails, removes all instances from the main DF,
  and returns them in a separate DF for manual inspection.

  Returns:
    cleaned_df: DF with unique emails
    inspection_df: DF containing all rows with duplicate emails
  """
  # Identify all rows involved in duplicates
  duplicate_mask = df.duplicated(subset=[EMAIL_COL], keep=False)
  # Split the data
  inspection_df = df[duplicate_mask].copy()
  cleaned_df = df[~duplicate_mask].copy()
  # Add Metadata to the inspection file
  inspection_df["removal_reason"] = "Duplicate email detected"
  inspection_df["original_index"] = df.index[duplicate_mask]
  # Log action
  n_duplicates = len(inspection_df)
  if n_duplicates > 0:
    logging.warning(f"Found {n_duplicates} rows with duplicate emails. Moved to inspection file")
  else:
    logging.info("No duplicate emails found")
  return cleaned_df, inspection_df

def handle_name_dob_duplicates(df: pd.DataFrame):
  """
  Identifies potential duplicates based on name and DOB.
  Moves all instances of a duplicate group to an inspection file.
  """
  # Prepare check dataframe
  check_df = df[PERSON_DUPLICATE_FIELDS].copy()
  # Detect duplicates
  duplicate_mask = check_df.duplicated(subset=PERSON_DUPLICATE_FIELDS, keep=False)
  # Split data
  inspection_subset = df[duplicate_mask].copy()
  cleaned_df = df[~duplicate_mask].copy()
  # Enrich metadata if duplicates found
  if len(inspection_subset) > 0:
    inspection_subset["removal_reason"] = "Potential person duplicate (name + dob)"
    inspection_subset["original_index"] = df.index[duplicate_mask]
    # Create grouping key in case manual inspection requires to sort rows with same name together
    inspection_subset["duplicate_group_key"] = (
      check_df.loc[duplicate_mask, FIRST_NAME_COL].astype(str) + "_" +
      check_df.loc[duplicate_mask, LAST_NAME_COL].astype(str)  + "_" +
      check_df.loc[duplicate_mask, DOB_COL].astype(str)
      )
    logging.warning(f"Found {len(inspection_subset)} rows with potential person duplicates.")
  else:
    logging.info("No potential person duplicates found")

  return cleaned_df, inspection_subset