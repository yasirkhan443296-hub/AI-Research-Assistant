# -*- coding: utf-8 -*-
"""AI Research Assistant Chatbot"""

import os
import streamlit as st
from dotenv import load_dotenv
from langchain_community.document_loaders import (
    CSVLoader,
    Docx2txtLoader,
    PyPDFLoader,
    WebBaseLoader,
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_groq import ChatGroq
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains import create_retrieval_chain
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores import FAISS
import tempfile


def loader_pdf(file_path):
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    return documents


def loader_csv(file_path):
    csv_loader = CSVLoader(file_path)
    documents = csv_loader.load()
    return documents


def loader_web(url):
    web_loader = WebBaseLoader(url)
    documents = web_loader.load()
    return documents


def loader_text(file_path):
    docs_loader = Docx2txtLoader(file_path)
    documents = docs_loader.load()
    return documents


def save_upload_file(upload_file):
    suffix = os.path.splitext(upload_file.name)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
        temp_file.write(upload_file.getvalue())
        return temp_file.name


def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )
    chunks = splitter.split_documents(documents)
    return chunks


@st.cache_resource
def create_embeddings():
    embedding = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    return embedding


@st.cache_resource
def create_vectorstore(chunks, _embeddings):
    vector_store = FAISS.from_documents(
        documents=chunks, embedding=_embeddings
    )
    return vector_store


@st.cache_resource
def create_retriever(_vector_store):
    retriever = _vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 3},
    )
    return retriever


@st.cache_resource
def load_llm():
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.5,
        api_key=api_key
    )
    return llm


def create_prompt():
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are an AI Research Assistant.

Answer ONLY from the provided context.

If the answer is not present in the context, say:
'I couldn't find the answer in the provided documents.'
""",
            ),
            (
                "human",
                "Context:\n{context}\n\nQuestion:\n{input}",
            ),
        ]
    )
    return prompt


def create_document_chain(llm, prompt):
    chain = create_stuff_documents_chain(
        llm=llm,
        prompt=prompt,
    )
    return chain


def create_rag_chain(retriever, chain):
    rag_chain = create_retrieval_chain(
        retriever,
        chain,
    )
    return rag_chain


def main():
    load_dotenv()
    st.set_page_config(page_title="AI Research Assistant", page_icon=":book:")

    st.header("AI Research Assistant")
    col1, col2 = st.columns([1, 1.3])

    with col1:
        st.subheader("📂 Upload Research Documents")
        st.write(
            """
Upload one or more documents and click **Process Documents**.

Supported formats:
- 📄 PDF
- 📊 CSV
- 📝 DOCX

After processing, ask questions in the chat.
"""
        )

    with col2:
        st.title("🤖 AI Research Assistant")
        st.markdown(
            """
**Features**

✅ Multi PDF Support
✅ CSV Support
✅ DOCX Support
✅ AI Question Answering
✅ Source Document Citation
✅ FAISS Vector Database
✅ HuggingFace Embeddings
✅ Groq Llama 3.3 70B

---

**How it Works**
1. Upload Documents
2. Process Documents
3. Ask Questions
4. Get AI Generated Answers
5. View Source Documents

---
"""
        )

    st.info("💡 Tip: Upload multiple research papers for better answers.")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    with st.sidebar:
        st.subheader("Upload Documents")
        uploaded_pdf = st.file_uploader(
            "Upload PDF research papers",
            type=["pdf"],
            accept_multiple_files=True,
        )
        uploaded_csv = st.file_uploader(
            "Upload CSV research documents",
            type=["csv"],
            accept_multiple_files=True,
        )
        uploaded_docx = st.file_uploader(
            "Upload DOCX research documents",
            type=["docx"],
            accept_multiple_files=True,
        )

        process = st.button("Process Documents")
        if st.button("🗑️ Clear Chat"):
            st.session_state.messages = []
            st.rerun()

    # --- Processing block: only runs when the button is clicked ---
    if process:
        with st.spinner("Processing documents..."):
            all_documents = []

            if uploaded_pdf:
                for pdf in uploaded_pdf:
                    temp_path = save_upload_file(pdf)
                    docs = loader_pdf(temp_path)
                    all_documents.extend(docs)

            if uploaded_csv:
                for csv_file in uploaded_csv:
                    temp_path = save_upload_file(csv_file)
                    docs = loader_csv(temp_path)
                    all_documents.extend(docs)

            if uploaded_docx:
                for docx_file in uploaded_docx:
                    temp_path = save_upload_file(docx_file)
                    docs = loader_text(temp_path)
                    all_documents.extend(docs)

            if not all_documents:
                st.warning("Please upload at least one document before processing.")
            else:
                chunks = split_documents(all_documents)
                embeddings = create_embeddings()
                vector_store = create_vectorstore(chunks, embeddings)
                retriever = create_retriever(vector_store)
                llm = load_llm()
                prompt = create_prompt()
                doc_chain = create_document_chain(llm, prompt)
                rag_chain = create_rag_chain(retriever, doc_chain)

                st.session_state.rag_chain = rag_chain
                st.session_state.doc_count = len(all_documents)
                st.session_state.chunk_count = len(chunks)
                st.success("Research documents processed successfully!")

    # --- Chat block: lives OUTSIDE `if process`, so it persists across reruns ---
    if "rag_chain" in st.session_state:
        if "doc_count" in st.session_state:
            st.caption(
                f"Indexed {st.session_state.doc_count} document(s) "
                f"into {st.session_state.chunk_count} chunk(s)."
            )

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        query = st.chat_input("Ask your research question")
        if query:
            st.session_state.messages.append({"role": "user", "content": query})
            with st.chat_message("user"):
                st.markdown(query)

            try:
                with st.spinner("Thinking..."):
                    response = st.session_state.rag_chain.invoke({"input": query})
                    answer = response["answer"]

                with st.chat_message("assistant"):
                    st.markdown(answer)
                    with st.expander("View source documents"):
                        for i, doc in enumerate(response["context"], start=1):
                            st.markdown(f"**Source {i}**")
                            st.write(doc.page_content)
                            st.divider()

                st.session_state.messages.append(
                    {"role": "assistant", "content": answer}
                )
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.info("Upload documents and click **Process Documents** to start chatting.")


if __name__ == "__main__":
    main()
