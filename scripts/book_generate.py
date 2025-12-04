#!/usr/bin/env python3
"""
Book chapter generator for FREE-DOM_Books.

Usage (local example):

  export OPENAI_API_KEY=sk-...
  python scripts/book_generate.py \
    --book 01 \
    --chapter 03 \
    --length long \
    --tone cinematic

This script:
- Reads the master arc map + outline if present
- Reads style / brainseed prompts
- Calls OpenAI to generate a draft chapter
- Writes to book_XX_*/manuscript/chNN_*.md (or prints to stdout if no path)
"""

import argparse
import os
import sys
from pathlib import Path
from datetime import datetime

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None  # We'll handle this gracefully


ROOT = Path(__file__).resolve().parents[1]  # repo root: FREE-DOM_Books/


def load_file(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def detect_book_folder(book_id: str) -> Path:
    """
    Given '01', try to find folder like 'book_01_*'.
    If multiple, pick the first alphabetically.
    """
    candidates = sorted(ROOT.glob(f"book_{book_id}_*"))
    if not candidates:
        raise SystemExit(f"[ERROR] No folder found matching book_{book_id}_*")
    return candidates[0]


def default_chapter_filename(chapter: str, book_folder: Path) -> Path:
    """
    For now we just name: chNN_generated.md if no specific title.
    You can rename later.
    """
    manu_dir = book_folder / "manuscript"
    manu_dir.mkdir(parents=True, exist_ok=True)
    return manu_dir / f"ch{chapter}_generated.md"


def build_prompt(
    book_id: str,
    chapter: str,
    length: str,
    tone: str,
) -> str:
    """Assemble a big system+user style prompt for the model."""
    # Core references
    arc_map_path = ROOT / "series_arc" / "00_master_arc_map.md"
    style_seed_path = ROOT / "prompts" / "style_seed.md"
    brainseed_path = ROOT / "prompts" / "Rige1_brainseed.txt"

    arc_map = load_file(arc_map_path)
    style_seed = load_file(style_seed_path)
    brainseed = load_file(brainseed_path)

    # Book-specific outline
    book_folder = detect_book_folder(book_id)
    outline_path = book_folder / "outline" / "Book01_outline.md"
    outline = load_file(outline_path) if outline_path.exists() else ""

    # Existing chapters for continuity (short snippets)
    manuscript_dir = book_folder / "manuscript"
    existing_snippets = []
    if manuscript_dir.exists():
        for p in sorted(manuscript_dir.glob("ch*.md")):
            try:
                text = p.read_text(encoding="utf-8")
                snippet = text[:2000]
                existing_snippets.append(f"# {p.name}\n\n{snippet}\n\n---\n")
            except Exception:
                continue

    existing_context = "\n".join(existing_snippets[-3:])  # last 3 chapters/snippets

    # Explain length mode
    if length == "short":
        length_hint = "Aim for 1200–2000 words."
    elif length == "medium":
        length_hint = "Aim for 2500–4000 words."
    else:
        length_hint = "Aim for 4000–6000 words, layered, with emotional depth and pacing."

    # Prompt text (given as user message to the model)
    prompt = f"""
You are assisting in writing a multi-book series in the FREE-DOM universe.

### GLOBAL SERIES CONTEXT
The following is the master arc map for the entire series:

{arc_map}

### BOOK-SPECIFIC OUTLINE (BOOK {book_id})
{outline}

### STYLE + VOICE SEED
{style_seed}

### RIGE1 BRAINSEED (TWIN AUTHOR ROLE)
{brainseed}

### EXISTING MANUSCRIPT CONTEXT (recent snippets)
{existing_context}

---

## TASK

Write **Book {book_id}, Chapter {chapter}** as a full prose chapter
in first-person POV (Rigel), consistent with the tone, ethics, and arc above.

- Tone requested: **{tone}**
- {length_hint}

RULES:
- Stay emotionally truthful and grounded.
- Do NOT sensationalize trauma.
- Do NOT introduce supernatural elements (ghosts are systemic/technical, not literal).
- Keep all technology plausible based on current or near-future systems.
- Respect the themes of Ghost_PAT, Phantom Trust, StegVerse, and systemic failure.
- The chapter should stand alone but clearly belong in the series arc.
- Include scene transitions and sensory details, but avoid purple prose.
- Do not add front-matter, headings, or markdown beyond light section breaks.
- Output ONLY the chapter prose, no commentary.
"""
    return prompt.strip()


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a FREE-DOM book chapter via OpenAI.")
    parser.add_argument("--book", required=True, help="Book ID, e.g. 01")
    parser.add_argument("--chapter", required=True, help="Chapter number, e.g. 02")
    parser.add_argument("--length", default="medium", choices=["short", "medium", "long"])
    parser.add_argument("--tone", default="cinematic")
    parser.add_argument(
        "--model",
        default="gpt-4.1",
        help="OpenAI model name (e.g. gpt-4.1, gpt-4.1-mini, gpt-5.1 if available).",
    )
    parser.add_argument(
        "--output",
        default="",
        help="Optional output path. If omitted, auto-selects chNN_generated.md in the book folder.",
    )

    args = parser.parse_args()

    api_key = os.getenv("OPENAI_API_KEY") or os.getenv("OPENAI_API_TOKEN")
    if not api_key:
        raise SystemExit("[ERROR] OPENAI_API_KEY (or OPENAI_API_TOKEN) env var is required.")

    if OpenAI is None:
        raise SystemExit(
            "[ERROR] openai package not installed. "
            "Add `openai` to requirements and `pip install openai` before running."
        )

    book_id = args.book.zfill(2)
    chapter = args.chapter.zfill(2)

    book_folder = detect_book_folder(book_id)
    if args.output:
        output_path = Path(args.output)
        if not output_path.is_absolute():
            output_path = book_folder / "manuscript" / output_path
        output_path.parent.mkdir(parents=True, exist_ok=True)
    else:
        output_path = default_chapter_filename(chapter, book_folder)

    prompt = build_prompt(book_id, chapter, args.length, args.tone)

    client = OpenAI(api_key=api_key)

    print(f"[INFO] Generating Book {book_id} Chapter {chapter} with model {args.model}...")
    # Using chat.completions style; adjust if using new Responses API.
    resp = client.chat.completions.create(
        model=args.model,
        messages=[
            {
                "role": "system",
                "content": "You are a careful, emotionally precise novelist and co-author. "
                           "You follow instructions exactly and respect trauma and truth.",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0.65,
    )

    text = resp.choices[0].message.content
    header = (
        f"<!-- Generated on {datetime.utcnow().isoformat()}Z "
        f"by book_generate.py, model={args.model}, length={args.length}, tone={args.tone} -->\n\n"
    )
    output_path.write_text(header + text, encoding="utf-8")

    print(f"[OK] Chapter written to: {output_path}")


if __name__ == "__main__":
    main()
