from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/publication_manifest.py"


class PublicationManifestTests(unittest.TestCase):
    def make_fixture(self, root: Path) -> tuple[Path, Path, Path]:
        manuscript = root / "manuscript"
        manuscript.mkdir()
        (manuscript / "ch01_alpha.md").write_text("# Alpha\n", encoding="utf-8")
        (manuscript / "ch02_beta.md").write_text("# Beta\n", encoding="utf-8")

        register = root / "register.md"
        register.write_text(
            "\n".join(
                [
                    "| Chapter | Working title | Current status | Required action |",
                    "|---|---|---|---|",
                    "| 01 | Alpha | VERIFIED_CANON | none |",
                    "| 02 | Beta | FACTUAL_REVIEW_REQUIRED | verify |",
                ]
            )
            + "\n",
            encoding="utf-8",
        )
        output = root / "manifest.txt"
        return manuscript, register, output

    def run_manifest(
        self,
        manuscript: Path,
        register: Path,
        output: Path,
        *extra: str,
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--manuscript",
                str(manuscript),
                "--register",
                str(register),
                "--output",
                str(output),
                *extra,
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_default_selects_only_verified_canon(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            manuscript, register, output = self.make_fixture(Path(tmp))
            result = self.run_manifest(manuscript, register, output)
            self.assertEqual(result.returncode, 0, result.stderr)
            content = output.read_text(encoding="utf-8")
            self.assertIn("ch01_alpha.md", content)
            self.assertNotIn("ch02_beta.md", content)

    def test_explicit_draft_mode_includes_unverified(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            manuscript, register, output = self.make_fixture(Path(tmp))
            result = self.run_manifest(
                manuscript, register, output, "--include-unverified"
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            content = output.read_text(encoding="utf-8")
            self.assertIn("ch01_alpha.md", content)
            self.assertIn("ch02_beta.md", content)
            self.assertIn("WARNING", result.stdout)

    def test_safe_build_fails_when_no_verified_chapters_exist(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            manuscript, register, output = self.make_fixture(Path(tmp))
            register.write_text(
                "\n".join(
                    [
                        "| Chapter | Working title | Current status | Required action |",
                        "|---|---|---|---|",
                        "| 01 | Alpha | CANON_DRAFT | review |",
                        "| 02 | Beta | NONCANONICAL_DRAFT | review |",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            result = self.run_manifest(manuscript, register, output)
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(output.exists())
            self.assertIn("no chapters selected", result.stderr)


if __name__ == "__main__":
    unittest.main()
