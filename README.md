# FREE-DOM Books Engine

An automated **story seed generator** that consumes structured, publicly
verifiable data from the [`FREE-DOM`](https://github.com/StegVerse/FREE-DOM)
repository and produces **anonymized fiction-ready prompts**.

- **Input:** CSV timelines & summaries from FREE-DOM (public GitHub raw URLs)
- **Engine:** GitHub Actions + Python + OpenAI (or compatible) models
- **Output:** Markdown story seeds under `seeds/` grouped by date and theme

This repo is *intentionally anonymizing*:
- No direct naming of real individuals as perpetrators or victims
- Focus on **patterns, timelines, power structures, and system failures**
- Seeds are meant for **fiction, composites, and educational narratives**

---

## 🔗 How it fits into StegVerse

1. `FREE-DOM` runs its **AI Search Agent** and **Auto Update** workflows.
2. After an update, FREE-DOM triggers a `repository_dispatch` event here.
3. `FREE-DOM-Books` workflow:
   - Pulls the latest CSVs from FREE-DOM via `raw.githubusercontent.com`
   - Groups events & entities into clusters
   - Calls the OpenAI API to generate **fiction-safe story seeds**
4. Seeds land under `seeds/YYYY/MMDD_topic-slug.md`.

You (and future AI entities) then:
- Turn seeds into outlines
- Turn outlines into chapters
- Turn chapters into full volumes

---

## 🧰 Quick Start (local dev)

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

export OPENAI_API_KEY="sk-..."  # or compatible key
python scripts/build_seeds.py
