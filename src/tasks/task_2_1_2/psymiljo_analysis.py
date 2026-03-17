"""
Main analysis script for Task 2.1.2: Psychological learning environment.

The script orchestrates the analysis of student-reported psychological learning
environment scores (indeks_psymiljo_15) across different study sites and fields of study.

The workflow includes:
1. Loading survey data from Excel.
2. Filtering sites based on minimum response thresholds to ensure statistical validity.
3. Identifying the top N study sites and their top N fields of study.
4. Generating a grouped bar chart with value labels, custom styling, and a descriptive title.
5. Saving the figure to the 'figures' directory and printing a summary table to the console.

Usage:
    python -m src.tasks.task_2_1_2.psymiljo_analysis
"""


import pandas as pd
import matplotlib.pyplot as plt
from .config import (
  DATA_PATH, PSY_COL, FAFGFELT_COL, STUDIESTED_COL, MIN_SITE_RESPONSE_THRESH,
  NUM_TOP_SITES, NUM_TOP_FIELDS, PLOT_FIGSIZE, BAR_WIDTH, BAR_EDGE_COLOR,
  BAR_LABEL_X_ADJUST, BAR_LABEL_Y_ADJUST, LEGEND_NUM_COLS,
  LEGEND_BBOX_TO_ANCHOR, LEGEND_LOC, FONT_SIZE_HEADER, FONT_SIZE_LABEL, FONT_SIZE_SUBHEADER,
  TITLE_FONT_WEIGHT, GRID_ALPHA, GRID_LINESTYLE, BOTTOM_LEGEND_RECT, SCRIPT_DIR,
  SAVED_FIGURE_TYPE, SAVED_FIGURE_DPI
)


def print_checkup_table(df_valid: pd.DataFrame) -> None:
    """
    Prints a hierarchical summary of learning environment scores to the console.

    Displays the overall mean score for each of the top study sites, followed by
    the mean scores of the top fields of study within each site. This provides
    a quick textual overview of the data distribution.

    Args:
        df_valid: A DataFrame containing the filtered survey data with valid
                  study sites (meeting the minimum response threshold).

    Returns:
        None: Prints the summary directly to stdout.
    """    
    # Get the top N sites by response count
    top_sites = df_valid[STUDIESTED_COL].value_counts().head(NUM_TOP_SITES).index

    for site in top_sites:
        # Calculate overall mean for the current site
        site_mean = df_valid[df_valid[STUDIESTED_COL] == site][PSY_COL].mean()
        print(f"\n{site} (Samlet gjennomsnitt: {site_mean:.2f})")

        # Filter data for the current site
        site_data = df_valid[df_valid[STUDIESTED_COL] == site]

        # Calculate mean for each field and sort descending
        field_stats = site_data.groupby(FAFGFELT_COL)[PSY_COL].mean().sort_values(ascending=False).head(NUM_TOP_FIELDS)

        # Print top fields
        for field, mean in field_stats.items():
            print(f"  - {field}: {mean:.2f}")


