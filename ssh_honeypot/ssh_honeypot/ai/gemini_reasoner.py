# ai/gemini_reasoner.py


def analyze(events):
"""
Later: send to Gemini via Vertex AI
For now: simple heuristic
"""
tactics = set(e.get("class") for e in events)
if "download" in tactics:
return "Malware staging detected"
if "recon" in tactics:
return "Reconnaissance phase"
return "Unknown behavior"