"""
Helper functions for task 2.1.1: Learning outcome visualization.

The module contains utility functions used across the learning outcome analysis:
  - Data validation (checking variable counts, filtering missing values)
  - Text formatting (wrapping long labels for plots)
  - Codebook parsing (extracting variable definitions/labels)
"""

import pandas as pd
import numpy as np
from .config import (
  DATA_PATH, CODEBOOK_START_HEADER_ROW, VARIABLE_NAME_COL,
  QUESTION_TEXT_COL, LEARN_OUTCOME_PREFIX, EXPECTED_VARIABLES_COUNT,
  WRAP_TEXT_MAX_WIDTH
)


def validate_learning_outcome_data(
  df_subset: pd.DataFrame, 
  expected_count: int = EXPECTED_VARIABLES_COUNT
  ) -> pd.DataFrame:
  """
  Validates and cleans learning outcome data.

  Performs the following checks:
  1. Verifies the number of columns matches the expected count.
  2. Filters out missing values coded as 9999
  3. Checks for unexpected values outside the valid range (1-5)

  Args:
    df_subset: DataFrame containing only the "laerutb_" variables
    expected_count: Expected number of variables (default from config).

  Returns:
    Cleaned DataFrame with "9999" values replaced by NaN and rows with invalid values removed.
  """
  # Check variable count
  if len(df_subset.columns) != expected_count:
    print(f"Warning: Found {len(df_subset.columns)} variables, expected {expected_count}")

  # Count "9999" values before filtering
  missing_count = (df_subset == 9999).sum().sum()

  # Filter out 9999 (missing values)
  # Replace 9999 with NaN, then drop rows with any NaN
  df_clean = df_subset.replace(9999, np.nan).dropna()

  # Check for unexpected values
  valid_range = [1, 2, 3, 4, 5]
  valid_mask = df_clean.isin(valid_range)
  unexpected = df_clean[~valid_mask].dropna()

  # Report findings
  if missing_count > 0:
    print(f"Info: Filtered out {missing_count} missing values (coded as 9999).")

  if not unexpected.empty:
    print(f"Warning: Found {len(unexpected)} unexpected values outside 1-5 range")

  return df_clean

  
def wrap_text(text: str, width: int = WRAP_TEXT_MAX_WIDTH) -> str:
  """
  Wraps text to a specified character width for better readability in plots.

  Splits long strings into multiple lines at word boundaries to prevent labels from
  being cut off or overlapping in visualization.

  Args:
    text: The input string to wrap.
    width: Maximum characters per line (default from config).

  Returns:
    The text with newline characters inserted at appropriate word breaks
  """
  words = text.split()
  lines = []
  current_line = []

  for word in words:
    # Check if adding the next word exceeds the width
    if len(" ".join(current_line + [word])) <= width:
      current_line.append(word)
    else:
      # Push current line to list and start a new one
      lines.append(" ".join(current_line))
      current_line = [word]
  
  # Add the last line if it exists
  if current_line:
    lines.append(" ".join(current_line))
  
  return "\n".join(lines)


def get_variable_definitions() -> pd.DataFrame:
  """
  Loads the codebook and extracts definitions for "laerutb_" variables.

  Reads the Excel codebook, skips the initial header section, and filters 
  for variables starting with the learning outcome prefix.

  Returns:
    DataFrame with columns "Variabelnavn 2025" and "Spørsmålstekst"
    containing the relevant variable definitions.

  Raises:
    FileNotFoundError: If the codebook file is not found at the configured path.
    ValueError: If the codebook is missing expected columns.
  """
  codebook_path = DATA_PATH / "Kodebok_SB2025_portal.xlsx"

  if not codebook_path.exists():
    raise FileNotFoundError(f"Codebook not found at {codebook_path}. Please check the path.")
  
  # Skip the first 44 rows (0 - 43), so row 44 becomes the header
  df_codebook = pd.read_excel(codebook_path, skiprows=CODEBOOK_START_HEADER_ROW)

  # Validate expected columns exist
  required_cols = [VARIABLE_NAME_COL, QUESTION_TEXT_COL]
  missing_cols = [col for col in required_cols if col not in df_codebook.columns]
  if missing_cols:
    raise ValueError(f"Codebook missing expected columns: {missing_cols}")

  # Filter for variables starting with "Laerutb_"
  mask = df_codebook[VARIABLE_NAME_COL].str.startswith(LEARN_OUTCOME_PREFIX, na=False)

  # Select only the relevant columns
  definitions_df = df_codebook[mask][[VARIABLE_NAME_COL, QUESTION_TEXT_COL]].reset_index(drop=True)

  return definitions_df