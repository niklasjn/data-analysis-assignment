"""
Data deduplication module for task 2.2: Cleaning pipeline.

Handles identification and isolation of duplicate records:
  - Email-based duplicates (exact matches)
  - Person-based duplicates (matching name + date of birth)

  Duplicates are moved to manual inspection/review file.
  This preserves data integrity while flagging ambiguous records for human review.

  The module runs after validation and before transformation,
  ensuring only unique records proceed to the final dataset.
"""


import pandas as pd
import logging
from typing import Tuple
from .config import (
  EMAIL_COL, PERSON_DUPLICATE_FIELDS, 
  FIRST_NAME_COL, LAST_NAME_COL, DOB_COL
)


def handle_duplicate_emails(df: pd.DataFrame):
  """
  Identifies duplicate email addresses and isolates all instances for manual review.

  Finds rows where the email address appears more than once. 
  The function moves **all** rows with instances of a duplicate email to an 
  inspection file. 

  Args:
    df: Input DataFrame to check for duplicates

    Returns:
      Tuple containing:
      - cleaned_df: DataFrame with all rows having unique emails
      - inspection_df: DataFrame containing all rows with duplicate emails,
                       including "removal_reason" and "original_index" columns.
  """
  # Identify all rows involved in duplicates (keep=False marks all occurrences)
  duplicate_mask = df.duplicated(subset=[EMAIL_COL], keep=False)

  # Split the data
  inspection_df = df[duplicate_mask].copy()
  cleaned_df = df[~duplicate_mask].copy()

  # Add metadata to the inspection file
  inspection_df["removal_reason"] = "Duplicate email detected"
  inspection_df["original_index"] = df.index[duplicate_mask]

  # Log action
  n_duplicates = len(inspection_df)
  if n_duplicates > 0:
    logging.warning(f"Found {n_duplicates} rows with duplicate emails. Moved to inspection file")
  else:
    logging.info("No duplicate emails found")

  return cleaned_df, inspection_df


def handle_name_dob_duplicates(
    df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
  """
  Identifies potential duplicates based on matching and date of birth.

  Finds rows where the combination of first name, last name and date of birth
  appears more than once. All instances are moved to an inspection file for 
  manual review to distinguish between true duplicates (data entry errors)
  and distinct individuals (e.g. happen to have exactly same name and date of birth).

  Args:
    df: Input DataFrame to check for duplicates

  Returns:
    Tuple containing:
    - cleaned_df: DataFrame with rows having unique name + DOB combinations
    - inspection_df: DataFrame containing all rows with duplicate name+DOB,
                     including "removal_reason", "original_index" and
                     "duplicate_group_key" columns.
  
  Note:
    duplicate_group_key is generated to help reviewers group related rows.
  """
  # Prepare check dataframe (ensure we are working with the correct columns)
  check_df = df[PERSON_DUPLICATE_FIELDS].copy()

  # Detect duplicates (keep=False marks all occurrences)
  duplicate_mask = check_df.duplicated(subset=PERSON_DUPLICATE_FIELDS, keep=False)

  # Split data
  inspection_subset = df[duplicate_mask].copy()
  cleaned_df = df[~duplicate_mask].copy()

  # Enrich metadata if duplicates found
  if len(inspection_subset) > 0:
    inspection_subset["removal_reason"] = "Potential person duplicate (name + dob)"
    inspection_subset["original_index"] = df.index[duplicate_mask]

    # Create grouping key for manual inspection
    # This allows reviewers to sort by this column to see all rows for a specific person
    inspection_subset["duplicate_group_key"] = (
      check_df.loc[duplicate_mask, FIRST_NAME_COL].astype(str) + "_" +
      check_df.loc[duplicate_mask, LAST_NAME_COL].astype(str)  + "_" +
      check_df.loc[duplicate_mask, DOB_COL].astype(str)
    )
    
    logging.warning(f"Found {len(inspection_subset)} rows with potential person duplicates.")
  else:
    logging.info("No potential person duplicates found")

  return cleaned_df, inspection_subset