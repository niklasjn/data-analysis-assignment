"""
Task 2.1.1: Learning Outcome Visualization.

This package contains the analysis and visualization code for student
learning outcome data from the Studentbarometeret survey.

Usage:
    python -m src.tasks.task_2_1_1.learning_outcome_visuals
"""

from .learning_outcome_visuals import visualize_learning_outcome

__all__ = ["visualize_learning_outcome"]
__version__ = "0.1.0"