# FREE-DOM Books Task Registry

Canonical handoff: `docs/handoff/FREE_DOM_BOOKS_MIRROR_HANDOFF.md`
Canonical execution inventory: `docs/SESSION_EXECUTION_INVENTORY.md`
Canonical issue: `#1`

## State vocabulary

`UNCLAIMED`, `CLAIMED_FOR_IMPLEMENTATION`, `CLAIMED_FOR_VALIDATION`, `CLAIMED_FOR_INTEGRATION`, `MACHINE_OWNED`, `BLOCKED`, `COMPLETE`, `SUPERSEDED`, `MERGED_INTO_CANONICAL_WORKSTREAM`.

## Active tasks

| Task ID | State | Owner | Surface | Release condition | Expected evidence | Next task |
|---|---|---|---|---|---|---|
| FDB-007 | CLAIMED_FOR_IMPLEMENTATION | FREE-DOM_Books canonical workstream | Chapters 2-18, metadata, audits | all chapters explicitly classified and mapped to provenance | commits, validator report, canon audit artifact | FDB-005 strict publication gate |
| FDB-008 | CLAIMED_FOR_IMPLEMENTATION | FREE-DOM_Books canonical workstream | Book 2 survivor-source boundary | boundary file and chronology schema committed | commit and validation report | Book 2 outline only after boundary passes |
| FDB-009 | CLAIMED_FOR_VALIDATION | FREE-DOM_Books validation lane | `prompts/style_seed.md`, `prompts/Rige1_brainseed.txt`, prompt loader | paths/content verified and loading test passes | test result and workflow artifact | integrate generation workflow |
| FDB-010 | MACHINE_OWNED | GitHub Actions | readiness, canon audit, governed reader build | qualifying workflow run completes and artifacts are inspectable | run, jobs, logs, artifacts | correct failures or mark COMPLETE |
| FDB-011 | CLAIMED_FOR_IMPLEMENTATION | FREE-DOM_Books canonical workstream | legacy links in manuscript/public surfaces | all links point to canonical repository or are intentionally retained | commit and link scan | regenerate reader build |
| FDB-012 | UNCLAIMED | cross-repository integration lane | FREE-DOM source contract and FREE-DOM_Books consumer contract | contracts committed in both owner repositories | source/consumer contract commits | activate dispatch only after tests |
| FDB-013 | BLOCKED | cross-repository publication lane | Site/Publisher propagation | at least one chapter VERIFIED_CANON and target handoffs authorize propagation | publication manifest, target handoff, integration receipt | propagate governed output |

## Completed or transferred tasks

| Task ID | State | Evidence |
|---|---|---|
| FDB-001 | MERGED_INTO_CANONICAL_WORKSTREAM | metadata/schema/validator records and Issue #1 |
| FDB-002 | COMPLETE | chronology rules in handoff/schema/validator |
| FDB-003 | BLOCKED | author-review boundary in memoir claim register; no chat retention required |
| FDB-004 | COMPLETE | dialogue and composite registers |
| FDB-005 | MACHINE_OWNED | publication manifest, governed build, tests |
| FDB-006 | COMPLETE | four provenance registers |
| FDB-014 | COMPLETE | inventory, handoff, issue, and claim-release record |

## Collision boundaries

- No chapter may be independently promoted to `VERIFIED_CANON` outside the canonical status register and metadata validator.
- No public build may bypass `scripts/publication_manifest.py`.
- No survivor-derived POV may be drafted as factual narrative before the Book 2 survivor-source boundary exists.
- No Site or Publisher propagation may occur before FDB-013's release condition.
- Chat sessions may take validation or integration roles only after recording a nonconflicting claim here or in the claim registry.
