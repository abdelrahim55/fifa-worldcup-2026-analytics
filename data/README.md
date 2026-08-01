# Data

The repository keeps the original raw and processed CSV layers used by the analysis notebooks and dashboard.

The `data/warehouse/` directory contains only a `.gitkeep` file in source control. The generated SQLite warehouse is intentionally ignored by Git because it is reproducible from the CSV source layer.

Build it with:

```bash
python scripts/build_sqlite_warehouse.py
```
