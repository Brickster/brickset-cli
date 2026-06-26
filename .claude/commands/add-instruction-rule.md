Add a new instruction filename rule to `brickset/instructions.py`.

The user will provide one or more examples of LEGO instruction descriptions that currently produce `None` from `_construct_instruction_filename` (i.e. they print a WARN and get skipped). Your job is to:

1. **Identify the pattern** — study the provided description(s) alongside the existing `@_rule` handlers in `brickset/instructions.py` to determine whether this is a variant of an existing rule (extend the regex) or a genuinely new rule (add a new handler).

2. **Write or update the rule** in `brickset/instructions.py`:
   - Use the `@_rule(regex, flags=0)` decorator
   - Follow the existing handler signature: `(set_number: str, pdf_number: str | None, match: re.Match[str], description: str) -> str`
   - Place the new rule in order of specificity — more specific patterns before more general ones
   - Use `_clean_region` for any region code (e.g. `V39`, `IN`, `NA`)
   - The filename format follows the pattern of sibling rules: `{set_number}_{region}_{pdf_number}.pdf`, `{set_number}_{region}_b{book}_{pdf_number}.pdf`, etc.

3. **Add parameterized test cases** to `tests/test_instructions.py`:
   - Find the right `@parameterized.expand` block for the rule type (e.g. `test_regionOnly`, `test_regionBook`, etc.), or add a new `@parameterized.expand` block if the rule is genuinely new
   - Each tuple is `(description_string, expected_filename)` for the default `set_number='1234-1'` and `cdn_filename='5678.pdf'` — use the 3-tuple `(name, description, expected)` form only when you need a non-default set_number or cdn_filename (see `test_buildAlt` and `test_inspirationalMaterial` for examples)
   - Cover edge cases the user provided plus any obvious variations you can infer

4. **Run the tests** and confirm they pass:
   ```
   pytest tests/test_instructions.py -x
   ```
   Fix any failures before reporting done.

5. **Report** what rule was added/modified, the regex used, and the test cases added. Suggest a conventional commit message (max 72 chars, `fix(instructions):` or `feat(instructions):` prefix).

Key context:
- `pdf_number` comes from `_parse_pdf_number(url)` — it's the numeric portion of the PDF filename (e.g. `'5678'` for `.../5678.pdf`)
- `_clean_region` strips whitespace/dots, normalises slashes to `_V`, lowercases — e.g. `'V29/39'` → `'v29_v39'`
- The `{No longer listed at LEGO.com}` case is handled before the rule loop — don't touch it
- CLAUDE.md warns: do not simplify the existing regexes without running the full test suite