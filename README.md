<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>AI Research Assistant — RAG Chatbot</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
  :root{
    --bg:#0d1117; --panel:#161b22; --border:#30363d;
    --text:#c9d1d9; --muted:#8b949e; --accent:#58a6ff;
    --accent2:#f55036; --green:#3fb950; --code-bg:#1f242c;
  }
  *{box-sizing:border-box;}
  body{
    background:var(--bg); color:var(--text); margin:0; padding:0;
    font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif;
    line-height:1.6;
  }
  .container{max-width:900px; margin:0 auto; padding:48px 24px 100px;}
  header.hero{text-align:center; padding-bottom:32px; border-bottom:1px solid var(--border); margin-bottom:32px;}
  header.hero h1{font-size:2rem; margin-bottom:8px;}
  header.hero p.tagline{color:var(--muted); font-size:1.05rem; max-width:600px; margin:0 auto 20px;}
  .badges{display:flex; flex-wrap:wrap; gap:6px; justify-content:center;}
  .badge{
    display:inline-block; padding:4px 10px; border-radius:6px; font-size:0.75rem;
    font-weight:600; color:#fff;
  }
  .b-python{background:#3776AB;} .b-streamlit{background:#FF4B4B;}
  .b-langchain{background:#1C3C3C;} .b-groq{background:var(--accent2);}
  .b-faiss{background:#0467DF;} .b-mit{background:var(--green); color:#0d1117;}

  h2{
    font-size:1.4rem; margin-top:48px; padding-bottom:8px;
    border-bottom:1px solid var(--border); display:flex; align-items:center; gap:8px;
  }
  h3{font-size:1.1rem; margin-top:28px; color:var(--text);}
  p{color:var(--text);}
  a{color:var(--accent); text-decoration:none;}
  a:hover{text-decoration:underline;}

  table{width:100%; border-collapse:collapse; margin:16px 0;}
  th,td{border:1px solid var(--border); padding:8px 12px; text-align:left; font-size:0.92rem;}
  th{background:var(--panel); color:var(--text);}
  tr:nth-child(even){background:rgba(255,255,255,0.02);}

  pre{
    background:var(--code-bg); border:1px solid var(--border); border-radius:8px;
    padding:16px; overflow-x:auto; font-size:0.85rem;
  }
  code{
    background:var(--code-bg); padding:2px 6px; border-radius:4px;
    font-family:"SFMono-Regular",Consolas,"Liberation Mono",Menlo,monospace; font-size:0.85em;
  }
  pre code{background:none; padding:0;}

  ul,ol{padding-left:1.4em;}
  li{margin-bottom:6px;}

  .diagram{
    background:var(--code-bg); border:1px solid var(--border); border-radius:8px;
    padding:16px; overflow-x:auto; font-family:monospace; font-size:0.82rem;
    white-space:pre; color:var(--accent);
  }

  .callout{
    border-left:4px solid var(--accent); background:rgba(88,166,255,0.08);
    padding:14px 18px; border-radius:6px; margin:20px 0;
  }
  .callout.warn{border-left-color:#d29922; background:rgba(210,153,34,0.08);}
  .callout h4{margin:0 0 8px; font-size:0.95rem;}

  .card-grid{display:grid; grid-template-columns:repeat(auto-fit,minmax(220px,1fr)); gap:12px; margin:20px 0;}
  .card{
    background:var(--panel); border:1px solid var(--border); border-radius:8px;
    padding:14px 16px;
  }
  .card strong{display:block; margin-bottom:4px; color:var(--accent);}

  footer{
    text-align:center; margin-top:60px; padding-top:24px;
    border-top:1px solid var(--border); color:var(--muted); font-size:0.85rem;
  }

  ::-webkit-scrollbar{height:8px; width:8px;}
  ::-webkit-scrollbar-thumb{background:var(--border); border-radius:4px;}
</style>
</head>
<body>
<div class="container">

  <header class="hero">
    <h1>📚 AI Research Assistant — RAG Chatbot</h1>
    <p class="tagline">Chat with your PDFs, CSVs, and DOCX files using Retrieval-Augmented Generation. Built with LangChain, Streamlit, Groq (Llama 3.3 70B), HuggingFace Embeddings, and FAISS.</p>
    <div class="badges">
      <span class="badge b-python">Python 3.10+</span>
      <span class="badge b-streamlit">Streamlit</span>
      <span class="badge b-langchain">LangChain</span>
      <span class="badge b-groq">Groq · Llama 3.3 70B</span>
      <span class="badge b-faiss">FAISS Vector Search</span>
      <span class="badge b-mit">MIT License</span>
    </div>
  </header>

  <h2>📖 Overview</h2>
  <p><strong>AI Research Assistant</strong> is a document-grounded chatbot. Upload your own research papers, spreadsheets, or Word documents, and ask questions in natural language — the app retrieves the most relevant chunks of your documents and uses an LLM to answer strictly from that context, avoiding hallucinated answers on topics your documents don't cover.</p>

  <h2>✨ Features</h2>
  <div class="card-grid">
    <div class="card"><strong>📄 Multi-format ingestion</strong>PDF, CSV, and DOCX support out of the box</div>
    <div class="card"><strong>✂️ Smart chunking</strong>Recursive character splitting (1000 chars, 200 overlap)</div>
    <div class="card"><strong>🧠 Semantic search</strong>all-MiniLM-L6-v2 embeddings indexed in FAISS</div>
    <div class="card"><strong>⚡ Fast inference</strong>Powered by Groq's llama-3.3-70b-versatile</div>
    <div class="card"><strong>💬 Chat interface</strong>Persistent session history + Clear Chat reset</div>
    <div class="card"><strong>🔍 Source transparency</strong>Expandable panel showing exact source chunks used</div>
  </div>

  <h2>🛠 Tech Stack</h2>
  <table>
    <tr><th>Layer</th><th>Technology</th></tr>
    <tr><td>UI / App framework</td><td>Streamlit</td></tr>
    <tr><td>Orchestration</td><td>LangChain (langchain-classic, langchain-community)</td></tr>
    <tr><td>LLM inference</td><td>Groq — llama-3.3-70b-versatile</td></tr>
    <tr><td>Embeddings</td><td>HuggingFace sentence-transformers/all-MiniLM-L6-v2</td></tr>
    <tr><td>Vector store</td><td>FAISS</td></tr>
    <tr><td>Document loaders</td><td>PyPDFLoader, CSVLoader, Docx2txtLoader, WebBaseLoader</td></tr>
    <tr><td>Config</td><td>python-dotenv</td></tr>
  </table>

  <h2>🏗 Architecture</h2>
  <div class="diagram">User Uploads (PDF / CSV / DOCX)
        │
        ▼
Document Loaders (PyPDF / CSV / Docx2txt)
        │
        ▼
Text Splitter (chunk=1000, overlap=200)
        │
        ▼
HF Embeddings (all-MiniLM-L6-v2)
        │
        ▼
FAISS Index (vector store)
        │
   User Query → top-k similarity search
        │
        ▼
     Retriever
        │
        ▼
Groq LLM (Llama 3.3 70B) + Prompt
        │
        ▼
Answer + Sources (Streamlit chat)</div>

  <h2>🔄 Workflow</h2>
  <ol>
    <li><strong>Upload</strong> — user drops one or more PDF, CSV, or DOCX files into the sidebar</li>
    <li><strong>Process</strong> — clicking "process" saves uploads to temp files and loads them into LangChain <code>Document</code> objects</li>
    <li><strong>Split</strong> — documents are chunked with <code>RecursiveCharacterTextSplitter</code></li>
    <li><strong>Embed</strong> — chunks are embedded with a HuggingFace sentence-transformer model</li>
    <li><strong>Index</strong> — embeddings are stored in an in-memory FAISS vector store</li>
    <li><strong>Retrieve</strong> — on each question, the top-3 most similar chunks are retrieved</li>
    <li><strong>Generate</strong> — retrieved context + question passed to Groq Llama 3.3 70B via <code>create_retrieval_chain</code></li>
    <li><strong>Answer</strong> — response and source chunks rendered in the chat UI</li>
  </ol>

  <h2>📂 Suggested Project Structure</h2>
  <pre><code>ai-research-assistant/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── .env                # Environment variables (not committed)
├── .env.example        # Template for required env vars
└── README.md</code></pre>

  <h2>⚙️ Installation</h2>
  <pre><code># 1. Clone the repository
git clone https://github.com/&lt;your-username&gt;/ai-research-assistant.git
cd ai-research-assistant

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt</code></pre>

  <h3>requirements.txt</h3>
  <pre><code>streamlit
python-dotenv
langchain
langchain-classic
langchain-community
langchain-text-splitters
langchain-groq
langchain-huggingface
faiss-cpu
pypdf
docx2txt
sentence-transformers</code></pre>

  <h2>🔑 Environment Variables</h2>
  <p>Create a <code>.env</code> file in the project root:</p>
  <pre><code>GROQ_API_KEY=your_groq_api_key_here</code></pre>
  <p>Get a free API key at <a href="https://console.groq.com/" target="_blank">console.groq.com</a>.</p>

  <h2>🚀 Running the App</h2>
  <pre><code>streamlit run app.py</code></pre>
  <p>Then open the local URL Streamlit prints (typically <code>http://localhost:8501</code>) in your browser.</p>

  <h2>💬 Usage</h2>
  <ol>
    <li>Open the sidebar and upload one or more PDF, CSV, or DOCX files</li>
    <li>Click <strong>process</strong> to chunk, embed, and index your documents</li>
    <li>Type a question in the chat input</li>
    <li>Read the answer, and expand <strong>"view source document"</strong> to see exactly which chunks it was based on</li>
    <li>Use <strong>🗑️ Clear Chat</strong> to reset the conversation</li>
  </ol>

  <h2>⚠️ Known Issues in the Current Notebook</h2>
  <div class="callout warn">
    <h4>These will need fixing before the app runs cleanly:</h4>
    <ul>
      <li><code>vector_store.as_retrievers(...)</code> → should be <code>.as_retriever(...)</code></li>
      <li><code>st.set_page_config(..., PageIcon=...)</code> → should be <code>page_icon</code></li>
      <li><code>tempfile</code> is used in <code>save_upload_file</code> but never imported</li>
      <li><code>save_upload_file</code> expects a single file, but is called with lists for CSV/DOCX uploads</li>
      <li><code>website_url</code> and <code>chains</code> are referenced but never defined before use</li>
      <li>The web-URL upload widget is commented out, so <code>loader_web</code> is currently unreachable</li>
      <li>Indentation nests the whole chat/query flow inside <code>if website_url:</code>, so it only runs when a URL is provided</li>
    </ul>
  </div>

  <h2>📈 Future Improvements</h2>
  <ul>
    <li>Re-enable and fix website URL ingestion via <code>WebBaseLoader</code></li>
    <li>Persist the FAISS index to disk so documents don't need re-processing every session</li>
    <li>Add multi-turn conversational retrieval (chat history-aware retriever)</li>
    <li>Add citation highlighting linking answers back to exact source pages</li>
    <li>Deploy to Streamlit Community Cloud with secrets-based <code>GROQ_API_KEY</code></li>
  </ul>

  <h2>🚀 Deployment (Streamlit Community Cloud)</h2>
  <ol>
    <li>Push your repo to GitHub</li>
    <li>Go to <a href="https://share.streamlit.io/" target="_blank">share.streamlit.io</a> and connect your repo</li>
    <li>Set <code>app.py</code> as the entry point</li>
    <li>Add <code>GROQ_API_KEY</code> under Settings → Secrets</li>
    <li>Deploy 🎉</li>
  </ol>

  <h2>🤝 Contributing</h2>
  <p>Contributions are welcome! Feel free to open an issue or submit a pull request.</p>

  <h2>📄 License</h2>
  <p>Licensed under the <a href="#">MIT License</a>.</p>

  <h2>👨‍💻 Author</h2>
  <p>Built by <em>[your name here]</em> — feel free to update this section with your name, GitHub, and LinkedIn.</p>

  <footer>Generated documentation for the AI Research Assistant RAG Chatbot project.</footer>
</div>
</body>
</html>
