import requests
from langchain.schema import Document

MITRE_URL = "https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json"

def load_mitre_attack():
    data = requests.get(MITRE_URL).json()
    docs = []

    for obj in data["objects"]:
        if obj.get("type") == "attack-pattern":
            docs.append(
                Document(
                    page_content=f"""
Technique: {obj.get("name")}
ID: {obj.get("external_references", [{}])[0].get("external_id")}
Description: {obj.get("description")}
""",
                    metadata={
                        "source": "MITRE_ATT&CK",
                        "technique_id": obj.get("external_references", [{}])[0].get("external_id")
                    }
                )
            )
    return docs
