#!/usr/bin/env python3

import sqlite3
import os

db = "/var/lib/honeypot/state.db"
os.makedirs("/var/lib/honeypot", exist_ok=True)

conn = sqlite3.connect(db)
conn.execute("""
CREATE TABLE IF NOT EXISTS layers (
  layer TEXT,
  path TEXT,
  created_at TEXT
)
""")
conn.close()
