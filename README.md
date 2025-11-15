# Document Intelligence Assistant 🤖

An AI-powered document processing system that enables intelligent search and Q&A across multiple document formats using local AI processing. Upload your documents and ask questions in natural language!

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-red)
![LangChain](https://img.shields.io/badge/LangChain-0.0.346-green)

## ✨ Features
- **Multi-Format Support**: Process PDF, TXT, and DOCX documents
- **Semantic Search**: AI-powered intelligent search using vector embeddings
- **Local Processing**: No external API dependencies
- **Context-Aware Answers**: Provides answers with source document citations
- **User-Friendly Interface**: Built with Streamlit for easy interaction

## 🛠️ Tech Stack
- **Frontend**: Streamlit
- **Backend**: Python, LangChain, ChromaDB
- **Embeddings**: Sentence Transformers
- **Document Processing**: PyPDF, python-docx

## 🚀 Quick Start
```bash
git clone https://github.com/yourusername/document-intelligence-assistant.git
cd document-intelligence-assistant
pip install -r requirements.txt
streamlit run app.py

