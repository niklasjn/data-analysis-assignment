"""
Task 2.1.2: Psychological learning environment analysis.

The package contains the analysis and visualization code for student
psychological learning environment data from the Studentbarometeret survey.

The main script breaks down the learning environment index by study site and
field of study, producing a grouped bar chart with value labels and summary statistics.

Usage:
    from src.tasks.task_2_1_2 import run_psymiljo_analysis
    run_psymiljo_analysis()
"""

from .psymiljo_analysis import run_psymiljo_analysis

__all__ = ["run_psymiljo_analysis"]
__version__ = "0.1.0"