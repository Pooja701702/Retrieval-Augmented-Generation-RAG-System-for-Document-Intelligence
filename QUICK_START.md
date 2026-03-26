# ⚡ Quick Start Guide

## 🎯 What You'll Do (3 Steps)

```
1. Add Documents → 2. Build Index → 3. Ask Questions
```

---

## Step 1: Add Your Documents

```bash
# Create data folder
mkdir data

# Add your files (examples)
echo "AI is transforming technology." > data\document1.txt
echo "Machine learning helps computers learn." > data\document2.txt
```

**Supported formats:** `.txt`, `.md`, `.pdf`

---

## Step 2: Build the Index

```bash
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Run ingestion
python .\ingest.py --data_dir data --out_dir index
```

**What happens:**
- Reads all documents from `data/`
- Splits them into chunks
- Creates embeddings (numerical representations)
- Saves to `index/` folder

**Output:**
```
✅ Ingested 2 files -> 5 chunks
✅ Wrote: index\embeddings.npy
✅ Wrote: index\chunks.jsonl
✅ Wrote: index\meta.json
```

---

## Step 3: Ask Questions

```bash
# Start the web app
streamlit run .\app.py
```

**In the browser:**
1. Type your question: "What is AI?"
2. Click "Ask"
3. See the answer!

---

## 🔑 Optional: Get AI Answers

**Without API key:** Shows retrieved document chunks  
**With API key:** Gets AI-generated answers

**To add API key:**
1. Get key from https://platform.openai.com/api-keys
2. Create `.env` file:
   ```
   OPENAI_API_KEY=sk-your-key-here
   ```
3. Restart the app

---

## 📋 Complete Example

```bash
# 1. Setup
cd C:\Users\POOJA\OneDrive\Desktop\sec-rag-project
.\.venv\Scripts\Activate.ps1

# 2. Add documents
mkdir data
echo "Artificial intelligence is revolutionizing how we work." > data\ai.txt

# 3. Build index
python .\ingest.py --data_dir data --out_dir index

# 4. Run app
streamlit run .\app.py

# 5. In browser: Ask "What is AI?"
```

---

## ❓ Troubleshooting

**"No module named 'rag'"**
→ Activate venv: `.\.venv\Scripts\Activate.ps1`

**"Missing index files"**
→ Run ingestion first: `python .\ingest.py`

**"No documents found"**
→ Add files to `data/` folder

---

## 📚 Want More Details?

👉 **Read [`HOW_TO_USE.md`](HOW_TO_USE.md)** for:
- Detailed explanations
- How RAG works
- Code structure
- Advanced usage
- Troubleshooting guide

---

**That's it! You're ready to use RAG! 🚀**