def run_psymiljo_analysis() -> None:
  """
  Executes the full psychological learning environment analysis pipeline.

  Performs the following steps:
  1. Loads the raw survey data from Excel.
  2. Filters out study sites with insufficient responses (< MIN_SITE_RESPONSE_THRESH).
  3. Identifies the top NUM_TOP_SITES sites by response count.
  4. For each top site, identifies the top NUM_TOP_FIELDS fields by mean score.
  5. Constructs a grouped bar chart visualizing these scores.
  6. Adds value labels, custom styling, and a descriptive title.
  7. Saves the figure to the 'figures' directory.
  8. Displays the plot and prints a summary table to the console.

  Returns:
    None: The function produces side effects (saving a file, printing to console,
          displaying a plot) but does not return a value.
   """  
  
  # 1. Load Data
  df = pd.read_excel(DATA_PATH / "programfil_SB2025_portal.xlsx")
  
  # 2. Filter to sites with enough responses (avoid noise)
  site_counts = df.groupby(STUDIESTED_COL).size()
  valid_sites = site_counts[site_counts >= MIN_SITE_RESPONSE_THRESH].index
  df_valid = df[df[STUDIESTED_COL].isin(valid_sites)]

  # 3. get top NUM_TOP_SITES sites by response count
  top_sites = df_valid[STUDIESTED_COL].value_counts().head(NUM_TOP_SITES).index

  # 4. for each site, get top NUM_TOP_FIELDS fields
  results = []
  for site in top_sites:
      site_data = df_valid[df_valid[STUDIESTED_COL] == site]
      field_stats = site_data.groupby(FAFGFELT_COL)[PSY_COL].mean().sort_values(ascending=False).head(NUM_TOP_FIELDS)
      for field, mean in field_stats.items():
          results.append({'Studiested': site, 'Fagfelt': field, 'Mean': mean})

  df_plot = pd.DataFrame(results)

  # 5. create the grouped bar chart
  fig, ax = plt.subplots(figsize=PLOT_FIGSIZE)

  # pivot for plotting: Index=Site, Columns=Field, Values=Mean
  pivot = df_plot.pivot(index=STUDIESTED_COL.capitalize(), columns=FAFGFELT_COL.capitalize(), values='Mean')

  # Plot the bars
  bars = pivot.plot(kind='bar', ax=ax, width=BAR_WIDTH, edgecolor=BAR_EDGE_COLOR)

  # 6. manually add labels only for bars with actual values
  for container in ax.containers:
      for i, rect in enumerate(container):
          height = rect.get_height()
          if height > 0:
              # Calculate position: Center of bar X, slightly above  bar Y
              x_pos = rect.get_x() + rect.get_width() / 2 + BAR_LABEL_X_ADJUST
              y_pos = height + BAR_LABEL_Y_ADJUST
              
              ax.text(
                  x_pos,
                  y_pos,
                  f'{height:.2f}',
                  ha="center",
                  va="bottom", 
                  fontsize=FONT_SIZE_LABEL,
                  rotation=90,
                  rotation_mode="anchor"
              )


  # 7. move legend to bottom
  ax.legend(title=FAFGFELT_COL.capitalize(), bbox_to_anchor=LEGEND_BBOX_TO_ANCHOR, loc=LEGEND_LOC, ncol=LEGEND_NUM_COLS)

  # 8. styling
  ax.set_xlabel("Studiested", fontsize=FONT_SIZE_SUBHEADER)
  ax.set_ylabel("Gjennomsnittsscore Skala 1 (Ikke tilfreds) - 5 (Svært tilfreds)", fontsize=FONT_SIZE_SUBHEADER)
  # Construct dynamic title
  title_text = (
      f"Studenters selvrapporterte læringsmiljø. \nTopp {NUM_TOP_SITES} studiesteder med høyest snittscore, " 
      f" og deres topp {NUM_TOP_FIELDS} fagfelt med høyest snittscore per studiested."
  )
  
  ax.set_title(title_text, fontsize=FONT_SIZE_HEADER, fontweight=TITLE_FONT_WEIGHT)
  ax.set_ylim(0, 5) # From score range, OK
  ax.grid(axis='y', linestyle=GRID_LINESTYLE, alpha=GRID_ALPHA)
  plt.xticks(rotation=45, ha='right')

  # Aajust layout for bottom legend
  plt.tight_layout(rect=BOTTOM_LEGEND_RECT)
  
  # 9. Save and show the figure
  figures_dir = SCRIPT_DIR / "figures"
  figures_dir.mkdir(exist_ok=True)
  plt.savefig(figures_dir / f"psymiljo.{SAVED_FIGURE_TYPE}", dpi=SAVED_FIGURE_DPI)
  plt.show()

  # Optional: Print summary in terminal
  print_checkup_table(df_valid)

if __name__ == "__main__":
    run_psymiljo_analysis()