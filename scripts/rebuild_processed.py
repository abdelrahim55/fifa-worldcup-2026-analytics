"""Documentation helper for rebuilding dashboard inputs from the notebooks.

The analytical notebooks remain the source of truth for the processed CSVs.
This script intentionally does not modify them automatically because notebook
execution can depend on the original data paths and environment.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

if __name__ == "__main__":
    print("Project root:", ROOT)
    print("Processed datasets live in:", ROOT / "data" / "processed")
    print("Re-run notebooks/01_Data_cleaning.ipynb and notebooks/03_Feature_Engineering.ipynb to regenerate them.")
