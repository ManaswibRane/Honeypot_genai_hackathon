from ingest import ingest_all
from vectorstore import init_vertex, split_documents, embed_chunks
from config import NVD_API_KEY, INDEX_ID
from google.cloud import aiplatform

def upload_to_vertex(chunks, vectors):
    datapoints = []

    for i, vec in enumerate(vectors):
        datapoints.append(
            aiplatform.MatchingEngineIndexDatapoint(
                datapoint_id=str(i),
                feature_vector=vec,
                restricts=[{
                    "namespace": "source",
                    "allow_list": [chunks[i].metadata.get("source", "unknown")]
                }]
            )
        )

    index = aiplatform.MatchingEngineIndex(INDEX_ID)
    index.upsert_datapoints(datapoints)

if __name__ == "__main__":
    init_vertex()

    docs = ingest_all(NVD_API_KEY)
    chunks = split_documents(docs)
    vectors = embed_chunks(chunks)

    upload_to_vertex(chunks, vectors)

    print("[✓] Vertex AI vector index populated")
