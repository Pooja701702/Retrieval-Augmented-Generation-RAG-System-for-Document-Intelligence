import os
import json
import numpy as np
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

# ===============================
# LLM CALLERS
# ===============================

def call_openai(prompt: str) -> str:
    from openai import OpenAI

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    response = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content


def call_groq(prompt: str) -> str:
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    completion = client.chat.completions.create(
        model=os.getenv("GROQ_MODEL", "llama-3.1-8b-instant"),
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )

    return completion.choices[0].message.content


def call_ollama(prompt: str, model_name: str) -> str:
    import requests

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": model_name,
            "prompt": prompt,
            "stream": False,
        },
        timeout=120,
    )

    response.raise_for_status()
    return response.json()["response"]


# ===============================
# VECTOR SEARCH (NUMPY)
# ===============================

def load_index(index_dir: str):
    embeddings = np.load(os.path.join(index_dir, "embeddings.npy"))
    chunks = []

    with open(os.path.join(index_dir, "chunks.jsonl"), "r", encoding="utf-8") as f:
        for line in f:
            chunks.append(json.loads(line))

    return embeddings, chunks


def cosine_similarity(query_vec, matrix):
    return np.dot(matrix, query_vec)


def retrieve_passages(question: str, index_dir: str, top_k: int):
    from sentence_transformers import SentenceTransformer

    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

    embeddings, chunks = load_index(index_dir)

    query_vec = model.encode(
        [question],
        normalize_embeddings=True
    )[0]

    scores = cosine_similarity(query_vec, embeddings)
    top_indices = np.argsort(scores)[::-1][:top_k]

    passages = [chunks[i]["text"] for i in top_indices]
    return passages


# ===============================
# MAIN RAG FUNCTION
# ===============================

def answer_question(question: str, index_dir: str, top_k: int, llm_choice: str):
    passages = retrieve_passages(question, index_dir, top_k)

    context = "\n\n".join(passages)

    prompt = f"""
Use the following context to answer the question clearly and concisely.

Context:
{context}

Question:
{question}
"""

    if llm_choice == "OpenAI":
        answer = call_openai(prompt)

    elif llm_choice == "Groq":
        answer = call_groq(prompt)

    elif llm_choice == "Mistral (Ollama)":
        answer = call_ollama(prompt, "mistral")

    elif llm_choice == "LLaMA3 (Ollama)":
        answer = call_ollama(prompt, "phi3")

    else:
        answer = "No LLM selected. Showing retrieved passages only."

    return answer, passages
