from src.data_processing.ingest import ingest_all
from src.rag.vectorstore import init_vertex, split_documents, embed_chunks
from src.config import NVD_API_KEY, INDEX_ID
from google.cloud import aiplatform

def get_document_id(chunk):
    metadata = chunk.metadata
    source = metadata.get("source")
    if source == "ExploitDB":
        doc_id = metadata.get('eb_id')
        return f"exploitdb-{doc_id}" if doc_id else None
    elif source == "NVD":
        doc_id = metadata.get('cve_id')
        return f"nvd-{doc_id}" if doc_id else None
    elif source == "MITRE ATT&CK":
        # For mitre and processed_mitre
        doc_id = metadata.get('technique_id') or metadata.get('id')
        return f"mitre-{doc_id}" if doc_id else None
    else:
        return None

def upload_to_vertex(chunks, vectors):
    datapoints = []

    for i, vec in enumerate(vectors):
        doc_id = get_document_id(chunks[i])
        if not doc_id:
            # Fallback to index if no ID is found
            datapoint_id = str(i)
        else:
            datapoint_id = f"{doc_id}-{i}"
            
        datapoints.append(
            aiplatform.MatchingEngineIndexDatapoint(
                datapoint_id=datapoint_id,
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
