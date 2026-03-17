"""
Configuration module for Task 2.1.2: Learning environment analysis.

The module centralizes all configuration constants used in the psychological
learning environment analysis pipeline, including:
- File paths for data and output
- Column names for the survey dataset
- Visualization styling parameters (figure size, fonts, colors, layout)
- Validation thresholds (minimum responses, top N selection)

All constants are defined here to ensure consistency across the project and
make future updates easier (e.g., changing the number of top sites or figure size).
"""


from pathlib import Path


# -----------------------------------------------------------------------------
# File paths
# -----------------------------------------------------------------------------

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent.parent
DATA_PATH = PROJECT_ROOT / 'data' / 'raw'

# -----------------------------------------------------------------------------
# Dataset column names
# -----------------------------------------------------------------------------

# Primary variable for psychological learning environment index
PSY_COL = "indeks_psymiljo_15"

# Categorical variables for grouping
FAFGFELT_COL = "fagfelt"      # field (of study)
STUDIESTED_COL = "studiested" # site (of study)

# -----------------------------------------------------------------------------
# Validation and filtering configuration
# -----------------------------------------------------------------------------

# Minimum number of responses required for a study site to be included
# (Filters out sites with too few responses to be statistically meaningful)
MIN_SITE_RESPONSE_THRESH = 20

# Number of top study sites to display in the visualization
NUM_TOP_SITES = 8

# Number of top fields of study to display per site
NUM_TOP_FIELDS = 4

# -----------------------------------------------------------------------------
# Statistical and visualization configuration
# -----------------------------------------------------------------------------

# Decimal places for statistics and value labels in visualization
NUM_DECIMAL_STAT_VISUAL = 2 

# Figure dimensions (width, height) in inches
PLOT_FIGSIZE = (18, 14)

# Font sizes for different text elements
FONT_SIZE_HEADER = 14     # Main title
FONT_SIZE_SUBHEADER = 12  # Axis labels
FONT_SIZE_LABEL = 10      # Value labels on bars

# Bar styling
BAR_WIDTH = 0.7
BAR_EDGE_COLOR = "black"

# Label positioning adjustments (relative to bar coordinates)
BAR_LABEL_X_ADJUST = 0.02
BAR_LABEL_Y_ADJUST = 0.15

# Legend configuration
LEGEND_NUM_COLS = 4
LEGEND_BBOX_TO_ANCHOR = (0.5, -0.15)
LEGEND_LOC = "upper center"
# Rect tuple: [left, bottom, right, top] to reserve space for bottom legend
BOTTOM_LEGEND_RECT = [0, 0.15, 1, 1]

# Title styling
TITLE_FONT_WEIGHT = "bold"

# Grid styling
GRID_ALPHA = 0.3          # Transparency (0.0 = invisible, 1.0 = opaque)
GRID_LINESTYLE = "--"     # Dashed lines for grid

# -----------------------------------------------------------------------------
# Output configuration
# -----------------------------------------------------------------------------
SAVED_FIGURE_TYPE = "png"
SAVED_FIGURE_DPI = 300