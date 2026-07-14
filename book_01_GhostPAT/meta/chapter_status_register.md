# Book 1 Chapter Status Register

Book: **Ghosts of Trust**
Repository: `StegVerse-Labs/FREE-DOM_Books`
Authority: `docs/handoff/FREE_DOM_BOOKS_MIRROR_HANDOFF.md`

## Status values

- `VERIFIED_CANON`: fact-checked, source-classified, and approved for manuscript use.
- `CANON_DRAFT`: accepted narrative direction but still requires line-level review.
- `FACTUAL_REVIEW_REQUIRED`: contains lived-memory or public-record claims requiring verification.
- `COMPOSITE_REVIEW_REQUIRED`: includes merged identities, compressed chronology, or reconstructed dialogue.
- `NONCANONICAL_DRAFT`: generated material retained only for possible salvage.
- `MISSING_FROM_REPOSITORY`: expected file not found at the recorded path.
- `UNRESOLVED_ORDER`: title or placement conflicts with another draft.

## Governing chronology

- Rigel's lived investigation ends by **February 2020**.
- Later Ghost_PAT material is a flash-forward/origin echo.
- No chapter may imply continued personal investigation after February 2020 without a separately sourced later-period basis.

## Register

| Chapter | Repository path / working title | Current status | Required action |
|---|---|---|---|
| Prologue | What Follows You Home | NONCANONICAL_DRAFT | Review I-35 details; remove invented sensory specifics unless remembered or documented. |
| 01 | `book_01_GhostPAT/manuscript/ch01_The_Key_That_Wouldn’t_Die.md` — The Night the Key Wouldn’t Die | FACTUAL_REVIEW_REQUIRED | Apply `research/chapter_01_fact_audit.md`; verify logs, routes, root cause, chronology, setting, symptoms, and dialogue. Observed blob SHA: `7886ae194bac2f3d01f6941dead31159d902e6a6`. |
| 02 | `book_01_GhostPAT/manuscript/ch02_The_First_Ghost.md` — The First Ghost | FACTUAL_REVIEW_REQUIRED | Reconcile VA role, veteran-call exposure, workstation chronology, and all causal implications. Observed blob SHA: `bbdde56482dd33ec6981b66fc814e52c8ce74bf3`. |
| 03 | `book_01_GhostPAT/manuscript/ch03_The_Call_I_Still_Hear.md` — The Call I Still Hear | COMPOSITE_REVIEW_REQUIRED | Classify caller identity, family details, payment timeline, quoted dialogue, and outcome. Observed blob SHA: `c08f5f9a455fb103ba965bfb05b615c8cc44c45b`. |
| 04 | The Ledger / alternate title unresolved | UNRESOLVED_ORDER | Verify repository path; remove invented meetings, dialogue, and unsupported policy specifics. |
| 05 | When the News Broke | FACTUAL_REVIEW_REQUIRED | Verify DOJ event, date, amounts, roles, and what Rigel actually saw or knew at the time. |
| 06 | The Whisper Network | NONCANONICAL_DRAFT | Treat rumors and credential behavior as unverified until sourced. |
| 07 | A Conversation I Still Think About | COMPOSITE_REVIEW_REQUIRED | Do not present veteran dialogue as verbatim unless documented. |
| 08 | The Shape of a Future | NONCANONICAL_DRAFT | Remove invented folder/file creation unless confirmed. |
| 09 | Impact Velocity | FACTUAL_REVIEW_REQUIRED | Preserve I-35 side-swipe by another federal employee; verify all physical and scene details. |
| 10 | Back to the Fluorescents | FACTUAL_REVIEW_REQUIRED | Preserve immediate return to work; verify call content and injuries. |
| 11 | Phantom Threads | NONCANONICAL_DRAFT | Separate thematic reflection from factual claims. |
| 12 | The Ledger Begins | NONCANONICAL_DRAFT | Confirm whether notebook, entries, and wording existed. |
| 13 | More Than Noise | NONCANONICAL_DRAFT | Remove invented meeting and supervisor dialogue unless confirmed. |
| 14 | Stop Taking It Personally | NONCANONICAL_DRAFT | Treat exact workplace dialogue as reconstruction or composite unless documented. |
| 15 | One Case I Refused to Let Go | COMPOSITE_REVIEW_REQUIRED | No real-person case details without source and protection review. |
| 16 | Credentials and Ghosts | FACTUAL_REVIEW_REQUIRED | Verify workstation/domain mechanics; preserve thematic distinction from later token events. |
| 17 | Almost Quitting | NONCANONICAL_DRAFT | Verify emotional event and any veteran self-harm statement before use. |
| 18 | Ghosts in the Machine | CANON_DRAFT | Preserve Ghost_PAT flash-forward role; verify technical details against incident records. |
| 19-25 | Bridge material | NONCANONICAL_DRAFT | Do not extend the lived investigation past February 2020; rebuild only after chronology review. |

## Verified build anchor

`book_01_GhostPAT/manuscript/book_01_master.md` exists with observed blob SHA `9958e4718a7ba0e14f944dc716c0aac89a5196cc`. It lists Chapters 1-18 and is consumed by `.github/workflows/build_book.yml`.

The master file and beta-reader build are **not evidence of canon approval**. They expose drafts for reading and must not override this register.

## Required provenance records

Before any chapter becomes `VERIFIED_CANON`, create or update:

- `book_01_GhostPAT/research/memoir_claim_register.md`
- `book_01_GhostPAT/research/source_reference_map.md`
- `book_01_GhostPAT/research/composite_character_register.md`
- `book_01_GhostPAT/research/dialogue_reconstruction_register.md`
- a chapter-specific factual audit where exact technical, medical, employment, allegation, or survivor details appear

## Immediate next action

Continue exact-path verification for Chapters 4-18, then add an automated advisory canon audit that compares manuscript files with this register before beta or publication builds.
