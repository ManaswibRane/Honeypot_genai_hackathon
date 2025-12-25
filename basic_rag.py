from langchain_community.document_loaders import UnstructuredURLLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI

# ---------------- CONFIG ----------------
URLS = [
    "https://www.victoriaonmove.com.au/index.html",
    "https://www.victoriaonmove.com.au/contact.html",
]

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150
# ---------------------------------------

def load_docs(urls):
    loader = UnstructuredURLLoader(urls=urls)
    return loader.load()

def split_docs(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )
    return splitter.split_documents(docs)

def build_vectorstore(docs):
    embeddings = FastEmbedEmbeddings(
        model_name="BAAI/bge-small-en-v1.5"
    )
    return FAISS.from_documents(docs, embeddings)

def ask(vectorstore, llm, query, k=4):
    retriever = vectorstore.as_retriever(search_kwargs={"k": k})
    docs = retriever.invoke(query)

    context = "\n\n".join(d.page_content for d in docs)

    prompt = f"""
Answer the question strictly using the context below.
If the answer is not present, say:
"No context available."

Context:
{context}

Question:
{query}

Answer:
"""

    response = llm.invoke(prompt)

    print("\n--- ANSWER ---\n")
    print(response.content)

    print("\n--- SOURCES ---")
    for d in docs:
        print("-", d.metadata.get("source", "unknown"))

# ---------------- MAIN ----------------
if __name__ == "__main__":
    print("[+] Loading documents...")
    documents = load_docs(URLS)
    # print(documents)
    print("[+] Splitting documents...")
    chunks = split_docs(documents)
    print(f"[+] Total chunks: {len(chunks)}")
    # print(chunks)
    print("[+] Building FAISS index...")
    vectorstore = build_vectorstore(chunks)
    print(vectorstore)
#     print("[+] Loading Gemini LLM...")
#     llm = ChatGoogleGenerativeAI(
#     model="models/gemini-2.5-flash",
#     temperature=0,
#     api_key=""
# )

    # ask(vectorstore, llm, "What kind of services do they provide?")
