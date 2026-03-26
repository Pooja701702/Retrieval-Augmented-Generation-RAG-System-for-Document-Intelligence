# 📚 Complete Guide: How to Use the RAG Project

## 🎯 What is RAG?

**RAG (Retrieval Augmented Generation)** is a technique that combines:
1. **Retrieval**: Finding relevant information from your documents
2. **Augmentation**: Adding that information to your question
3. **Generation**: Using an AI model to answer based on the retrieved context

Think of it like having a smart assistant that:
- Reads all your documents first
- When you ask a question, it finds the most relevant parts
- Then answers your question using only that information

---

## 🏗️ How This Project Works (Step-by-Step)

### **Step 1: Document Ingestion** (`ingest.py`)

**What happens:**
1. **Reads your documents** from the `data/` folder (`.txt`, `.md`, `.pdf` files)
2. **Chunks them** into smaller pieces (900 characters each, with 150 character overlap)
   - Why chunk? Large documents are split so we can find specific relevant sections
3. **Creates embeddings** using a sentence transformer model
   - Embeddings = numerical representations of text that capture meaning
   - Similar texts have similar numbers
4. **Saves everything**:
   - `embeddings.npy`: All the numerical vectors
   - `chunks.jsonl`: The actual text chunks with metadata
   - `meta.json`: Information about the index

**Visual Flow:**
```
Your Documents → Chunking → Embeddings → Saved to index/
```

---

### **Step 2: Question Answering** (`rag.py`)

**What happens when you ask a question:**

1. **Your question is converted to an embedding** (same process as documents)
2. **Similarity search** finds the most similar document chunks
   - Uses cosine similarity (measures how similar two vectors are)
   - Returns top 5 most relevant chunks
3. **Context building**: Those chunks are combined into a prompt
4. **Answer generation** (if OpenAI API key is set):
   - Sends question + context to OpenAI
   - Gets an answer based on your documents
   - OR shows retrieved chunks if no API key

**Visual Flow:**
```
Your Question → Embedding → Find Similar Chunks → Build Context → Generate Answer
```

---

## 🚀 How to Use (Detailed Steps)

### **Prerequisites Check**

First, make sure you have Python 3.12.10:

```bash
python --version
```

If it shows Python 3.7 or older, you need to install Python 3.10+ from https://www.python.org/downloads/

---

### **Step 1: Activate Your Virtual Environment**

Your project has a virtual environment (`.venv`) with all dependencies installed.

**In PowerShell:**
```bash
.\.venv\Scripts\Activate.ps1
```

You should see `(.venv)` appear in your prompt, like:
```
(.venv) PS C:\Users\POOJA\OneDrive\Desktop\sec-rag-project>
```

**If you get an execution policy error**, run this once:
```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

### **Step 2: Prepare Your Documents**

Create a `data` folder and add your documents:

```bash
mkdir data
```

**Add files to `data/` folder:**
- `data\my_document.txt`
- `data\notes.md`
- `data\report.pdf`

**Example:** Create a test file:
```bash
# Create a sample document
echo "This is a test document about artificial intelligence. AI is transforming how we work." > data\test.txt
```

---

### **Step 3: Build the Index (Ingest Documents)**

This step reads your documents and creates the searchable index.

**Run the ingest script:**
```bash
python .\ingest.py --data_dir data --out_dir index
```

**What you'll see:**
```
Loading sentence transformer model...
Encoding documents...
✅ Ingested 3 files -> 15 chunks
✅ Wrote: index\embeddings.npy
✅ Wrote: index\chunks.jsonl
✅ Wrote: index\meta.json
```

**What each file does:**
- `embeddings.npy`: All document embeddings (the "searchable" part)
- `chunks.jsonl`: Your actual text chunks (one per line in JSON format)
- `meta.json`: Metadata (model used, number of chunks, etc.)

**Understanding the output:**
- "Ingested 3 files" = Found 3 documents
- "15 chunks" = Split into 15 searchable pieces
- This might take 1-2 minutes the first time (downloading the model)

---

### **Step 4: Run the Streamlit App**

**Start the web interface:**
```bash
streamlit run .\app.py
```

**What happens:**
- Opens your browser automatically
- Shows a web interface at `http://localhost:8501`
- You can ask questions in the chat box

