#!/usr/bin/env python3
"""Advisory canon audit for FREE-DOM Books.

The audit compares manuscript chapter files with the chapter status register.
It produces a Markdown report and only fails when --strict is supplied and
publication-ineligible chapters are present.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REGISTER = ROOT / "book_01_GhostPAT/meta/chapter_status_register.md"
DEFAULT_MANUSCRIPT = ROOT / "book_01_GhostPAT/manuscript"
DEFAULT_REPORT = ROOT / "reports/canon_audit.md"

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


@dataclass(frozen=True)
class RegisterEntry:
    chapter: str
    descriptor: str
    status: str
    action: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--register", type=Path, default=DEFAULT_REGISTER)
    parser.add_argument("--manuscript", type=Path, default=DEFAULT_MANUSCRIPT)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Return non-zero when any discovered chapter is not VERIFIED_CANON.",
    )
    return parser.parse_args()


def parse_register(path: Path) -> list[RegisterEntry]:
    if not path.is_file():
        raise FileNotFoundError(f"chapter status register not found: {path}")

    entries: list[RegisterEntry] = []
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line.startswith("|") or line.startswith("|---"):
            continue

        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) != 4 or cells[0] == "Chapter":
            continue

        chapter, descriptor, status, action = cells
        if status not in KNOWN_STATUSES:
            continue
        entries.append(RegisterEntry(chapter, descriptor, status, action))

    if not entries:
        raise ValueError(f"no chapter entries parsed from {path}")
    return entries


def chapter_number(path: Path) -> str | None:
    match = re.match(r"ch(\d{2})_", path.name, flags=re.IGNORECASE)
    return match.group(1) if match else None


def discover_chapters(directory: Path) -> list[Path]:
    if not directory.is_dir():
        raise FileNotFoundError(f"manuscript directory not found: {directory}")
    return sorted(
        path for path in directory.glob("ch*.md") if chapter_number(path) is not None
    )


def index_entries(entries: Iterable[RegisterEntry]) -> dict[str, RegisterEntry]:
    result: dict[str, RegisterEntry] = {}
    for entry in entries:
        if re.fullmatch(r"\d{2}", entry.chapter):
            result[entry.chapter] = entry
    return result


def build_report(
    register_path: Path,
    manuscript_path: Path,
    entries: list[RegisterEntry],
    chapters: list[Path],
) -> tuple[str, bool]:
    indexed = index_entries(entries)
    rows: list[str] = []
    strict_failure = False

    for path in chapters:
        number = chapter_number(path)
        assert number is not None
        entry = indexed.get(number)
        if entry is None:
            status = "UNREGISTERED"
            action = "Add this chapter to the status register."
            strict_failure = True
        else:
            status = entry.status
            action = entry.action
            if status not in PUBLICATION_ELIGIBLE:
                strict_failure = True

        relative = path.relative_to(ROOT).as_posix()
        rows.append(f"| {number} | `{relative}` | {status} | {action} |")

    discovered_numbers = {chapter_number(path) for path in chapters}
    missing_registered: list[RegisterEntry] = []
    for number, entry in sorted(indexed.items()):
        if number not in discovered_numbers:
            missing_registered.append(entry)
            strict_failure = True

    report_lines = [
        "# Canon Audit Report",
        "",
        f"- Register: `{register_path.relative_to(ROOT).as_posix()}`",
        f"- Manuscript directory: `{manuscript_path.relative_to(ROOT).as_posix()}`",
        f"- Discovered chapter files: **{len(chapters)}**",
        f"- Publication-eligible status: `{', '.join(sorted(PUBLICATION_ELIGIBLE))}`",
        "",
        "## Discovered chapters",
        "",
        "| Chapter | Path | Status | Required action |",
        "|---|---|---|---|",
        *rows,
        "",
        "## Registered chapters missing from the manuscript directory",
        "",
    ]

    if missing_registered:
        for entry in missing_registered:
            report_lines.append(
                f"- Chapter {entry.chapter}: {entry.descriptor} — `{entry.status}`"
            )
    else:
        report_lines.append("None.")

    report_lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "This is an advisory provenance check, not a factual verification engine.",
            "A file's presence in the manuscript or beta-reader build does not make it canon.",
            "Only chapters marked `VERIFIED_CANON` are eligible for strict publication builds.",
            "",
        ]
    )
    return "\n".join(report_lines), strict_failure


def main() -> int:
    args = parse_args()
    try:
        entries = parse_register(args.register)
        chapters = discover_chapters(args.manuscript)
        report, strict_failure = build_report(
            args.register, args.manuscript, entries, chapters
        )
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(report, encoding="utf-8")
        print(report)
        if args.strict and strict_failure:
            print(
                "Strict canon audit failed: one or more chapters are not publication eligible.",
                file=sys.stderr,
            )
            return 1
        return 0
    except (FileNotFoundError, ValueError) as exc:
        print(f"canon audit error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
