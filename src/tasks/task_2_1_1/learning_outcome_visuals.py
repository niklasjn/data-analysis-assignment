import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from .config import DATA_PATH, CODEBOOK_START_HEADER_ROW, VARIABLE_NAME_COL, QUESTION_TEXT_COL, LEARN_OUTCOME_PREFIX

def wrap_text(text, width=30):
  """
  Wrap text to specified character width
  """
  words = text.split()
  lines = []
  current_line = []
  for word in words:
    if len(" ".join(current_line + [word])) <= width:
      current_line.append(word)
    else:
      lines.append(" ".join(current_line))
      current_line = [word]
  
  if current_line:
    lines.append(" ".join(current_line))
  
  return "\n".join(lines)

def get_variable_definitions():
  """
  Loads the codebook and extracts definitions for "laerutb_" variables.

  Returns:
    pd.DataFrame: A DataFrame with columns "Variabelnavn 2025" and "Spørsmålstekst"
                  containing only rows where the variable name starts with "laerutb_"
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


def visualize_learning_outcome():
  """
  Main function to load data, extract definitions, and prepare for visualization
  """
  # Load definitions
  print("Loading variable definitions from codebook...")
  definitions = get_variable_definitions()

  # Create label map from definitions
  label_map = definitions.set_index(VARIABLE_NAME_COL)[QUESTION_TEXT_COL].to_dict()
  wrapped_label_map = {k: wrap_text(v) for k, v in label_map.items()}
  # Load main data
  main_data = DATA_PATH / "programfil_SB2025_portal.xlsx"
  df = pd.read_excel(main_data)

  # Filter for the 10 variables
  main_vars = [col for col in df.columns if col.startswith(LEARN_OUTCOME_PREFIX)]

  if len(main_vars) != 10:
    print(f"Warning: Found {len(main_vars)} variables starting with '{LEARN_OUTCOME_PREFIX}', expected 10.")
  
  df_subset = df[main_vars].copy()

  # Calculate statistics
  stats = df_subset.agg(["mean", "min", "max"]).round(2)

  # Transpose so rows=variables, columns=stats
  stats = stats.T

  stats = stats.sort_values(by="mean")

  # Replace index with question text
  stats.index = stats.index.map(wrapped_label_map)

  # Create the plot
  fig, ax = plt.subplots(figsize=(12, 8))

  # Create the bar chart for means
  means = stats["mean"]

  cmap = plt.get_cmap("Blues")
  colors = cmap(np.linspace(0.3, 0.8, len(means)))

  bars = ax.barh(means.index, means, color=colors, edgecolor="black", alpha=0.8)

  # Add value labels to the end of each bar
  for i, (idx, mean_val) in enumerate(means.items()):
    # Place the text slightly to the right of the bar end
    # va="center" centers the text vertically on the bar
    ax.text(mean_val + 0.05, i, f"{mean_val:.2f}", va="center", fontsize=10, fontweight="bold")
  

  
  # Labels and title
  ax.set_xlabel("Gjennomsnittsscore (skala 1 - 5)", fontsize=12)
  ax.set_ylabel("Tilfredshet med eget læringsutbytte, når det gjelder:", fontsize=12)
  ax.set_title("Studenters gjennomsnittlige selvrapporterte læringsutbytte", fontsize=14, fontweight="bold")

  # Add grid for readability
  ax.grid(axis="x", linestyle="--", alpha=0.3)

  # Rotate x-axis labels if they are too long 
  plt.tight_layout()

  # Save and show
  # plt.savefig("figures/laerutb_mean_with_range.png", dpi=300)
  plt.show()

  # Optional: Print a summary table
  print("\nSummary Statistics:")
  print(stats)
  
if __name__ == "__main__":
  visualize_learning_outcome()