**The UI has two modes:**

#### **Mode 1: Ingest Documents (from UI)**
- Click "Ingest Documents" tab
- Select your data folder
- Click "Start Ingestion"
- Wait for completion

#### **Mode 2: Ask Questions**
- Type your question in the text box
- Click "Ask"
- See the answer (or retrieved chunks if no API key)

---

### **Step 5: Ask Questions**

**Example questions:**
- "What is artificial intelligence?"
- "Summarize the main points"
- "What does the document say about [topic]?"

**What happens behind the scenes:**
1. Your question → converted to embedding
2. Compared with all document embeddings
3. Top 5 most similar chunks retrieved
4. If API key exists: Sent to OpenAI for answer
5. If no API key: Shows the retrieved chunks

---

## 🔑 Optional: Add OpenAI API Key

**Why add it?**
- Without it: You see retrieved chunks (raw text)
- With it: You get AI-generated answers based on those chunks

**How to add:**

1. **Get an API key** from https://platform.openai.com/api-keys

2. **Create a `.env` file** in your project root:
   ```bash
   # Create .env file
   echo "OPENAI_API_KEY=sk-your-actual-key-here" > .env
   ```

3. **Or edit manually:**
   - Create a file named `.env` (no extension)
   - Add this line:
     ```
     OPENAI_API_KEY=sk-your-actual-key-here
     OPENAI_MODEL=gpt-4o-mini
     ```

4. **Restart the app** for changes to take effect

---

## 📖 Understanding the Code Structure

### **`ingest.py` - Document Processing**

```python
# Main steps:
1. Find all .txt, .md, .pdf files in data/
2. Read each file's text
3. Split into chunks (900 chars, 150 overlap)
4. Convert chunks to embeddings using sentence-transformers
5. Save embeddings + chunks + metadata
```

**Key functions:**
- `iter_files()`: Finds document files
- `read_text()`: Reads text from files (handles PDFs too)
- `chunk_text()`: Splits text into smaller pieces
- `main()`: Orchestrates the whole process

---

### **`rag.py` - Question Answering**

```python
# Main steps:
1. Load saved embeddings and chunks
2. Convert question to embedding
3. Find most similar chunks (cosine similarity)
4. Build prompt with question + context
5. Send to OpenAI (or return chunks)
```

**Key class:**
- `RAG`: Main class that handles retrieval and answering
  - `__init__()`: Loads the index
  - `retrieve()`: Finds similar chunks
  - `answer()`: Generates or returns answer

---

### **`app.py` - Web Interface**

```python
# Main features:
1. Streamlit UI with tabs
2. Document ingestion interface
3. Question-answering interface
4. Displays results nicely
```

**UI Components:**
- **Sidebar**: Settings and info
- **Main area**: Chat interface or ingestion form
- **Results**: Shows answer + source chunks

---

## 🔍 Troubleshooting

### **Problem: "No module named 'rag'"**

**Solution:**
```bash
# Make sure you're in the project directory
cd C:\Users\POOJA\OneDrive\Desktop\sec-rag-project

# Activate venv
.\.venv\Scripts\Activate.ps1

# Verify Python version
python --version  # Should show 3.12.10
```

---

### **Problem: "Missing index files"**

**Solution:**
You need to run ingestion first:
```bash
python .\ingest.py --data_dir data --out_dir index
```

Make sure:
- `data/` folder exists and has files
- Files are `.txt`, `.md`, or `.pdf`

---

### **Problem: "No documents found"**

**Solution:**
```bash
# Check if data folder exists
dir data

# If empty, add some files:
echo "Test content" > data\test.txt
```

---

### **Problem: Streamlit won't start**

**Solution:**
```bash
# Make sure venv is activated
.\.venv\Scripts\Activate.ps1

# Check if streamlit is installed
pip list | findstr streamlit

# If not, reinstall:
pip install -r requirements.txt
```

