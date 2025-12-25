from google.cloud import aiplatform
from vertexai.preview.language_models import TextEmbeddingModel
from langchain_google_genai import ChatGoogleGenerativeAI
from src.config import PROJECT_ID, REGION, ENDPOINT_ID, DEPLOYED_INDEX_ID

def ask_rag(question):
    aiplatform.init(project=PROJECT_ID, location=REGION)

    embed_model = TextEmbeddingModel.from_pretrained("text-embedding-004")
    query_vector = embed_model.get_embeddings([question])[0].values

    endpoint = aiplatform.MatchingEngineIndexEndpoint(ENDPOINT_ID)

    response = endpoint.find_neighbors(
        deployed_index_id=DEPLOYED_INDEX_ID,
        queries=[query_vector],
        num_neighbors=6
    )

    context = "\n\n".join(
        n.datapoint.datapoint_id
        for n in response[0].neighbors
    )

    llm = ChatGoogleGenerativeAI(
        model="models/gemini-2.5-flash",
        temperature=0
    )

    prompt = f"""
You are a cyber threat intelligence engine.

Context:
{context}

Question:
{question}

Answer:
"""

    return llm.invoke(prompt).content
