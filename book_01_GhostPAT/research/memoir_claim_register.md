# Memoir Claim Register

Book: **Ghosts of Trust**
Purpose: track every factual memoir claim before it enters verified canon.

## Status values

- `UNREVIEWED`
- `LIVED_MEMORY_CONFIRMED`
- `DOCUMENT_SUPPORTED`
- `PUBLIC_RECORD_SUPPORTED`
- `COMPOSITE_ONLY`
- `DISPUTED`
- `EXCLUDED`

## Required fields

| Claim ID | Chapter | Claim summary | Time window | Location | Evidence class | Source pointer | Confidence | Protection need | Status | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| GOT-MEM-001 | 09 | Rigel was sideswiped on I-35 after work by another federal employee. | Before 2020-02 | I-35, Texas | LIVED_MEMORY | pending | high for core event; details pending | personal/privacy review | LIVED_MEMORY_CONFIRMED | Preserve core event. Do not invent speed, weather, injuries, dialogue, vehicle details, or aftermath. |
| GOT-MEM-002 | 10 | Rigel returned to work immediately after the collision. | Before 2020-02 | Waco VAMC | LIVED_MEMORY | pending | high | personal/privacy review | LIVED_MEMORY_CONFIRMED | Exact next-day timing and physical symptoms require confirmation or records. |
| GOT-MEM-003 | 01-18 | Rigel's own investigation ended by February 2020. | through 2020-02 | Texas | LIVED_MEMORY | handoff decision | high | none | LIVED_MEMORY_CONFIRMED | Governing chronology boundary. |
| GOT-MEM-004 | 05 | DOJ San Antonio arrests involved disability-payment fraud and former federal employees. | 2019 | San Antonio, Texas | UNVERIFIED_LEAD | pending public-record research | unknown | allegation sensitivity | UNREVIEWED | No amount, role, causal connection, or named person enters canon until sourced. |
| GOT-MEM-005 | 02-16 | Workstations repeatedly dropped from the network/domain and were often reimaged. | 2017-2020 | Waco VAMC | LIVED_MEMORY | pending records/witness corroboration | medium-high | workplace/privacy review | UNREVIEWED | Preserve observation; do not infer malicious cause. |

## Admission rule

A factual sentence may enter `VERIFIED_CANON` only when this register contains:

1. a stable claim ID;
2. an evidence class;
3. a source pointer or explicit lived-memory confirmation;
4. a confidence statement;
5. privacy and survivor-protection treatment;
6. a status other than `UNREVIEWED`, `DISPUTED`, or `EXCLUDED`.

## Prohibited transformations

- Turning thematic resemblance into factual causation.
- Converting remembered gist into verbatim dialogue.
- Combining different people without marking the result `COMPOSITE_ONLY`.
- Assigning motives, crimes, or knowledge to real people without admissible evidence.
- Extending Rigel's investigation beyond February 2020 because later technical events rhyme with earlier ones.
