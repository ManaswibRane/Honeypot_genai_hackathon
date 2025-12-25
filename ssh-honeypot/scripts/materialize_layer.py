#!/usr/bin/env python3

import os
import sys
import sqlite3
from datetime import datetime

layer = sys.argv[1]

DB = "/var/lib/honeypot/state.db"

os.makedirs("/var/lib/honeypot", exist_ok=True)

conn = sqlite3.connect(DB)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS layers (
  layer TEXT,
  path TEXT,
  created_at TEXT
)
""")

def record(path):
    cur.execute(
        "INSERT INTO layers VALUES (?,?,?)",
        (layer, path, datetime.utcnow().isoformat())
    )

# -------- LAYER‑2 CONTENT --------
if layer == "layer2":
    base = "/opt/payments/config"
    os.makedirs(base, exist_ok=True)

    prod = os.path.join(base, "prod.env")
    with open(prod, "w") as f:
        f.write(
            "DB_HOST=payments-db.internal\n"
            "DB_USER=payments_admin\n"
            "DB_PASS=PayLegacy!2021\n"
        )

    os.chmod(prod, 0o640)
    record(prod)

conn.commit()
conn.close()
