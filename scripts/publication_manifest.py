#!/usr/bin/env python3
"""Build a manuscript file manifest from the chapter status register.

By default, only VERIFIED_CANON chapters are emitted. Draft inclusion requires
an explicit --include-unverified flag and is labeled as non-publication-safe.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTER = ROOT / "book_01_GhostPAT/meta/chapter_status_register.md"
MANUSCRIPT = ROOT / "book_01_GhostPAT/manuscript"
DEFAULT_OUTPUT = ROOT / "build/publication_manifest.txt"

PUBLICATION_ELIGIBLE = {"VERIFIED_CANON"}
KNOWN_STATUSES = {
    "VERIFIED_CANON",
    "CANON_DRAFT",
    "FACTUAL_REVIEW_REQUIRED",
    "COMPOSITE_REVIEW_REQUIRED",
    "NONCANONICAL_DRAFT",
    "MISSING_FROM_REPOSITORY",
    "UNRESOLVED_ORDER",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--register", type=Path, default=REGISTER)
    parser.add_argument("--manuscript", type=Path, default=MANUSCRIPT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--include-unverified",
        action="store_true",
        help="Include all discovered chapters. Output is draft-only and not publication-safe.",
    )
    return parser.parse_args()


def parse_statuses(path: Path) -> dict[str, str]:
    if not path.is_file():
        raise FileNotFoundError(f"status register not found: {path}")

    statuses: dict[str, str] = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line.startswith("|") or line.startswith("|---"):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) != 4 or cells[0] == "Chapter":
            continue
        chapter, _title, status, _action = cells
        if re.fullmatch(r"\d{2}", chapter) and status in KNOWN_STATUSES:
            statuses[chapter] = status
    if not statuses:
        raise ValueError("no chapter statuses were parsed")
    return statuses


def chapter_number(path: Path) -> str | None:
    match = re.match(r"ch(\d{2})_", path.name, flags=re.IGNORECASE)
    return match.group(1) if match else None


def main() -> int:
    args = parse_args()
    try:
        statuses = parse_statuses(args.register)
        if not args.manuscript.is_dir():
            raise FileNotFoundError(f"manuscript directory not found: {args.manuscript}")

        selected: list[Path] = []
        excluded: list[tuple[Path, str]] = []
        for path in sorted(args.manuscript.glob("ch*.md")):
            number = chapter_number(path)
            if number is None:
                continue
            status = statuses.get(number, "UNREGISTERED")
            if args.include_unverified or status in PUBLICATION_ELIGIBLE:
                selected.append(path)
            else:
                excluded.append((path, status))

        if not selected:
            mode = "draft" if args.include_unverified else "publication-safe"
            raise ValueError(f"no chapters selected for {mode} build")

        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            "\n".join(path.relative_to(ROOT).as_posix() for path in selected) + "\n",
            encoding="utf-8",
        )

        print(f"Selected {len(selected)} chapter(s):")
        for path in selected:
            number = chapter_number(path)
            print(f"  {path.relative_to(ROOT)} [{statuses.get(number or '', 'UNREGISTERED')}]")

        if excluded:
            print("Excluded chapters:")
            for path, status in excluded:
                print(f"  {path.relative_to(ROOT)} [{status}]")

        if args.include_unverified:
            print("WARNING: draft mode includes chapters that are not publication eligible.")
        return 0
    except (FileNotFoundError, ValueError) as exc:
        print(f"publication manifest error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
