import os
from pathlib import Path
from gtts import gTTS
from tqdm import tqdm

ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT_DIR = ROOT / "book_01_GhostPAT" / "manuscript"
OUTPUT_DIR = ROOT / "book_01_GhostPAT" / "audiobook"

def load_chapter_text(path: Path) -> str:
    with path.open("r", encoding="utf-8") as f:
        return f.read()

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # All chapter files, sorted
    chapters = sorted(MANUSCRIPT_DIR.glob("ch*.md"))

    if not chapters:
        print("No chapter files found.")
        return

    for chap in tqdm(chapters, desc="Generating audio"):
        text = load_chapter_text(chap)
        if not text.strip():
            continue

        base = chap.stem  # e.g. ch01_The_Key_That_Wouldn_t_Die
        out_file = OUTPUT_DIR / f"{base}.mp3"

        print(f"Creating {out_file.name}")
        tts = gTTS(text=text, lang="en")
        tts.save(str(out_file))

    print(f"Done. Files in: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
