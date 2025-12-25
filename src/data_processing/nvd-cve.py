import requests
from langchain.schema import Document

def load_nvd_cves(api_key, results=50):
    url = "https://services.nvd.nist.gov/rest/json/cves/2.0"
    headers = {"apiKey": api_key}
    params = {"resultsPerPage": results}

    res = requests.get(url, headers=headers, params=params).json()
    docs = []

    for item in res["vulnerabilities"]:
        cve = item["cve"]
        docs.append(
            Document(
                page_content=f"""
CVE ID: {cve['id']}
Description: {cve['descriptions'][0]['value']}
""",
                metadata={
                    "source": "NVD",
                    "cve_id": cve["id"]
                }
            )
        )
    return docs
