# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-test.txt
```

## Commands

```bash
# Run all tests
pytest tests/

# Run a single test file
pytest tests/test_api.py

# Run a single test
pytest tests/test_api.py::TestApi::test_executeApiRequest

# Run the CLI
python bin/brickset --help
```

## Architecture

The project is a CLI wrapper around the [Brickset v3 API](https://brickset.com/article/52664/api-version-3-documentation).

- `brickset/` — main package
  - `api.py` — HTTP layer: `execute_api_request` (all API calls), `download_instruction` (PDF download), and filename construction logic for instruction PDFs
  - `config.py` — manages `~/.brickset/config` (API key + user hash) and `~/.brickset/cache` (setID ↔ set number mapping). Also contains `show_usage` and `log_in` which use the API.
  - `sets.py` — set/instruction/theme/subtheme/year query logic
  - `minifigs.py` — minifig query logic
- `bin/brickset` — CLI entry point (argparse); adds the project root to `sys.path` so `brickset` is importable as a package, then delegates everything to `brickset/`

## Key details

**Instruction filename construction** (`api._construct_instruction_filename`) is complex — it parses LEGO's free-text instruction descriptions using a series of regex patterns to extract region codes (e.g. `V39`) and book numbers. There are 130+ parameterized test cases covering this. Do not simplify the regexes without running the full test suite.

**`sys.exit` pattern** — validation functions (`_is_iso8601_date`, `_is_valid_order_by`, `_is_valid_limit`) call `sys.exit` on invalid input. Tests assert on this by catching `SystemExit` with `assertRaises` — do not mock `sys.exit`.

**Cache** — `config.update_cache` returns the updated cache dict; callers must use the return value. `config.get_cache` returns `{'sets': {}}` when no cache file exists.

**Circular import** — `config.py` imports `api` (for `show_usage`/`log_in`). This is a known smell; avoid adding more cross-imports between these modules.