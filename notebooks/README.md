# Analysis notebooks

These notebooks are part of the original analytical workflow and are intentionally kept in the repository.

| Notebook | Purpose |
|---|---|
| `01_Data_cleaning.ipynb` | Cleaning and preparing the project datasets. |
| `03_EDA.ipynb` | Exploratory analysis, distributions, team/player comparisons and tournament insights. |
| `03_Feature_Engineering.ipynb` | Derived match, team and player metrics used by the dashboard. |

The notebook filenames are preserved from the original project so the analytical history remains traceable. The dashboard consumes the resulting `data/processed/*.csv` tables and enriches them with raw event, venue and referee data.
