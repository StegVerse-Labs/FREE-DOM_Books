import os, json, datetime, openai
from pathlib import Path

CONFIG = ".book-bridge/book_bridge_config.yaml"

def load_config():
    import yaml
    return yaml.safe_load(Path(CONFIG).read_text())

def ask(prompt, model="gpt-4.1"):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    completion = openai.ChatCompletion.create(
        model=model,
        messages=[{"role":"user","content":prompt}]
    )
    return completion.choices[0].message.content

def run(seed_file):
    cfg = load_config()
    seeds = Path(cfg["paths"]["seeds"])
    drafts = Path(cfg["paths"]["drafts"])
    sessions = Path(cfg["paths"]["sessions"])

    text = Path(seed_file).read_text()
    ts = datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    session_dir = sessions / f"session_{ts}"
    session_dir.mkdir(parents=True, exist_ok=True)

    prompt = f"""
    You are writing within the FREE-DOM Book universe.
    Tone: {cfg['project']['style']}
    Voice: {cfg['project']['voice_reference']}

    Convert the following seed into a narrative scene,
    prioritizing emotion, pacing, stakes, and verifiable context.
    Cite facts where known.

    SEED INPUT:
    {text}
    """

    output = ask(prompt)
    (session_dir / "draft.md").write_text(output)

    draft_file = drafts / f"{ts}_draft.md"
    draft_file.write_text(output)

    print("\nDraft generated →", draft_file)

if __name__ == "__main__":
    import sys
    run(sys.argv[1])
