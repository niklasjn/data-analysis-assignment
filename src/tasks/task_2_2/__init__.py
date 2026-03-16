"""
Task 2.2: Respondent data cleaning pipeline.

The package orchestrates the end-to-end data cleaning workflow for respondent data,
including normalization, validation, deduplication, transformation and enrichment.

Usage:
  fron src.tasks.task_2_2 import run_cleaning_pipeline
  run_cleaning_pipeline()
"""

from .cleaning_pipeline import run_cleaning_pipeline

__all__ = ["run_cleaning_pipeline"]
__version__ = "0.1.0"