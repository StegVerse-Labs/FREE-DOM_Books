# Book 2 — Survivor-Source Boundary

Task: `FDB-008` · Goal: `FDB-CANON-001` · Book: `book_02_LedgerOfSilence`
(*The Ledger of Silence*)

This file is the survivor-source boundary for Book 2. It is a release
condition of `docs/TASKS.md`: **no survivor-derived POV may be drafted
as factual narrative before this boundary and the evidence-chronology
schema exist, are committed, and validate.** The boundary governs
which source material may ground a survivor-derived point of view, in
what form, and under what review. It authorizes no drafting and no
publication by itself.

## 1. Authority and governing decisions

- Canonical decisions 4, 5, 6, 10, 11 of
  `docs/handoff/FREE_DOM_BOOKS_MIRROR_HANDOFF.md`: Epstein-era POVs
  begin well before February 2020 and must be grounded in evidence;
  the youngest evidence-supported victim POVs may continue as adult
  protagonists in later books only after chronology and protection
  review; survivor identities must be protected; unsupported
  allegations about real people are prohibited; publication requires
  explicit author approval.
- The repository evidence and protection posture (`README.md`): no
  unsupported naming of real individuals as perpetrators or victims;
  no survivor identification without explicit authority and
  protection review; no generated dialogue presented as a verbatim
  historical quotation without a source; no conversion of thematic
  resemblance into factual causation; composites must be explicitly
  registered.
- The `StegVerse-Labs/FREE-DOM` Sensitive Information Protocol:
  identifying details, personal testimony, and allegations are never
  placed in the public repository; only non-identifying details
  (dates, locations, public sources) are publicly integrated.

## 2. Admissible sources

A Book 2 scene, claim, or POV may be grounded only in an
evidence-chronology entry that validates against
`book_02_LedgerOfSilence/boundary/evidence_chronology.schema.json`
and is recorded under `book_02_LedgerOfSilence/chronology/`.

Source lifecycle rule (from `StegVerse-Labs/FREE-DOM`):

| FREE-DOM lifecycle | Use in Book 2 |
|---|---|
| `data/master/` (verified) | May ground factual narrative within this boundary. |
| `data/archive/` (processed batches) | May ground factual narrative if the entry cites the archive batch and the underlying master record. |
| `data/pending/` | Lead only. May motivate further verification; may not ground a factual claim or a POV. |
| `data/unverified/` | Never grounds fact or POV. An entry resting on it is `NOT_ELIGIBLE`. |

Evidence classes follow the series vocabulary: `LIVED_MEMORY`,
`DOCUMENTED_FACT`, `PUBLIC_RECORD`, `COMPOSITE`,
`FICTIONAL_CONNECTIVE_TISSUE`, `UNVERIFIED_LEAD`,
`NONCANONICAL_DRAFT`. An entry carrying `UNVERIFIED_LEAD` is never
POV-eligible.

## 3. Identity protection (non-waivable)

1. No chronology entry, register, draft, or published text may carry
   a survivor's name, contact detail, image, or any combination of
   details that identifies a survivor. `identifying_details` is
   `NONE_PRESENT` in every entry, without exception.
2. Survivor-derived POV characters are **composites by default**.
   A composite must be registered in the Book 2 composite register
   (escrow custody, §6) before any drafting from it, and the
   chronology entry must record `protection_class:
   COMPOSITE_REQUIRED` and `composite_required: true`.
3. No re-identification: anonymized entries must not be correlated
   back to private individuals, in the text or in working notes.
4. No survivor testimony may be rendered as verbatim dialogue
   unless the entry cites a public-record source for the quotation
   itself.
5. Age is handled as a band only (`MINOR`, `ADULT`, `UNKNOWN`,
   `NOT_APPLICABLE`). No birthdates or age-exact data for survivors
   are recorded anywhere in this workstream.

## 4. Chronology rules

1. Every survivor-derived POV scene binds to one or more chronology
   entries; the scene's event window must fall entirely inside the
   union of its entries' `event_window` bounds.
2. Epstein-era POV events begin well before February 2020
   (decision 4). An entry whose window opens on or after
   2020-03-01 cannot ground an Epstein-era POV.
3. Adult continuation (decision 5): a victim POV may continue as an
   adult protagonist in a later book only when the continuation
   entry records `pov_eligibility: ADULT_CONTINUATION_ELIGIBLE`,
   `age_band_at_event: ADULT`, and both chronology and
   survivor-protection review complete. `UNKNOWN` age band is never
   continuation-eligible.
4. Thematic resemblance is not chronology: co-occurrence in time
   does not establish causation, contact, or presence.

## 5. Eligibility and the gate

`pov_eligibility` is computed per entry, never asserted globally:

- `NOT_ELIGIBLE` — default; all `ESCROW_ONLY` and `PROHIBITED`
  material, all unverified material, all unreviewed material.
- `COMPOSITE_POV_ELIGIBLE` — verified sources, composite protection
  in force, chronology review and survivor-protection review both
  recorded complete.
- `ADULT_CONTINUATION_ELIGIBLE` — §4.3 satisfied in full.

The validator `scripts/validate_survivor_boundary.py` enforces
these rules mechanically and fails closed. Survivor protection is
an independent gate: a failure here blocks Book 2 POV drafting
regardless of any other task state, and it is not waivable by any
lane. Drafting under an eligible entry still produces
`NONCANONICAL_DRAFT` material only; canon admission runs through
the canonical registers, and publication remains the author's
explicit act alone (decision 11).

## 6. Custody

The Book 2 survivor-source register, the Book 2 composite register,
and any survivor-sensitive analysis are **escrow custody material**
(Option 3 separation, 2026-11-26): they are held in the private
escrow destination of record for `FDB-CANON-001`, never in this
public repository. This boundary file, the chronology schema, the
validator, and its validation report are protective infrastructure
and remain public. Chronology entries under
`book_02_LedgerOfSilence/chronology/` carry only non-identifying
structure (dates, classes, source references, protection state) and
may be committed publicly; any entry that cannot be written without
identifying detail does not belong here at all — it is escrow-only
and its public trace is a hash reference in the package manifest.