---

### **Problem: Slow first run**

**Normal!** The first time you run:
- Downloads the sentence transformer model (~80MB)
- Takes 1-2 minutes
- Subsequent runs are much faster

---

## 🎓 Key Concepts Explained

### **What are Embeddings?**

Think of embeddings as "coordinates" for text:
- Similar texts → similar coordinates
- "Dog" and "Puppy" → close coordinates
- "Dog" and "Car" → far coordinates

**In this project:**
- Each document chunk gets coordinates (embedding)
- Your question gets coordinates
- We find chunks with closest coordinates

---

### **What is Cosine Similarity?**

A way to measure how similar two vectors are:
- **1.0** = Identical
- **0.8** = Very similar
- **0.0** = Completely different

**In this project:**
- We compute similarity between question and all chunks
- Pick top 5 most similar (highest scores)

---

### **Why Chunk Documents?**

**Problem:** A 10-page document is too big to search efficiently

**Solution:** Split into smaller pieces:
- Each chunk = 900 characters
- Overlap = 150 characters (so context isn't lost)
- Now we can find the exact relevant section

**Example:**
```
Document: "AI is transforming healthcare. [5000 more words]"

Chunk 1: "AI is transforming healthcare. Machine learning..."
Chunk 2: "...healthcare. Machine learning helps doctors..."
Chunk 3: "...doctors diagnose diseases faster..."
```

---

## 📊 Example Workflow

**Complete example from start to finish:**

```bash
# 1. Navigate to project
cd C:\Users\POOJA\OneDrive\Desktop\sec-rag-project

# 2. Activate venv
.\.venv\Scripts\Activate.ps1

# 3. Create data folder and add documents
mkdir data
echo "Artificial intelligence is revolutionizing technology." > data\ai.txt
echo "Machine learning helps computers learn from data." > data\ml.txt

# 4. Build index
python .\ingest.py --data_dir data --out_dir index

# 5. Start app
streamlit run .\app.py

# 6. In browser:
# - Type question: "What is AI?"
# - Click "Ask"
# - See answer!
```

---

## 🎯 Best Practices

1. **Organize your documents** in the `data/` folder
2. **Re-run ingestion** when you add new documents
3. **Use descriptive questions** for better results
4. **Check retrieved chunks** to verify the answer is based on your documents
5. **Keep `.env` file secure** (don't commit API keys to git)

---

## 🚀 Next Steps

Once you understand the basics:

1. **Add more documents** to improve answers
2. **Experiment with different questions**
3. **Try different embedding models** (change in `ingest.py`)
4. **Adjust chunk size** (currently 900 chars)
5. **Add citations** to show which document each answer came from

---

## 💡 Quick Reference

**Essential Commands:**
```bash
# Activate venv
.\.venv\Scripts\Activate.ps1

# Ingest documents
python .\ingest.py --data_dir data --out_dir index

# Run app
streamlit run .\app.py

# Check Python version
python --version
```

**File Structure:**
```
sec-rag-project/
├── data/              # Your documents go here
├── index/             # Generated index files
├── .venv/             # Virtual environment
├── app.py             # Streamlit UI
├── ingest.py          # Document processing
├── rag.py             # Question answering
├── requirements.txt  # Dependencies
└── .env              # API keys (create this)
```

---

## ❓ Common Questions

**Q: Do I need internet?**
- First time: Yes (downloads model)
- After that: No (unless using OpenAI API)

**Q: Can I use my own documents?**
- Yes! Add `.txt`, `.md`, or `.pdf` files to `data/`

**Q: How many documents can I add?**
- Thousands! But more = slower search (still fast with numpy)

**Q: Can I change the AI model?**
- Yes! Edit `OPENAI_MODEL` in `.env` file

**Q: Why pure Python (no FAISS)?**
- Works on Windows without C++ build tools
- Easier to install and debug
- Still fast for most use cases

---

**Happy RAG-ing! 🎉**
