from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_chapter_metadata.py"


class ChapterMetadataValidatorTests(unittest.TestCase):
    def run_validator(self, metadata: dict, manuscript_exists: bool = True) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            metadata_dir = root / "meta"
            manuscript_dir = root / "manuscript"
            metadata_dir.mkdir()
            manuscript_dir.mkdir()

            manuscript_name = Path(metadata["manuscript_path"]).name
            if manuscript_exists:
                (manuscript_dir / manuscript_name).write_text("# chapter\n", encoding="utf-8")

            metadata["manuscript_path"] = f"book_01_GhostPAT/manuscript/{manuscript_name}"
            (metadata_dir / "ch01.json").write_text(json.dumps(metadata), encoding="utf-8")
            report = root / "report.md"

            return subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--metadata-dir",
                    str(metadata_dir),
                    "--manuscript-dir",
                    str(manuscript_dir),
                    "--report",
                    str(report),
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

    @staticmethod
    def base_metadata() -> dict:
        return {
            "schema_version": "1.0.0",
            "book_id": "book_01_GhostPAT",
            "chapter_number": "01",
            "title": "Test Chapter",
            "manuscript_path": "book_01_GhostPAT/manuscript/ch01_Test.md",
            "canon_status": "FACTUAL_REVIEW_REQUIRED",
            "chronology": {
                "era": "GHOST_PAT_FLASH_FORWARD",
                "not_before": None,
                "not_after": None,
                "notes": "test",
            },
            "evidence_classes": ["LIVED_MEMORY"],
            "claim_ids": [],
            "dialogue_ids": [],
            "composite_ids": [],
            "source_ids": [],
            "publication_eligible": False,
            "review_notes": [],
            "last_reviewed_commit": None,
        }

    def test_valid_metadata_passes(self) -> None:
        result = self.run_validator(self.base_metadata())
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_unverified_chapter_cannot_be_publication_eligible(self) -> None:
        metadata = self.base_metadata()
        metadata["publication_eligible"] = True
        result = self.run_validator(metadata)
        self.assertEqual(result.returncode, 1)
        self.assertIn("publication_eligible must be true only for VERIFIED_CANON", result.stdout)

    def test_va_era_must_end_by_february_2020(self) -> None:
        metadata = self.base_metadata()
        metadata["chronology"] = {
            "era": "VA_ERA",
            "not_before": None,
            "not_after": "2021-01-01",
            "notes": "invalid extension",
        }
        result = self.run_validator(metadata)
        self.assertEqual(result.returncode, 1)
        self.assertIn("VA_ERA chronology.not_after must be 2020-02-29", result.stdout)


if __name__ == "__main__":
    unittest.main()
