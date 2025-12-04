import sys
from pathlib import Path
from openai import OpenAI

client = OpenAI()

def load_all_seeds():
    seed_root = Path("seeds")
    texts = []

    for file in seed_root.rglob("*.md"):
        texts.append(f"\nSOURCE FILE: {file.name}\n{file.read_text()}\n---\n")

    return "\n".join(texts)

def main(prompt):
    base = load_all_seeds()

    final_prompt = f"""
You are writing the FREE-DOM book series.
Use the following seed files:

{base}

Task: {prompt}
Generate ~2-5 pages of content.
Maintain tone: investigative, emotionally grounded, evidence-aware.
    """

    resp = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": final_prompt}],
        max_tokens=4000,
        temperature=0.6,
    )

    text = resp.choices[0].message.content
    outpath = Path("output/first_chapter.md")
    outpath.write_text(text)
    print("\n\n✔ Output saved to output/first_chapter.md\n")

if __name__ == "__main__":
    prompt = sys.argv[1] if len(sys.argv) > 1 else "Generate intro"
    main(prompt)
