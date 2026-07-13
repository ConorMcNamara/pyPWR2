"""Keep the minimum-Python knobs in sync with the lowest trove classifier.

The ``Programming Language :: Python :: 3.X`` classifiers in ``pyproject.toml``
are the single source of truth for the Python versions this project supports
(see ``.github/workflows/ci.yml``). The *lowest* of those classifiers implies
three other settings that must agree with it:

* ``project.requires-python`` floor (``>=3.X``)
* ``[tool.zuban] python_version`` (``3.X``)
* ``[tool.ruff] target-version`` (``py3X``)

This script asserts they stay in sync. Run with ``--fix`` to rewrite the values
in place (targeted line edits that preserve the rest of the file's formatting).
"""

from __future__ import annotations

import re
import sys
import tomllib
from pathlib import Path

PYPROJECT = Path(__file__).resolve().parent.parent / "pyproject.toml"

CLASSIFIER_RE = re.compile(r"Programming Language :: Python :: (\d+\.\d+)$")


def lowest_version(data: dict) -> tuple[int, int]:
    """Return the lowest ``(major, minor)`` from the Python trove classifiers."""
    classifiers = data["project"].get("classifiers", [])
    versions = sorted(
        {tuple(int(p) for p in m.group(1).split(".")) for c in classifiers if (m := CLASSIFIER_RE.match(c))}
    )
    if not versions:
        sys.exit("No 'Programming Language :: Python :: X.Y' classifiers found in pyproject.toml")
    return versions[0]


def expected(major: int, minor: int) -> dict[str, str]:
    """Return the expected value for each derived knob given the lowest version."""
    return {
        "requires-python": f">={major}.{minor}",
        "python_version": f"{major}.{minor}",
        "target-version": f"py{major}{minor}",
    }


# Each knob: how to read its current value, and how to rewrite its line for --fix.
CHECKS = {
    "requires-python": {
        "read": lambda d: re.search(r">=\s*(\d+\.\d+)", d["project"]["requires-python"]).group(1),
        "compare": lambda cur, exp: f">={cur}" == exp,
        "line_re": re.compile(r'^(requires-python\s*=\s*")([^"]*)(")', re.M),
        "replace": lambda exp: exp,  # full new inner string, e.g. ">=3.13"
    },
    "python_version": {
        "read": lambda d: d["tool"]["zuban"]["python_version"],
        "compare": lambda cur, exp: cur == exp,
        "line_re": re.compile(r'^(python_version\s*=\s*")([^"]*)(")', re.M),
        "replace": lambda exp: exp,
    },
    "target-version": {
        "read": lambda d: d["tool"]["ruff"]["target-version"],
        "compare": lambda cur, exp: cur == exp,
        "line_re": re.compile(r'^(target-version\s*=\s*")([^"]*)(")', re.M),
        "replace": lambda exp: exp,
    },
}


def main(argv: list[str]) -> int:
    """Assert (or ``--fix``) that the min-Python knobs match the lowest classifier."""
    fix = "--fix" in argv

    data = tomllib.loads(PYPROJECT.read_text(encoding="utf-8"))
    major, minor = lowest_version(data)
    exp = expected(major, minor)

    problems: list[str] = []
    text = PYPROJECT.read_text(encoding="utf-8")

    for key, spec in CHECKS.items():
        current = spec["read"](data)
        want = exp[key]
        if spec["compare"](current, want):
            continue
        if fix:
            new_inner = spec["replace"](want)
            text, n = spec["line_re"].subn(rf"\g<1>{new_inner}\g<3>", text)
            if n != 1:
                problems.append(f"{key}: could not locate a unique line to fix")
            else:
                print(f"fixed {key}: {current!r} -> {new_inner!r}")
        else:
            problems.append(f"{key} is {current!r} but the lowest classifier is {major}.{minor} (expected {want!r})")

    if fix:
        PYPROJECT.write_text(text, encoding="utf-8")
        return 0

    if problems:
        print("pyproject.toml min-Python knobs are out of sync with the lowest classifier:")
        for p in problems:
            print(f"  - {p}")
        print("\nRun `python scripts/check_python_versions.py --fix` to update them.")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
