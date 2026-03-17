"""
Configuration module for task 2.1.1: Learning outcome visualization.

The module centralizes all configuration constants used in the learning
outcome analysis pipeline, including:
  - File paths for data and codebook
  - Column names and variable prefixes
  - Visualization styling parameters (figure size, fonts, colors)
  - Validation thresholds (expected variable count, decimal precision)
"""


from pathlib import Path


# -----------------------------------------------------------------------------
# File paths
# -----------------------------------------------------------------------------

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent.parent
DATA_PATH = PROJECT_ROOT / 'data' / 'raw'

# -----------------------------------------------------------------------------
# Codebook configuration
# -----------------------------------------------------------------------------

# Row number where the second header begins (0-indexed, i.e. row 43 = 44th row)
CODEBOOK_START_HEADER_ROW = 43

# Column names in the codebook Excel file
VARIABLE_NAME_COL = "Variabelnavn 2025"
QUESTION_TEXT_COL = "Spørsmålstekst"

# Prefix for learning outcome variables in the dataset
LEARN_OUTCOME_PREFIX = "laerutb_"

# -----------------------------------------------------------------------------
# Validation configuration
# -----------------------------------------------------------------------------

# Expected number of learning outcome variables (should match dataset)
EXPECTED_VARIABLES_COUNT = 10

# -----------------------------------------------------------------------------
# Plot styling configuration
# -----------------------------------------------------------------------------

# Decimal places for statistics and value labels in visualization
NUM_DECIMAL_STAT_VISUAL = 2 

# Figure dimensions (width, height) in inches
PLOT_FIGSIZE = (12, 8)

# Font sizes for different text elements
FONT_SIZE_HEADER = 14     # Main title
FONT_SIZE_SUBHEADER = 12  # Axis labels
FONT_SIZE_LABEL = 10      # Value labels on bars

# Text wrapping
WRAP_TEXT_MAX_WIDTH = 30  # Max characters per line for wrapped labels in plots

# Grid styling
GRID_ALPHA = 0.3          # Transparency (0.0 = invisible, 1.0 = opaque)
GRID_LINESTYLE = "--"     # Dashed lines for grid

# Color gradient range for bar chart (0.0 to 1.0 for colormap)
COLOR_MAP_START = 0.3
COLOR_MAP_END = 0.8

# Bar styling
BAR_ALPHA = 0.8               # Transparency of bar fills
BAR_COLOR_MAP = "Blues"       # Pre defined pyplot cmap
BAR_EDGE_COLOR = "black"      

# -----------------------------------------------------------------------------
# Output figure save configuration
# --------------------------------------------------------------------------

SAVED_FIGURE_DPI = 300
SAVED_FIGURE_TYPE = "png"
