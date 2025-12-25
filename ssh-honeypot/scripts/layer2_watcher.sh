#!/bin/bash

WATCH_DIR="/home/legacy/legacy_data"
FLAG="/var/lib/honeypot/layer2.done"

mkdir -p /var/lib/honeypot

if [ -f "$FLAG" ]; then
  exit 0
fi

inotifywait -m "$WATCH_DIR" -e open,access --format '%f' |
while read file; do
  if [ ! -f "$FLAG" ]; then
    logger "[honeypot] Layer-2 triggered by access to $file"

    /usr/local/bin/materialize_layer.py layer2

    touch "$FLAG"
  fi
done
