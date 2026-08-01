# Contributing

Thanks for contributing to the World Cup Analytics project.

## Development setup

```bash
python -m venv .venv
# Windows
.venv\\Scripts\\activate
# macOS / Linux
source .venv/bin/activate

python -m pip install -r requirements-dev.txt
```

## Before opening a pull request

Run:

```bash
pytest -q
python -m compileall -q app.py src pages scripts tests
ruff check app.py src pages scripts tests
```

Keep the dashboard layer separated from the analytical notebooks. Changes to feature definitions should be documented in the relevant notebook and reflected in the dashboard methodology page.
