from sources.mitre import load_mitre_attack
from sources.nvd_cve import load_nvd_cves
from sources.exploitdb import load_exploitdb
from sources.processed_mitre import load_processed_mitre_attack # New import

def ingest_all(nvd_api_key):
    documents = []

    print("[+] Loading MITRE ATT&CK (original source)...")
    documents.extend(load_mitre_attack())

    print("[+] Loading NVD CVEs...")
    documents.extend(load_nvd_cves(nvd_api_key))

    print("[+] Loading ExploitDB...")
    documents.extend(load_exploitdb())

    print("[+] Loading Processed MITRE ATT&CK (from XLSX)...") # New loading step
    documents.extend(load_processed_mitre_attack())

    print(f"[+] Total documents loaded: {len(documents)}")
    return documents
