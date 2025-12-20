import vertexai
from vertexai.preview.language_models import TextEmbeddingModel
from langchain_text_splitters import RecursiveCharacterTextSplitter
from google.cloud import aiplatform

from config import PROJECT_ID, REGION

EMBEDDING_MODEL = "text-embedding-004"

def init_vertex():
    vertexai.init(project=PROJECT_ID, location=REGION)
    aiplatform.init(project=PROJECT_ID, location=REGION)

def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )
    return splitter.split_documents(documents)

def embed_chunks(chunks):
    model = TextEmbeddingModel.from_pretrained(EMBEDDING_MODEL)
    return [
        model.get_embeddings([chunk.page_content])[0].values
        for chunk in chunks
    ]
