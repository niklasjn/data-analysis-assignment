"""
Main orchestration module for the data cleaning pipeline.

Coordinates the end-to-end data processing workflow:
1. Loading raw data and reference tables
2. Normalizing formats (dates, strings)
3. Validating data quality and flagging issues
4. Detecting duplicates for manual review
5. Transforming data structure (merging names, formatting)
6. Enriching with external data (county numbers, income levels)
7. Finalization with standardizing output schema and saving results

The module manages the flow of the data between the stages, accumulates
inspection records for manual review and handles logging.

Usage:
    python cleaning_pipeline.py
"""


import pandas as pd
import logging
from .config import DATA_PATH, LOG_PATH, PROCESSED_PATH, COMMENT_COL, EXPECTED_COLUMNS
from .normalization import normalize_data
from .validation import apply_validation_rules
from .deduplication import handle_duplicate_emails, handle_name_dob_duplicates
from .transformation import merge_names, standardize_columns
from .enrichment import add_county_number, add_income_level, add_unique_id


def run_cleaning_pipeline():
    """
    Executes the full data cleaning and enrichment pipeline.

    Orchestrates the following steps:
    1. Initialization: Configures logging and loads raw data and reference data.
    2. Normalization: Standardizes date formats and string cases.
    3. Validation: Checks data integrity (regex, ranges, referential integrity).
    4. Deduplication: Identifies duplicate emails and name+DOB combinations.
    5. Transformation: Merges names and standardizes column schema.
    6. Enrichment: Adds county numbers, income levels and unique IDs.
    7. Finalization: Saves cleaned data and consolidates inspection records.

    Outputs:
        - cleaned_data.xlsx: Final processed dataset.
        - needs_manual_inspection.xlsx: Rows flagged for human review
        - removed_rows.xlsx: Rows deleted due to failing checks
        - processing.log: Execution log
    
    Note:
        The pipeline assumes the raw data files exist in DATA_PATH.
        If the county reference file is missing, municipality validation
        skips the referential integrity check but still validates numeric format.
    """

    # -----------------------------------------------------------------------------
    # 1. Initialize logging and load data
    # -----------------------------------------------------------------------------
    # Configure logging
    logging.basicConfig(
    filename= LOG_PATH / 'processing.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
    )
    logging.info("Starting cleaning pipeline")
    
    # Initialize accumulator for rows requiring manual review/inspection
    all_inspection_dfs = []

    # Load raw data
    logging.info("Loading raw data")
    df = pd.read_excel(DATA_PATH / "fiktiv_kontaktinformasjon.xlsx")
    df.columns = df.columns.str.strip()

    # Load reference table for municipality validation (optional)
    try:
        county_df = pd.read_excel(DATA_PATH / "kommune_fylke_kartverketXXX.xlsx")
        logging.info("County reference table loaded successfully")
    except FileNotFoundError:
        logging.warning("County reference file not found. Skipping municipality validation.")
        county_df = None

    # -----------------------------------------------------------------------------
    # 2. Normalize data
    # -----------------------------------------------------------------------------
    logging.info("Normalizing data formats")
    df = normalize_data(df)

    # -----------------------------------------------------------------------------
    # 3. Validate data
    # -----------------------------------------------------------------------------
    logging.info("Validating data quality")
    valid_mask, invalid_df = apply_validation_rules(df, county_df=county_df)

    # Split invalid rows: those for manual review vs those to be removed
    inspection_mask = invalid_df["removal_reason"].str.contains("manual review", case=False, na=False)
    validation_inspection_df = invalid_df[inspection_mask].copy()
    removed_df = invalid_df[~inspection_mask].copy()

    # Save removed rows (errors)
    if not removed_df.empty:
        logging.warning(f"Removing {len(removed_df)} rows due to validation errors.")
        removed_df.to_excel(LOG_PATH / "removed_rows.xlsx", index=False)

    # Add validation inspection rows to accumulator
    if not validation_inspection_df.empty:
        validation_inspection_df["inspection_stage"] = "validation"
        all_inspection_dfs.append(validation_inspection_df)

    # Filter to keep only valid rows
    df = df[valid_mask]

    # Drop columns that are no longer needed (comments, unexpected columns)
    # This cleans the dataframe before further processing
    if COMMENT_COL in df.columns:
        df = df.drop(columns=[COMMENT_COL])
    
    # Drop unexpected columns that might have slipped through
    unexpected_cols = [col for col in df.columns if col not in EXPECTED_COLUMNS]
    if unexpected_cols:
        df = df.drop(columns=unexpected_cols)
        logging.info(f"Dropped {len(unexpected_cols)} unexpected columns")

    # -----------------------------------------------------------------------------
    # 4. Deduplicate data
    # -----------------------------------------------------------------------------
    logging.info("Checking for duplicates")
    df, email_inspection = handle_duplicate_emails(df)
    df, person_inspection = handle_name_dob_duplicates(df)
    
    # Add deduplication inspection rows to accumulator
    if not email_inspection.empty:
        email_inspection["inspection_stage"] = "email duplicate"
        all_inspection_dfs.append(email_inspection)
    
    if not person_inspection.empty:
        person_inspection["inspection_stage"] = "person_duplicate"
        all_inspection_dfs.append(person_inspection)

    # -----------------------------------------------------------------------------
    # 5. Transform data
    # -----------------------------------------------------------------------------
    logging.info("Transforming data structure")
    df = merge_names(df)   

    # -----------------------------------------------------------------------------
    # 6. Enrich data
    # -----------------------------------------------------------------------------
    logging.info("Enriching data with external information")
    df = add_county_number(df, county_df)
    df = add_income_level(df)
    df = add_unique_id(df)


    # -----------------------------------------------------------------------------
    # 7. Finalize/standardize output and save
    # -----------------------------------------------------------------------------
    logging.info("Standardizing output schema")
    df = standardize_columns(df)

    # Save final cleaned dataset
    df.to_excel(PROCESSED_PATH / 'cleaned_data.xlsx', index=False)
    logging.info(f"Saved cleaned dataset with {len(df)} rows")

    # Consolidate and save all inspection records
    if all_inspection_dfs:
        final_inspection_df = pd.concat(all_inspection_dfs, ignore_index=True)
        # Sort by stage and reason for easier review
        final_inspection_df = final_inspection_df.sort_values(
            by=["inspection_stage", "removal_reason"]
        )
        final_inspection_df.to_excel(LOG_PATH / "needs_manual_inspection.xlsx", index=False)
        logging.info(f"Saved {len(final_inspection_df)} rows to manual inspection file.")
    else:
        logging.info("No rows required manual inspection")

    logging.info("Cleaning pipeline complete")


if __name__ == "__main__":
    run_cleaning_pipeline()
