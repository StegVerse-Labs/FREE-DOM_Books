import os
import sys
import json
from datetime import datetime
from pathlib import Path

from openai import OpenAI


# --------- Config ---------
MODEL = os.getenv("BOOKS_MODEL", "gpt-4.1-mini")  # you can change to gpt-4.1 or gpt-5.1 later
MAX_SEEDS = int(os.getenv("BOOKS_MAX_SEEDS", "10"))  # safety: don’t feed 100 files at once

BASE_PROMPT = """You are a careful, high-end ghostwriter helping draft a multi-volume
fictionalized series based on the FREE-DOM research repository.

You are working on a **single chapter draft**. Your job:

1. Read the SEED NOTES carefully.
2. Preserve factual texture (dates, locations, mechanisms) but do **not** directly name
   real-world people. Treat them as composites or anonymized characters.
3. Make the writing emotionally compelling, cinematic, and tense — but grounded in
   plausibility.
4. End the chapter on a hook that makes the reader want to continue.

Output:
- A chapter title on the first line.
- Then the chapter in Markdown (headings, scene breaks, etc).
"""

# --------- Helpers ---------


def get_project_root() -> Path:
    # scripts/book_agent.py -> scripts/ -> repo root
    return Path(__file__).resolve().parent.parent


def load_seed_files(year: str = "2025") -> list[dict]:
    """
    Load Markdown seed files from seeds/<year>/.

    Returns a list of:
    { "name": "...", "path": "...", "content": "..." }
    """
    root = get_project_root()
    seeds_dir = root / "seeds" / year

    if not seeds_dir.exists():
        raise FileNotFoundError(f"Seeds directory does not exist: {seeds_dir}")

    seeds = []
    for seed_file in sorted(seeds_dir.glob("*.md")):
        text = seed_file.read_text(encoding="utf-8")
        seeds.append(
            {
                "name": seed_file.name,
                "path": str(seed_file.relative_to(root)),
                "content": text,
            }
        )
        if len(seeds) >= MAX_SEEDS:
            break

    if not seeds:
        raise RuntimeError(f"No .md seed files found in {seeds_dir}")

    return seeds


def build_seed_summary(seeds: list[dict]) -> str:
    """
    Build a single text block summarizing all seeds for the model.
    """
    blocks = []
    for s in seeds:
        header = f"# Seed: {s['name']}\n\n"
        blocks.append(header + s["content"].strip() + "\n")

    return "\n\n---\n\n".join(blocks)


def get_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set in the environment.")
    return OpenAI(api_key=api_key)


# --------- Memory Archive ---------


def write_memory_archive(
    seeds: list[dict],
    extra_instructions: str,
    model: str,
    chapter_text: str,
) -> None:
    """
    Persist a durable record of:
    - which seeds were used
    - when the run happened
    - which model was used
    - the full generated chapter
    """
    root = get_project_root()
    memory_root = root / "memory"

    run_id = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    run_dir = memory_root / "runs" / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    # Save seeds bundle
    seeds_bundle = []
    for s in seeds:
        seeds_bundle.append(
            {
                "name": s["name"],
                "path": s["path"],
            }
        )

    meta = {
        "run_id": run_id,
        "timestamp_utc": datetime.utcnow().isoformat() + "Z",
        "model": model,
        "extra_instructions": extra_instructions,
        "seeds": seeds_bundle,
    }

    # meta.json
    (run_dir / "meta.json").write_text(
        json.dumps(meta, indent=2), encoding="utf-8"
    )

    # seeds_snapshot.md (contents for human inspection)
    seeds_text = build_seed_summary(seeds)
    (run_dir / "seeds_snapshot.md").write_text(seeds_text, encoding="utf-8")

    # chapter.md
    (run_dir / "chapter.md").write_text(chapter_text, encoding="utf-8")

    # Append a line to memory/index.jsonl
    index_path = memory_root / "index.jsonl"
    index_path.parent.mkdir(parents=True, exist_ok=True)
    with index_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(meta) + "\n")


# --------- Core generation ---------


def generate_chapter(extra_instructions: str = "") -> str:
    seeds = load_seed_files(year="2025")
    seeds_block = build_seed_summary(seeds)

    system_msg = BASE_PROMPT.strip()

    user_content = f"""SEED NOTES:

{seeds_block}

---

Now write a single, cohesive chapter draft based on the above.

Extra instructions (if any) from the human:
{extra_instructions or "(none specified)"}"""

    client = get_client()

    resp = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_content},
        ],
    )

    chapter = resp.choices[0].message.content
    if chapter is None:
        raise RuntimeError("Model returned no content.")

    # Write archive
    write_memory_archive(seeds, extra_instructions, MODEL, chapter)

    # Also write a convenience output for the repo (latest_chapter.md)
    out_path = get_project_root() / "latest_chapter.md"
    out_path.write_text(chapter, encoding="utf-8")

    return chapter


def main() -> None:
    """
    CLI entrypoint.

    Any arguments passed are treated as **extra instructions** for the model,
    not as file paths. So either of these is fine:

        python scripts/book_agent.py
        python scripts/book_agent.py Generate the first chapter using all seed files.

    """
    extra = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else ""
    chapter = generate_chapter(extra_instructions=extra)

    # Print a short confirmation so the Action log is readable
    print("=== Chapter generated ===")
    print(f"Model: {MODEL}")
    print(f"Extra instructions: {extra!r}")
    print("Output saved to: latest_chapter.md and memory/runs/<run_id>/chapter.md")


if __name__ == "__main__":
    main()
