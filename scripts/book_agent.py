import os
import sys
import json
from pathlib import Path
from datetime import datetime, timezone

from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Where your seed notes live
SEEDS_DIR = Path("seeds/2025")

# Where we keep run history
MEMORY_ROOT = Path("memory/runs")


def ask(prompt: str) -> str:
    """Call OpenAI Chat Completions to draft the chapter."""
    resp = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a collaborative book-writing assistant. "
                    "You help turn structured seed notes into a vivid, "
                    "emotionally intense but grounded narrative. "
                    "Write in clean, modern prose. Avoid purple prose."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0.7,
    )
    return resp.choices[0].message.content


def build_prompt() -> str:
    """Load all seed markdown files and build a single prompt."""
    parts = []

    if not SEEDS_DIR.exists():
        raise FileNotFoundError(f"Seeds directory not found: {SEEDS_DIR}")

    for seed_path in sorted(SEEDS_DIR.glob("*.md")):
        text = seed_path.read_text(encoding="utf-8")
        parts.append(f"# Seed: {seed_path.name}\n\n{text}")

    seeds_text = "\n\n---\n\n".join(parts)

    instructions = (
        "Using the seed material below, draft the **first chapter** of a book in "
        "the FREE-DOM series.\n\n"
        "- Maintain factual tone about verifiable events.\n"
        "- Use a single POV for this chapter.\n"
        "- Build emotional and moral tension without naming real people "
        "beyond what the notes explicitly, factually support.\n"
        "- Aim for ~2,000–3,000 words, but prioritise coherence over length.\n"
        "- Keep the narrative readable for a wide audience (no legalese).\n"
    )

    return f"{instructions}\n\n==== SEED NOTES START ====\n\n{seeds_text}\n\n==== SEED NOTES END ====\n"


def run(extra_instructions: str | None = None) -> None:
    """Generate a chapter, save to memory + output/latest_chapter.md."""
    base_prompt = build_prompt()

    if extra_instructions:
        prompt = f"{base_prompt}\n\nEXTRA INSTRUCTIONS:\n{extra_instructions}\n"
    else:
        prompt = (
            f"{base_prompt}\n\nEXTRA INSTRUCTIONS:\n"
            "Draft Chapter 1 using seed notes and create a dramatic tension arc."
        )

    text = ask(prompt)

    # Timestamped run id
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    # Memory folder
    run_dir = MEMORY_ROOT / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    # Metadata
    meta = {
        "run_id": run_id,
        "model": "gpt-4.1-mini",
        "timestamp_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "seeds_dir": str(SEEDS_DIR),
        "extra_instructions": extra_instructions,
    }

    # Save into memory
    (run_dir / "chapter.md").write_text(text, encoding="utf-8")
    (run_dir / "meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")

    # Also save to output/latest_chapter.md for GitHub artifact
    out_dir = Path("output")
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "latest_chapter.md").write_text(text, encoding="utf-8")

    print("=== Chapter generated ===")
    print(f"Run id: {run_id}")
    print("Model: gpt-4.1-mini")
    print("Output saved to: output/latest_chapter.md and", run_dir / "chapter.md")


if __name__ == "__main__":
    # Allow optional custom instructions via CLI argument
    extra = sys.argv[1] if len(sys.argv) > 1 else None
    run(extra)
