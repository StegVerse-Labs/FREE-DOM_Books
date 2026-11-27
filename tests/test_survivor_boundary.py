"""Tests for the FDB-008 survivor-source boundary validator."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import validate_survivor_boundary as vsb


def entry(**overrides):
    base = {
        "schema_version": "1.0.0",
        "entry_id": "LOS-CHRON-001",
        "book_id": "book_02_LedgerOfSilence",
        "title": "Public docket event, anonymized",
        "event_window": {"not_before": "1998-01-01", "not_after": "1999-12-31"},
        "evidence_classes": ["PUBLIC_RECORD", "DOCUMENTED_FACT"],
        "source_refs": [
            {"repository": "StegVerse-Labs/FREE-DOM",
             "path": "data/master/master_timeline.csv",
             "lifecycle": "MASTER_VERIFIED"}
        ],
        "protection_class": "PUBLIC_ANONYMIZED",
        "subject_handling": {"identifying_details": "NONE_PRESENT",
                             "age_band_at_event": "NOT_APPLICABLE",
                             "composite_required": False},
        "pov_eligibility": "NOT_ELIGIBLE",
        "review": {"chronology_reviewed": False,
                   "survivor_protection_reviewed": False,
                   "reviewed_by": None},
    }
    base.update(overrides)
    return base


class TestSurvivorBoundary(unittest.TestCase):
    def test_valid_ineligible_entry_passes(self):
        self.assertEqual(vsb.validate_entry(entry()), [])

    def test_valid_composite_eligible_entry_passes(self):
        e = entry(protection_class="COMPOSITE_REQUIRED",
                  pov_eligibility="COMPOSITE_POV_ELIGIBLE",
                  subject_handling={"identifying_details": "NONE_PRESENT",
                                    "age_band_at_event": "MINOR",
                                    "composite_required": True},
                  review={"chronology_reviewed": True,
                          "survivor_protection_reviewed": True,
                          "reviewed_by": "test"})
        self.assertEqual(vsb.validate_entry(e), [])

    def test_unverified_lead_never_eligible(self):
        e = entry(evidence_classes=["UNVERIFIED_LEAD"],
                  pov_eligibility="COMPOSITE_POV_ELIGIBLE",
                  protection_class="COMPOSITE_REQUIRED",
                  subject_handling={"identifying_details": "NONE_PRESENT",
                                    "age_band_at_event": "MINOR",
                                    "composite_required": True},
                  review={"chronology_reviewed": True,
                          "survivor_protection_reviewed": True,
                          "reviewed_by": "test"})
        self.assertTrue(any(x.startswith("R1") for x in vsb.validate_entry(e)))

    def test_pending_source_cannot_ground_pov(self):
        e = entry(source_refs=[{"repository": "StegVerse-Labs/FREE-DOM",
                                "path": "data/pending/pending_people_template.csv",
                                "lifecycle": "PENDING"}],
                  pov_eligibility="COMPOSITE_POV_ELIGIBLE",
                  protection_class="COMPOSITE_REQUIRED",
                  subject_handling={"identifying_details": "NONE_PRESENT",
                                    "age_band_at_event": "MINOR",
                                    "composite_required": True},
                  review={"chronology_reviewed": True,
                          "survivor_protection_reviewed": True,
                          "reviewed_by": "test"})
        self.assertTrue(any(x.startswith("R2") for x in vsb.validate_entry(e)))

    def test_eligibility_requires_both_reviews(self):
        e = entry(pov_eligibility="COMPOSITE_POV_ELIGIBLE",
                  protection_class="COMPOSITE_REQUIRED",
                  subject_handling={"identifying_details": "NONE_PRESENT",
                                    "age_band_at_event": "MINOR",
                                    "composite_required": True})
        self.assertTrue(any(x.startswith("R3") for x in vsb.validate_entry(e)))

    def test_identifying_details_fail_closed(self):
        e = entry(subject_handling={"identifying_details": "PRESENT",
                                    "age_band_at_event": "ADULT",
                                    "composite_required": False})
        self.assertTrue(any("NONE_PRESENT" in x for x in vsb.validate_entry(e)))

    def test_adult_continuation_requires_adult_band(self):
        e = entry(pov_eligibility="ADULT_CONTINUATION_ELIGIBLE",
                  subject_handling={"identifying_details": "NONE_PRESENT",
                                    "age_band_at_event": "UNKNOWN",
                                    "composite_required": False},
                  review={"chronology_reviewed": True,
                          "survivor_protection_reviewed": True,
                          "reviewed_by": "test"})
        self.assertTrue(any(x.startswith("R5") for x in vsb.validate_entry(e)))

    def test_escrow_only_never_eligible(self):
        e = entry(protection_class="ESCROW_ONLY",
                  pov_eligibility="COMPOSITE_POV_ELIGIBLE",
                  subject_handling={"identifying_details": "NONE_PRESENT",
                                    "age_band_at_event": "MINOR",
                                    "composite_required": True},
                  review={"chronology_reviewed": True,
                          "survivor_protection_reviewed": True,
                          "reviewed_by": "test"})
        self.assertTrue(any(x.startswith("R6") for x in vsb.validate_entry(e)))

    def test_window_order_enforced(self):
        e = entry(event_window={"not_before": "2001-01-01", "not_after": "2000-01-01"})
        self.assertTrue(any("not_before" in x for x in vsb.validate_entry(e)))

    def test_boundary_file_sections_present(self):
        self.assertEqual(vsb.validate_boundary(), [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
