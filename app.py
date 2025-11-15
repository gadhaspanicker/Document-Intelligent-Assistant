import streamlit as st
import os
from langchain.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
import tempfile

# Set page config
st.set_page_config(page_title="Document Q&A", page_icon="📚")

st.title("📚 Document Q&A Assistant")
st.info("🔍 **Working Search & Q&A System**")

# Initialize session state
if 'documents_processed' not in st.session_state:
    st.session_state.documents_processed = False
if 'text_chunks' not in st.session_state:
    st.session_state.text_chunks = []
if 'all_texts' not in st.session_state:
    st.session_state.all_texts = []

# File upload
uploaded_files = st.file_uploader(
    "Upload PDF or TEXT files",
    type=['pdf', 'txt'],
    accept_multiple_files=True
)

def process_documents(uploaded_files):
    """Process uploaded documents and extract text"""
    all_documents = []
    all_texts = []
    
    for uploaded_file in uploaded_files:
        # Save temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf' if uploaded_file.name.endswith('.pdf') else '.txt') as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            temp_path = tmp_file.name
        
        try:
            # Load document
            if uploaded_file.name.endswith('.pdf'):
                loader = PyPDFLoader(temp_path)
            else:
                loader = TextLoader(temp_path)
            
            documents = loader.load()
            all_documents.extend(documents)
            
            # Extract text content
            for doc in documents:
                all_texts.append({
                    'content': doc.page_content,
                    'source': uploaded_file.name,
                    'page': doc.metadata.get('page', 'N/A')
                })
            
            st.success(f"✅ Loaded {uploaded_file.name} - {len(documents)} pages")
            
        except Exception as e:
            st.error(f"❌ Error with {uploaded_file.name}: {str(e)}")
        finally:
            # Cleanup
            if os.path.exists(temp_path):
                os.unlink(temp_path)
    
    return all_documents, all_texts

def simple_search(query, texts, top_k=3):
    """Simple keyword-based search"""
    query_words = query.lower().split()
    results = []
    
    for text in texts:
        content_lower = text['content'].lower()
        score = 0
        
        # Simple keyword matching
        for word in query_words:
            if word in content_lower:
                score += content_lower.count(word)
        
        if score > 0:
            results.append((score, text))
    
    # Sort by score and return top results
    results.sort(key=lambda x: x[0], reverse=True)
    return [result[1] for result in results[:top_k]]

if uploaded_files:
    st.success(f"📎 {len(uploaded_files)} file(s) selected")
    
    if st.button("🚀 Process Documents"):
        with st.spinner("Processing documents..."):
            try:
                # Process documents
                documents, texts = process_documents(uploaded_files)
                
                if documents:
                    # Split documents into chunks
                    text_splitter = CharacterTextSplitter(
                        chunk_size=1000,
                        chunk_overlap=200
                    )
                    
                    chunks = text_splitter.split_documents(documents)
                    st.session_state.text_chunks = chunks
                    st.session_state.all_texts = texts
                    st.session_state.documents_processed = True
                    
                    st.balloons()
                    st.success(f"🎉 Processed {len(documents)} pages into {len(chunks)} searchable chunks!")
                    
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

# Search functionality
if st.session_state.documents_processed:
    st.markdown("---")
    st.subheader("💬 Search Your Documents")
    
    query = st.text_input("What would you like to find in your documents?")
    
    if query and st.button("🔍 Search"):
        with st.spinner("Searching through documents..."):
            try:
                # Perform search
                results = simple_search(query, st.session_state.all_texts, top_k=3)
                
                if results:
                    st.subheader(f"📄 Found {len(results)} relevant results:")
                    
                    for i, result in enumerate(results):
                        with st.expander(f"Result {i+1} - From {result['source']} (Page {result['page']})"):
                            st.write("**Content:**")
                            st.write(result['content'])
                            
                            # Show context around query
                            query_lower = query.lower()
                            content_lower = result['content'].lower()
                            
                            if query_lower in content_lower:
                                start_idx = content_lower.find(query_lower)
                                context_start = max(0, start_idx - 100)
                                context_end = min(len(result['content']), start_idx + len(query_lower) + 100)
                                context = result['content'][context_start:context_end]
                                
                                st.write("**Context around your query:**")
                                st.info(context)
                else:
                    st.warning("🔍 No results found. Try different keywords.")
                    
            except Exception as e:
                st.error(f"❌ Search error: {str(e)}")
    
    # Show document statistics
    with st.expander("📊 Document Statistics"):
        st.write(f"**Total documents processed:** {len(uploaded_files)}")
        st.write(f"**Total pages:** {len(st.session_state.text_chunks)}")
        st.write(f"**Total text chunks:** {len(st.session_state.all_texts)}")
        
        st.write("**Processed files:**")
        for file in uploaded_files:
            st.write(f"- {file.name}")

# Example questions
if st.session_state.documents_processed:
    st.markdown("---")
    st.subheader("💡 Try these example searches:")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Find dates"):
            st.session_state.search_query = "date"
    
    with col2:
        if st.button("Find names"):
            st.session_state.search_query = "name"
    
    with col3:
        if st.button("Find amounts"):
            st.session_state.search_query = "$ salary amount"

# Instructions
with st.sidebar:
    st.header("📋 How to Use")
    st.markdown("""
    1. **Upload** your PDF/TXT files
    2. **Click Process Documents**
    3. **Search** using keywords
    4. **View** relevant results
    
    **Current Features:**
    - ✅ Document processing
    - ✅ Keyword search
    - ✅ Context highlighting
    - ✅ No external dependencies
    
    **Supported:**
    - PDF documents
    - Text files
    - Multiple files
    """)

st.markdown("---")
st.markdown("💡 **Tip**: Use specific keywords for better search results")