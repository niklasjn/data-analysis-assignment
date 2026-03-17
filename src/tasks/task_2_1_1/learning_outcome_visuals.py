"""
Main visualization script for task 2.1.1: Learning outcome analysis.

The script orchestrates an end-to-end basic descriptive analysis of student learning outcomes:
1. Loads variable definitions from the codebook.
2. Loads the main survey data
3. Validates and cleans the data (filters missing values, checks ranges).
4. Calculates descriptive statistics (mean, min, max, std)
5. Generates a horizontal bar chart with wrapped labels and value annotations
6. Saves the figure to the "figures" directory

The script relies on helper functions for data validation and text wrapping,
and configuration constants for styling and paths.

Usage:
  python -m src.tasks.task_2_1_1.learning_outcome_visuals
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from .config import (
  SCRIPT_DIR, DATA_PATH, VARIABLE_NAME_COL, QUESTION_TEXT_COL, LEARN_OUTCOME_PREFIX,
  EXPECTED_VARIABLES_COUNT, NUM_DECIMAL_STAT_VISUAL, PLOT_FIGSIZE, COLOR_MAP_START, 
  COLOR_MAP_END, FONT_SIZE_HEADER, GRID_ALPHA, GRID_LINESTYLE, BAR_ALPHA, 
  FONT_SIZE_LABEL, FONT_SIZE_SUBHEADER, BAR_COLOR_MAP, BAR_EDGE_COLOR,
  SAVED_FIGURE_DPI, SAVED_FIGURE_TYPE
)
from .helpers import wrap_text, get_variable_definitions, validate_learning_outcome_data


def visualize_learning_outcome() -> None:
  """
  Main function to load data, extract definitions and prepare for visualization.

  Executes the full pipeline:
    - Loads codebook definitions and creates a mapping of variable codes to question text.
    - Loads the main survey data and filters for "laerutb_" variables.
    - Validates the data (checks counts, filters 9999/missing, checks range).
    - Calculates mean, min, max and standard deviation.
    - Generates a horizontal bar chart with wrapped labels and value annotations.
    - Saves the figure as a PNG.

  Returns:
    None
  """
  # -----------------------------------------------------------------------------
  # 1. Load variable definitions
  # -----------------------------------------------------------------------------

  definitions = get_variable_definitions()

  # Create a mapping dictionary: Variable code -> Question text
  # then wrap the text to fit the plot width
  label_map = definitions.set_index(VARIABLE_NAME_COL)[QUESTION_TEXT_COL].to_dict()
  wrapped_label_map = {k: wrap_text(v) for k, v in label_map.items()}

  # -----------------------------------------------------------------------------
  # 2. Load main survey data
  # -----------------------------------------------------------------------------
  main_data = DATA_PATH / "programfil_SB2025_portal.xlsx"
  df = pd.read_excel(main_data)

  # Filter for the 10 learning outcome variables
  main_vars = [col for col in df.columns if col.startswith(LEARN_OUTCOME_PREFIX)]
  
  # Create a subset of the dataframe with only these columns
  df_subset = df[main_vars].copy()

  # -----------------------------------------------------------------------------
  # 3. Validate and clean the data
  # -----------------------------------------------------------------------------

  # This step filters out 9999 (missing) and checks for invalid values
  df_subset = validate_learning_outcome_data(df_subset)

  # -----------------------------------------------------------------------------
  # 4. Calculate statistics
  # -----------------------------------------------------------------------------

  # Agg computes mean, min, max and standard deviation for each columns
  stats = df_subset.agg(["mean", "min", "max", "std"]).round(NUM_DECIMAL_STAT_VISUAL)

  # Transpose so rows are variables and columns are statistics
  stats = stats.T

  # Sort by mean score (ascending) for the bar chart
  stats = stats.sort_values(by="mean")

  # Replace index (variable codes) with the wrapped question text
  stats.index = stats.index.map(wrapped_label_map)

  # -----------------------------------------------------------------------------
  # 5. Create the plot
  # -----------------------------------------------------------------------------

  fig, ax = plt.subplots(figsize=PLOT_FIGSIZE)

  # Extract the mean values for the bars
  means = stats["mean"]

  # Generate a gradient of colors from the bar colormap
  cmap = plt.get_cmap(BAR_COLOR_MAP)
  colors = cmap(np.linspace(COLOR_MAP_START, COLOR_MAP_END, len(means)))

  # Create the horizontal bar chart
  bars = ax.barh(means.index, means, color=colors, edgecolor=BAR_EDGE_COLOR, alpha=BAR_ALPHA)

  # Add value labels to the end of each bar
  for i, (idx, mean_val) in enumerate(means.items()):
    # Place the text slightly to the right of the bar end
    ax.text(mean_val + 0.05, i, f"{mean_val:.2f}", va="center", fontsize=FONT_SIZE_LABEL, fontweight="bold")
  
  # Set labels and title
  ax.set_xlabel("Gjennomsnittsscore. Skala 1 (Ikke tilfreds) - 5 (Svært tilfreds)", fontsize=FONT_SIZE_SUBHEADER)
  ax.set_ylabel("Tilfredshet med eget læringsutbytte, når det gjelder:", fontsize=FONT_SIZE_SUBHEADER)
  ax.set_title("Studenters selvrapporterte læringsutbytte", fontsize=FONT_SIZE_HEADER, fontweight="bold")

  # Add grid for readability
  ax.grid(axis="x", linestyle=GRID_LINESTYLE, alpha=GRID_ALPHA)

  # Adjust layout to prevent label cutoff
  plt.tight_layout()

  # -----------------------------------------------------------------------------
  # 6. Save and show the figure
  # -----------------------------------------------------------------------------

  figures_dir = SCRIPT_DIR / "figures"
  figures_dir.mkdir(exist_ok=True)
  plt.savefig(figures_dir / f"laerutb_mean_scores.{SAVED_FIGURE_TYPE}", dpi=SAVED_FIGURE_DPI)
  plt.show()

  # Optional: Print a summary table
  print("\nSummary Statistics:")
  print(stats)
  
if __name__ == "__main__":
  visualize_learning_outcome()