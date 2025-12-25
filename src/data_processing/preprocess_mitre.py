
import pandas as pd
import json

def preprocess_mitre_attack(file_path="RAG/enterprise-attack-v18.1-techniques.xlsx"):
    """
    Reads the MITRE ATT&CK XLSX file and returns a list of dictionaries.
    """
    df = pd.read_excel(file_path)
    documents = []
    for index, row in df.iterrows():
        doc = {
            "content": (
                f"ID: {row.get('ID', '')}\n"
                f"Name: {row.get('name', '')}\n"
                f"Description: {row.get('description', '')}\n"
                f"Tactics: {row.get('tactics', '')}"
            ),
            "metadata": {"source": "MITRE ATT&CK", "id": row.get('ID', '')}
        }
        documents.append(doc)
    return documents

if __name__ == "__main__":
    processed_documents = preprocess_mitre_attack()
    with open("RAG/mitre_attack_documents.jsonl", "w") as f:
        for doc in processed_documents:
            f.write(json.dumps(doc) + "\n")
    print(f"Processed {len(processed_documents)} documents and saved to RAG/mitre_attack_documents.jsonl")

