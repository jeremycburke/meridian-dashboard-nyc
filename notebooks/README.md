# Notebooks

Run the notebooks in number order.
Each one reads `data/raw/`, so download the sources first:

```bash
uv run python -m meridian_dashboard_nyc.pull
```

| Notebook | What it does |
|---|---|
| `01_look_at_each_source.ipynb` | Opens each source on its own: its size, its columns, a few rows, and the column that names the lot |

## Open a notebook

- In VS Code or PyCharm, open the file and choose the project's Python (`.venv`) as the kernel.
- From a terminal, run `uv run --with jupyter jupyter lab`.

## Rules

- Read from `data/raw/`. Never write to it.
- Write each table that combines sources to `data/processed/`.
- Clear all outputs before you commit a notebook. Outputs can hold many rows of data, and the repo is public.
