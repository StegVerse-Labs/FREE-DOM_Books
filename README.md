# FREE-DOM Books Engine

FREE-DOM Books turns structured, publicly verifiable evidence into protected story seeds, outlines, manuscripts, and publication-ready volumes without collapsing research, memory, composites, and fiction into one undifferentiated narrative layer.

## Repository roles

This repository has four connected roles:

1. **Evidence-to-seed engine** — consumes structured material from [`StegVerse-Labs/FREE-DOM`](https://github.com/StegVerse-Labs/FREE-DOM) and creates anonymized fiction-ready prompts.
2. **Manuscript workspace** — stores book outlines, chapter drafts, continuity records, and version history.
3. **Provenance boundary** — classifies lived memory, documentary fact, public records, composites, fictional connective tissue, and unverified leads before they enter canon.
4. **Rige1 author continuity** — preserves Rigel Randolph's narrative voice, visual reasoning, values, and long-form continuity while prohibiting unsupported invention.

## Evidence and protection posture

This repository is intentionally protective:

- No unsupported naming of real individuals as perpetrators or victims.
- No survivor identification without explicit authority and protection review.
- No generated dialogue presented as a verbatim historical quotation without a source.
- No conversion of thematic resemblance into factual causation.
- Composites must be explicitly registered.
- Publication and irreversible public release require explicit user approval.

The governing evidence classes are:

- `LIVED_MEMORY`
- `DOCUMENTED_FACT`
- `PUBLIC_RECORD`
- `COMPOSITE`
- `FICTIONAL_CONNECTIVE_TISSUE`
- `UNVERIFIED_LEAD`
- `NONCANONICAL_DRAFT`

## Current book program

### Book 1 — *Ghosts of Trust*

Book 1 follows Rigel's lived institutional and technical origin story. His own investigation ends by **February 2020**. Later Ghost_PAT material is a flash-forward and origin echo, not evidence that the earlier investigation continued beyond that date.

Required memoir anchors include:

- the Waco VAMC period;
- workstation/domain trust failures;
- veteran-payment concerns and institutional friction;
- the I-35 side-swipe by another federal employee after work;
- Rigel's immediate return to work;
- the later Ghost_PAT event as an architectural echo.

All chapter drafts after the verified opening remain subject to the chapter-status and provenance registers.

### Book 2 — *The Ledger of Silence*

Epstein-era and trafficking-survivor POVs begin well before February 2020 and must follow the available evidence chronology. The youngest evidence-supported victim POVs may continue into later 3I/ATLAS-era books as adults, but only after survivor-protection, identity, chronology, and evidentiary review.

## Durable continuity records

- Human-readable handoff: `docs/handoff/FREE_DOM_BOOKS_MIRROR_HANDOFF.md`
- Machine-readable state: `.stegverse/handoffs/free_dom_books_handoff.json`
- Book 1 chapter status: `book_01_GhostPAT/meta/chapter_status_register.md`
- Memoir claims: `book_01_GhostPAT/research/memoir_claim_register.md`
- Source map: `book_01_GhostPAT/research/source_reference_map.md`
- Composite register: `book_01_GhostPAT/research/composite_character_register.md`
- Dialogue register: `book_01_GhostPAT/research/dialogue_reconstruction_register.md`
- Active reconciliation task: GitHub Issue #1

## Evidence-to-seed flow

1. `StegVerse-Labs/FREE-DOM` runs evidence collection and update workflows.
2. Structured evidence is exported with source references and lifecycle metadata.
3. FREE-DOM Books groups admissible material by chronology, theme, and protection class.
4. The model creates fiction-safe story seeds under `seeds/`.
5. Seeds become outlines and noncanonical chapter drafts.
6. Claims, dialogue, composites, and chronology are reconciled through the provenance registers.
7. Only publication-eligible chapters enter compiled book outputs.

## Local environment

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

export OPENAI_API_KEY="sk-..."
```

The exact generation command and workflow entry points must be taken from verified repository scripts rather than assumed from older documentation.

## Continuation rule

Continue non-destructive documentation, continuity extraction, draft classification, repository inspection, evidence-index scaffolding, and workflow diagnosis without requiring Rigel. Request user input only when a decision materially changes factual truth, survivor protection, personal privacy, real-person identification, or irreversible publication posture.
