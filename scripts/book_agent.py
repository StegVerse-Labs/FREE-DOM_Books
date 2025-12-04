import os, datetime, yaml
from pathlib import Path
from openai import OpenAI

CONFIG_PATH = ".book-bridge/book_bridge_config.yaml"

def load_config():
    return yaml.safe_load(Path(CONFIG_PATH).read_text())

def ask(prompt, model="gpt-4.1"):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise Exception("OPENAI_API_KEY missing")

    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content

def run(seed_file):
    cfg = load_config()

    seed_path = Path(seed_file)
    text = seed_path.read_text()

    drafts = Path(cfg["paths"]["drafts"])
    sessions = Path(cfg["paths"]["sessions"])
    drafts.mkdir(exist_ok=True)
    sessions.mkdir(exist_ok=True)

    ts = datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    session_dir = sessions / f"session_{ts}"
    session_dir.mkdir(parents=True, exist_ok=True)

    prompt = f"""
    You are writing in the FREE-DOM Book narrative universe.
    Tone: {cfg['project']['style']}
    Voice: {cfg['project']['voice_reference']}

    Convert the following seed into a narrative scene.
    Maintain emotional tension and pacing.
    Cite facts when known & draw connections carefully.
    Output should read like the first pages of a book.

    ---
    SEED INPUT:
    {text}
    """

    output = ask(prompt, cfg["model"]["engine"])

    (session_dir / "draft.md").write_text(output)
    draft_file = drafts / f"{ts}_draft.md"
    draft_file.write_text(output)

    print(f"\n📄 Draft generated → {draft_file}\n")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python scripts/book_agent.py seeds/2025/<file>.md")
    else:
        run(sys.argv[1])
