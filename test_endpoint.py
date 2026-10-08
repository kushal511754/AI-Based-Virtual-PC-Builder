#!/usr/bin/env python
from server.routes.compatibility import check_build_compatibility
from flask import Flask, request

# Create a Flask test context
app = Flask(__name__)

with app.test_request_context(
    '/api/builder/check',
    method='POST',
    json={'cpu': 1, 'motherboard': 3}
):
    try:
        result = check_build_compatibility()
        print("Response:", result)
        if hasattr(result, 'get_json'):
            print("JSON:", result.get_json())
    except Exception as e:
        print(f"Error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
