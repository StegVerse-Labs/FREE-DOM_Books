#!/usr/bin/env python3
"""Validate machine-readable chapter metadata without external dependencies."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_METADATA_DIR = ROOT / "book_01_GhostPAT/meta/chapters"
DEFAULT_MANUSCRIPT_DIR = ROOT / "book_01_GhostPAT/manuscript"
DEFAULT_REPORT = ROOT / "reports/chapter_metadata_validation.md"

STATUSES = {
    "VERIFIED_CANON",
    "CANON_DRAFT",
    "FACTUAL_REVIEW_REQUIRED",
    "COMPOSITE_REVIEW_REQUIRED",
    "NONCANONICAL_DRAFT",
    "MISSING_FROM_REPOSITORY",
    "UNRESOLVED_ORDER",
}
EVIDENCE_CLASSES = {
    "LIVED_MEMORY",
    "DOCUMENTED_FACT",
    "PUBLIC_RECORD",
    "COMPOSITE",
    "FICTIONAL_CONNECTIVE_TISSUE",
    "UNVERIFIED_LEAD",
    "NONCANONICAL_DRAFT",
}
ERAS = {"VA_ERA", "GHOST_PAT_FLASH_FORWARD", "BRIDGE", "OTHER"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--metadata-dir", type=Path, default=DEFAULT_METADATA_DIR)
    parser.add_argument("--manuscript-dir", type=Path, default=DEFAULT_MANUSCRIPT_DIR)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    return parser.parse_args()


def require_string(data: dict, key: str, errors: list[str]) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not value:
        errors.append(f"{key}: required non-empty string")
        return ""
    return value


def validate_ids(values: object, pattern: str, field: str, errors: list[str]) -> None:
    if not isinstance(values, list):
        errors.append(f"{field}: required array")
        return
    if len(values) != len(set(values)):
        errors.append(f"{field}: duplicate identifiers")
    for value in values:
        if not isinstance(value, str) or not re.fullmatch(pattern, value):
            errors.append(f"{field}: invalid identifier {value!r}")


def validate_file(path: Path, manuscript_dir: Path) -> tuple[str, list[str]]:
    errors: list[str] = []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return path.name, [f"invalid JSON: {exc}"]

    if not isinstance(data, dict):
        return path.name, ["root must be an object"]

    if data.get("schema_version") != "1.0.0":
        errors.append("schema_version: expected 1.0.0")
    if data.get("book_id") != "book_01_GhostPAT":
        errors.append("book_id: expected book_01_GhostPAT")

    chapter = require_string(data, "chapter_number", errors)
    if chapter and not re.fullmatch(r"\d{2}", chapter):
        errors.append("chapter_number: expected two digits")

    require_string(data, "title", errors)
    manuscript_path = require_string(data, "manuscript_path", errors)
    if manuscript_path:
        expected_prefix = "book_01_GhostPAT/manuscript/ch"
        if not manuscript_path.startswith(expected_prefix) or not manuscript_path.endswith(".md"):
            errors.append("manuscript_path: invalid chapter path")
        manuscript_file = manuscript_dir / Path(manuscript_path).name
        status = data.get("canon_status")
        if status != "MISSING_FROM_REPOSITORY" and not manuscript_file.is_file():
            errors.append(f"manuscript_path: file not found: {manuscript_path}")
        if chapter and Path(manuscript_path).name[:4].lower() != f"ch{chapter}".lower():
            errors.append("manuscript_path: chapter number does not match metadata")

    status = data.get("canon_status")
    if status not in STATUSES:
        errors.append(f"canon_status: unknown value {status!r}")

    publication_eligible = data.get("publication_eligible")
    if not isinstance(publication_eligible, bool):
        errors.append("publication_eligible: required boolean")
    elif publication_eligible != (status == "VERIFIED_CANON"):
        errors.append("publication_eligible must be true only for VERIFIED_CANON")

    chronology = data.get("chronology")
    if not isinstance(chronology, dict):
        errors.append("chronology: required object")
    else:
        era = chronology.get("era")
        if era not in ERAS:
            errors.append(f"chronology.era: unknown value {era!r}")
        if "not_after" not in chronology:
            errors.append("chronology.not_after: required")
        if era == "VA_ERA" and chronology.get("not_after") != "2020-02-29":
            errors.append("VA_ERA chronology.not_after must be 2020-02-29")

    classes = data.get("evidence_classes")
    if not isinstance(classes, list) or not classes:
        errors.append("evidence_classes: required non-empty array")
    else:
        unknown = sorted(set(classes) - EVIDENCE_CLASSES)
        if unknown:
            errors.append("evidence_classes: unknown values " + ", ".join(unknown))
        if len(classes) != len(set(classes)):
            errors.append("evidence_classes: duplicate values")

    validate_ids(data.get("claim_ids"), r"GOT-MEM-\d{3}", "claim_ids", errors)
    validate_ids(data.get("dialogue_ids"), r"GOT-DLG-\d{3}", "dialogue_ids", errors)
    validate_ids(data.get("composite_ids"), r"GOT-COMP-\d{3}", "composite_ids", errors)
    validate_ids(data.get("source_ids", []), r"GOT-SRC-[A-Z]{2}-\d{3}", "source_ids", errors)

    return path.name, errors


def main() -> int:
    args = parse_args()
    if not args.metadata_dir.is_dir():
        print(f"metadata directory not found: {args.metadata_dir}", file=sys.stderr)
        return 2

    rows: list[str] = []
    failed = False
    files = sorted(args.metadata_dir.glob("ch*.json"))
    if not files:
        print("no chapter metadata files found", file=sys.stderr)
        return 2

    for path in files:
        name, errors = validate_file(path, args.manuscript_dir)
        if errors:
            failed = True
            result = "FAIL: " + "; ".join(errors)
        else:
            result = "PASS"
        rows.append(f"| `{name}` | {result} |")

    report = "\n".join([
        "# Chapter Metadata Validation",
        "",
        f"Validated files: **{len(files)}**",
        "",
        "| Metadata file | Result |",
        "|---|---|",
        *rows,
        "",
    ])
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(report, encoding="utf-8")
    print(report)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
