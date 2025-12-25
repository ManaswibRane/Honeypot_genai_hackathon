import json
from langchain_core.documents import Document


def load_processed_mitre_attack(file_path="RAG/mitre_attack_documents.jsonl"):
    """
    Loads processed MITRE ATT&CK documents from a JSONL file.
    """
    documents = []
    with open(file_path, "r") as f:
        for line in f:
            data = json.loads(line)
            doc = Document(page_content=data['content'], metadata=data['metadata'])
            documents.append(doc)
    return documents
