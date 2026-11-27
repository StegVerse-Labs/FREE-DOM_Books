#!/usr/bin/env python3
"""Validate the Book 2 survivor-source boundary and evidence chronology.

Stdlib-only, fail-closed. Enforces FDB-008: the boundary file and the
chronology schema must exist and every chronology entry must satisfy
the identity-protection, source-lifecycle, chronology, and review
rules of book_02_LedgerOfSilence/boundary/survivor_source_boundary.md.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOUNDARY_FILE = ROOT / "book_02_LedgerOfSilence/boundary/survivor_source_boundary.md"
SCHEMA_FILE = ROOT / "book_02_LedgerOfSilence/boundary/evidence_chronology.schema.json"
DEFAULT_ENTRIES_DIR = ROOT / "book_02_LedgerOfSilence/chronology"
DEFAULT_REPORT = ROOT / "reports/survivor_boundary_validation.md"

EVIDENCE_CLASSES = {
    "LIVED_MEMORY", "DOCUMENTED_FACT", "PUBLIC_RECORD", "COMPOSITE",
    "FICTIONAL_CONNECTIVE_TISSUE", "UNVERIFIED_LEAD", "NONCANONICAL_DRAFT",
}
PROTECTION_CLASSES = {"PUBLIC_ANONYMIZED", "COMPOSITE_REQUIRED", "ESCROW_ONLY", "PROHIBITED"}
ELIGIBILITY = {"NOT_ELIGIBLE", "COMPOSITE_POV_ELIGIBLE", "ADULT_CONTINUATION_ELIGIBLE"}
AGE_BANDS = {"MINOR", "ADULT", "UNKNOWN", "NOT_APPLICABLE"}
LIFECYCLES = {"MASTER_VERIFIED", "PENDING", "UNVERIFIED", "ARCHIVE"}
GROUNDING_LIFECYCLES = {"MASTER_VERIFIED", "ARCHIVE"}
ENTRY_ID = re.compile(r"^LOS-CHRON-[0-9]{3}$")
SOURCE_PATH = re.compile(r"^data/(master|pending|unverified|archive)/.+")
EPSTEIN_ERA_POV_LATEST_OPEN = date(2020, 3, 1)

BOUNDARY_SECTIONS = (
    "## 1. Authority and governing decisions",
    "## 2. Admissible sources",
    "## 3. Identity protection (non-waivable)",
    "## 4. Chronology rules",
    "## 5. Eligibility and the gate",
    "## 6. Custody",
)


def _parse_date(value: object) -> date | None:
    if not isinstance(value, str):
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def validate_entry(data: object) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["entry: must be a JSON object"]
    if data.get("schema_version") != "1.0.0":
        errors.append("schema_version: must be '1.0.0'")
    if data.get("book_id") != "book_02_LedgerOfSilence":
        errors.append("book_id: must be 'book_02_LedgerOfSilence'")
    if not ENTRY_ID.match(str(data.get("entry_id", ""))):
        errors.append("entry_id: must match LOS-CHRON-NNN")
    if not isinstance(data.get("title"), str) or not data["title"]:
        errors.append("title: required non-empty string")

    window = data.get("event_window")
    if not isinstance(window, dict):
        errors.append("event_window: required object")
        window = {}
    nb, na = _parse_date(window.get("not_before")), _parse_date(window.get("not_after"))
    if nb is None:
        errors.append("event_window.not_before: required ISO date")
    if na is None:
        errors.append("event_window.not_after: required ISO date")
    if nb and na and nb > na:
        errors.append("event_window: not_before must not exceed not_after")

    classes = data.get("evidence_classes")
    if not isinstance(classes, list) or not classes:
        errors.append("evidence_classes: required non-empty array")
        classes = []
    for c in classes:
        if c not in EVIDENCE_CLASSES:
            errors.append(f"evidence_classes: unknown class '{c}'")
    if len(classes) != len(set(classes)):
        errors.append("evidence_classes: duplicates")

    refs = data.get("source_refs")
    if not isinstance(refs, list) or not refs:
        errors.append("source_refs: required non-empty array")
        refs = []
    lifecycles = []
    for ref in refs:
        if not isinstance(ref, dict):
            errors.append("source_refs: each ref must be an object")
            continue
        if ref.get("repository") != "StegVerse-Labs/FREE-DOM":
            errors.append("source_refs.repository: must be StegVerse-Labs/FREE-DOM")
        if not SOURCE_PATH.match(str(ref.get("path", ""))):
            errors.append(f"source_refs.path: '{ref.get('path')}' is outside data/(master|pending|unverified|archive)/")
        if ref.get("lifecycle") not in LIFECYCLES:
            errors.append(f"source_refs.lifecycle: unknown '{ref.get('lifecycle')}'")
        lifecycles.append(ref.get("lifecycle"))

    protection = data.get("protection_class")
    if protection not in PROTECTION_CLASSES:
        errors.append(f"protection_class: unknown '{protection}'")

    handling = data.get("subject_handling")
    if not isinstance(handling, dict):
        errors.append("subject_handling: required object")
        handling = {}
    if handling.get("identifying_details") != "NONE_PRESENT":
        errors.append("subject_handling.identifying_details: must be NONE_PRESENT, without exception")
    if handling.get("age_band_at_event") not in AGE_BANDS:
        errors.append(f"subject_handling.age_band_at_event: unknown '{handling.get('age_band_at_event')}'")

    elig = data.get("pov_eligibility")
    if elig not in ELIGIBILITY:
        errors.append(f"pov_eligibility: unknown '{elig}'")

    review = data.get("review")
    if not isinstance(review, dict):
        errors.append("review: required object")
        review = {}

    # Boundary rules R1-R7 (survivor_source_boundary.md SS2-SS5).
    if elig != "NOT_ELIGIBLE":
        if "UNVERIFIED_LEAD" in classes:
            errors.append("R1: UNVERIFIED_LEAD material is never POV-eligible")
        if any(lc not in GROUNDING_LIFECYCLES for lc in lifecycles):
            errors.append("R2: every source_ref must be MASTER_VERIFIED or ARCHIVE for POV eligibility")
        if review.get("chronology_reviewed") is not True or review.get("survivor_protection_reviewed") is not True:
            errors.append("R3: POV eligibility requires chronology and survivor-protection review complete")
        if protection in ("ESCROW_ONLY", "PROHIBITED"):
            errors.append("R6: ESCROW_ONLY/PROHIBITED material is never POV-eligible")
    if elig == "COMPOSITE_POV_ELIGIBLE":
        if protection != "COMPOSITE_REQUIRED":
            errors.append("R4: COMPOSITE_POV_ELIGIBLE requires protection_class COMPOSITE_REQUIRED")
        if handling.get("composite_required") is not True:
            errors.append("R4: COMPOSITE_POV_ELIGIBLE requires composite_required=true")
    if elig == "ADULT_CONTINUATION_ELIGIBLE":
        if handling.get("age_band_at_event") != "ADULT":
            errors.append("R5: adult continuation requires age_band_at_event=ADULT")
    return errors


def validate_boundary() -> list[str]:
    errors: list[str] = []
    if not BOUNDARY_FILE.exists():
        return [f"boundary file missing: {BOUNDARY_FILE.relative_to(ROOT)}"]
    text = BOUNDARY_FILE.read_text(encoding="utf-8")
    for section in BOUNDARY_SECTIONS:
        if section not in text:
            errors.append(f"boundary file missing section: {section}")
    if not SCHEMA_FILE.exists():
        errors.append(f"chronology schema missing: {SCHEMA_FILE.relative_to(ROOT)}")
    else:
        try:
            schema = json.loads(SCHEMA_FILE.read_text(encoding="utf-8"))
            if schema.get("$id") != "https://stegverse.org/schemas/free-dom-books/evidence_chronology.schema.json":
                errors.append("schema $id mismatch")
        except json.JSONDecodeError as exc:
            errors.append(f"schema is not valid JSON: {exc}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--entries-dir", type=Path, default=DEFAULT_ENTRIES_DIR)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    args = parser.parse_args()

    errors = validate_boundary()
    entries = sorted(args.entries_dir.glob("*.json")) if args.entries_dir.exists() else []
    per_entry: dict[str, list[str]] = {}
    for path in entries:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            errs = validate_entry(data)
        except json.JSONDecodeError as exc:
            errs = [f"invalid JSON: {exc}"]
        per_entry[path.name] = errs
        errors.extend(f"{path.name}: {e}" for e in errs)

    status = "PASS" if not errors else "FAIL"
    lines = [
        "# Survivor Boundary Validation Report",
        "",
        f"- Boundary file: `{BOUNDARY_FILE.relative_to(ROOT)}`",
        f"- Chronology schema: `{SCHEMA_FILE.relative_to(ROOT)}`",
        f"- Chronology entries validated: {len(entries)}",
        f"- Result: **{status}**",
        "",
    ]
    if errors:
        lines.append("## Errors")
        lines.extend(f"- {e}" for e in errors)
    else:
        lines.append("No errors. The boundary and schema satisfy FDB-008's mechanical rules;")
        lines.append("survivor protection remains an independent human/lane review gate.")
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"survivor boundary validation: {status} ({len(entries)} entries, {len(errors)} errors)")
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
