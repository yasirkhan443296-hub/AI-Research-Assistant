
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
