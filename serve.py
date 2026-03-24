#!/usr/bin/env python3
"""
Simple HTTP server for the Pixel Arcade web interface.

Usage:
    python serve.py          # serves on http://localhost:8000
    python serve.py 9000     # custom port
"""

import http.server
import socketserver
import sys
import os
import socket

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8000

# Serve from the directory this script lives in
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Find local IP for convenience
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    local_ip = s.getsockname()[0]
    s.close()
except Exception:
    local_ip = "unknown"

Handler = http.server.SimpleHTTPRequestHandler

# Silence default request logs — comment out to see them
Handler.log_message = lambda *_: None

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    httpd.allow_reuse_address = True
    print(f"""
  ┌─────────────────────────────────────────┐
  │         ★  PIXEL  ARCADE  ★             │
  ├─────────────────────────────────────────┤
  │  Local   → http://localhost:{PORT:<5}      │
  │  Réseau  → http://{local_ip:<16}:{PORT}  │
  ├─────────────────────────────────────────┤
  │  Ctrl+C pour arrêter                    │
  └─────────────────────────────────────────┘
""")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n  Serveur arrêté.")
