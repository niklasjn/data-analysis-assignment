import pandas as pd
import logging
import os
from .config import SCRIPT_DIR, PROJECT_ROOT, DATA_PATH, LOG_PATH, PROCESSED_PATH, DOB_COL, COMMENT_COL, EXPECTED_COLUMNS
from .normalization import normalize_data
from .validation import apply_validation_rules
from .deduplication import handle_duplicate_emails, handle_name_dob_duplicates
from .transformation import merge_names, standardize_columns
from .enrichment import add_county_number, add_income_level, add_unique_id

def run_cleaning_pipeline():
    # Configure logging
    logging.basicConfig(
    filename= LOG_PATH / 'processing.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
    )

    logging.info("Running cleaning pipeline")

    all_inspection_dfs = []

    # Load data
    df = pd.read_excel(DATA_PATH / "fiktiv_kontaktinformasjon.xlsx")
    df.columns = df.columns.str.strip()
    try:
        county_df = pd.read_excel(DATA_PATH / "kommune_fylke_kartverketXXX.xlsx")
    except FileNotFoundError:
        logging.warning("County reference file not found. Skipping muncipality validation")
        county_df = None

    # Normalize data
    df = normalize_data(df)

    # Validate data
    valid_mask, invalid_df = apply_validation_rules(df, county_df=county_df)
    inspection_mask = invalid_df["removal_reason"].str.contains("manual review", case=False, na=False)
    validation_inspection_df = invalid_df[inspection_mask].copy()
    removed_df = invalid_df[~inspection_mask].copy()
    if not removed_df.empty:
        removed_df.to_excel(LOG_PATH / "removed_rows.xlsx", index=False)

    if not validation_inspection_df.empty:
        validation_inspection_df["inspection_stage"] = "validation"
        all_inspection_dfs.append(validation_inspection_df)

    df = df[valid_mask]
    df = df.drop(columns=[COMMENT_COL])
    df = df.drop(columns = [col for col in df.columns if col not in EXPECTED_COLUMNS])

    # Deduplicate data
    df, email_inspection = handle_duplicate_emails(df)
    df, person_inspection = handle_name_dob_duplicates(df)
    
    if not email_inspection.empty:
        email_inspection["inspection_stage"] = "email duplicate"
        all_inspection_dfs.append(email_inspection)
    
    if not person_inspection.empty:
        person_inspection["inspection_stage"] = "person_duplicate"
        all_inspection_dfs.append(person_inspection)

    # Transform data
    df = merge_names(df)   

    # Enrich data
    df = add_county_number(df, county_df)
    df = add_income_level(df)
    df = add_unique_id(df)

    # Standardize output columns
    df = standardize_columns(df)

    # Save
    df.to_excel(PROCESSED_PATH / 'cleaned_data.xlsx', index=False)

    if all_inspection_dfs:
        final_inspection_df = pd.concat(all_inspection_dfs, ignore_index=True)
        final_inspection_df = final_inspection_df.sort_values(by=["inspection_stage", "removal_reason"])
        final_inspection_df.to_excel(LOG_PATH / "needs_manual_inspection.xlsx", index=False)
        logging.info(f"Saved {len(final_inspection_df)} rows to manual inspection file.")
    else:
        logging.info("No rows required manual inspection")

    logging.info("Cleaning pipeline complete")


if __name__ == "__main__":
    run_cleaning_pipeline()
