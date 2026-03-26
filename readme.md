## sec-rag-project

A minimal end-to-end **RAG (Retrieval Augmented Generation)** starter:

- **Ingest** documents from `data/` (`.txt`, `.md`, `.pdf`)
- Build a local vector index using **sentence-transformers** embeddings
- **Windows-friendly**: Pure-Python numpy-based cosine similarity (no C++ build tools needed!)
- **Ask questions** in a Streamlit UI
- **Optional**: if you set `OPENAI_API_KEY`, it will generate answers; otherwise it runs in retrieval-only mode

### 📖 **New to RAG?** 
👉 **Read [`HOW_TO_USE.md`](HOW_TO_USE.md)** for a complete step-by-step guide with detailed explanations!

## Setup (Windows / PowerShell)

### Prerequisite: Python 3.10+ (recommended)

This project works best with **Python 3.10+**.

If needed, install a newer Python from the official site (`https://www.python.org/downloads/windows/`).

Important: on Windows, `python` might still point to an older install (like 3.7). Prefer the **Python Launcher**:

```bash
py -0p
```

Pick a 3.10/3.11 interpreter and use it consistently below (examples use 3.11).

Create a virtual environment and install dependencies:

```bash
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python --version
pip install -r requirements.txt
```

## Add documents

Create a folder named `data` and put your files inside:

- `data\policy.md`
- `data\report.pdf`
- `data\notes.txt`

## Build the index

You can ingest from the UI, or run:

```bash
python .\ingest.py --data_dir data --out_dir index
```

This writes:

- `index\embeddings.npy` (numpy array of embeddings)
- `index\chunks.jsonl` (text chunks with metadata)
- `index\meta.json` (index metadata)

## Run the app

```bash
streamlit run .\app.py
```

## (Optional) Enable LLM answering

Create a file named `.env` in the project root:

```bash
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4o-mini
```

If `OPENAI_API_KEY` is not set, the app still works (it will show the most relevant passages instead of an LLM-generated answer).

## Notes / next improvements

- Add better chunking (by headings / sentences)
- Add support for more file types (DOCX, HTML)
- Add citations in the final answer (source + chunk id)