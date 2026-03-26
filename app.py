import os
import sys
import pickle
import subprocess
import streamlit as st
import faiss
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
from groq import Groq

# ---------------- CONFIG ----------------
load_dotenv()
st.set_page_config(page_title="Security RAG", layout="wide")

# ---------------- SIDEBAR ----------------
st.sidebar.title("Index Settings")

data_dir = st.sidebar.text_input("Data folder", "data")
index_dir = st.sidebar.text_input("Index folder", "index")
top_k = st.sidebar.slider("Top-k passages", 1, 5, 2)

st.sidebar.divider()

st.sidebar.title("LLM Settings")
llm_choice = st.sidebar.selectbox(
    "Choose LLM",
    [
        "None (retrieval only)",
        "Groq",
        "OpenAI",
        "Mistral (Ollama)",
        "LLaMA3 (Ollama)"
    ]
)

# ---------------- MAIN TITLE ----------------
st.title("🔐 Security RAG (Files + URLs + Multi-LLM)")

# ---------------- BUILD / REBUILD INDEX ----------------
st.header("1. Build / Rebuild Index")

if st.button("Run ingest"):
    with st.spinner("Running ingest..."):
        try:
            subprocess.run(
                [
                    sys.executable,
                    "ingest.py",
                    "--data_dir",
                    data_dir,
                    "--out_dir",
                    index_dir,
                ],
                check=True,
            )
            st.success("✅ Index built successfully")
        except subprocess.CalledProcessError as e:
            st.error("❌ Ingest failed")
            st.code(str(e))

# ---------------- ASK QUESTIONS ----------------
st.header("2. Ask Questions")

index_path = os.path.join(index_dir, "index.faiss")
docs_path = os.path.join(index_dir, "docs.pkl")

if not os.path.exists(index_path) or not os.path.exists(docs_path):
    st.info("Question answering will activate once index is ready.")
    st.stop()

# Load FAISS index
index = faiss.read_index(index_path)
docs = pickle.load(open(docs_path, "rb"))

embed_model = SentenceTransformer("all-MiniLM-L6-v2")

question = st.text_input("Enter your question")

if question:
    q_emb = embed_model.encode([question])
    D, I = index.search(q_emb, top_k)
    retrieved_chunks = [docs[i] for i in I[0]]

    st.subheader("📄 Retrieved Context")
    for chunk in retrieved_chunks:
        st.write("•", chunk)

    # ---------------- ANSWER ----------------
    if llm_choice == "None (retrieval only)":
        st.info("LLM disabled. Showing retrieved passages only.")

    elif llm_choice == "Groq":
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))

        prompt = f"""
You are a cybersecurity assistant.

Context:
{chr(10).join(retrieved_chunks)}

Question:
{question}

Answer clearly in 3–4 sentences.
"""

        with st.spinner("Generating answer..."):
            response = client.chat.completions.create(
                model=os.getenv("GROQ_MODEL", "llama-3.1-8b-instant"),
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt},
                ],
            )

        st.subheader("✅ Answer")
        st.write(response.choices[0].message.content)

    else:
        st.warning("⚠️ Selected LLM is not wired yet. Use Groq or Retrieval-only.")
