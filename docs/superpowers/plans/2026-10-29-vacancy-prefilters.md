# Vacancy Prefilters Implementation Plan

> **For agentic workers:** Use superpowers:executing-plans for inline execution.

**Goal:** Reduce unnecessary LLM requests using optional conservative salary filtering and configurable company exclusions.

**Architecture:** Parse only clearly monthly ruble ranges from the vacancy page; uncertain data passes. Apply the existing rejection transition before AI. Preserve profile fields through the setup wizard.

**Tech Stack:** Python, Playwright, PyYAML, pytest.

1. Add failing tests for salary boundary, ambiguity, missing currency and period; implement conservative parser in `vacancy_filter.py`.
2. Add tests for reading optional salary and integrating the filter before LLM; implement `VacancyDetails`, profile config validation and `process_vacancy` changes.
3. Add tests for company exclusions and salary setting round trips through `setup_wizard.py`; implement wizard inputs and field preservation.
4. Document configuration, run focused and full tests, inspect diff; do not access live HH or send applications.

**Review focus:** Salary lower-only and currencies; gross versus net; month versus hour; missing salary selector; profile values surviving edits; unknown vacancy HTML; excluded company before LLM.
