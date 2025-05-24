#!/bin/bash

echo "🔁 Avvio Flask su http://localhost:5000..."
export FLASK_APP=app.py
export FLASK_ENV=development
flask run --host=0.0.0.0 --port=5000 &

sleep 3

echo "🌍 Avvio LocalTunnel su https://amidoc.loca.lt..."
lt --port 5000 --subdomain amidoc
