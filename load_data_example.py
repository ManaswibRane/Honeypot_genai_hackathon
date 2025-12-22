import json

def load_documents_from_jsonl(file_path):
    """
    Loads documents from a JSONL file.
    """
    documents = []
    with open(file_path, "r") as f:
        for line in f:
            data = json.loads(line)
            documents.append(data)
    return documents

if __name__ == "__main__":
    loaded_documents = load_documents_from_jsonl("RAG/mitre_attack_documents.jsonl")
    print(f"Successfully loaded {len(loaded_documents)} documents.")
    # You can now use these documents in your RAG pipeline
    # For example, you can pass them to a text splitter or an embedding model.
    print("\nExample of a loaded document:")
    print(loaded_documents[0])
