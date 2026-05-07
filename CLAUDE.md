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
  - `api.py` — HTTP layer: `execute_api_request` (all API calls)
  - `cache.py` — manages `~/.brickset/cache` (setID ↔ set number mapping); `get_cache`, `update_cache`, `id_to_set_number_generator`, `set_number_to_id_generator`
  - `config.py` — manages `~/.brickset/config` (API key + user hash); `get_config`, `configure`
  - `instructions.py` — instruction PDF download logic: `get_instructions`, `download_instruction`, `_construct_instruction_filename` (regex-based filename builder)
  - `sets.py` — set query logic: `get_sets` (takes a `SetFilters` dataclass), `update_set`, `get_themes`, `get_subthemes`, `get_years`
  - `minifigs.py` — minifig query logic
  - `user.py` — `show_usage`, `log_in`
- `bin/brickset` — CLI entry point (argparse); adds the project root to `sys.path` so `brickset` is importable as a package, then delegates everything to `brickset/`

## Workflow

After implementing a plan, suggest a commit message following [Conventional Commits](https://www.conventionalcommits.org/) format, max 72 characters.

## Key details

**Instruction filename construction** (`instructions._construct_instruction_filename`) is complex — it parses LEGO's free-text instruction descriptions using a series of `@_rule`-decorated handlers to extract region codes (e.g. `V39`) and book numbers. There are 130+ parameterized test cases covering this. Do not simplify the regexes without running the full test suite.

**`sys.exit` pattern** — validation functions (`_is_iso8601_date`, `_is_valid_order_by`, `_is_valid_limit`) call `sys.exit` on invalid input. Tests assert on this by catching `SystemExit` with `assertRaises` — do not mock `sys.exit`.

**Cache** — `cache.update_cache` returns the updated cache dict; callers must use the return value. `cache.get_cache` returns `{'sets': {}}` when no cache file exists.

**`SetFilters`** — `get_sets` takes a `SetFilters` dataclass (defined in `sets.py`) rather than 10 flat filter parameters. The CLI adapter in `bin/brickset` constructs it from the flat argparse dict.