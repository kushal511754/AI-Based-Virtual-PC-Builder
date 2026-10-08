#!/usr/bin/env python
"""Debug health endpoint directly."""
import sys
sys.path.insert(0, '.')

from flask import Flask
from server.routes.ml_routes import ml_bp

app = Flask(__name__)
app.register_blueprint(ml_bp)

with app.test_client() as client:
    print("Testing /api/ml/health endpoint...")
    response = client.get('/api/ml/health')
    print(f"Status: {response.status_code}")
    print(f"Response: {response.get_json()}")
