import os
import argparse
import requests
from bs4 import BeautifulSoup
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import faiss
import pickle

# ---------------- CONFIG ----------------
CHUNK_SIZE = 800
CHUNK_OVERLAP = 100
HEADERS = {"User-Agent": "Mozilla/5.0"}
EMBED_MODEL = "all-MiniLM-L6-v2"

# ---------------- READERS ----------------
def read_txt(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()

def read_pdf(path):
    reader = PdfReader(path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def read_url(url):
    r = requests.get(url, headers=HEADERS, timeout=20)
    soup = BeautifulSoup(r.text, "html.parser")
    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()
    return soup.get_text(separator=" ")

def extract_url_from_file(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            if line.lower().startswith("url="):
                return line.split("=", 1)[1].strip()
    return None

# ---------------- CHUNKING ----------------
def chunk_text(text):
    text = " ".join(text.split())
    chunks = []
    start = 0

    while start < len(text):
        end = start + CHUNK_SIZE
        chunks.append(text[start:end])
        start = end - CHUNK_OVERLAP

    return chunks

# ---------------- INGEST ----------------
def ingest(data_dir, out_dir):
    print("Starting ingest...")
    docs = []

    for file in os.listdir(data_dir):
        path = os.path.join(data_dir, file)

        try:
            if file.endswith(".txt") or file.endswith(".md"):
                text = read_txt(path)

            elif file.endswith(".pdf"):
                text = read_pdf(path)

            elif file.endswith(".url"):
                url = extract_url_from_file(path)
                if not url:
                    continue
                text = read_url(url)

            elif file.startswith("http"):
                text = read_url(file)

            else:
                continue

            for chunk in chunk_text(text):
                if len(chunk.strip()) > 50:
                    docs.append(chunk)

        except Exception as e:
            print(f"❌ Skipped {file}: {e}")

    if not docs:
        raise RuntimeError("No documents were ingested.")

    # ---------------- EMBEDDINGS ----------------
    model = SentenceTransformer(EMBED_MODEL)
    embeddings = model.encode(docs, show_progress_bar=True)

    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    os.makedirs(out_dir, exist_ok=True)

    faiss.write_index(index, os.path.join(out_dir, "index.faiss"))
    with open(os.path.join(out_dir, "docs.pkl"), "wb") as f:
        pickle.dump(docs, f)

    print("Ingest completed.")
    print(f"Chunks indexed: {len(docs)}")

# ---------------- MAIN ----------------
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_dir", required=True)
    parser.add_argument("--out_dir", required=True)
    args = parser.parse_args()

    ingest(args.data_dir, args.out_dir)

if __name__ == "__main__":
    main()
