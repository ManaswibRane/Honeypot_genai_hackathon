#!/bin/bash

WATCH_DIR="/home/legacy/legacy_data"

FLAG="/opt/legacy/.layer2_created"

if [ -f "$FLAG" ]; then
  exit 0
fi

inotifywait -m "$WATCH_DIR" -e open,access |
while read path action file; do
  if [ ! -f "$FLAG" ]; then
    echo "[+] Generating Layer-2 assets"

    ############################
    # Internal application creds
    ############################
    mkdir -p /opt/legacy/.config
    cat <<EOF > /opt/legacy/.config/.env
DB_HOST=legacy-db.internal
DB_USER=legacy_admin
DB_PASS=legacy123
EOF
    chmod 600 /opt/legacy/.config/.env

    ############################
    # Fake SQL backup (pivot bait)
    ############################
    mkdir -p /opt/legacy/backups
    cat <<EOF > /opt/legacy/backups/db_dump.sql
-- Legacy Payments DB
-- Dump Date: 2021-06-14

CREATE TABLE users (
  id INT,
  username VARCHAR(50),
  password VARCHAR(50)
);

INSERT INTO users VALUES (1,'admin','admin123');
EOF

    ############################
    # Fake AWS credentials
    ############################
    mkdir -p /home/legacy/.aws
    cat <<EOF > /home/legacy/.aws/credentials
[default]
aws_access_key_id = AKIALEGACYFAKE123
aws_secret_access_key = fakeLegacySecretKey987
EOF
    chmod 600 /home/legacy/.aws/credentials

    ############################
    # Fake GCP service account
    ############################
    mkdir -p /var/lib/legacy/creds
    cat <<EOF > /var/lib/legacy/creds/gcp.json
{
  "type": "service_account",
  "project_id": "legacy-payments-dev",
  "private_key_id": "fakekeyid123",
  "private_key": "-----BEGIN PRIVATE KEY-----\nFAKEKEYDATA\n-----END PRIVATE KEY-----\n",
  "client_email": "legacy-sa@legacy-payments-dev.iam.gserviceaccount.com",
  "client_id": "12345678901234567890",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token"
}
EOF
    chmod 600 /var/lib/legacy/creds/gcp.json

    ############################
    # Ownership & finalization
    ############################
    chown -R legacy:legacy /home/legacy/.aws
    chown -R legacy:legacy /opt/legacy
    chown -R legacy:legacy /var/lib/legacy || true

    touch "$FLAG"
    echo "[+] Layer-2 generation complete"
  fi
done
