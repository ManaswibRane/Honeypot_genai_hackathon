import os
import pandas as pd
import json
import faiss
import numpy as np
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# --- Constants ---
# Using absolute paths for robustness
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MITRE_ATTACK_FILE = os.path.join(BASE_DIR, 'data', 'processed', 'mitre_attack_documents.jsonl')
EXPLOITS_FILE = os.path.join(BASE_DIR, 'data', 'raw', 'files_exploits.csv')
VECTORSTORE_PATH = os.path.join(BASE_DIR, 'data', 'vectorstore', 'faiss_index')

# --- Document Loading ---

def load_documents():
    """
    Loads documents from the MITRE ATT&CK JSONL file and the Exploits CSV file.
    """
    documents = []

    # Load MITRE ATT&CK data
    if os.path.exists(MITRE_ATTACK_FILE):
        with open(MITRE_ATTACK_FILE, 'r') as f:
            for line in f:
                data = json.loads(line)
                doc = Document(page_content=data.get('content', ''), metadata=data.get('metadata', {}))
                documents.append(doc)
    else:
        print(f"Warning: MITRE ATT&CK file not found at {MITRE_ATTACK_FILE}")


    # Load Exploits data
    if os.path.exists(EXPLOITS_FILE):
        df = pd.read_csv(EXPLOITS_FILE)
        for _, row in df.iterrows():
            # Combine relevant fields into a single content string
            content = f"Exploit: {row['description']}\nType: {row['type']}\nPlatform: {row['platform']}"
            metadata = {
                'source': 'exploit-db',
                'id': row['id'],
                'file': row['file']
            }
            doc = Document(page_content=content, metadata=metadata)
            documents.append(doc)
    else:
        print(f"Warning: Exploits file not found at {EXPLOITS_FILE}")

    return documents

# --- Vector Store Creation ---

def create_vector_store(documents, embedding_model):
    """
    Creates and saves a FAISS vector store from the given documents.
    """
    if not documents:
        print("No documents to process. Vector store not created.")
        return None
        
    print(f"Creating vector store from {len(documents)} documents...")
    
    # Using FAISS from langchain to create the vector store
    vectorstore = FAISS.from_documents(documents, embedding_model)
    
    # Ensure the directory for the vector store exists
    os.makedirs(os.path.dirname(VECTORSTORE_PATH), exist_ok=True)
    
    # Save the vector store locally
    vectorstore.save_local(VECTORSTORE_PATH)
    print(f"Vector store saved to {VECTORSTORE_PATH}")
    
    return vectorstore

# --- Main Execution ---

if __name__ == '__main__':
    # 1. Initialize embedding model
    print("Initializing embedding model...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    db = None
    # Check if the vector store already exists
    if os.path.exists(VECTORSTORE_PATH):
        print(f"Loading existing vector store from {VECTORSTORE_PATH}...")
        db = FAISS.load_local(VECTORSTORE_PATH, embeddings, allow_dangerous_deserialization=True)
    else:
        # If not, create it
        print("Vector store not found. Creating a new one...")
        # 2. Load documents
        print("Loading documents...")
        docs = load_documents()
        
        if docs:
            # 3. Create and save the vector store
            db = create_vector_store(docs, embeddings)
        else:
            print("Could not load any documents. Exiting.")

    # 4. (Optional) Example of loading and querying the vector store
    if db:
        print("\n--- Testing the vector store ---")
        
        # Example query
        query = "privilege escalation via scheduled task"
        print(f"\nPerforming a similarity search for: '{query}'")
        
        results = db.similarity_search(query, k=5)
        
        print(f"\nFound {len(results)} similar documents:")
        for i, result in enumerate(results):
            print(f"\n--- Result {i+1} ---")
            print(f"Source: {result.metadata.get('source', 'N/A')}")
            if result.metadata.get('id'):
                print(f"ID: {result.metadata.get('id')}")
            print(f"Content:\n{result.page_content}") # Print the full content
            print("-" * 20)
