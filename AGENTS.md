# Agents Tooling Specification

Python tooling and conventions for this repo, based on the shared
[Agents Tooling Specification](https://gist.github.com/maehr/6c48ef14f37c9f745fa1fbaa315d106b).
This is a Jekyll/CollectionBuilder static site; the only Python is the Omeka export
script `.github/workflows/process_data.py`. The subset below is what actually applies
here. Pin versions in `pyproject.toml` and commit `uv.lock`. Dev tools must not ship to
runtime.

## Dev Tooling (dev-only)

- **[uv](https://docs.astral.sh/uv/)** — deps, venvs, Python versions, lockfile.
- **[ruff](https://docs.astral.sh/ruff/)** — lint + format.
- **[ty](https://docs.astral.sh/ty/)** — static type checker; pinned exactly while beta.
- **[pytest](https://docs.pytest.org/)** / **[pytest-cov](https://pytest-cov.readthedocs.io/)** — tests + coverage.
- **[prek](https://prek.j178.dev/)** — hook manager; reads `.pre-commit-config.yaml`.
- **[commitizen](https://commitizen-tools.github.io/commitizen/)** (`cz`) — Conventional Commits + SemVer bumps.
- **[git-cliff](https://git-cliff.org/docs/)** — changelog generation (Rust binary, not a Python dep; see `cliff.toml`).

## Runtime

- **[HTTPX2](https://github.com/pydantic/httpx2)** — Pydantic-maintained HTTP client (package/import `httpx2`).
- **[pandas](https://pandas.pydata.org/docs/)** — tabular data / CSV export.

## Standards

- **[SemVer 2.0.0](https://semver.org/)** — versioning; drives `cz bump`.
- **[Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/)** — commit format; feeds `cz` and `git-cliff`.

## Coding Guidelines

- Type hints everywhere; check with `ty`.
- Prefer pure functions for core logic; test them (`tests/test_process_data.py`).
- Network I/O is best-effort: a single failed file download must not abort the whole export.
- Enforce Conventional Commits with `cz` via the `prek` `commit-msg` hook.
- Generate changelogs with `git-cliff`.

## Common commands

```bash
npm run check      # prettier + ruff check/format + ty
uv run pytest      # unit tests
uv run prek run -a # all hooks
npm run populate   # run the Omeka export (needs OMEKA_* env vars)
```

## Not used in this repo

The full spec also lists FastAPI, sqlite3, Pydantic models, pydantic-settings, Typer,
marimo, structlog, Altair, Matplotlib, DESIGN.md, and Pyodide/WASM targets. None apply to
a single-script static site — omitted deliberately. Add them only if the Python footprint
grows to need them.
