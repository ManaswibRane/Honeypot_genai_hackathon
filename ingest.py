from sources.mitre import load_mitre_attack
from sources.nvd_cve import load_nvd_cves
from sources.exploitdb import load_exploitdb

def ingest_all(nvd_api_key):
    documents = []

    print("[+] Loading MITRE ATT&CK...")
    documents.extend(load_mitre_attack())

    print("[+] Loading NVD CVEs...")
    documents.extend(load_nvd_cves(nvd_api_key))

    print("[+] Loading ExploitDB...")
    documents.extend(load_exploitdb())

    print(f"[+] Total documents loaded: {len(documents)}")
    return documents
