#!/usr/bin/env bash
PORT=${1:-3000}
echo "Starting Fazail of 'Umrah Web Viewer on http://localhost:$PORT ..."
python3 -m http.server "$PORT"
